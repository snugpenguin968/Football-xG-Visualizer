from understatapi import UnderstatClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import numpy as np
import plotly.express as px
from matplotlib.patches import Rectangle
from matplotlib.patches import Arc
from matplotlib.patches import ConnectionPatch
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import datetime as dt

player_id=st.text_input("Understat ID","2371")
#dates_input=st.date_input('This site supports years ranging from 2014 to 2021.',value=(dt.date(2014,1,1).year,dt.date(2021,1,1).year),max_value=dt.date(2021,1,1).year,min_value=dt.date(2014,1,1).year)
dates_input=st.slider('Select Season Range',value=(dt.date(2014,1,1).year,dt.date(2021,1,1).year),min_value=2014,max_value=2021)
st.write('As an example, this represents CR7')
button=st.button("Search")
start=dates_input[0]
end=dates_input[1]


def p90_Calculator(variable_value, minutes_played):
    ninety_minute_periods = minutes_played/90
    p90_value = variable_value/ninety_minute_periods
    return p90_value
def shotMap(player):
    fig = px.scatter(player, x='X', y='Y', color='shotType', size='xG', hover_data=['date', 'result'], width=800,
                     height=600)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, xaxis_showticklabels=False,
                      yaxis_showticklabels=False, xaxis_visible=False, yaxis_visible=False,margin=dict(l=0, r=0, b=0, t=0))
    fig.add_shape(type="line", x0=1.01, y0=0, x1=1.01, y1=1, line=dict(color="white"))
    fig.add_shape(type="line", x0=1.01, y0=1, x1=0.40, y1=1, line=dict(color="white"))
    fig.add_shape(type="line", x0=0.40, y0=0, x1=1.01, y1=0, line=dict(color="white"))
    fig.add_shape(type='rect', x0=0.81, y0=0.20, x1=1.01, y1=0.79, line=dict(color='white'))
    fig.add_shape(type='rect', x0=0.94, y0=0.36, x1=1.01, y1=0.63, line=dict(color='white'))
    return fig
def lineChart(player):
    fig = go.Figure()
    fig.update_layout(width=750)
    fig.add_trace(go.Scatter(x=player.date, y=player['cum goals'], mode='lines', name='goals', line_color="#006400"))
    fig.add_trace(go.Scatter(x=player.date, y=player['cum xg'], mode='lines', name='xG', line_color='#ff0000'))
    fig.update_layout(title='Player Goals vs xG',
                      xaxis_title='Date',
                      yaxis_title='Goals')
    fig.update_traces(line=dict(width=2.2))
    return fig

def shotTypes(player):
    shotTypes = pd.DataFrame(player['shotType'].value_counts())
    fig = px.pie(shotTypes, values='shotType', names=shotTypes.index, color_discrete_sequence=px.colors.sequential.RdBu,title='Player Shot Types')
    return fig
def results(player):
    result = pd.DataFrame(player['result'].value_counts())
    fig = px.pie(result, values='result', names=result.index, color_discrete_sequence=px.colors.sequential.RdBu,title='Outcome of Player Attempts')
    return fig

def shotTypesxG(player):
    shotTypexG = player.groupby('shotType')['xG'].mean()
    fig = px.bar(shotTypexG, x=shotTypexG.index, y='xG', color_discrete_sequence=['goldenrod'],title='Mean xG for each Shot Type')
    return fig

def resultsxG(player):
    resultxG = player.groupby('result')['xG'].mean()
    fig = px.bar(resultxG, x=resultxG.index, y='xG', color_discrete_sequence=['goldenrod'],title='Mean xG for each Shot Result')
    return fig

def hist(player):
    fig = px.histogram(player, x='xG', color='IsGoal', marginal='box', color_discrete_sequence=['red', 'green'], width=800,height=600,title='Distribution of Shot Successes')
    return fig




if button:
    understat = UnderstatClient()
    
    player_shot_data = understat.player(player=player_id).get_shot_data()
    player = pd.DataFrame(player_shot_data)
    player.loc[:, ['X', 'Y', 'minute', 'xG', 'season', 'h_goals', 'a_goals']] = player.loc[:,['X', 'Y', 'minute', 'xG', 'season','h_goals', 'a_goals']].astype(float)
    player = player[player.result != 'OwnGoal']
    player['date'] = pd.to_datetime(player['date']).dt.date
    player['Goals Scored'] = 0
    for index, row in player.iterrows():
        if row['result'] == 'Goal':
            player.at[index, 'Goals Scored'] = 1

    player['cum goals'] = np.round(player['Goals Scored'].cumsum().to_numpy().astype(np.double), decimals=6)
    player['cum xg'] = np.round(player['xG'].cumsum().to_numpy().astype(np.double), decimals=6)
    player['diff'] = np.round((player['Goals Scored'] - player['xG']).to_numpy().astype(np.double), decimals=6)
    player['xG'] = np.round(player['xG'].to_numpy().astype(np.double), decimals=6)
    player['IsGoal'] = np.nan
    for index, row in player.iterrows():
        if row['result'] == 'Goal':
            player.at[index, 'IsGoal'] = 'Goal'
        else:
            player.at[index, 'IsGoal'] = 'No Goal'
    player=player.loc[(player['season'] >= start) & (player['season'] <= end)]
    st.plotly_chart(shotMap(player))
    st.plotly_chart(lineChart(player))
    st.plotly_chart(shotTypes(player))
    st.plotly_chart(results(player))
    st.plotly_chart(shotTypesxG(player))
    st.plotly_chart(resultsxG(player))
    st.plotly_chart(hist(player))

    st.write('There was an error. Please try again with a different ID or date')
