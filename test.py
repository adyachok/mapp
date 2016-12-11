import time
import unittest

from stock.calculator import Calculator
from stock.share import Order, OrderException, OrderHistory, PreferredShare, Share
from stock.share_repo import ShareRepository


class TestShareRepository(unittest.TestCase):

    def test_uniqueness(self):
        sr = ShareRepository()
        s1 = sr.get_share('appl')
        s2 = sr.get_share('appl')
        self.assertEqual(id(s1), id(s2))

    def test_difference(self):
        sr = ShareRepository()
        s1 = sr.get_share('appl')
        s2 = sr.get_share('eric')
        self.assertNotEqual(id(s1), id(s2))

    def test_preferred_share_creation(self):
        sr = ShareRepository()
        ps = sr.get_share('rbs', 'preferred', 100, 10)
        self.assertTrue(isinstance(ps, PreferredShare))

    def test_preferred_uniqueness(self):
        sr = ShareRepository()
        ps1 = sr.get_share('rbs', 'preferred', 100, 10)
        ps2 = sr.get_share('rbs', 'preferred', 100, 10)
        self.assertEqual(id(ps1), id(ps2))

    def test_preferred_uniqueness_diff_args(self):
        sr = ShareRepository()
        ps1 = sr.get_share('rbs', 'preferred', 100, 10)
        ps2 = sr.get_share('rbs', 'preferred', 200, 30)
        self.assertEqual(id(ps1), id(ps2))

class TestOrder(unittest.TestCase):

    def test_order_creation(self):
        o = Order(200, 'sell', 100.31, "2016-2-3 10:11:12")
        self.assertEqual(o.quantity, 200)
        self.assertEqual(o.indicator, 'sell')
        self.assertEqual(o.price, 100.31)
        self.assertEqual(o.timestamp,
                         time.mktime(time.strptime("2016-2-3 10:11:12",
                                                   "%Y-%m-%d %H:%M:%S")))

    def test_wrong_indicator(self):
        with self.assertRaises(OrderException):
            Order(200, 'go', 100)

    def test_process_timestamp(self):
        with self.assertRaises(OrderException):
            Order(200, 'sell', 100.31, "aaaa")


class TestShare(unittest.TestCase):

    def test_get_common_dividend_yield(self):
        s = Share('gld')
        s.set_order(100, 'buy', 55)
        self.assertEqual(s.get_last_price(), 55)
        self.assertEqual(s.get_dividend_yield(5), 0.0909)

    def test_get_preferred_dividend_yield(self):
        s = PreferredShare('gld', 100, 10)
        s.set_order(100, 'buy', 55)
        self.assertEqual(s.get_last_price(), 55)
        self.assertEqual(s.get_dividend_yield(), 0.1818)

    def test_volume_weighted_stock_price(self):
        s = Share('aapl')
        fixtures = [(100, 'buy', 10, "2016-2-3 10:11:12"),
                    (100, 'buy', 12, "2016-2-3 15:00:12"),
                    (100, 'buy', 11, "2016-2-3 15:04:12"),
                    (100, 'buy', 15, "2016-2-3 15:08:12"),
                    (100, 'buy', 14, "2016-2-3 15:10:12"),
                    (100, 'buy', 9, "2016-2-3 15:11:12")]
        for o in fixtures:
            s.set_order(*o)
        self.assertEqual(12.2, s.get_volume_weighted_stock_price())

    def test_geometric_mean(self):
        s = Share('aapl')
        fixtures = [(100, 'buy', 10, "2016-2-3 10:11:12"),
                    (100, 'buy', 12, "2016-2-3 15:00:12"),
                    (100, 'buy', 11, "2016-2-3 15:04:12"),
                    (100, 'buy', 15, "2016-2-3 15:08:12"),
                    (100, 'buy', 14, "2016-2-3 15:10:12"),
                    (100, 'buy', 9, "2016-2-3 15:11:12")]
        for o in fixtures:
            s.set_order(*o)
        self.assertEqual(11.6459, s.get_geometric_mean())

class TestCalculator(unittest.TestCase):

    def test_get_common_dividend_yield(self):
        s = Share('gld')
        s.set_order(100, 'buy', 55)
        self.assertEqual(Calculator.get_dividend_yield(s, 5), 0.0909)

    def test_get_preferred_dividend_yield(self):
        s = PreferredShare('gld', 100, 10)
        s.set_order(100, 'buy', 55)
        self.assertEqual(Calculator.get_dividend_yield(s), 0.1818)

    def test_get_common_PE_ratio(self):
        s = Share('gld')
        s.set_order(100, 'buy', 60)
        self.assertEqual(Calculator.get_PE_ratio(s, 30), 2.0)

    def test_get_common_PE_ratio_same_price(self):
        s = PreferredShare('gld', 100, 10)
        s.set_order(100, 'buy', 100)
        self.assertEqual(Calculator.get_PE_ratio(s), 10.0)

    def test_get_common_PE_ratio_small_price(self):
        s = PreferredShare('gld', 100, 10)
        s.set_order(100, 'buy', 50)
        self.assertEqual(Calculator.get_PE_ratio(s), 5.0)

    def test_get_common_PE_ratio_big_price(self):
        s = PreferredShare('gld', 100, 10)
        s.set_order(100, 'buy', 200)
        self.assertEqual(Calculator.get_PE_ratio(s), 20.0)

    def test_volume_weighted_stock_price_only_one(self):
        s = Share('gld')
        fixtures = [(100, 'buy', 10, "2016-2-3 10:11:12"),
                    (100, 'buy', 12, "2016-2-3 11:11:12"),
                    (100, 'buy', 11, "2016-2-3 12:11:12"),
                    (100, 'buy', 15, "2016-2-3 13:11:12"),
                    (100, 'buy', 14, "2016-2-3 14:11:12"),
                    (100, 'buy', 9, "2016-2-3 15:11:12")]
        for o in fixtures:
            s.set_order(*o)
        self.assertEqual(Calculator.get_volume_weighted_stock_price(s), 9)


class TestOrderHistory(unittest.TestCase):

    def test_indexing(self):
        oh = OrderHistory()
        fixtures = [(100, 'buy', 10, "2016-2-3 10:11:12"),
                    (100, 'buy', 12, "2016-2-3 11:11:12"),
                    (100, 'buy', 11, "2016-2-3 12:11:12"),
                    (100, 'buy', 15, "2016-2-3 13:11:12"),
                    (100, 'buy', 14, "2016-2-3 14:11:12"),
                    (100, 'buy', 9, "2016-2-3 15:11:12")]
        for o in fixtures:
            oh.set_order(*o)
        self.assertEqual(5, oh._get_el_index("2016-2-3 15:11:12", 'left'))
        self.assertEqual(6, oh._get_el_index("2016-2-3 15:11:12", 'right'))


if __name__ == '__main__':
    unittest.main()
