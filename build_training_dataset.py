import numpy as np
import pandas as pd


training_df = pd.DataFrame(columns=['year','winning_team_id','losing_team_id','seed_diff','in_tourney_last_year','historical_avg_ppg'])
tournament_game_results_df = pd.read_csv('input/NCAATourneyCompactResults.csv')
seeds_df = pd.read_csv('input/NCAATourneySeeds.csv')

for game in range(len(tournament_game_results_df.index)):
    curr_row = tournament_game_results_df.iloc[game]
    year = curr_row['Season']
    print(year)
