import pandas as pd

# All womens data
wta_1990_rankings_raw = pd.read_csv('tennis_wta/wta_rankings_90s.csv')
wta_2000_rankings_raw = pd.read_csv('tennis_wta/wta_rankings_00s.csv')
wta_2010_rankings_raw = pd.read_csv('tennis_wta/wta_rankings_10s.csv')
wta_2020_rankings_raw = pd.read_csv('tennis_wta/wta_rankings_20s.csv')
wta_current_rankings_raw = pd.read_csv('tennis_wta/wta_rankings_current.csv')
wta_players_raw = pd.read_csv('tennis_wta/wta_players.csv')
wta_players_raw['dob'] = wta_players_raw['dob'].fillna(19000101)
wta_players_raw['dob'] = wta_players_raw['dob'].astype('int64')


# Concatenate all raw data
ranking_dflist = [wta_1990_rankings_raw, wta_2000_rankings_raw,
                  wta_2010_rankings_raw, wta_2020_rankings_raw, wta_current_rankings_raw]
complete_ranking_raw = pd.concat(ranking_dflist)
complete_ranking_raw.rename(columns={'player': 'player_id'}, inplace=True)

# Top 1000 data
wta_top_1000 = wta_current_rankings_raw.loc[wta_current_rankings_raw['rank'] <= 1000]
wta_top_1000 = wta_top_1000[wta_top_1000['ranking_date'] == 20220627]
wta_top_1000.rename(columns={'player': 'player_id'}, inplace=True)


# Top 1000 players
wta_top_1000_players = pd.merge(
    wta_top_1000, wta_players_raw, on=['player_id'])
wta_top_1000_players = wta_top_1000_players.drop_duplicates(
    subset=['player_id']).drop(columns=['ranking_date'])
wta_top_1000_players.drop(columns=['wikidata_id'], inplace=True)

# Player timeseries
player_timeseries = pd.merge(
    complete_ranking_raw, wta_top_1000_players, on=['player_id'])
player_timeseries.drop(columns=[
                       'points_x', 'points_y', 'name_first', 'name_last', 'height', 'hand'], inplace=True)
player_timeseries['ranking_date'] = pd.to_datetime(
    player_timeseries.ranking_date, format='%Y%m%d').dt.year

wta_top_1000_players = pd.merge(
    wta_top_1000, wta_players_raw, on=['player_id'])
wta_top_1000_players = wta_top_1000_players.drop_duplicates(
    subset=['player_id']).drop(columns=['ranking_date'])
wta_top_1000_players.drop(columns=['wikidata_id'], inplace=True)

player_timeseries = pd.merge(
    complete_ranking_raw, wta_top_1000_players, on=['player_id'])
player_timeseries.drop(columns=[
                       'points_x', 'points_y', 'name_first', 'name_last', 'height', 'hand'], inplace=True)
player_timeseries['ranking_date'] = pd.to_datetime(
    player_timeseries.ranking_date, format='%Y%m%d').dt.year

# Top 1000 timeseries
top_1000_timeseries = player_timeseries.groupby(
    ['player_id', 'ranking_date']).agg({'min'})[['rank_x']].unstack(0)
top_1000_timeseries = top_1000_timeseries.stack(
    [0, 1]).reset_index([1, 2], drop=True)

# Top 1000 dictionary with all the info
top_1000_historical = {}
for player_id in top_1000_timeseries.columns:
    player_timeseries = top_1000_timeseries[player_id].to_frame().rename(columns={
        player_id: 'rank'})
    player_timeseries['player_id'] = player_id
    player_historical = player_timeseries.reset_index().merge(wta_top_1000_players, on=[
        'player_id']).rename(columns={'rank_x': 'annual_best_rank', 'rank_y': 'current_rank'})
    player_historical = player_historical[player_historical['annual_best_rank'].notna(
    )].reset_index(drop=True)
    player_historical['age'] = player_historical['ranking_date'] - \
        pd.to_datetime(player_historical['dob'], format='%Y%m%d').dt.year
    top_1000_historical[player_historical.iat[0, 3]] = player_historical


# All historical
ind_players = wta_players_raw[wta_players_raw['ioc'] == 'IND']
player_timeseries_ind = pd.merge(
    complete_ranking_raw, ind_players, on=['player_id'])
player_timeseries_ind.drop(columns=['points', 'name_first', 'name_last',
                           'height', 'hand', 'dob', 'ioc', 'wikidata_id'], inplace=True)
player_timeseries_ind['ranking_date'] = pd.to_datetime(
    player_timeseries_ind.ranking_date, format='%Y%m%d').dt.year

# Strength players
strength_players = wta_players_raw[wta_players_raw['ioc'].isin(
    ['USA', 'SUI', 'ESP', 'GBR'])]
player_timeseries_world = pd.merge(
    complete_ranking_raw, strength_players, on=['player_id'])
player_timeseries_world.drop(columns=[
                             'points', 'name_first', 'name_last', 'height', 'hand', 'dob', 'ioc', 'wikidata_id'], inplace=True)
player_timeseries_world['ranking_date'] = pd.to_datetime(
    player_timeseries_world.ranking_date, format='%Y%m%d').dt.year

# All Indians timeseries
all_ind_timeseries = player_timeseries_ind.groupby(
    ['player_id', 'ranking_date']).agg({'min'})[['rank']].unstack(0)
all_ind_timeseries = all_ind_timeseries.stack(
    [0, 1]).reset_index([1, 2], drop=True)

# All Strength timeseries
all_world_timeseries = player_timeseries_world.groupby(
    ['player_id', 'ranking_date']).agg({'min'})[['rank']].unstack(0)
all_world_timeseries = all_world_timeseries.stack(
    [0, 1]).reset_index([1, 2], drop=True)

# All historical players considered
all_historical = {}
all_timeseries = pd.concat([all_ind_timeseries, all_world_timeseries])
players = pd.concat([ind_players, strength_players])
for player_id in all_timeseries.columns:
    player_timeseries = all_timeseries[player_id].to_frame().rename(columns={
        player_id: 'rank'})
    player_timeseries['player_id'] = player_id
    player_historical = player_timeseries.reset_index().merge(
        players, on=['player_id']).rename(columns={'rank': 'annual_best_rank'})
    player_historical = player_historical[player_historical['annual_best_rank'].notna(
    )].reset_index(drop=True)
    player_historical['age'] = player_historical['ranking_date'] - \
        pd.to_datetime(player_historical['dob'], format='%Y%m%d').dt.year
    player_historical['birth_decade'] = pd.to_datetime(
        player_historical['dob'], format='%Y%m%d').dt.year//10*10
    all_historical[player_historical.iat[0, 3] + ' ' +
                   player_historical.iat[0, 4]] = player_historical


# Junior players
itf_juniors = pd.read_csv(
    'scrapy/Tennis_player_details_100_girls.csv', on_bad_lines='skip')
itf_juniors['player_name'] = itf_juniors['name_first'] + \
    ' ' + itf_juniors['name_last']
itf_juniors = itf_juniors[['player_name', 'rank', 'year', 'birth_year']]

# Getting their info in ATP rankings
wta_players_raw['player_name'] = wta_players_raw['name_first'] + \
    ' ' + wta_players_raw['name_last']
wta_players_raw.dropna(subset=['dob'], how='all', inplace=True)
wta_players_raw['birth_year'] = wta_players_raw['dob'].apply(
    lambda x: int(x)//10000)
junior_players = wta_players_raw.merge(itf_juniors, on=[
                                       'player_name', 'birth_year']).drop(columns=['name_first', 'name_last'])
junior_players = junior_players.sort_values(
    by=['rank'], ascending=True).groupby('player_name').first().reset_index()

# Getting top junior players
junior_players = junior_players[(junior_players['ioc'] == 'IND') | ((junior_players['rank'] <= 20) & (
    junior_players['ioc'].isin(['USA', 'ESP', 'GBR', 'AUS', 'FRA', 'GER', 'CAN'])))]
# Getting their ranking over time
player_timeseries = pd.merge(
    complete_ranking_raw, junior_players, on=['player_id'])
player_timeseries.drop(columns=['points', 'player_name', 'year',
                       'height', 'hand', 'year', 'wikidata_id'], inplace=True)
player_timeseries['ranking_date'] = pd.to_datetime(
    player_timeseries.ranking_date, format='%Y%m%d').dt.year

junior_timeseries = player_timeseries.groupby(
    ['player_id', 'ranking_date']).agg({'min'})[['rank_x']].unstack(0)
junior_timeseries = junior_timeseries.stack(
    [0, 1]).reset_index([1, 2], drop=True)
# Junior players historical data
junior_historical = {}
for player_id in junior_timeseries.columns:
    player_timeseries = junior_timeseries[player_id].to_frame().rename(columns={
        player_id: 'rank'})
    player_timeseries['player_id'] = player_id
    player_historical = player_timeseries.reset_index().merge(
        junior_players, on=['player_id']).rename(columns={'rank_x': 'annual_best_rank'})
    player_historical = player_historical[player_historical['annual_best_rank'].notna(
    )].reset_index(drop=True)
    player_historical['age'] = player_historical['ranking_date'] - \
        pd.to_datetime(player_historical['dob'], format='%Y%m%d').dt.year
    junior_historical[player_historical.iat[0, 8]] = player_historical
