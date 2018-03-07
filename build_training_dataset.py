import pandas as pd


training_df = pd.DataFrame(columns=['year','winning_team_id','losing_team_id','seed_diff','in_tourney_last_year','historical_avg_ppg'])
tournament_game_results_df = pd.read_csv('input/NCAATourneyCompactResults.csv')
seeds_df = pd.read_csv('input/NCAATourneySeeds.csv')

def matchup_to_string(team1_num, team2_num, team1_seed, team2_seed, team1_presence_last_year, team2_presence_last_year, exp_diff):
	print("Team 1: "+str(team1_num)+"	seed: "+str(team1_seed)+"	in tourney last year: "+str(team1_presence_last_year))
	print("Team 2: "+str(team2_num)+"	seed: "+str(team2_seed)+"	in tourney last year: "+str(team2_presence_last_year))
	print("Seed differential: "+str(team2_seed - team1_seed)+" -- presence differential: "+str(exp_diff)+'\n')

#def prior_avg_ppg(team_id, up_to_year):

for game in range(len(tournament_game_results_df.index)):
	curr_row = tournament_game_results_df.iloc[game]
	year = curr_row['Season']
	w_team_id = curr_row['WTeamID']
	l_team_id = curr_row['LTeamID']
	w_team_seed = seeds_df.loc[(seeds_df['Season'] == year) & (seeds_df['TeamID'] == w_team_id)] #string
	print(w_team_seed)
	l_team_seed = seeds_df.loc[(seeds_df['Season'] == year) & (seeds_df['TeamID'] == l_team_id)] #string
	w_team_seed = w_team_seed.Seed.astype(str)
	l_team_seed = l_team_seed.Seed.astype(str)
	print(w_team_seed)
	seed_diff = int(l_team_seed[1:]) - int(w_team_seed[1:])
	w_team_in_tourney_last_year = (seeds['Season'] == year and seeds['TeamID'] == w_team_id).any()
	l_team_in_tourney_last_year = (seeds['Season'] == year and seeds['TeamID'] == l_team_id).any()
	exp_diff = int(w_team_in_tourney_last_year) - int(l_team_in_tourney_last_year)
	matchup_to_string(w_team_id, l_team_id, w_team_seed, l_team_seed, w_team_in_tourney_last_year, l_team_in_tourney_last_year, exp_diff)
