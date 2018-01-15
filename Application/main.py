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
stateList = df_death_final["State"].unique()
#build the option list of the state dropdown list
options_state_list = [{'label': 'All', 'value': 'All'}]
options_state_list.extend([{'label': i, 'value': i} for i in stateList])
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-state',
                options = options_state_list,
                value='All'
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            # dcc.Dropdown(
            #     id='crossfilter-question',
            #     options=['Life expectancy at birth, total (years)'],
            #     value='Life expectancy at birth, total (years)'
            # )
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
    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=yearList.min(),
        max=yearList.max(),
        value=yearList.max(),
        step=None,
        marks={str(year): str(year) for year in yearList}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
[dash.dependencies.Input('crossfilter-state', 'value')])
def update_graph(state_input):
    #df_death_final = df_death_final.loc[df_death_final['Year'] >= year]

    data = []
    if(state_input != 'All'):
        data=[ go.Scatter(
            x=df_death_final.loc[df_death_final['State'] == state_input]["Cause Name"],
            y=df_death_final.loc[df_death_final['State'] == state_input]["Deaths"],
            name=state,
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            })]
    else:
        for state in stateList:
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
            title='Cause of death',
            xaxis=dict(title='Cause'),
            yaxis=dict(title='Avg'),
            height=450
        )
    }





#
# def create_time_series(dff, axis_type, title):
#     return {
#         'data': [go.Scatter(
#             x=dff['Year'],
#             y=dff['Value'],
#             mode='lines+markers'
#         )],
#         'layout': {
#             'height': 225,
#             'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
#             'annotations': [{
#                 'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                 'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                 'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                 'text': title
#             }],
#             'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
#             'xaxis': {'showgrid': False}
#         }
#     }
#
#
# @app.callback(
#     dash.dependencies.Output('x-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
# def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#     country_name = hoverData['points'][0]['customdata']
#     dff = df[df['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)
#
#
# @app.callback(
#     dash.dependencies.Output('y-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)


if __name__ == '__main__':
    app.run_server()