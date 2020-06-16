# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:02:43 2020

@author: Cédric
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')

#============================salary parsing=================================

#df = df[df['Salary Estimate'] != '-1'] #No Salary are missing (1000 -> 1000 rows)

#Makes a column specifying if the salary is on a hourly basis
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

# Clean the useless part of th salary estimate column
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))
min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour',''))

#Makes the min/max/avg salary columns
df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#============================Company name text only========================
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

#===========================state abreviation==============================
#Keeps the state if possible
df['job_state'] = df['Location'].apply(lambda x: x.split(",")[1] if  len(x.split(",")) == 2 else x.split(",")[0])
df.job_state.value_counts() #Shows how many jobs are in each states

#Is in the same State at the Headquarter
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

#============================age of company================================
#Gives the age of the company
df['age'] = df.Founded.apply(lambda x: x if x < 1 else 2020 - x)

#=======================parsing of job description=========================
#Tools that could have impact on future predictions
#spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark.value_counts()
#aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws.value_counts()
#python
df['python_yn'] = df['Job Description']. apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()

#Degrees
#PhD
df['phd_dg'] = df['Job Description'].apply(lambda x: 3 if 'PhD' in x else 0)
df.phd_dg.value_counts()
#Master
df['master_dg'] = df['Job Description'].apply(lambda x: 2 if 'Masters' in x or 'M.Sc.' in x or 'MS' in x or 'MA' in x else 0)
df.master_dg.value_counts()
#Bachelor
df['bachelor_dg'] = df['Job Description'].apply(lambda x: 1 if 'Bachelor' in x or 'B.S.' in x or 'BS' in x or 'BA' in x else 0)
df.bachelor_dg.value_counts()

#skills requiered by the job
df['skills'] = df[["phd_dg", "master_dg", "bachelor_dg"]].max(axis=1)
df.skills.value_counts()

df.to_csv('salary_data_cleaned.csv', index = False)
