import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from conjurers_calling import ConjCalling


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def conjcall_avg_stats(hs_format,
                       show=False,
                       save=False):
    conj_calling = ConjCalling(hs_format)
    avg_stats = conj_calling.avg_stats()
    # Construct a DataFrame for Average Minions Stats from avg_stats Dictionary
    # Average stats DataFrame will contain the following columns: mana_cost, stats, type_of_stats
    # We select those columns in order to take advantage of hue parameter of seaborn.barplot later
    avg_stats_columns = [
        'mana_cost',
        'stats',
        'type_of_stats'
    ]
    avg_stats_df = pd.DataFrame(columns=avg_stats_columns)
    for key, value in avg_stats.items():
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
           title='Conjurer\'s Calling: Average stats per Mana Cost ({})'.format(hs_format))
    # Now we will annotate the top of the bars with their corresponding value
    # Setting up bar annotation
    xpos = 'center'
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    # Annotate the top of the bars with their corresponding values
    for rect in ax.patches:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom', rotation=90)
    # Customize plot's Legend
    leg = ax.legend(loc=2)
    leg.set_title('Type of Stats')
    for t, l in zip(leg.texts, ['Average Attack', 'Average Health']):
        t.set_text(l)

    plt.ylim(0, 12)
    if save:
        filename = 'conj_calling_avg_stats_{}.png'.format(hs_format)
        plt.savefig('../Plots/' + filename)
    if show:
        plt.tight_layout()
        plt.show()


def conjcall_taunt_probability(hs_format,
                               show=False,
                               save=False):
    conj_calling = ConjCalling(hs_format)
    taunt_prob = conj_calling.taunt_probability()
    # Construct a DataFrame for Conjurer's Calling taunt probability on each mana cost
    taunt_prob_columns = ['mana_cost', 'taunt_prob']  # DataFrames Columns
    taunt_prob_df = pd.DataFrame(columns=taunt_prob_columns)  # Create an empty DataFrame
    # Build taunt_prob_df from taunt_prob Dictionary
    for key, value in taunt_prob.items():
        taunt_prob_df = taunt_prob_df.append({'mana_cost': int(key),
                                              'taunt_prob': value * 100},
                                             ignore_index=True)
    # End of DataFrame Construction
    # Creating a Seaborn BarPlot to visualize DataFrame's data
    # X Axis Mana Cost
    # Y Axis Taunt Probability
    ax = sns.barplot(x="mana_cost", y="taunt_prob", data=taunt_prob_df, palette='pastel')
    # Customize X & Y Axis labels and the plot title
    ax.set(xlabel='Mana Cost',
           ylabel='Taunt Probability',
           title='Conjurer\'s Calling: Taunt Probability per Mana Cost ({})'.format(hs_format))
    # Annotate top of the Bars with the corresponding probability
    for p in ax.patches:
        ax.annotate(str(int(p.get_height())) + '%', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points', rotation=90)
    # Set limits for Y Axis
    plt.ylim(0, taunt_prob_df['taunt_prob'].max() + 5)  # This will never be greater than 100
    if save:
        filename = 'conj_calling_taunt_prob_{0}.png'.format(hs_format)
        plt.savefig('../Plots/' + filename)
    if show:
        plt.tight_layout()
        plt.show()


# Testing Zone
if __name__ == '__main__':
    conjcall_avg_stats('Standard', show=True, save=True)
    conjcall_avg_stats('Wild', show=True, save=True)
    conjcall_taunt_probability('Standard', show=True, save=True)
    conjcall_taunt_probability('Wild', show=True, save=True)
# end of file
