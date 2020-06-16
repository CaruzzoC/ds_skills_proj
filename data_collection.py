# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 12:53:41 2020

@author: Cédric
"""

import glassdoor_scraper as gs
import pandas as pd

path = "D:/programmation/Data_Science/ds_skills_proj/chromedriver"

df = gs.get_jobs('data_scientist', 1000, False, path, 20)

df.to_csv('glassdoor_jobs.csv', index = False)
