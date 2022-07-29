from atp_ranking_progression import top_1000_historical, all_historical, junior_historical
from helper import formatting
import matplotlib.patches as mpatches
import matplotlib
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
import pandas as pd
import matplotlib.pyplot as plt
plt.xkcd(randomness=0.5, scale=0.25)

fig, axes = plt.subplots(figsize=(10, 6))
for player, player_ts in top_1000_historical.items():
    if player_ts.loc[0, 'current_rank'] <= 20:
        player_ts.plot(x='ranking_date', y='annual_best_rank',
                       legend=False, logy=True, color='#FEBA4F', ax=axes)
    elif player_ts.loc[0, 'ioc'] == 'IND':
        player_ts.plot(x='ranking_date', y='annual_best_rank',
                       legend=False, logy=True, color='#4580B1', ax=axes)
axes.plot(range(2000, 2023), (100,)*len(range(2000, 2023)),
          '--', color='#E16671', linewidth=2)
formatting(axis=axes)
fig.suptitle('ATP ranking progression - Rank vs Year')
plt.savefig('figures/rankvsyear.eps', dpi=1000)


# Second plot
fig, axes = plt.subplots(figsize=(10, 6))
for player, player_ts in top_1000_historical.items():
    if player_ts.loc[0, 'current_rank'] <= 20:
        player_ts.plot(x='age', y='annual_best_rank',
                       legend=False, logy=True, color='#FEBA4F', ax=axes)
    elif player_ts.loc[0, 'ioc'] == 'IND':
        player_ts.plot(x='age', y='annual_best_rank',
                       legend=False, logy=True, color='#4580B1', ax=axes)
axes.plot(range(15, 37), (100,)*len(range(15, 37)),
          '--', color='#E16671', linewidth=2)
formatting(axis=axes, xaxis='age')
fig.suptitle('ATP Ranking progression - Rank vs age')
plt.savefig('figures/rankvsage.eps', dpi=1000)


# ATP Performance over decades
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
for player, player_ts in all_historical.items():
    if player_ts['annual_best_rank'].min() <= 500 and player_ts.loc[0, 'ioc'] == 'IND':
        if player_ts.at[0, 'birth_decade'] in [1960, 1970]:
            player_ts.plot(x='age', y='annual_best_rank',
                           legend=False, logy=True, color='#74BBFB', ax=axes[0])
        elif player_ts.at[0, 'birth_decade'] in [1980, 1990, 2000]:
            player_ts.plot(x='age', y='annual_best_rank',
                           legend=False, logy=True, color='#77dd77', ax=axes[0])
    elif player_ts['annual_best_rank'].min() <= 10:
        if player_ts.at[0, 'birth_decade'] in [1960, 1970]:
            player_ts.plot(x='age', y='annual_best_rank',
                           legend=False, logy=True, color='#74BBFB', ax=axes[1])
        elif player_ts.at[0, 'birth_decade'] in [1980, 1990, 2000]:
            player_ts.plot(x='age', y='annual_best_rank',
                           legend=False, logy=True, color='#77dd77', ax=axes[1])

axes[0].plot(range(15, 40), (100,)*len(range(15, 40)),
             '--', color='#E16671', linewidth=2)
axes[1].plot(range(15, 40), (100,)*len(range(15, 40)),
             '--', color='#E16671', linewidth=2)
[ax.invert_yaxis() for ax in axes]
[ax.plot(range(15, 40), 25*(1,), 'k--') for ax in axes]
[ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) for ax in axes]
[ax.set_ylabel('rank', rotation=0) for ax in axes]
old_patch = mpatches.Patch(color='#74BBFB', label='Born before 1980')
new_patch = mpatches.Patch(color='#77dd77', label='Born after 1980')
# [ax.legend(handles=[old_patch,new_patch],loc='center right') for ax in axes]
fig.suptitle('ATP Performance over decades - Rank vs Age')
axes[0].set_title('Indian Men players')
axes[1].set_title('International Men players')
plt.subplots_adjust(top=0.8)
plt.savefig('figures/PerformanceOverDecades.eps', dpi=1000)


# Junior players progression
fig, axes = plt.subplots(figsize=(10, 6))
for player, player_ts in junior_historical.items():
    if player_ts.loc[0, 'ioc'] == 'IND':
        player_ts.plot(x='age', y='annual_best_rank',
                       legend=False, logy=True, color='#4580B1', ax=axes)
    else:
        player_ts.plot(x='age', y='annual_best_rank',
                       legend=False, logy=True, color='#FEBA4F', ax=axes)
axes.plot(range(15, 40), (100,)*len(range(15, 40)),
          '--', color='#E16671', linewidth=2)
axes.plot(range(15, 40), (1,)*len(range(15, 40)),
          '--', color='#FFFFFF', linewidth=2)
formatting(axis=axes, label1='World Juniors', label2='India Juniors')
fig.suptitle('Junior boys champs in ATP ranking progression - Rank vs Age')
plt.savefig('figures/juniorprogression.eps', dpi=1000)
