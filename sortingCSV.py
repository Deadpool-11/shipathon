d={
    "CLASS":0,
    "LAB":1,
    "TUT":2,
    "DEBSOC":3,
    "QC":4,
    "SM"    :5,
    "DRAMA" :6,
    "DANCE" :7,
    "HS":8,
    "MUSIC" :9,
    "LITERARY"   :10,
    "DESIGN":11,
    "PFC":12,
    "FACC":13,
    "RDV":14,
    "SEMINAR":15,
    "OTHER":16,
}

import pandas as pd
df = pd.read_csv('input22.csv')

df=pd.read_csv('input22.csv')
for i in range(len(df)):
    if(df['Type'][i] in d):
        df['Priority index'][i]=d[df['Type'][i]]
df = df.sort_values(by=['Date','Priority index', 'Time'])
df.to_csv('test3.csv',index=False)

'''
input format:
d is dictionary of priorities taken from input
input22.csv is the csv file made
df is the final output that con be used
'''
