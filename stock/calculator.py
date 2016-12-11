class Calculator(object):

    @staticmethod
    def get_dividend_yield(share, dividend=None):
        return share.get_dividend_yield(dividend)

    @staticmethod
    def get_PE_ratio(share, dividend=None):
        return share.get_PE_ratio(dividend)

    @staticmethod
    def get_geometric_mean(share):
        return share.get_geometric_mean()

    @staticmethod
    def get_volume_weighted_stock_price(share):
        return share.get_volume_weighted_stock_price()

    @staticmethod
    def get_GBCE(share_repo):
        sum_geo_mean = 0
        for share in share_repo:
            sum_geo_mean += Calculator.get_geometric_mean(share)
        return round(sum_geo_mean / len(share_repo), 4)
