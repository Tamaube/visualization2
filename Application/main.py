import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash()

#preparing data set for question 1
df_nutrition = pd.read_csv('Nutrition.csv')
df_death = pd.read_csv('Leading_Causes_Death.csv')
#only keep data from 2011 onwards
df_death_final = df_death.loc[df_death['Year'] >= 2011]
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
df_nutrition_final = df_nutrition[['YearStart', 'LocationDesc', 'Question', 'Data_Value', 'Gender']]
#year list for slider
year_list = df_nutrition_final["YearStart"].unique()

#TODO: add the third plot, change title display, add slider for the year, put text when all is selected

#replace long questions with a shorter equivalent
df_nutrition_final["Question"].replace('Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)', 'Percent of adults who workout moderately at least 150 mins a week',inplace=True)
df_nutrition_final["Question"].replace('Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week','Percent of adults who achieve at workout 150 mins a week & muscle-strengthening activities 2+ days a week',inplace=True)
df_nutrition_final["Question"].replace('Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)','Percent of adults who workout moderately at least 300 mins a week',inplace=True)

#question list for the dropdown list
question_list = df_nutrition_final["Question"].unique()
print(question_list)
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
        ], style={'width': '49%','float': 'right', 'display': 'inline-block'})
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
        dcc.Graph(id='parallel-coordinate'),
    ], style={'display': 'inline-block', 'width': '49%'}),
    html.Div(dcc.Slider(
        id='year-slider',
        min=year_list.min(),
        max=year_list.max(),
        value=year_list.max(),
        step=None,
        marks={str(year): str(year) for year in year_list}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
[dash.dependencies.Input('options-state', 'value'),
dash.dependencies.Input('year-slider', 'value')])
def update_graph(state_input,year):
    #df_death_graph = df_death_final[df_death_final['Year'] >= year]
    df_death_graph= df_death_final
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
           # title='Cause of death',
            xaxis=dict(title='Cause'),
            yaxis=dict(title='Avg'),
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('options-state', 'value'),
     dash.dependencies.Input('percentage-type', 'value'),
     dash.dependencies.Input('year-slider', 'value')])
def bar_chart_percentage(state, percentage_type, year):
    # selected from lists
    #df_nutrition_question = df_nutrition_final[df_nutrition_final['YearStart'] == year]
    #df_nutrition_question = df_nutrition_question.loc[df_nutrition_question['LocationDesc'] == state]
    df_nutrition_question = df_nutrition_final[df_nutrition_final['LocationDesc'] == state]
    df_nutrition_question = df_nutrition_question.loc[df_nutrition_question['Question'] == percentage_type]

    data = []
    gender_list = df_nutrition_question["Gender"].unique()

    for gender in gender_list:
        trace = go.Bar(
            x=df_nutrition_question.loc[df_nutrition_question['Gender'] == gender]["YearStart"],
            y=df_nutrition_question.loc[df_nutrition_question['Gender'] == gender]["Data_Value"],
            name=gender
        )
        data.append(trace)

    return {
        'data': data,
        'layout': go.Layout(
            barmode='stack',
            #TODO show title but smaller
            #title=percentage_type,
            height= 225,
            margin ={'l': 20, 'b': 30, 'r': 10, 't': 10},
        )
    }


@app.callback(
    dash.dependencies.Output('parallel-coordinate', 'figure'),
    [dash.dependencies.Input('options-state', 'value'),
    dash.dependencies.Input('year-slider', 'value')
     ])
def update_pcp(state, year):
    # select year
    df_nutrition_pcp = df_nutrition_final[df_nutrition_final['YearStart'] == year]
    df_nutrition_pcp = df_nutrition_pcp.loc[df_nutrition_pcp['LocationDesc'] == state]

    df_nutrition_pcp = df_nutrition_pcp.replace(np.nan, 'unknown')

    # convert categories into numerical vals
    df_nutrition_pcp['Education'] = pd.Categorical(df_nutrition_pcp['Education'])
    df_nutrition_pcp['EducationCode'] = df_nutrition_pcp['Education'].cat.codes
    df_nutrition_pcp['Gender'] = pd.Categorical(df_nutrition_pcp['Gender'])
    df_nutrition_pcp['GenderCode'] = df_nutrition_pcp['Gender'].cat.codes
    df_nutrition_pcp['Income'] = pd.Categorical(df_nutrition_pcp['Income'])
    df_nutrition_pcp['IncomeCode'] = df_nutrition_pcp['Income'].cat.codes
    df_nutrition_pcp['Age(years)'] = pd.Categorical(df_nutrition_pcp['Age(years)'])
    df_nutrition_pcp['Age(years)Code'] = df_nutrition_pcp['Age(years)'].cat.codes
    df_nutrition_pcp['Race/Ethnicity'] = pd.Categorical(df_nutrition_pcp['Race/Ethnicity'])
    df_nutrition_pcp['Race/EthnicityCode'] = df_nutrition_pcp['Race/Ethnicity'].cat.codes

    data = [
        go.Parcoords(
            line=dict(color=year,
                      colorscale='Jet',
                      showscale=True,
                      # reversescale=True,
                      cmin=2011,
                      cmax=2015),
            dimensions=list([
                dict(tickvals=[4, 3, 2, 1, 0],
                     ticktext=['unknown', 'Less HS', 'HS', 'TS', 'C'],
                     label='education categories', values=df_nutrition_pcp['EducationCode']),
                dict(tickvals=[7, 6, 5, 4, 3, 2, 1, 0],
                     ticktext=['unknown', '<15K', 'not reported', '>75k', '50k-75k', '35k-50k', '25k-35k', '15k-25k'],
                     label='income levels', values=df_nutrition_pcp['IncomeCode']),
                dict(tickvals=[2, 1, 0],
                     ticktext=['unknown', 'M', 'F'],
                     label='genders', values=df_nutrition_pcp['GenderCode']),
                dict(tickvals=[6, 5, 4, 3, 2, 1, 0],
                     ticktext=['unknown', '65+', '55-64', '45-54', '35-44', '25-34', '18-24'],
                     label='age categories', values=df_nutrition_pcp['Age(years)Code']),
                dict(tickvals=[8, 7, 6, 5, 4, 3, 2, 1, 0],
                     ticktext=['unknown', 'other', 'NonHisp W', 'NonHisp B', 'Hisp', 'Hawaiian', 'Asian', 'AmericInd',
                               '2+ races'],
                     label='races', values=df_nutrition_pcp['Race/EthnicityCode'])
            ])
        )
    ]
    return {
        'data': data,
        'layout': go.Layout(
            plot_bgcolor='#E5E5E5',
            paper_bgcolor='#E5E5E5',
            showlegend=True,
            height=225,
            margin={'l': 20, 'b': 30, 'r': 10, 't': 10}
        )
    }


if __name__ == '__main__':
    app.run_server()