import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash()

#preparing data set for question 1
df_nutrition = pd.read_csv('Nutrition.csv')

#replace long questions with a shorter equivalent
df_nutrition["Question"].replace('Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)', 'Percent of adults who workout moderately at least 150 mins a week',inplace=True)
df_nutrition["Question"].replace('Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week','Percent of adults who achieve at workout 150 mins a week & muscle-strengthening activities 2+ days a week',inplace=True)
df_nutrition["Question"].replace('Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)','Percent of adults who workout moderately at least 300 mins a week',inplace=True)

df_death = pd.read_csv('Leading_Causes_Death.csv')

#only keep data from 2011 until 2015
df_death = df_death.loc[df_death['Year'] >= 2011]
df_nutrition = df_nutrition.loc[df_nutrition['YearStart'] <= 2015]

#remove 'All Causes'
df_death_final = df_death.loc[df_death['Cause Name'] != 'All Causes']

#remove irrelevant columns
df_death_final = df_death_final.drop('113 Cause Name', axis=1)
df_death_final = df_death_final.drop('Age-adjusted Death Rate', axis=1)
#df_death_final = df_death_final.drop('Year', axis=1)

#aggregate per cause of death per state and compute average number of deaths
df_death_final = df_death_final.groupby(['Cause Name', 'State'],as_index=False).mean()

#extract list of state
state_list = df_death_final["State"].unique()

#only keep interesting columns
df_nutrition_final = df_nutrition[['YearStart', 'YearEnd','LocationDesc','Education','Income', 'Age(years)','Race/Ethnicity' , 'Question', 'Data_Value', 'Gender']]

#year list for slider
year_list = df_nutrition_final["YearStart"].unique()

#question list for the dropdown list
question_list = df_nutrition_final["Question"].unique()

#build the option list of the state dropdown list
options_state_list = [{'label': 'All', 'value': 'All'}]
options_state_list.extend([{'label': i, 'value': i} for i in state_list])

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='options-state',
                options = options_state_list,
                value='All'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='percentage-type',
                options=[{'label': i, 'value': i} for i in question_list],
                value='Percent of adults aged 18 years and older who have obesity'
            )
        ], style={'width': '49%','float': 'right', 'display': 'inline-block'}),
        html.Div(dcc.Slider(
            id='year-slider',
            min=year_list.min(),
            max=year_list.max(),
            value=year_list.max(),
            step=None,
            marks={str(year): str(year) for year in year_list}
        ), style={'padding': '10px 20px 20px 20px'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Alabama'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
    ], style={'display': 'inline-block', 'width': '49%'}),

])

#updating main plot
@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('options-state', 'value'),
    dash.dependencies.Input('year-slider', 'value')])
def update_graph(state_input,year):
    df_death_graph = df_death_final[df_death_final['Year'] <= year]
    # df_death_graph= df_death_final

    data = []

    if(state_input != 'All'):
        data=[ go.Scatter(
            x=df_death_graph.loc[df_death_graph['State'] == state_input]["Cause Name"],
            y=df_death_graph.loc[df_death_graph['State'] == state_input]["Deaths"],
            name=state_input,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            })]
    else:
        for state in state_list:
            trace = go.Scatter(
                x=df_death_graph.loc[df_death_graph['State'] == state]["Cause Name"],
                y=df_death_graph.loc[df_death_graph['State'] == state]["Deaths"],
                name=state,
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 0.5, 'color': 'white'}
                }
            )
            data.append(trace)
    return {
        'data': data,
        'layout': go.Layout(
            margin={'l': 40, 'b': 120, 't': 10, 'r': 0},
            height=550,
            hovermode='closest'
        )
    }

#updating second plot
@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('options-state', 'value'),
     dash.dependencies.Input('percentage-type', 'value'),
     dash.dependencies.Input('year-slider', 'value')])
def bar_chart_percentage(state, percentage_type, year):
    # selected from lists
   # df_nutrition_question = df_nutrition_final[df_nutrition_final['YearEnd'] == year]
  #  df_nutrition_question = df_nutrition_question.loc[df_nutrition_question['YearStart'] == 2011]
    #df_nutrition_question = df_nutrition_question.loc[df_nutrition_question['LocationDesc'] == state]
    data = []

    if(state == 'All'):
        return {
        'data': data,
        'layout': go.Layout(
            height= 250,
            margin ={'l': 20, 'b': 30, 'r': 10, 't': 10},
            annotations=[dict(
                x=0, y=0.85, xanchor='left', yanchor='bottom',
                xref='paper', yref='paper', showarrow=False,
                align='left', bgcolor='rgba(255, 255, 255, 0.5)',
                text="You have to select a state in the left dropdown list", font=dict(family='sans serif', size=18)
            )]
        )
    }

    df_nutrition_question = df_nutrition_final.copy()
    df_nutrition_question = df_nutrition_question[df_nutrition_question['YearStart'] <= year]
    df_nutrition_question = df_nutrition_question.loc[df_nutrition_final['LocationDesc'] == state]
    df_nutrition_question = df_nutrition_question.loc[df_nutrition_question['Question'] == percentage_type]

    gender_list = df_nutrition_question["Gender"].unique()
    gender_color_list = {"Female": '#FFB6C1', "Male" : '#ADD8E6', np.nan : '#FFFFFF' }

    for gender in gender_list:
        value = df_nutrition_question.loc[df_nutrition_question['Gender'] == gender]["Data_Value"]
        trace = go.Bar(
            x=df_nutrition_question.loc[df_nutrition_question['Gender'] == gender]["YearStart"],
            y=value,
            name=gender,
            marker=dict( color=gender_color_list[gender])
        )
        data.append(trace)


    return {
        'data': data,
        'layout': go.Layout(
            barmode='stack',
            height= 250,
            margin ={'l': 20, 'b': 30, 'r': 10, 't': 10},
            annotations=[dict(
                x=0, y=0.85, xanchor='left', yanchor='bottom',
                xref='paper', yref='paper', showarrow=False,
                align='left', bgcolor='rgba(255, 255, 255, 0.5)',
                text="", font=dict(family='sans serif', size=18)#percentage_type
            )]
        )
    }

#updating third plot
@app.callback(
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('options-state', 'value'),
    dash.dependencies.Input('year-slider', 'value')
     ])
def update_pcp(state, year):
    if (state == 'All'):
        return {
            'data': [],
            'layout': go.Layout(
                height=300,
                margin={'l': 20, 'b': 30, 'r': 10, 't': 10},
                annotations=[dict(
                    x=0, y=0.85, xanchor='left', yanchor='bottom',
                    xref='paper', yref='paper', showarrow=False,
                    align='left', bgcolor='rgba(255, 255, 255, 0.5)',
                    text="You have to select a state in the left dropdown list",
                    font=dict(family='sans serif', size=18)
                )]
            )
        }
    # select year
    df_nutrition_pcp = df_nutrition_final.copy()
    df_nutrition_pcp = df_nutrition_pcp.loc[df_nutrition_final['YearStart'] <= year]
    df_nutrition_pcp = df_nutrition_pcp.loc[df_nutrition_pcp['LocationDesc'] == state]

    df_nutrition_pcp.replace(np.nan, 'unknown', inplace=True)
    df_nutrition_pcp.replace('Less than $15,000', '25k', inplace=True)
    df_nutrition_pcp.replace('$15,000 - $24,999', '25k', inplace=True)
    df_nutrition_pcp.replace('$25,000 - $34,999', '25k-50k', inplace=True)
    df_nutrition_pcp.replace('$35,000 - $49,999', '25k-50k', inplace=True)
    df_nutrition_pcp.replace('$50,000 - $74,999', '>50k', inplace=True)
    df_nutrition_pcp.replace('$75,000 or greater', '>50k', inplace=True)

    # education
    # keep relevant columns
    df_education = df_nutrition_pcp[['YearStart', 'LocationDesc', 'Education', 'YearEnd']]
    df_education = df_education.groupby(['LocationDesc', 'YearStart', 'Education'], as_index=False).count()

    # income
    # keep relevant columns
    df_income = df_nutrition_pcp[['YearStart', 'LocationDesc', 'Income', 'YearEnd']]
    df_income = df_income.groupby(['LocationDesc', 'YearStart', 'Income'], as_index=False).count()

    # age
    # keep rrelevant columns
    df_age = df_nutrition_pcp[['YearStart', 'LocationDesc', 'Age(years)', 'YearEnd']]
    df_age = df_age.groupby(['LocationDesc', 'YearStart', 'Age(years)'], as_index=False).count()

    # race
    # keep rrelevant columns
    df_race = df_nutrition_pcp[['YearStart', 'LocationDesc', 'Race/Ethnicity', 'YearEnd']]
    df_race = df_race.groupby(['LocationDesc', 'YearStart', 'Race/Ethnicity'], as_index=False).count()

    data = []

    educationList = df_education["Education"].unique()
    for ed in educationList:
        trace = go.Scatter(
            x=df_education.loc[df_education['Education'] == ed]["YearStart"],
            y=df_education.loc[df_education['Education'] == ed]["YearEnd"],
            mode='lines',
            name="Ed_" + ed
        )
        data.append(trace)

    incomeList = df_income["Income"].unique()
    for ed in incomeList:
        trace = go.Scatter(
            x=df_income.loc[df_income['Income'] == ed]["YearStart"],
            y=df_income.loc[df_income['Income'] == ed]["YearEnd"],
            mode='lines',
            name="In_" + ed
        )
        data.append(trace)

    ageList = df_age["Age(years)"].unique()
    for ed in ageList:
        trace = go.Scatter(
            x=df_age.loc[df_age['Age(years)'] == ed]["YearStart"],
            y=df_age.loc[df_age['Age(years)'] == ed]["YearEnd"],
            mode='lines',
            name="Age_" + ed
        )
        data.append(trace)

    raceList = df_race["Race/Ethnicity"].unique()
    for ed in raceList:
        trace = go.Scatter(
            x=df_race.loc[df_race['Race/Ethnicity'] == ed]["YearStart"],
            y=df_race.loc[df_race['Race/Ethnicity'] == ed]["YearEnd"],
            mode='lines',
            name="Race_" + ed
        )
        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            #xaxis=dict(title='year'),
            #yaxis=dict(title='count'),
            height=300,
            margin={'l': 40, 'b': 30, 'r': 10, 't': 10},
            annotations=[dict(
                x=0, y=1, xanchor='left', yanchor='bottom',
                xref='paper', yref='paper', showarrow=False,
                align='left', bgcolor='rgba(255, 255, 255, 0.5)',
                text="", font=dict(family='sans serif', size=18)
            )]
        )
    }


if __name__ == '__main__':
    app.run_server()