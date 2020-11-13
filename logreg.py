import logging
import pandas as pd
import numpy as np
import scipy.stats as stats
from flask import g

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split

