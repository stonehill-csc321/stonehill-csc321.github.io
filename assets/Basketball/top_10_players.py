import pandas as pd
df = pd.read_csv('players_per_game_stats.csv')
df = df.drop_duplicates(subset=['Player'], keep='first')
df2 = df.head(10)
df2.to_csv('top10_players.csv', index=False)

df3 = pd.read_csv('team_per_game_stats_24-25.csv')
df3 = df3.head(10)
df3.to_csv('top10_teams.csv', index=False)