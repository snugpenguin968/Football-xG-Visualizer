import streamlit as st
import pandas as pd
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
from plotly.subplots import make_subplots




def format_title(title, subtitle=None, subtitle_font_size=14):
    title = f'<b>{title}</b>'
    if not subtitle:
        return title
    subtitle = f'<span style="font-size: {subtitle_font_size}px;">{subtitle}</span>'
    return f'{title}<br>{subtitle}'
def ExpectedPoints(points_df):
    fig = px.bar(points_df, x=points_df.index, y=['Expected Points', 'Points'], barmode='group',
                 title='{} {} Expected Points and Points'.format(league_choice,search_year), color_discrete_sequence=['red', 'green'],width=1400)
    fig.update_layout(xaxis_title='Team',yaxis_title='Points')
    return fig

def ExpectedGoals(goals_df):
    fig = make_subplots(rows=2, cols=1,vertical_spacing=0.15)
    fig.update_layout(title='{} {} xG and Goals Scored'.format(league_choice,search_year), width=1400,height=800)
    fig.add_trace(go.Bar(y=goals_df['xG'], x=goals_df.index,name='Expected Goals',marker=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Bar(y=goals_df['Scored'], x=goals_df.index, name='Goals',marker=dict(color='green')), row=1, col=1)
    fig.add_trace(go.Bar(y=goals_df['Goals Scored-Expected Goals'], x=goals_df.index,name='Goals Scored-Expected Goals'), row=2, col=1)
    return fig

def ExpectedConceded(ga_df):
    fig = px.bar(ga_df, x=ga_df.index, y=['Conceded', 'Expected Goals Against'], barmode='group',
                 title='Disneyliga 2021 Goals Conceded and xGA')
    fig = px.bar(ga_df, x=ga_df.index, y='Expected Goals Against-Goals Against')

    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.15)
    fig.update_layout(title='{} {} Expected Goals Against and Goals Conceded'.format(league_choice, search_year), width=1400, height=800)
    fig.add_trace(go.Bar(y=ga_df['Expected Goals Against'], x=ga_df.index, name='Expected Goals Against', marker=dict(color='red')), row=1,
                  col=1)
    fig.add_trace(go.Bar(y=ga_df['Conceded'], x=ga_df.index, name='Goals Against', marker=dict(color='green')), row=1,
                  col=1)
    fig.add_trace(
        go.Bar(y=ga_df['Expected Goals Against-Goals Against'], x=ga_df.index, name='Expected Goals Against-Goals Conceded'), row=2,
        col=1)
    return fig
def GoalsScatter(goals_df):
    fig = px.scatter(goals_df, x=goals_df['xG'], y=goals_df['Scored'], hover_data=[goals_df.index],
                     color='Goals Scored-Expected Goals', size='Scored',
                     color_continuous_scale=px.colors.sequential.BuGn)
    fig.update_layout(title='{} {} Goals Scored vs xG'.format(league_choice, search_year),
                      width=1000, height=500)
    return fig
def ConcededScatter(ga_df):
    fig = px.scatter(ga_df, x=ga_df['Expected Goals Against'], y=ga_df['Conceded'], hover_data=[ga_df.index],
                     color='Expected Goals Against-Goals Against', size='Conceded',
                     color_continuous_scale=px.colors.sequential.Hot)
    fig.update_layout(title='{} {} Goals Against vs Expected Goals Against'.format(league_choice, search_year),
                      width=1000, height=500)
    return fig
def DeepPasses(deep_df):
    fig = px.scatter(deep_df, x=deep_df['Deep Passes'], y=deep_df['Scored'], hover_data=[deep_df.index],
                     color='Scored', size='Scored')
    fig.update_layout(title=format_title('{} {} Goals Scored vs Deep Passes'.format(league_choice, search_year),
                                         "Deep passes are passes completed within 20 yards of the opponent's goal (crosses excluded)"),
                      width=1000, height=500)

    return fig

def DeepAllowed(deep_df):
    fig = px.scatter(deep_df, x=deep_df['Deep Passes Allowed'], y=deep_df['Conceded'], hover_data=[deep_df.index],
                     color='Conceded', size='Conceded', color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_layout(title=format_title('{} {} Goals Allowed vs Deep Passes Allowed'.format(league_choice, search_year),"Deep passes are opponent passes completed within 20 yards of goal (crosses excluded)"),
                      width=1000, height=500)
    return fig
def PPDA(deeo_df):
    fig = px.scatter(deep_df, x=deep_df['PPDA'], y=deep_df['Scored'], hover_data=[deep_df.index], size='Scored',
                     color='Deep Passes', color_continuous_scale=px.colors.sequential.YlGn)
    fig.update_layout(
        title=format_title('{} {} Goals Scored vs PPDA'.format(league_choice, search_year),
                           "PPDA is passes allowed per defensive action in the opposition half - i.e. team's pressing power"),
        width=1000, height=500)
    return fig
def OPPDA(deep_df):
    fig = px.scatter(deep_df, x=deep_df['OPPDA'], y=deep_df['Conceded'], hover_data=[deep_df.index],
                     color='Deep Passes Allowed', size='Conceded', color_continuous_scale=px.colors.sequential.OrRd)
    fig.update_layout(
        title=format_title('{} {} Goals Allowed vs OPPDA'.format(league_choice, search_year),
                           "OPPDA is how many passes the opponent allowed per defensive action in your team's half - i.e. opponent's pressing power."),
        width=1000, height=500)
    return fig



st.set_page_config(layout='wide',initial_sidebar_state='collapsed')
all_teams=pd.read_csv('teams.csv')
all_teams=all_teams.rename(columns={'Unnamed: 0':'league','Unnamed: 1':'year'})
all_teams.set_index(['league','year'],inplace=True)
league_list=['Bundesliga','La Liga','Ligue 1','Premier League','Serie A']

league_choice=st.selectbox('Select a League',league_list)
search_year=st.selectbox('Choose a Season',[2014,2015,2016,2017,2018,2019,2020,2021])
button=st.button('Submit')

if button:
    try:
        league_new=None
        if league_choice=="La Liga":
            league_new="La_liga"
        elif league_choice=="Premier League":
            league_new="EPL"
        elif league_choice=="Serie A":
            league_new="Serie_A"
        elif league_choice=="Ligue 1":
            league_new="Ligue_1"
        else:
            league_new="Bundesliga"
        league = []
        for index, row in all_teams.iterrows():
            if index[0] == league_new and index[1] == search_year:
                league.append(row)

        all_points = []
        all_xpts = []
        xpts_diff = []
        team_names = []
        goals_scored = []
        xG = []
        xgdiff = []
        goals_against = []
        xgoals_against = []
        xgoals_against_diff = []
        deep = []
        deep_allowed = []
        ppda = []
        oppda = []
        for i in league:
            team_names.append(i['team'])
            all_points.append(i['pts'])
            all_xpts.append(i['xpts'])
            xpts_diff.append(i['xpts_diff'])
            goals_scored.append(i['scored'])
            xG.append(i['xG'])
            xgdiff.append(i['xG_diff'])
            goals_against.append(i['missed'])
            xgoals_against.append(i['xGA'])
            xgoals_against_diff.append(i['xGA_diff'])
            deep.append(i['deep'])
            deep_allowed.append(i['deep_allowed'])
            ppda.append(i['ppda_coef'])
            oppda.append(i['oppda_coef'])

        points_df = pd.DataFrame({'Points': all_points, 'Expected Points': all_xpts})
        points_df.index = team_names
        goals_df = pd.DataFrame({'Scored': goals_scored, 'xG': xG, 'Goals Scored-Expected Goals': xgdiff})
        goals_df.index = team_names
        ga_df = pd.DataFrame({'Conceded': goals_against, 'Expected Goals Against': xgoals_against,
                              'Expected Goals Against-Goals Against': xgoals_against_diff})
        ga_df.index = team_names
        deep_df = pd.DataFrame(
            {'Deep Passes': deep, 'Deep Passes Allowed': deep_allowed, 'Scored': goals_scored, 'Conceded': goals_against,
             'PPDA': ppda, 'OPPDA': oppda})
        deep_df.index = team_names

        st.plotly_chart(ExpectedPoints(points_df))
        st.plotly_chart(ExpectedGoals((goals_df)))
        st.plotly_chart(ExpectedConceded(ga_df))
        st.plotly_chart(GoalsScatter(goals_df))
        st.plotly_chart(ConcededScatter(ga_df))

        st.plotly_chart(DeepPasses(deep_df))
        st.plotly_chart(DeepAllowed(deep_df))
        st.plotly_chart(PPDA(deep_df))
        st.plotly_chart(OPPDA(deep_df))
    except:
        st.write("There was an error. Please try again with different values.")




