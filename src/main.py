from card_pool import CardPool
from dt_viz import (avg_stats,
                    probabilities)


def report_run():
    keywords = [
        'taunt',
        'rush',
        'charge'
    ]
    formats = [
        'standard_format',
        'wild_format'
    ]

    card_pool_obj = {
        'standard_format': CardPool(formats[0]),
        'wild_format': CardPool(formats[1])
    }

    for hs_format in formats:
        avg_stats(hs_format,
                  card_pool_obj[hs_format].avg_stats(),
                  show=True,
                  save=True)
        for keyword in keywords:
            probabilities(hs_format,
                          keyword,
                          card_pool_obj[hs_format].probability(keyword),
                          show=True,
                          save=True)
            card_pool_obj[hs_format].generate_xlsx_file(keyword)


if __name__ == '__main__':
    report_run()


# end of file
