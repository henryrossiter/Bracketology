import pandas as pd

training_df = pd.DataFrame(columns=['year','winning_team_id','losing_team_id','seed_diff','in_tourney_last_year'])#todo - add historical ppg
tournament_game_results_df = pd.read_csv('input/NCAATourneyCompactResults.csv')
seeds_df = pd.read_csv('input/NCAATourneySeeds.csv')
seeds_df.Seed = seeds_df.Seed.str[1:3]

def matchup_to_string(year, team1_num, team2_num, team1_seed, team2_seed, team1_presence_last_year, team2_presence_last_year, exp_diff):
	print("Year: "+str(year) + "\nTeam 1: "+str(team1_num) +"	seed: "+str(team1_seed) +"	Prior year tournament apperance?: " +str(team1_presence_last_year) + "\nTeam 2: "+str(team2_num)+"	seed: "+str(team2_seed)+"	Prior year tournament apperance?: "+str(team2_presence_last_year)+"\nSeed differential: "+str(int(team2_seed) - int(team1_seed))+" -- presence differential: "+str(exp_diff)+'\n')

#def prior_avg_ppg(team_id, up_to_year):

for game in range(64, len(tournament_game_results_df.index)):
	curr_row = tournament_game_results_df.iloc[game]
	year = curr_row['Season']
	w_team_id = curr_row['WTeamID']
	l_team_id = curr_row['LTeamID']
	w_team_seed_row = seeds_df.loc[(seeds_df['Season'] == year) & (seeds_df['TeamID'] == w_team_id)] #string
	l_team_seed_row = seeds_df.loc[(seeds_df['Season'] == year) & (seeds_df['TeamID'] == l_team_id)] #string
	w_team_seed = w_team_seed_row['Seed'].iloc[0]
	l_team_seed = l_team_seed_row['Seed'].iloc[0]
	seed_diff = int(l_team_seed) - int(w_team_seed)
	w_team_in_tourney_last_year = ((seeds_df['Season'] == year-1) & (seeds_df['TeamID'] == w_team_id)).any()
	l_team_in_tourney_last_year = ((seeds_df['Season'] == year-1) & (seeds_df['TeamID'] == l_team_id)).any()
	exp_diff = int(w_team_in_tourney_last_year) - int(l_team_in_tourney_last_year)
	matchup_to_string(year, w_team_id, l_team_id, w_team_seed, l_team_seed, w_team_in_tourney_last_year, l_team_in_tourney_last_year, exp_diff)
	new_row = [year, w_team_id, l_team_id, seed_diff,  exp_diff]
	training_df.loc[len(training_df)] = new_row
training_df.to_csv('training_data.csv')
