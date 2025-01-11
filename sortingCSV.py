import pandas as pd

df=pd.read_csv(input_file)

df.sort_values(by=['column_name'], inplace=True)
