import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def save_plot(plot_type,
              hs_format,
              path,
              extension='.png'):
    plt.savefig('{path}{chart_type}_{hs_format}{ext}'.format(path=path,
                                                             chart_type=plot_type,
                                                             hs_format=hs_format,
                                                             ext=extension))


def format_format_title(wrd):
    return wrd.split('_')[0].title()


def minion_distribution(hs_format,
                        minion_dict,
                        keyword='Total',
                        show=False,
                        save=False):
    minion_columns = ['mana_cost', 'minions']
    minion_df = pd.DataFrame(columns=minion_columns)
    for key, value in minion_dict.items():
        minion_df = minion_df.append({'mana_cost': key,
                                      'minions': value},
                                     ignore_index=True)
    ax = sns.barplot(x="mana_cost", y="minions", data=minion_df, palette='pastel')
    # Customize X & Y Axis Labels and the title of the Plot
    ax.set(xlabel='Mana Cost',
           ylabel='Total Minions',
           title='{} Minions per Mana Cost ({})'.format(keyword.title(),
                                                        format_format_title(hs_format)))
    # Now we will annotate the top of the bars with their corresponding value
    # Setting up bar annotation
    xpos = 'center'
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    # Annotate the top of the bars with their corresponding values
    for rect in ax.patches:
        height = int(rect.get_height())
        if height == 0:
            continue
        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

    lim = minion_df['minions'].max() + minion_df['minions'].max() * 0.15
    plt.ylim(0, lim)
    if save:
        # filename = 'avg_stats_{}.png'.format(hs_format)
        # plt.savefig('../Plots/' + filename)
        save_plot('{}_minions_per_mana_cost'.format(keyword.lower()),
                  hs_format,
                  '../Plots/')
    if show:
        plt.tight_layout()
        plt.show()


def avg_stats(hs_format,
              avg_stats_dict,
              show=False,
              save=False):
    # hearthstone_cards = CardPool(hs_format)
    # minion_avg_stats = hearthstone_cards.avg_stats()
    minion_avg_stats = avg_stats_dict
    # Construct a DataFrame for Average Minions Stats from minion_avg_stats Dictionary
    # Average stats DataFrame will contain the following columns: mana_cost, stats, type_of_stats
    # We select those columns in order to take advantage of hue parameter of seaborn.barplot later
    avg_stats_columns = [
        'mana_cost',
        'stats',
        'type_of_stats'
    ]
    avg_stats_df = pd.DataFrame(columns=avg_stats_columns)
    for key, value in minion_avg_stats.items():
        for ikey, ivalue in value.items():
            avg_stats_df = avg_stats_df.append({'mana_cost': int(key),
                                                'stats': round(ivalue, 2),
                                                'type_of_stats': ikey},
                                               ignore_index=True)
    # End of DataFrame Construction
    # Now we will visualize DataFrame's data using grouped barplot (Group A: attack, Group B: Health)
    # X Axis: Mana Cost
    # Y Axis: Minion Stats
    ax = sns.barplot(x="mana_cost", y="stats", hue="type_of_stats", data=avg_stats_df, palette='pastel')
    # Customize X & Y Axis Labels and the title of the Plot
    ax.set(xlabel='Mana Cost',
           ylabel='Minion Stats',
           title='Average Minion Stats per Mana Cost ({})'.format(format_format_title(hs_format)))
    # Now we will annotate the top of the bars with their corresponding value
    # Setting up bar annotation
    xpos = 'center'
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    # Annotate the top of the bars with their corresponding values
    for rect in ax.patches:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() * offset[xpos], 1.01 * height,
                '{}'.format(height), ha=ha[xpos], va='bottom', rotation=90)
    # Customize plot's Legend
    leg = ax.legend(loc=2)
    leg.set_title('Type of Stats')
    for t, l in zip(leg.texts, ['Average Attack', 'Average Health']):
        t.set_text(l)

    plt.ylim(0, 12)
    if save:
        # filename = 'avg_stats_{}.png'.format(hs_format)
        # plt.savefig('../Plots/' + filename)
        save_plot('avg_stats',
                  hs_format,
                  '../Plots/')
    if show:
        plt.tight_layout()
        plt.show()


def probabilities(hs_format,
                  keyword,
                  probabilities_dict,
                  show=False,
                  save=False):
    # hearthstone_cards = CardPool(hs_format)
    # probability = hearthstone_cards.probability(keyword)
    probability = probabilities_dict
    # Construct a DataFrame for Conjurer's Calling taunt probability on each mana cost
    probability_columns = ['mana_cost', 'probability']  # DataFrames Columns
    probability_df = pd.DataFrame(columns=probability_columns)  # Create an empty DataFrame
    # Build taunt_prob_df from taunt_prob Dictionary
    for key, value in probability.items():
        probability_df = probability_df.append({'mana_cost': int(key),
                                                'probability': value * 100},
                                               ignore_index=True)
    # End of DataFrame Construction
    # Creating a Seaborn BarPlot to visualize DataFrame's data
    # X Axis Mana Cost
    # Y Axis Taunt Probability
    ax = sns.barplot(x="mana_cost", y="probability", data=probability_df, palette='pastel')
    # Customize X & Y Axis labels and the plot title
    ax.set(xlabel='Mana Cost',
           ylabel='Probability',
           title='{keyword} Probability per Mana Cost ({hs_format})'.format(keyword=keyword.title(),
                                                                            hs_format=format_format_title(hs_format)))
    # Annotate top of the Bars with the corresponding probability
    for p in ax.patches:
        ax.annotate(str(int(p.get_height())) + '%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', rotation=90)
    # Set limits for Y Axis
    plt.ylim(0, probability_df['probability'].max() + 5)  # This will never be greater than 100
    if save:
        # filename = '{keyword}_probability_{hs_format}.png'.format(keyword=keyword.title(),
        #                                                           hs_format=hs_format)
        # plt.savefig('../Plots/' + filename)
        save_plot('{key}_probability'.format(key=keyword),
                  hs_format,
                  '../Plots/')
    if show:
        plt.tight_layout()
        plt.show()

# end of file
