
# coding: utf-8

# # Lasso and Ridge Regression
# ##### First use Linear Regression to predict automobile prices. Then apply Lasso and Ridge Regression models on the same data and compare results

import pandas as pd
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab
import os

_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

print(pd.__version__)

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
                           columns=['make',
                                    'fuel-type',
                                    'aspiration',
                                    'num-of-doors',
                                    'body-style',
                                    'drive-wheels',
                                    'engine-location',
                                    'engine-type',
                                    'fuel-system'])

auto_data = auto_data.dropna()

for col in auto_data.select_dtypes(include=['object']).columns:
    auto_data[col] = pd.to_numeric(auto_data[col], errors='coerce')
auto_data = auto_data.dropna()

auto_data[auto_data.isnull().any(axis=1)]

from sklearn.model_selection import train_test_split

X = auto_data.drop('price', axis=1)
Y = auto_data['price']
X_train, x_test, Y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

from sklearn.linear_model import LinearRegression

linear_model = LinearRegression()
linear_model.fit(X_train, Y_train)

linear_model.score(X_train, Y_train)

linear_model.coef_

predictors = X_train.columns
coef = pd.Series(linear_model.coef_,predictors).sort_values()

print(coef)

y_predict = linear_model.predict(x_test)

print("LinearRegression predictions done")

r_square = linear_model.score(x_test, y_test)
print("R-square:", r_square)

from sklearn.metrics import mean_squared_error

linear_model_mse = mean_squared_error(y_predict, y_test)
print("MSE:", linear_model_mse)

math.sqrt(linear_model_mse)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
x_test_scaled = scaler.transform(x_test)

lasso_model = Lasso(alpha=0.5)
lasso_model.fit(X_train_scaled, Y_train)

lasso_model.score(X_train_scaled, Y_train)

y_predict = lasso_model.predict(x_test_scaled)

print("Lasso predictions done")

r_square = lasso_model.score(x_test_scaled, y_test)
print("Lasso R-square:", r_square)

lasso_model_mse = mean_squared_error(y_predict, y_test)
math.sqrt(lasso_model_mse)

from sklearn.linear_model import Ridge

ridge_model = Ridge(alpha=0.05)
ridge_model.fit(X_train_scaled, Y_train)

ridge_model.score(X_train_scaled, Y_train)

y_predict = ridge_model.predict(x_test_scaled)

print("Ridge predictions done")

r_square = ridge_model.score(x_test_scaled, y_test)
print("Ridge R-square:", r_square)

ridge_model_mse = mean_squared_error(y_predict, y_test)
math.sqrt(ridge_model_mse)

from sklearn.svm import SVR

regression_model = SVR(kernel='linear', C=1.0)
regression_model.fit(X_train_scaled, Y_train.values.ravel())

regression_model.score(X_train_scaled, Y_train)

y_predict = regression_model.predict(x_test_scaled)

print("SVR predictions done")

r_square = regression_model.score(x_test_scaled, y_test)
print("SVR R-square:", r_square)

regression_model_mse = mean_squared_error(y_predict, y_test)
math.sqrt(regression_model_mse)
