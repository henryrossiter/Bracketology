import pandas as pd

training_df = pd.DataFrame(columns=['year','team1_id','team2_id','seed_diff','in_tourney_last_year','previous_ppg_diff','result'])#todo - add historical ppg
tournament_game_results_df = pd.read_csv('input/NCAATourneyCompactResults.csv')
seeds_df = pd.read_csv('input/NCAATourneySeeds.csv')
seeds_df.Seed = seeds_df.Seed.str[1:3]

def matchup_to_string(year, team1_num, team2_num, team1_seed, team2_seed, team1_presence_last_year, team2_presence_last_year, exp_diff):
	print("Year: "+str(year) + "\nTeam 1: "+str(team1_num) +"	seed: "+str(team1_seed) +"	Prior year tournament apperance?: " +str(team1_presence_last_year) + "\nTeam 2: "+str(team2_num)+"	seed: "+str(team2_seed)+"	Prior year tournament apperance?: "+str(team2_presence_last_year)+"\nSeed differential: "+str(int(team2_seed) - int(team1_seed))+" -- presence differential: "+str(exp_diff)+'\n')

def last3_avg_points(team_id, year):
	cum_sum = 0
	all_prior_games = tournament_game_results_df['Season'] < year
	all_won_team_games = tournament_game_results_df['WTeamID'] == team_id
	all_lost_team_games = tournament_game_results_df['LTeamID'] == team_id
	all_prior_team_games = tournament_game_results_df[(all_won_team_games | all_lost_team_games) & all_prior_games]
	if len(all_prior_team_games.index) == 0:
		return 0
	if len(all_prior_team_games.index) > 3:
		last_3_games = all_prior_team_games.tail(3)
	else:
		last_3_games = all_prior_team_games
	for row in last_3_games.itertuples():
		if row[3] == team_id:
			cum_sum = cum_sum + row[4]
		elif row[5] == team_id:
			cum_sum = cum_sum + row[6]
	return cum_sum/len(last_3_games.index)

for game in range(64, len(tournament_game_results_df.index)):
	curr_row = tournament_game_results_df.iloc[game]
	year = curr_row['Season']
	w_team_id = curr_row['WTeamID']
	l_team_id = curr_row['LTeamID']
	w_team_seed_row = seeds_df.loc[(seeds_df['Season'] == year) & (seeds_df['TeamID'] == w_team_id)]
	l_team_seed_row = seeds_df.loc[(seeds_df['Season'] == year) & (seeds_df['TeamID'] == l_team_id)]
	w_team_seed = w_team_seed_row['Seed'].iloc[0]
	l_team_seed = l_team_seed_row['Seed'].iloc[0]
	seed_diff = int(l_team_seed) - int(w_team_seed)
	w_team_in_tourney_last_year = ((seeds_df['Season'] == year-1) & (seeds_df['TeamID'] == w_team_id)).any()
	l_team_in_tourney_last_year = ((seeds_df['Season'] == year-1) & (seeds_df['TeamID'] == l_team_id)).any()
	exp_diff = int(w_team_in_tourney_last_year) - int(l_team_in_tourney_last_year)
	ppg_prev_diff = last3_avg_points(w_team_id, year) - last3_avg_points(l_team_id, year)
	matchup_to_string(year, w_team_id, l_team_id, w_team_seed, l_team_seed, w_team_in_tourney_last_year, l_team_in_tourney_last_year, exp_diff)
	if game % 2 == 1:
		new_row = [year, w_team_id, l_team_id, seed_diff,  exp_diff, ppg_prev_diff, 1]
	else:
		new_row = [year, l_team_id, w_team_id, -seed_diff,  -exp_diff, -ppg_prev_diff, 0]
	training_df.loc[len(training_df)] = new_row
training_df.to_csv('training_data.csv', index=False)
