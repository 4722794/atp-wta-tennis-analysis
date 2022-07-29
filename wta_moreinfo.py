from wta_ranking_progression import top_1000_historical, all_historical
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from pprint import pprint

# ATP Performance over decades
career_length = defaultdict(list)
fig, axes = plt.subplots(1, 2, figsize=(14, 4))
for player, player_ts in all_historical.items():
    if player_ts['annual_best_rank'].min() <= 1000 and player_ts.loc[0, 'ioc'] == 'IND' and player_ts['age'].max() >= 29:
        if player_ts.at[0, 'birth_decade'] in [1960, 1970]:
            career_length['old_ind'].append(
                (player, player_ts['age'].max()))
        elif player_ts.at[0, 'birth_decade'] in [1980, 1990, 2000]:
            career_length['new_ind'].append(
                (player, player_ts['age'].max()))
    elif player_ts['annual_best_rank'].min() <= 20 and player_ts['age'].max() >= 29:
        if player_ts.at[0, 'birth_decade'] in [1960, 1970]:
            career_length['old_world'].append(
                (player, player_ts['age'].max()))
        elif player_ts.at[0, 'birth_decade'] in [1980, 1990, 2000]:
            career_length['new_world'].append(
                (player, player_ts['age'].max()))

pprint({k: sum([j[1] for j in v])/len(v) for k, v in career_length.items()})
