import pandas as pd
from collections import Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

seeds_df = pd.read_csv('input/NCAATourneySeeds.csv')
seasons_df = pd.read_csv('input/Seasons.csv')
conf_games_df = pd.read_csv('input/ConferenceTourneyGames.csv')
coaches_df = pd.read_csv('input/TeamCoaches.csv')
teams_df = pd.read_csv('input/Teams.csv')
tourney_results_df = pd.read_csv('input/NCAATourneyCompactResults.csv')
season_results_df = pd.read_csv('input/RegularSeasonCompactResults.csv')
season_extended_results_df = pd.read_csv('input/RegularSeasonDetailedResults.csv')

#create dict to map team id's to team names
teams = {}
for row in teams_df.itertuples():
    teams[str(row[1])] = str(row[2])

def one_seeds_barplot():
    #count one seeds
    one_seeds_by_team = Counter()
    for row in seeds_df.itertuples():
        if int(row[2][1:3]) == 1:
            one_seeds_by_team[teams[str(row[3])]] += 1

    #make DataFrame out of Counter
    one_seeds_df = pd.DataFrame.from_dict(one_seeds_by_team, orient = 'index').reset_index()
    one_seeds_df.columns = ['team','one seeds']
    one_seeds_df = one_seeds_df.sort_values(by = 'one seeds', ascending = False)

    sns.set(style="whitegrid")

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(10, 8), dpi=96)

    sns.set_color_codes("pastel")
    sns.barplot(x="one seeds", y="team", data=one_seeds_df, color="b")

    # Add a legend and informative axis label
    #ax.legend(ncol=1, loc="lower right", frameon=True)
    ax.set(xlim=(0, 14), ylabel="",
           xlabel="one seeds in history")
    sns.despine(left=True, bottom=True)

    plt.savefig('oneseeds.svg')


def get_tourney_wins(year, team_id):
    df = tourney_results_df.loc[tourney_results_df['Season'] == year]
    df = df.loc[df['WTeamID'] == team_id]
    return df.shape[0]

def get_reg_season_wins(year, team_id):
    df = season_results_df.loc[season_results_df['Season'] == year]
    df = df.loc[df['WTeamID'] == team_id]
    return df.shape[0]

def get_seed(year, team_id):
    df = seeds_df.loc[seeds_df['Season'] == year]
    print(df.shape[0])
    df = df.loc[df['TeamID'] == team_id]
    print(df.shape[0])
    return df['Seed'].iloc[0][1:3]

def get_reg_season_games(year, team_id):
    df = season_results_df.loc[season_results_df['Season'] == year]
    df = df.loc[(df['WTeamID'] == team_id) | (df['LTeamID'] == team_id)]
    return df.shape[0]

def get_reg_season_points(year, team_id):
    df = season_results_df.loc[season_results_df['Season'] == year]
    df1 = df.loc[df['WTeamID'] == team_id]
    tot_points = df1['WScore'].sum()
    df2 = df.loc[df['LTeamID'] == team_id]
    tot_points += df2['LScore'].sum()
    return tot_points
def get_reg_season_blocks(year, team_id):
    df = season_extended_results_df.loc[season_extended_results_df['Season'] == year]
    df1 = df.loc[df['WTeamID'] == team_id]
    tot_blks = df1['WBlk'].sum()
    df2 = df.loc[df['LTeamID'] == team_id]
    tot_blks += df2['LBlk'].sum()
    return tot_blks
def get_turnovers(year, team_id):
    df = season_extended_results_df.loc[season_extended_results_df['Season'] == year]
    df1 = df.loc[df['WTeamID'] == team_id]
    tot_to = df1['WTO'].sum()
    df2 = df.loc[df['LTeamID'] == team_id]
    tot_to += df2['LTO'].sum()
    return tot_to

def get_takeaways(year, team_id):
    df = season_extended_results_df.loc[season_extended_results_df['Season'] == year]
    df1 = df.loc[df['WTeamID'] == team_id]
    tot_ta = df1['LTO'].sum()
    df2 = df.loc[df['LTeamID'] == team_id]
    tot_ta += df2['WTO'].sum()
    return tot_ta

def get_reg_season_ppg(year, team_id):
    return get_reg_season_points(year, team_id)/get_reg_season_games(year, team_id)

def get_reg_season_ot_games(year, team_id):
    df = season_results_df.loc[season_results_df['Season'] == year]
    df = df.loc[(df['WTeamID'] == team_id) | (df['LTeamID'] == team_id)]
    df = df.loc[df['NumOT'] != 0]
    return df.shape[0]

accum_data_df = pd.DataFrame(columns=['tourney_wins','seed','season_games','season_win_pct','season_ppg','bpg','topg','tapg','season_ot_games'])

def construct_master_dataset():
    index = 0
    for row in seeds_df.itertuples():
        year = row[1]
        team = row[3]
        print('year: {}      team: {}'.format(str(year),str(team)))
        new_row = []
        new_row.append(get_tourney_wins(year,team))
        new_row.append(get_seed(year,team))
        games = get_reg_season_games(year,team)
        wins = get_reg_season_wins(year,team)
        new_row.append(games)
        new_row.append(wins/games)
        new_row.append(get_reg_season_ppg(year,team))
        new_row.append(get_reg_season_blocks(year,team)/games)
        new_row.append(get_turnovers(year,team)/games)
        new_row.append(get_takeaways(year,team)/games)
        new_row.append(get_reg_season_ot_games(year,team))
        print(new_row)
        accum_data_df.loc[index] = new_row
        index += 1
    recent_data_df = accum_data_df.dropna()
    accum_data_df.to_csv('all_training_data.csv', index=False)
    recent_data_df.to_csv('recent_training_data.csv', index=False)
construct_master_dataset()
