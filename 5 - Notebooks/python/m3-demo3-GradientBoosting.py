
# coding: utf-8

# # Gradient Boost Model for Regression
# ##### Using Gradient Boosting to predict the price of an automobile

import pandas as pd
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import os

_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

auto_data = pd.read_csv(os.path.join(_data_dir, 'imports-85.data'), sep=r'\s*,\s*', engine='python')

auto_data = auto_data.replace('?', np.nan)

auto_data.describe()

auto_data.describe(include='all')

auto_data['price'].describe()

auto_data['price'] = pd.to_numeric(auto_data['price'], errors='coerce')

auto_data['price'].describe()

auto_data = auto_data.drop('normalized-losses', axis=1)

auto_data.describe()

auto_data['horsepower'].describe()

auto_data['horsepower'] = pd.to_numeric(auto_data['horsepower'], errors='coerce')

auto_data['horsepower'].describe()

auto_data['num-of-cylinders'].describe()

cylinders_dict = {'two': 2,
                  'three': 3, 'four': 4, 'five': 5, 'six': 6, 'eight': 8, 'twelve': 12}
auto_data['num-of-cylinders'] = auto_data['num-of-cylinders'].astype(str).replace(cylinders_dict).astype(float)

auto_data = pd.get_dummies(auto_data,
                           columns=['make', 'fuel-type', 'aspiration', 'num-of-doors',
                                    'body-style', 'drive-wheels', 'engine-location',
                                   'engine-type', 'fuel-system'])

auto_data = auto_data.dropna()

for col in auto_data.select_dtypes(include=['object']).columns:
    auto_data[col] = pd.to_numeric(auto_data[col], errors='coerce')
auto_data = auto_data.dropna()

auto_data[auto_data.isnull().any(axis=1)]

from sklearn.model_selection import train_test_split

X = auto_data.drop('price', axis=1)
Y = auto_data['price']
X_train, x_test, Y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

from sklearn.ensemble import GradientBoostingRegressor

params = {'n_estimators': 500, 'max_depth': 6, 'min_samples_split': 2,
          'learning_rate': 0.01, 'loss': 'squared_error'}
gbr_model = GradientBoostingRegressor(**params)
gbr_model.fit(X_train, Y_train)

gbr_model.score(X_train, Y_train)

y_predict = gbr_model.predict(x_test)

print("First model done")

r_square = gbr_model.score(x_test, y_test)
print("R-square:", r_square)

from sklearn.metrics import mean_squared_error

gbr_model_mse = mean_squared_error(y_predict, y_test)
math.sqrt(gbr_model_mse)

from sklearn.model_selection import GridSearchCV

num_estimators = [100, 200, 500]
learn_rates = [0.01, 0.02, 0.05, 0.1]
max_depths = [4, 6, 8]

param_grid = {'n_estimators': num_estimators,
              'learning_rate': learn_rates,
              'max_depth': max_depths}

grid_search = GridSearchCV(GradientBoostingRegressor(min_samples_split=2, loss='squared_error'),
                           param_grid, cv=3, return_train_score=True)
grid_search.fit(X_train, Y_train)

print("Best params:", grid_search.best_params_)

for i in range(36):
    print('Parameters: ', grid_search.cv_results_['params'][i])
    print('Mean Test Score: ', grid_search.cv_results_['mean_test_score'][i])
    print('Rank: ', grid_search.cv_results_['rank_test_score'][i])
    print()

params = {'n_estimators': 200, 'max_depth': 4, 'min_samples_split': 2,
          'learning_rate': 0.05, 'loss': 'squared_error'}
gbr_model = GradientBoostingRegressor(**params)
gbr_model.fit(X_train, Y_train)

y_predict = gbr_model.predict(x_test)

print("Optimized model done")

r_square = gbr_model.score(x_test, y_test)
print("Optimized R-square:", r_square)

gbr_model_mse = mean_squared_error(y_predict, y_test)
math.sqrt(gbr_model_mse)
