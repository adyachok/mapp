from tabulate import tabulate

from generator import RandDataGenerator
from stock.calculator import Calculator as calc
from stock.share_repo import ShareRepository


def print_result(data, headers):
    print tabulate(data, headers)


def calculate_data(share_repo):
    data = []
    for share in share_repo:
        item = [share.name,
                calc.get_dividend_yield(share,
                                        (20 if share.s_type == 'common'
                                         else None)),
                calc.get_PE_ratio(share,
                                  20 if share.s_type == 'common' else None),
                calc.get_geometric_mean(share),
                calc.get_volume_weighted_stock_price(share)]
        data.append(item)
    return data


def main():
    sr = ShareRepository()
    RandDataGenerator.generate_random_data(sr)

    data = calculate_data(sr)

    headers = ['Stock Code', 'Dividend Yield', 'P / E', 'Geometric Mean',
               'Vol.Weighted Stock Price']
    print_result(data, headers)
    print "\nThe GBCE All Share Index: ", calc.get_GBCE(sr)


if __name__ == '__main__':
    main()
