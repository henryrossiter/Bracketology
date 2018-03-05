import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import random

year_to_predict = int(input("enter a year to generate match predictions: "))
seeds = pd.read_csv('input/NCAATourneySeeds.csv')
seeds_last_year = seeds.loc[seeds['Season'] == year_to_predict-1]
seeds = seeds.loc[seeds['Season'] == year_to_predict]
tournament_results = pd.read_csv('input/NCAATourneyCompactResults.csv')
input_data = pd.DataFrame(columns=['team1_id','team2_id','seed_diff','in_tourney_last_year','wins_in_history'])
seed_list = seeds.Seed.tolist()
team_list = seeds.TeamID.tolist()
n_teams = len(team_list)
for i in range(n_teams):
    for j in range(i+1,n_teams):
        if bool(random.getrandbits(1)):
            team1 = team_list[i]
            team2 = team_list[j]
            team1_seed = int(seed_list[i][1:])
            team2_seed = int(seed_list[j][1:])
            seed_differential = team1_seed - team2_seed
            in_tourney_last_year = int(team1 in seeds_last_year.TeamID) - int(team1 in seeds_last_year.TeamID)
            print(str(team1)+" "+str(team2)+" "+str(team1_seed)+" "+str(team2_seed)+" "+str(seed_differential)+" "+str(in_tourney_last_year))
