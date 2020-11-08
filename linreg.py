import logging
import pandas as pd
import numpy as np
import scipy.stats as stats
from flask import g

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.model_selection import train_test_split



def linreg(df, target):
    selected_features = list(df.corr()[target].abs().sort_values(ascending=False)[1:2].index)
    g.selected_features = selected_features

    X = df[selected_features].values
    y = df[target].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
    
    model = LinearRegression()
    model.fit(X_train, y_train)


    y_pred = model.predict(X_test)
    g.r_squared = metrics.r2_score(y_test, y_pred)
    g.mae = metrics.mean_absolute_error(y_test, y_pred)
    
    # r_squared = metrics.r2_score(y_test, y_pred)
    # mae = metrics.mean_absolute_error(y_test, y_pred)
    # print('R-Squared Score:', r_squared)
    # print("Mean Absolute Error:", mae)
    print(df.corr())
    return model