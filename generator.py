import random


stock_codes = ['ASBE', 'ABF', 'AA', 'ABDP', 'ABC', 'AAS', 'GFS', 'GMAA',
               'GATC', 'WINK', 'MPO', 'EMG', 'MARL', 'OCDO', 'OSEC', 'OML',
               'WRES', 'ZPLA']


stock_base_data = {code: {'price': random.randrange(5, 500),
                          'timestamp': 1454490672.0,
                          'preferred': random.choice([True, False])} for code
                   in stock_codes}


class RandDataGenerator(object):

    @staticmethod
    def generate_random_data(share_repo):
        for key, val in stock_base_data.iteritems():
            if val['preferred']:
                share = share_repo.get_share(key, 'preferred', val['price'],
                                             random.randrange(2,20))
            else:
                share = share_repo.get_share(key)

            timestamp = val['timestamp']
            for i in range(10):
                rand_price = RandDataGenerator.gen_random_price(val['price'])
                share.set_order(random.randint(10, 1000),
                                random.choice(['buy', 'sell']),
                                rand_price,
                                timestamp)
                timestamp += 300

    @staticmethod
    def gen_random_price(price):
        price_delta = random.randint(1, ((price/10)+2))
        sign = random.choice([-1, 1])
        price = price + (price_delta * sign)
        return price
