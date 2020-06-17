# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:15:18 2020

@author: Cédric
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('eda_data.csv')

# choose relevant columns
df.columns 

df_model = df[['skills','Rating','Size','Type of ownership','Industry','Sector',
               'Revenue','num_comp','hourly','job_state','same_state','age',
               'spark','aws','python_yn','job_simp','seniority','avg_salary',
               'company_txt']]

# get dummy data
df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split

X = df_dum.drop('skills', axis = 1)
y = df_dum.skills.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# multiple linear regression
import statsmodels.api as sm

X_sm = X = sm.add_constant(X)
model = sm.OLS(y,X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm,X_train,y_train, scoring = 'neg_mean_absolute_error', cv = 3))

# lasso regression
lm_l = Lasso(alpha = 0.01)
lm_l.fit(X_train,y_train)
np.mean(cross_val_score(lm_l,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3))

alpha = []
error = []

for i in range(1,10):
    alpha.append(i/100)
    lml = Lasso(alpha=(i/100))
    error.append(np.mean(cross_val_score(lml,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
plt.plot(alpha,error)

err = list(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha','error'])
df_err[df_err.error == max(df_err.error)] # out : alpha : 0.01 | error : -0.607412

# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()

np.mean(cross_val_score(rf,X_train,y_train,scoring = 'neg_mean_absolute_error', cv = 3)) #◘out : -0355


# XGBoost
from xgboost import XGBRegressor

xgb = XGBRegressor(n_estimators=500)
xgb.fit(X_train, y_train, 
             early_stopping_rounds=5, 
             eval_set=[(X_test, y_test)],
             verbose=False)

np.mean(cross_val_score(xgb,X_train,y_train,scoring = 'neg_mean_absolute_error', cv = 3)) #out : -0.4171

# tune models GridsearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators' : range(10,200,10)}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_

rf = RandomForestRegressor(n_estimators=100,criterion='mae')

# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)
tpred_xgb = xgb.predict(X_test)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test,tpred_lm) #out : 424856873.5866135
mean_absolute_error(y_test,tpred_lml) #out : 0.5763085951975947
mean_absolute_error(y_test,tpred_rf) #out : 0.3355283333333334
mean_absolute_error(y_test,tpred_xgb) #out : 0.4728345754742622

mean_absolute_error(y_test,(tpred_rf+tpred_xgb)/2) #out : 0.3987738179083665
