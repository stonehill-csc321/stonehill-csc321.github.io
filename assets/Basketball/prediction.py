import pandas as pd
from sklearn.linear_model import LinearRegression

df23 = pd.read_csv("team_stats_23-34.csv")
df24 = pd.read_csv("team_stats_24-25.csv")

features = ['ORtg','DRtg','NRtg','Pace','FTr','3PAr','TS%','eFG%','TOV%','ORB%','FT/FGA','eFG%','TOV%','DRB%','FT/FGA']

df23['WinPercentage'] = df23['W'] / (df23['W'] + df23['L'])
df24['WinPercentage'] = df24['W'] / (df24['W'] + df24['L'])

model = LinearRegression()
X_train = df23[features]
Y_train = df24['WinPercentage']
model.fit(X_train, Y_train)
df24['Predicted'] = model.predict(df24[features])

df24[['Team', 'Predicted', 'WinPercentage']].to_csv('predicted_vs_actual_24-25.csv')
