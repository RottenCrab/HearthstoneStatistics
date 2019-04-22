import matplotlib.pyplot as plt
import pandas as pd
from conjurers_calling import ConjCalling

# Plotting Avg Stats on each mana cost
conj_obj = ConjCalling('Standard')
avg_stats = conj_obj.avg_stats()
mana_curve = avg_stats.keys()

df = pd.DataFrame(data=avg_stats)
df = df.T
ax = df.plot.bar(rot=0,
                 title='Conjurer\'s Call: Average minion Attack/Health per Mana Cost (Standard)')
ax.legend(['Attack', 'Health'])
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
plt.tight_layout()
fig = ax.get_figure()
fig.savefig('stats.png')
plt.show()
# Plotting Taunt Probability on each mana cost

# end of file
