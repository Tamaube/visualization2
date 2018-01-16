import plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

#preparing data set for question 3

df = pd.read_csv('Nutrition.csv')

df.replace('Less than $15,000', '25k',inplace=True)
df.replace('$15,000 - $24,999', '25k',inplace=True)
df.replace('$25,000 - $34,999', '25k-50k',inplace=True)
df.replace('$35,000 - $49,999', '25k-50k',inplace=True)
df.replace('$50,000 - $74,999', '>50k',inplace=True)
df.replace('$75,000 or greater', '>50k',inplace=True)

#only keep interesting columns
df_nutrition = df[['YearStart','YearEnd','LocationDesc','Education','Income','Gender','Age(years)','Race/Ethnicity']]

#assume clicked state
df_nutrition = df_nutrition.loc[df_nutrition['LocationDesc'] == 'Hawaii']


#select year
#df_nutrition = df_nutrition.loc[df_nutrition['YearStart'] == 2014]

df_nutrition.replace(np.nan, 'unknown',inplace=True)

#education
#keep rrelevant columns
df_education = df_nutrition[['YearStart','LocationDesc','Education','YearEnd']]
#aggregate and count
df_education = df_education.groupby(['LocationDesc', 'YearStart','Education'],as_index=False).count()

#income
#keep rrelevant columns
df_income = df_nutrition[['YearStart','LocationDesc','Income','YearEnd']]
#aggregate and count
df_income = df_income.groupby(['LocationDesc', 'YearStart', 'Income'],as_index=False).count()

#age
#keep rrelevant columns
df_age = df_nutrition[['YearStart','LocationDesc','Age(years)','YearEnd']]
#aggregate and count
df_age = df_age.groupby(['LocationDesc', 'YearStart', 'Age(years)'],as_index=False).count()

#race
#keep rrelevant columns
df_race = df_nutrition[['YearStart','LocationDesc','Race/Ethnicity','YearEnd']]
#aggregate and count
df_race = df_race.groupby(['LocationDesc', 'YearStart', 'Race/Ethnicity'],as_index=False).count()

data = []

educationList = df_education["Education"].unique()
for ed in educationList:
    trace = go.Scatter(
        x=df_education.loc[df_education['Education'] == ed]["YearStart"],
        y=df_education.loc[df_education['Education'] == ed]["YearEnd"],
        mode='lines',
        name="Ed_"+ed
    )
    data.append(trace)

incomeList = df_income["Income"].unique()
for ed in incomeList:
    trace = go.Scatter(
        x=df_income.loc[df_income['Income'] == ed]["YearStart"],
        y=df_income.loc[df_income['Income'] == ed]["YearEnd"],
        mode='lines',
        name="In_"+ed
    )
    data.append(trace)

ageList = df_age["Age(years)"].unique()
for ed in ageList:
    trace = go.Scatter(
        x=df_age.loc[df_age['Age(years)'] == ed]["YearStart"],
        y=df_age.loc[df_age['Age(years)'] == ed]["YearEnd"],
        mode='lines',
        name="Age_"+ed
    )
    data.append(trace)

raceList = df_race["Race/Ethnicity"].unique()
for ed in raceList:
    trace = go.Scatter(
        x=df_race.loc[df_race['Race/Ethnicity'] == ed]["YearStart"],
        y=df_race.loc[df_race['Race/Ethnicity'] == ed]["YearEnd"],
        mode='lines',
        name="Race_"+ed
    )
    data.append(trace)

layout = go.Layout(
    xaxis=dict(title='year'),
    yaxis=dict(title='count')
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)

