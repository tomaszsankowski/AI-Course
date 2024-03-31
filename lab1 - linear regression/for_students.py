import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data


def standardization(in_data, avg1, std1):
    in_data = (in_data - avg1) / std1
    return in_data


data = get_data()
#inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# TODO: calculate closed-form solution

X = np.column_stack((np.ones_like(x_train), x_train))

theta_best = np.linalg.inv(X.T @ X) @ X.T @ y_train

print("Theta = ", theta_best)

# TODO: calculate error

# train error

MSE = 0
for i in range(y_train.size):
    MSE += (theta_best[0] + theta_best[1] * x_train[i] - y_train[i]) ** 2

MSE /= y_train.size
print("MSE train = ", MSE)

# test error

MSE = 0
for i in range(y_test.size):
    MSE += (theta_best[0] + theta_best[1] * x_test[i] - y_test[i]) ** 2

MSE /= y_test.size
print("MSE test = ", MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: standardization

avg = np.mean(x_train)
std = np.std(x_train)

x_test = standardization(x_test, avg, std)
x_train = standardization(x_train, avg, std)

avg = np.mean(y_train)
std = np.std(y_train)

y_test = standardization(y_test, avg, std)
y_train = standardization(y_train, avg, std)

X = np.column_stack((np.ones_like(x_train), x_train))

theta_best = np.linalg.inv(X.T @ X) @ X.T @ y_train

print("Standardized Theta = ", theta_best)

# train error

MSE = 0
for i in range(y_train.size):
    MSE += (theta_best[0] + theta_best[1] * x_train[i] - y_train[i]) ** 2

MSE /= y_train.size
print("After Standardization train MSE = ", MSE)

# test error

MSE = 0
for i in range(y_test.size):
    MSE += (theta_best[0] + theta_best[1] * x_test[i] - y_test[i]) ** 2

MSE /= y_test.size
print("After Standardization test MSE = ", MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# TODO: calculate theta using Batch Gradient Descent

theta_best = np.random.rand(2)

learning_rate = 0.001
iterations = 3000

for i in range(iterations):
    theta_best = theta_best - learning_rate * 2 / len(x_train) * X.T @ (X @ theta_best - y_train)

print("Gradient Descent Theta = ", theta_best)

# TODO: calculate error

# train error

MSE = 0
for i in range(y_train.size):
    MSE += (theta_best[0] + theta_best[1] * x_train[i] - y_train[i]) ** 2

MSE /= y_train.size
print("Gradient Descent train MSE = ", MSE)

# test error

MSE = 0
for i in range(y_test.size):
    MSE += (theta_best[0] + theta_best[1] * x_test[i] - y_test[i]) ** 2

MSE /= y_test.size
print("Gradient Descent test MSE = ", MSE)

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()
