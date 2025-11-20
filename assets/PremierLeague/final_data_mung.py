import pandas as pd
import numpy as np
import os

#GOALS SCORED BY TEAMS
goals_df = pd.read_csv(os.path.join("csv_files", "PremierLeague24_25(Goals).csv"), encoding="latin-1")
goals_df["Goals"] = 1
teams_goals = goals_df.groupby("Team")["Goals"].sum().reset_index()
player_goals = goals_df.groupby(["Team", "Scorer"])["Goals"].sum().reset_index()
teams_goals.to_csv("PremierLeague24_25(Teams_Goals).csv", index=False)
player_goals.to_csv("PremierLeague24_25(Player_Goals).csv", index=False)

#GOALS CONCEDED BY TEAMS
if 'Opponent' in goals_df.columns:
    goals_conceded = goals_df.groupby("Opponent")["Goals"].sum().reset_index()
    goals_conceded.columns = ["Team", "Goals_Conceded"]
    goals_conceded.to_csv("PremierLeague24_25(Goals_Conceded).csv", index=False)

#OPPOSITION SCORES (Head-to-Head)
if 'Opponent' in goals_df.columns:
    opposition_scores = goals_df.groupby(["Team", "Opponent", "Round"])["Goals"].sum().reset_index()
    opposition_scores.columns = ["Team", "Opponent", "Gameweek", "Goals_Scored"]
    opposition_scores = opposition_scores.sort_values(["Team", "Gameweek"])
    opposition_scores.to_csv("csv_files/PremierLeague24_25(Opposition_Scores).csv", index=False)

#GOALS CONCEDED BY GAMEWEEK
goals_conceded_gw = goals_df.groupby(["Opponent", "Round"])["Goals"].sum().reset_index()
goals_conceded_gw["Round_Num"] = goals_conceded_gw["Round"].astype(str).str.extract(r"(\d+)").astype(int)
goals_conceded_gw = goals_conceded_gw.sort_values(["Opponent", "Round_Num"])
teams = goals_conceded_gw["Opponent"].unique()
rounds = range(1, 39)
complete_index = pd.MultiIndex.from_product([teams, rounds], names=["Opponent", "Round_Num"])

# Fill missing with 0s
goals_conceded_gw = (
    goals_conceded_gw.set_index(["Opponent", "Round_Num"])
    .reindex(complete_index, fill_value=0)
    .reset_index()
)

goals_conceded_gw["Cumulative_Goals_Conceded"] = goals_conceded_gw.groupby("Opponent")["Goals"].cumsum()
goals_conceded_gw = goals_conceded_gw[["Opponent", "Round_Num", "Goals", "Cumulative_Goals_Conceded"]]
goals_conceded_gw.columns = ["Team", "Gameweek", "Goals_Conceded", "Total_Goals_Conceded"]
goals_conceded_gw.to_csv("PremierLeague24_25(Goals_Conceded_By_Gameweek).csv", index=False)

#GOALS SCORED BY GAMEWEEK
goals_scored_gw = goals_df.groupby(["Team", "Round"])["Goals"].sum().reset_index()
goals_scored_gw["Round_Num"] = goals_scored_gw["Round"].astype(str).str.extract(r"(\d+)").astype(int)
goals_scored_gw = goals_scored_gw.sort_values(["Team", "Round_Num"])
teams = goals_scored_gw["Team"].unique()
rounds = range(1, 39)
complete_index = pd.MultiIndex.from_product([teams, rounds], names=["Team", "Gameweek"])

goals_scored_gw = (
    goals_scored_gw.set_index(["Team", "Round_Num"])
    .reindex(complete_index, fill_value=0)
    .rename_axis(["Team", "Gameweek"])
    .reset_index()
)

goals_scored_gw["Total_Goals"] = goals_scored_gw.groupby("Team")["Goals"].cumsum()
goals_scored_gw = goals_scored_gw.drop("Round", axis=1)
goals_scored_gw.to_csv("PremierLeague24_25(Goals_Scored_By_Gameweek).csv", index=False)
