#Not used, linechart was used instead
import plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#preparing data set for question 3

df = pd.read_csv('Nutrition.csv')

#only keep interesting columns
df_nutrition = df[['YearStart','LocationDesc','Education','Income','Gender','Age(years)','Race/Ethnicity']]

#assume clicked state
df_nutrition = df_nutrition.loc[df_nutrition['LocationDesc'] == 'Hawaii']

#select year
df_nutrition = df_nutrition.loc[df_nutrition['YearStart'] == 2014]

df_nutrition.replace(np.nan, 'unknown',inplace=True)

#convert categories into numerical vals
df_nutrition['Education'] = pd.Categorical(df_nutrition['Education'])
df_nutrition['EducationCode'] = df_nutrition['Education'].cat.codes
df_nutrition['Gender'] = pd.Categorical(df_nutrition['Gender'])
df_nutrition['GenderCode'] = df_nutrition['Gender'].cat.codes
df_nutrition['Income'] = pd.Categorical(df_nutrition['Income'])
df_nutrition['IncomeCode'] = df_nutrition['Income'].cat.codes
df_nutrition['Age(years)'] = pd.Categorical(df_nutrition['Age(years)'])
df_nutrition['Age(years)Code'] = df_nutrition['Age(years)'].cat.codes
df_nutrition['Race/Ethnicity'] = pd.Categorical(df_nutrition['Race/Ethnicity'])
df_nutrition['Race/EthnicityCode'] = df_nutrition['Race/Ethnicity'].cat.codes

data = [
    go.Parcoords(
        line = dict(color = df_nutrition['YearStart'],
                    colorscale='Jet',
                    showscale=True,
                    #reversescale=True,
                    cmin=2011,
                    cmax=2015),
        dimensions = list([
            dict(tickvals = [4,3,2,1,0],
                ticktext = ['unknown','Less HS','HS','TS','C'],
                label = 'education categories', values = df_nutrition['EducationCode']),
            dict(tickvals = [7,6,5,4,3,2,1,0],
           ticktext = ['unknown','<15K','not reported','>75k','50k-75k','35k-50k','25k-35k','15k-25k'],
                label = 'income levels', values = df_nutrition['IncomeCode']),
            dict(tickvals = [2,1,0],
                ticktext = ['unknown','M','F'],
                label = 'genders', values = df_nutrition['GenderCode']),
            dict(tickvals = [6,5,4,3,2,1,0],
                ticktext = ['unknown','65+','55-64','45-54','35-44','25-34','18-24'],
                label = 'age categories', values = df_nutrition['Age(years)Code']),
            dict(tickvals = [8,7,6,5,4,3,2,1,0],
                ticktext = ['unknown','other','NonHisp W','NonHisp B','Hisp','Hawaiian','Asian','AmericInd','2+ races'],
                label = 'races', values = df_nutrition['Race/EthnicityCode'])
        ])
    )
]

layout = go.Layout(
    plot_bgcolor = '#E5E5E5',
    paper_bgcolor = '#E5E5E5',
    showlegend=True
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)