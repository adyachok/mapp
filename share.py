import bisect
import operator
import time


VOLUME_WEIGHTED_STOCK_TIME_SPAN = 15 * 60


class Share(object):

    def __init__(self, name):
        self.name = name
        self.s_type = 'common'
        self._history = OrderHistory()

    def get_dividend_yield(self, dividend):
        last_price = self.get_last_price()
        return round(float(dividend) / last_price, 4)

    def get_last_price(self):
        return self._history[-1].price

    def set_order(self, quantity, indicator, price, timestamp=None):
        self._history.set_order(quantity, indicator, price, timestamp)

    def get_PE_ratio(self, dividend):
        return 1 / self.get_dividend_yield(dividend)

    def get_geometric_mean(self, from_time=None, to_time=None):
        orders = self._history.get_orders(from_time, to_time)
        return round(self._get_geometric_mean(orders), 4)

    def _get_geometric_mean(self, iterable):
        return (reduce(operator.mul, iterable)) ** (1.0/len(iterable))

    def get_volume_weighted_stock_price(self):
        last_o = self._history[-1]
        end_period = time.mktime(last_o.timestamp)
        start_period = end_period - VOLUME_WEIGHTED_STOCK_TIME_SPAN
        orders = self._history.get_orders(from_time=start_period)
        quantity = 0
        price_quantity = 0
        for order in orders:
            price_quantity += order.price * order.quantity
            quantity += order.quantity
        return round(float(price_quantity) / quantity, 4)



class PreferredShare(Share):

    def __init__(self, name, par_value, dividend_par_val):
        super(PreferredShare, self).__init__(name)
        self.s_type = 'preferred'
        self.par_value = par_value
        self.dividend_par_val = dividend_par_val

    def get_dividend_yield(self, dividend=None):
        last_price = self.get_last_price()
        if dividend is None:
            dividend = float(self.dividend_par_val) / 100 * self.par_value
        return round(dividend / last_price, 4)


class Order(object):
    __slots__ = ['timestamp', 'quantity', 'indicator', 'price']

    def __init__(self, quantity, indicator, price, timestamp=None):
        """
        :param quantity: quantity of shares bought or sold
        :param indicator: "buy" or "sell"
        :param price: price of the order agreement
        :param timestamp: time of the agreement in the format
               like "2016-2-3 10:11:12"
        """
        self.quantity = quantity
        self.indicator = self._check_indicator(indicator)
        self.price = price
        self.timestamp = self._process_timestamp(timestamp)

    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __mul__(self, other):
        if isinstance(other, Order):
            return self.price * other.price
        else:
            return self.price * other

    __rmul__ = __mul__

    def _check_indicator(self, indicator):
        if indicator not in ['buy', 'sell']:
            raise OrderException("Indicator value is invalid")
        return indicator

    def _process_timestamp(self, timestamp):
        if timestamp is None:
            timestamp = time.time()
        else:
            if isinstance(timestamp, str):
                timestamp = convert_timestamp(timestamp)
        return timestamp


class OrderException(Exception):
    pass


class OrderHistory(object):

    def __init__(self):
        self._history = []

    def __getitem__(self, item):
        return self._history[item]

    def __len__(self):
        return len(self._history)

    def set_order(self, quantity, indicator, price, timestamp=None):
        o = Order(quantity, indicator, price, timestamp)
        self._history.append(o)

    def get_orders(self, from_time=None, to_time=None):
        if from_time is None and to_time is None:
            return self._history[:]
        elif from_time is None:
            last_index = self._get_el_index(to_time, 'right')
            last_index = self._check_el_index(last_index)
            return self._history[:last_index]
        elif to_time is None:
            first_index = self._get_el_index(from_time, 'left')
            return self._history[first_index + 1:]
        else:
            first_index = self._get_el_index(from_time, 'left')
            last_index = self._get_el_index(to_time, 'right')
            last_index = self._check_el_index(last_index)
            return self._history[first_index, last_index]

    def _get_el_index(self, order_time, left_or_right):
        fake_order = Order(0, 'buy', 0, order_time)
        if left_or_right == 'left':
            return bisect.bisect_left(self._history, fake_order)
        else:
            return bisect.bisect_right(self._history, fake_order)

    def _check_el_index(self, idx):
        return idx if idx < len(self) else len(self) - 1

def convert_timestamp(timestamp):
    try:
        timestamp = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise OrderException('''Timestamp value should be specified in
        the next format year-month-day hours-minutes-seconds''')
    return timestamp
