import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import random


def matchup_to_string(team1_num, team2_num, team1_seed, team2_seed, team1_presence_last_year, team2_presence_last_year, exp_diff):
    print("Team 1: "+str(team1_num)+"   seed: "+str(team1_seed)+"   in tourney last year: "+str(team1_presence_last_year))
    print("Team 2: "+str(team2_num)+"   seed: "+str(team2_seed)+"   in tourney last year: "+str(team2_presence_last_year))
    print("Seed differential: "+str(team2_seed - team1_seed)+" -- presence differential: "+str(exp_diff)+'\n')

year_to_predict = int(input("enter a year to generate match predictions: "))

# read in teams and corresponding seeds
seeds = pd.read_csv('input/NCAATourneySeeds.csv')
seeds_last_year = seeds.loc[seeds['Season'] == year_to_predict-1]
seeds = seeds.loc[seeds['Season'] == year_to_predict]
tournament_results = pd.read_csv('input/NCAATourneyCompactResults.csv')
input_data = pd.DataFrame(columns=['team1_id','team2_id','seed_diff','in_tourney_last_year','wins_in_history'])
seed_list = seeds.Seed.tolist()
team_list = seeds.TeamID.tolist()
last_year_team_list = seeds_last_year.TeamID.tolist()
n_teams = len(team_list)
print(str(n_teams)+" teams have been identified from the "+str(year_to_predict)+" tournament")

#calculate past wins in tournaments for each team

#assemble dataset for teams
for i in range(n_teams):
    for j in range(i+1,n_teams):
        team1 = team_list[i]
        team2 = team_list[j]
        team1_seed = int(seed_list[i][1:])
        team2_seed = int(seed_list[j][1:])
        seed_differential = team2_seed - team1_seed
        experience_differential = int(team1 in last_year_team_list) - int(team2 in last_year_team_list)
        matchup_to_string(team1, team2, team1_seed, team2_seed, team1 in last_year_team_list, team2 in last_year_team_list, experience_differential)
print(str(count)+" potential matchups generated")
