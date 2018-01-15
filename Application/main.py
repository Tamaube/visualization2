import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

#preparing data set for question 1
df_nutrition = pd.read_csv('Nutrition.csv')
df_death = pd.read_csv('Leading_Causes_Death.csv')
#only keep data from 2011 onwards
df_death_final = df_death.loc[df_death['Year'] >= 2011]
#remove 'All Causes'
df_death_final = df_death.loc[df_death['Cause Name'] != 'All Causes']
#save Year
yearList = df_death_final["Year"].unique()
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
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
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
    # html.Div(dcc.Slider(
    #     id='crossfilter-year--slider',
    #     min=yearList.min(),
    #     max=yearList.max(),
    #     value=yearList.max(),
    #     step=None,
    #     marks={str(year): str(year) for year in yearList}
    # ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
[dash.dependencies.Input('options-state', 'value')])
def update_graph(state_input):
    #df_death_final = df_death_final.loc[df_death_final['Year'] >= year]

    data = []
    if(state_input != 'All'):
        data=[ go.Scatter(
            x=df_death_final.loc[df_death_final['State'] == state_input]["Cause Name"],
            y=df_death_final.loc[df_death_final['State'] == state_input]["Deaths"],
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
                x=df_death_final.loc[df_death_final['State'] == state]["Cause Name"],
                y=df_death_final.loc[df_death_final['State'] == state]["Deaths"],
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
     dash.dependencies.Input('percentage-type', 'value')])
def bar_chart_percentage(state, percentage_type):
    # selected from list
    df_nutrition_question = df_nutrition_final[df_nutrition_final['Question'] == percentage_type]
    # assume clicked state
   # state = hoverData['points'][0]['customdata']
    df_nutrition_question = df_nutrition_question.loc[df_nutrition_question['LocationDesc'] == state]
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
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData')])
def update_x_timeseries(hoverData):
    data = []
    return {
        'data': data,
        'layout': go.Layout(
        barmode='stack',
       # xaxis=dict(title='year'),
        #yaxis=dict(title='percentage')
        height= 225,
        margin = {'l': 20, 'b': 30, 'r': 10, 't': 10}
    )
    }


if __name__ == '__main__':
    app.run_server()