# Data Science Degree Level Requirement Estimator : Project Overview

## Presentation

I m a student myself at this time, so i know this issue quite well. We can have a job goal, a company goal, a location we prefer. Therefore we can wonder what Degree level will the company expect from us for a given mission.

The goal is to get a number between 0 and 3 :
* **0:** No degrees expectation / years of experiences requiered.
* **1:** Bachelor degree at least.
* **2:** Master degree at least.
* **3:** PhD degree at least.
The predicted number is a float, we will then have an idea of the degree level.

## Summary

* Created a tool that estimates Data Science (and some related jobs) degree level required (BER ~10%) to help students realizing what skills level they need for their goal job.
* Scraped 1000 job description from glassdoor using python and selenium.
* Engineered features from the text of each job description to quantify the value companies put on python, aws, spark and educational degrees.
* Optimized Linear, Lasso, Random Forest Regressors and Extreme Gradient Boosting Regressor using GridsearchCV to reach the best paramters for a non underfitting/overfitting model.
* Built a client facing API using flask

## Code and Resources Used

**Python Version:** 3.7\
**Packages:** pandas, numpy, sklearn, xgboost, matplotlib, seaborn, selenium, flask, json, pickle\
**For Web Framework Requierements:** `pip install -r requirements.txt`\
[**Scraper Github**](https://github.com/arapfaik/scraping-glassdoor-selenium)\
[**Scraper Article**](https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905)\
[**Flask Productionization**](https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2)(code and use)

## Web Scraping

Used the glassdoor scraper github repo (as linked above)(made a few change) to scrape 1000 job postings from glassdoor.com. With each job, I got the following:

* Jobe title
* Salary Estimate
* Job Description
* Rating
* Company
* Location
* Company Headquarters
* Type of Ownership
* Industry
* Sector
* Revenue
* Competitors

## Data Cleaning

The scraped data needed to be cleaned for use. I made the following changes and created the following variables:

* Parsed numeric data out of Salary.
* Made columns for minimum salary, maximum salary, average salary and hourly wages.
* Checked that every salary are provided
* Parsed the rating out of company text
* Made a column for the state and only kept the abreviation
* Made a conditional column to know wether a job state is within the headquarter state
* Transformed founded date into age of company
* Engineered the job Description column to get specifics values :
  * Python
  * AWS
  * Spark
  * PhD
  * Master
  * Bachelor
  * Skills
* Column for simplified job title and Seniority
* Column for description length

## EDA
I analysed the data distribution and the impact they could have as a feature for the future models.

![Correlation Heatmap](https://github.com/CaruzzoC/ds_skills_proj/blob/master/img/correlation_heatmap.PNG)
![top 20 State](https://github.com/CaruzzoC/ds_skills_proj/blob/master/img/top20_state.PNG)
![pivot table Job/Skills](https://github.com/CaruzzoC/ds_skills_proj/blob/master/img/pivot_table_job_skills.PNG)

The correlation table made me realise that the description_len column shouldn't be used as a feature to prevent target leakage.

## Model Building

First, i used the One hot encoding for the categorical variables. I also split the data into train set and tests set. The test size is .2.

I tried four different models and evaluated them using MAE. I chose MAE for the easy interpretations we can make from it.

I tried these models:

* **Multiple Linear Regression** - Baseline for the model
* **Lasso Regression** - Because of the sparse data from the one hot encoding.
* **Random Forest** - Due to the One hot encoding, i thought that the Random forest would be a good model.
* **Extreme Gradient Boosting Regressor** - Beacause i thought it would get a smaller MAE with time.

## Model performance

I chose the Random Forest and tuned it because it had the best MAE with default settings.

* **Random Forest:** MAE = 0.32142499999999996
* **XGBRegressor:** MAE = 0.4728345754742622
* **Lasso Regression:** MAE = 0.5763085951975947
* **Linear Regression:** MAE = 424856873.5866135 (for sure a wrong implementation)

## Productionization

In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a job listing and returns an estimated Degree level requirement.
