# Data Science Degree Level Requirement Estimator : Project Overview

* Created a tool that estimates Data Science (and some related jobs) degree level required (BER ~10%) to help students realizing what skills level they need for their goal job.
* Scraped 1000 job description from glassdoor using python and selenium.
* Engineered features from the text of each job description to quantify the value companies put on python, aws, spark and educational degrees.
* Optimized Linear, Lasso, Random Firest Regressors and Extreme Gradient Boosting Regressor using GridsearchCV to reach the best paramters for a non underfitting/overfitting model.
* Built a client facing API using flask

## Code and Resources Used

**Python Version:** 3.7
**Packages:** pandas, numpy, sklearn, xgboost, matplotlib, seaborn, selenium, flask, json, pickle
**For Web Framework Requierements:** `pip install -r requirements.txt`
[**Scraper Github**](https://github.com/arapfaik/scraping-glassdoor-selenium)
[**Scraper Article**](https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905)
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
