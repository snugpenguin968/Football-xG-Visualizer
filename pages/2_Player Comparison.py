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
import datetime as dt
from plotly import tools
from plotly.subplots import make_subplots
from plotly.offline import plot
import streamlit as st


def p90_Calculator(variable_value, minutes_played):
    ninety_minute_periods = minutes_played/90
    p90_value = variable_value/ninety_minute_periods
    return p90_value

def shotMap(bigdf):
    fig = px.scatter(bigdf, x='X', y='Y', color='shotType', size='xG', hover_data=['date', 'result'], width=1300,
                     height=800, facet_col='player', facet_col_wrap=2)
    # fig=px.scatter(mane,x='X',y='Y',color='shotType',size='xG',hover_data=['date','result'],width=800,height=800)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, xaxis_showticklabels=False,
                      yaxis_showticklabels=False, xaxis_visible=False, yaxis_visible=False, xaxis2_showgrid=False,
                      yaxis2_showgrid=False, xaxis2_showticklabels=False, yaxis2_showticklabels=False,
                      xaxis2_visible=False, yaxis2_visible=False)
    fig.add_shape(type="line", x0=1.01, y0=0, x1=1.01, y1=1, line=dict(color="white"))
    fig.add_shape(type="line", x0=1.01, y0=1, x1=0.55, y1=1, line=dict(color="white"))
    fig.add_shape(type="line", x0=0.55, y0=0, x1=1.01, y1=0, line=dict(color="white"))
    fig.add_shape(type='rect', x0=0.81, y0=0.20, x1=1.01, y1=0.79, line=dict(color='white'))
    fig.add_shape(type='rect', x0=0.94, y0=0.36, x1=1.01, y1=0.63, line=dict(color='white'))

    fig.add_shape(type="line", x0=1.01, y0=0, x1=1.01, y1=1, line=dict(color="white"), row=1, col=2)
    fig.add_shape(type="line", x0=1.01, y0=1, x1=0.55, y1=1, line=dict(color="white"), row=1, col=2)
    fig.add_shape(type="line", x0=0.55, y0=0, x1=1.01, y1=0, line=dict(color="white"), row=1, col=2)
    fig.add_shape(type='rect', x0=0.81, y0=0.20, x1=1.01, y1=0.79, line=dict(color='white'), row=1, col=2)
    fig.add_shape(type='rect', x0=0.94, y0=0.36, x1=1.01, y1=0.63, line=dict(color='white'), row=1, col=2)

    return fig
def lineChart(player,player2,player1name,player2name):
    fig = make_subplots(rows=1, cols=2,shared_yaxes=True)
    fig.update_layout(title='Cumulative Goals and Cumulative xG Over Time',width=1300)
    fig.add_trace(go.Scatter(x=player.date, y=player['cum goals'], name='{} goals'.format(player1name), mode='lines',
                             line_color="#006400"), row=1, col=1)
    fig.add_trace(
        go.Scatter(x=player.date, y=player['cum xg'], name='{} xG'.format(player1name), mode='lines', line_color='#ff0000'),
        row=1, col=1)

    fig.add_trace(go.Scatter(x=player2.date, y=player2['cum goals'], name='{} goals'.format(player2name), mode='lines',
                             line_color="#006400"), row=1, col=2)
    fig.add_trace(
        go.Scatter(x=player2.date, y=player2['cum xg'], name='{} xG'.format(player2name), mode='lines', line_color='#ff0000'),
        row=1, col=2)
    return fig
def shotTypes(player,player2,player1name,player2name):
    shotTypes = pd.DataFrame(player['shotType'].value_counts())
    shotTypes2 = pd.DataFrame(player2['shotType'].value_counts())

    labels1 = shotTypes.index
    values1 = shotTypes['shotType']

    labels2 = shotTypes2.index
    values2 = shotTypes2['shotType']

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])
    fig.update_layout(title='Player Shot Types',width=1200)
    fig.add_trace(go.Pie(values=values1, labels=labels1, name=player1name, marker=dict(colors=px.colors.sequential.RdBu)),
                  row=1, col=1)
    fig.add_trace(go.Pie(values=values2, labels=labels2, name=player2name), row=1, col=2)
    return fig
def results(player,player2,player1name,player2name):
    result1 = pd.DataFrame(player['result'].value_counts())
    result2 = pd.DataFrame(player2['result'].value_counts())

    labels1 = result1.index
    values1 = result1['result']

    labels2 = result2.index
    values2 = result2['result']

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])
    fig.update_layout(title='Player Shot Results',width=1200)
    fig.add_trace(go.Pie(values=values1, labels=labels1, name=player1name, marker=dict(colors=px.colors.sequential.RdBu)),
                  row=1, col=1)
    fig.add_trace(go.Pie(values=values2, labels=labels2, name=player2name), row=1, col=2)
    return fig
def shotTypesxG(player,player2,player1name,player2name):
    values1 = player.groupby('shotType')['xG'].mean()
    values2 = player2.groupby('shotType')['xG'].mean()

    labels1 = values1.index

    labels2 = values2.index

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'bar'}]],shared_yaxes=True)
    fig.update_layout(title='Player Shot Types by Mean xG',width=1400)
    fig.add_trace(go.Bar(y=values1, x=labels1, name=player1name, marker=dict(color='goldenrod')), row=1, col=1)
    fig.add_trace(go.Bar(y=values2, x=labels2, name=player2name, marker=dict(color='palegoldenrod')), row=1, col=2)
    return fig
def resultsxG(player,player2,player1name,player2name):
    values1 = player.groupby('result')['xG'].mean()
    values2 = player2.groupby('result')['xG'].mean()

    labels1 = values1.index

    labels2 = values2.index

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'bar'}, {'type': 'bar'}]],shared_yaxes=True)
    fig.update_layout(title='Player Shot Results by Mean xG',width=1400)
    fig.add_trace(go.Bar(y=values1, x=labels1, name=player1name), row=1, col=1)
    fig.add_trace(go.Bar(y=values2, x=labels2, name=player2name), row=1, col=2)
    return fig
def hist(bigdf):
    fig = px.histogram(bigdf, x="xG", marginal="box", facet_col='player', color_discrete_sequence=['red', 'green'],
                       width=1400, color='IsGoal')
    fig.update_layout(title='Distribution of xG')
    return fig
st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
player1_id=st.text_input("Understat ID","2371")
player2_id=st.text_input("Understat ID","2097")
dates_input=st.slider('Select Season Range',value=(dt.date(2014,1,1).year,dt.date(2021,1,1).year),min_value=2014,max_value=2021)
st.write('As an example, this compares Ronaldo and Messi')
button=st.button("Search")
start=dates_input[0]
end=dates_input[1]

if button:
    understat = UnderstatClient()
    try:
        player_shot_data1 = understat.player(player=player1_id).get_shot_data()
        player = pd.DataFrame(player_shot_data1)
        player_shot_data2=understat.player(player=player2_id).get_shot_data()
        player2=pd.DataFrame(player_shot_data2)
        player.loc[:, ['X', 'Y', 'minute', 'xG', 'season', 'h_goals', 'a_goals']] = player.loc[:,['X', 'Y', 'minute', 'xG', 'season','h_goals', 'a_goals']].astype(float)
        player2.loc[:, ['X', 'Y', 'minute', 'xG', 'season', 'h_goals', 'a_goals']] = player2.loc[:,['X', 'Y', 'minute', 'xG', 'season','h_goals', 'a_goals']].astype(float)
        player = player[player.result != 'OwnGoal']
        player2 = player2[player2.result != 'OwnGoal']
        player['date'] = pd.to_datetime(player['date']).dt.date
        player['Goals Scored'] = 0
        player2['date'] = pd.to_datetime(player2['date']).dt.date
        player2['Goals Scored'] = 0
        player1name = player['player'][0]
        player2name = player2['player'][0]
        for index, row in player.iterrows():
            if row['result'] == 'Goal':
                player.at[index, 'Goals Scored'] = 1
        for index, row in player2.iterrows():
            if row['result'] == 'Goal':
                player2.at[index, 'Goals Scored'] = 1

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

        player2['cum goals'] = np.round(player2['Goals Scored'].cumsum().to_numpy().astype(np.double), decimals=6)
        player2['cum xg'] = np.round(player2['xG'].cumsum().to_numpy().astype(np.double), decimals=6)
        player2['diff'] = np.round((player2['Goals Scored'] - player2['xG']).to_numpy().astype(np.double), decimals=6)
        player2['xG'] = np.round(player2['xG'].to_numpy().astype(np.double), decimals=6)
        player2['IsGoal'] = np.nan
        for index, row in player2.iterrows():
            if row['result'] == 'Goal':
                player2.at[index, 'IsGoal'] = 'Goal'
            else:
                player2.at[index, 'IsGoal'] = 'No Goal'
        player2 = player2.loc[(player2['season'] >= start) & (player2['season'] <= end)]

        bigdf = pd.concat([player, player2], ignore_index=True)


        st.plotly_chart(shotMap(bigdf))
        st.plotly_chart(lineChart(player,player2,player1name,player2name))
        st.plotly_chart(shotTypes(player,player2,player1name,player2name))
        st.plotly_chart(results(player,player2,player1name,player2name))
        st.plotly_chart(shotTypesxG(player,player2,player1name,player2name))
        st.plotly_chart(resultsxG(player,player2,player1name,player2name))
        st.plotly_chart(hist(bigdf))
    except Exception as e:
        st.write("There was an error. Please retry with different values. ")
