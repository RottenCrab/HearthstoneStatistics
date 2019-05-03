from card_pool import CardPool
from reporting_tool import reporting
from dt_viz import (avg_stats,
                    probabilities,
                    minion_distribution)


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
        minion_distribution(hs_format,
                            card_pool_obj[hs_format].total_minion_per_mana_cost,
                            show=True,
                            save=True)
        minion_distribution(hs_format,
                            card_pool_obj[hs_format].total_taunt_per_mana_cost,
                            keyword='taunt',
                            show=True,
                            save=True)
        minion_distribution(hs_format,
                            card_pool_obj[hs_format].total_rush_per_mana_cost,
                            keyword='rush',
                            show=True,
                            save=True)
        minion_distribution(hs_format,
                            card_pool_obj[hs_format].total_charge_per_mana_cost,
                            keyword='charge',
                            show=True,
                            save=True)
        for keyword in keywords:
            probabilities(hs_format,
                          keyword,
                          card_pool_obj[hs_format].probability(keyword),
                          show=True,
                          save=True)
            card_pool_obj[hs_format].generate_xlsx_file(keyword)
    reporting(card_pool_obj['standard_format'].total_card_pool,
              card_pool_obj['wild_format'].total_card_pool)


if __name__ == '__main__':
    report_run()


# end of file
