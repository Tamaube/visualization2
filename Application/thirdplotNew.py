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
df_education_college = df_education.loc[df_education['Education'] == 'College graduate']
df_education_HG = df_education.loc[df_education['Education'] == 'High school graduate']
df_education_lessHG = df_education.loc[df_education['Education'] == 'Less than high school']
df_education_tech = df_education.loc[df_education['Education'] == 'Some college or technical school']
df_education_unknown = df_education.loc[df_education['Education'] == 'unknown']

#income
#keep rrelevant columns
df_income = df_nutrition[['YearStart','LocationDesc','Income','YearEnd']]
#aggregate and count
df_income = df_income.groupby(['LocationDesc', 'YearStart', 'Income'],as_index=False).count()
df_income_25k = df_income.loc[df_income['Income'] == '25k']
df_income_50k = df_income.loc[df_income['Income'] == '25k-50k']
df_income_50kplus = df_income.loc[df_income['Income'] == '>50k']
df_income_unknown = df_income.loc[df_income['Income'] == 'unknown']

# #gender
# #keep rrelevant columns
# df_gender = df_nutrition[['YearStart','LocationDesc','Gender','YearEnd']]
# #aggregate and count
# df_gender = df_gender.groupby(['LocationDesc', 'YearStart', 'Gender'],as_index=False).count()

# #age
# #keep rrelevant columns
# df_age = df_nutrition[['YearStart','LocationDesc','Age(years)','YearEnd']]
# #aggregate and count
# df_age = df_age.groupby(['LocationDesc', 'YearStart', 'Age(years)'],as_index=False).count()

# #race
# #keep rrelevant columns
# df_race = df_nutrition[['YearStart','LocationDesc','Race/Ethnicity','YearEnd']]
# #aggregate and count
# df_race = df_race.groupby(['LocationDesc', 'YearStart', 'Race/Ethnicity'],as_index=False).count()

# df_education.to_csv('education.csv', sep=',')
# df_income.to_csv('income.csv', sep=',')
# df_age.to_csv('age.csv', sep=',')
# df_race.to_csv('race.csv', sep=',')
# df_gender.to_csv('gender.csv', sep=',')

data = [
    go.Parcoords(
        line = dict(color = df_education['YearStart'],
                    colorscale='Jet',
                    showscale=True,
                    #reversescale=True,
                    cmin=2011,
                    cmax=2015),
        dimensions = list([
            dict(range = [0,10],
                label = 'college', values = df_education_college['YearEnd']),
            dict(range = [0,10],
                label = 'high school (HS)', values = df_education_HG['YearEnd']),
            dict(range = [0,10],
                label = 'less than HS', values = df_education_lessHG['YearEnd']),
            dict(range = [0,10],
                label = 'technical', values = df_education_tech['YearEnd']),
            dict(range = [0,220],
                label = '?education', values = df_education_unknown['YearEnd']),
            dict(range = [0,20],
                label = '<25K', values = df_income_25k['YearEnd']),
            dict(range = [0,20],
                label = '25k-50k', values = df_income_50k['YearEnd']),
            dict(range = [0,20],
                label = '50k+', values = df_income_50kplus['YearEnd']),
            dict(range = [0,190],
                label = '?income', values = df_income_unknown['YearEnd'])#,
            # dict(range = [0,235],
            #     label = 'gender', values = df_gender['YearEnd']),
            # dict(range = [0,200],
            #     label = 'age', values = df_age['YearEnd'])#,
            # dict(range = [0,180],
            #     label = 'race', values = df_race['YearEnd']),
            ])
    )
]

layout = go.Layout(
    title='Bla',
    plot_bgcolor = '#E5E5E5',
    paper_bgcolor = '#E5E5E5',
    showlegend=True
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig)