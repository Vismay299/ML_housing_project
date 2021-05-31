# -*- coding: utf-8 -*-
"""ML proj 01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d8uSRAepIZBSfqoQouAEmNP4_ZMBCO6u
"""

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
df=pd.read_csv("data.csv")
df.head()
df.info()
df.describe()

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

df.hist(bins=50,figsize=(20,15))
plt.show()

#train_set,test_set=split_train_test(df,0.2)

from sklearn.model_selection import train_test_split
train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)
print(len(train_set,))
print(len(test_set))

from sklearn.model_selection import StratifiedShuffleSplit
split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
for train_index,test_index in split.split(df,df['CHAS']):
  strat_train_set=df.loc[train_index]
  strat_test_set=df.loc[test_index]

df=strat_train_set.copy()

corr_matrix = df.corr()
corr_matrix['MEDV'].sort_values(ascending=False)

from pandas.plotting import scatter_matrix
attributes =  ['MEDV','ZN','RM','LSTAT']
scatter_matrix(df[attributes],figsize=(12,5))

df['TAXRM']=df['TAX']/df['RM']
df.head()
df.plot(kind='scatter',x='TAXRM',y='MEDV',alpha=0.8)

df=strat_train_set.drop('MEDV',axis=1)
df_labels=strat_train_set['MEDV'].copy()

from sklearn.impute import SimpleImputer
imputer=SimpleImputer(strategy='median')
imputer.fit(df)

x=imputer.transform(df)
df_2=pd.DataFrame(df,columns=df.columns)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
my_pipeline = Pipeline([
                        ('imputer',SimpleImputer(strategy='median')),
                        ('std_scaler',StandardScaler()),
])

df_num_2=my_pipeline.fit_transform(df_2)

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
model=RandomForestRegressor()
#model = LinearRegression()
#model=DecisionTreeRegressor()
model.fit(df_num_2,df_labels)

some_data=df.iloc[:5]
some_labels = df.iloc[:5]
prepared_data=my_pipeline.transform(some_data)
model.predict(prepared_data)

from sklearn.metrics import  mean_squared_error
df_predictions=model.predict(df_num_2)
mse=mean_squared_error(df_labels,df_predictions)
rmse=np.sqrt(mse)
rmse

from sklearn.model_selection import cross_val_score
scores=cross_val_score(model,df_num_2,df_labels,scoring='neg_mean_squared_error',cv=10)
rmse_scores=np.sqrt(-scores)
rmse_scores

def print_scores(scores):
  print('scored',scores)
  print('mean',scores.mean())
  print('standard seviation',scores.std())

print_scores(rmse_scores)

from joblib import dump,load
dump(model,'projet.joblib')

x_test=strat_test_set.drop('MEDV',axis=1)
y_test=strat_test_set['MEDV'].copy()
x_test_prepared=my_pipeline.transform(x_test)
final_predictions=model.predict(x_test_prepared)
final_mse=mean_squared_error(y_test,final_predictions)
final_rmse=np.sqrt(final_mse)
final_rmse

features=np.array([[-0.43942006,  3.12628155, -1.12165014, -0.27288841, -1.42262747,
       -0.23979304, -1.31238772,  2.61111401, -1.0016859 , -0.5778192 ,
       -0.97491834,  0.41164221, -0.86091034]])
model.predict(features)

prepared_data[0]