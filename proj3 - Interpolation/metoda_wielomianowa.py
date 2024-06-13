import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_csv(file_name):
    df = pd.read_csv(file_name)
    x_csv = df['x'].tolist()
    y_csv = df['y'].tolist()
    return x_csv, y_csv


def plot(x_plot, y_plot, title, x_label, y_label):
    plt.plot(x_plot, y_plot)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def plot_interpolation(x_org, y_org, x_inter_dot, y_inter_dot, y_inter, title, x_label, y_label):
    plt.plot(x_org, y_org, label='Original function')
    plt.plot(x_org, y_inter, label='Interpolated function')
    plt.scatter(x_inter_dot, y_inter_dot, color='red', label='Interpolation points')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.show()


def equal_indices(x_org, num_points):
    if num_points < 2:
        return [0]
    step = (len(x_org) - 1) / (num_points - 1)
    return [int(step * k) for k in range(num_points)]


def chebyshev_indices(x_org_len, num_points):
    if num_points < 2:
        return [0]
    chebyshev_tmp = [np.cos((num_points - k - 1) * np.pi / (num_points - 1)) for k in range(num_points)]  # [-1,1]
    chebyshev_ids = [int((chebyshev_tmp[k] + 1) * (x_org_len-1) / 2) for k in range(num_points)]  # [0, len(x_org)]
    return chebyshev_ids


def evaluate_polynomial(path, name, equal_nodes, chebyshev_nodes):

    # Read CSV

    x, y = read_csv('paths/' + name + '.csv')
    n_org = len(x)

    x = np.array(x)
    y = np.array(y)

    # Lagrange interpolation

    indices = equal_indices(x, equal_nodes)

    x_equal = x[indices]
    y_equal = y[indices]

    # Vandermonde matrix

    n = len(x_equal)
    V = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            V[i][j] = x_equal[i] ** (n - j - 1)

    # Solve the system of equations

    p = np.linalg.solve(V, y_equal)  # coefficients

    # Interpolated function plot

    y_interpolated = [sum([p[j] * x[i] ** (n - j - 1) for j in range(n)]) for i in range(n_org)]
    y_inter_nodes = [sum([p[j] * x_equal[i] ** (n - j - 1) for j in range(n)]) for i in range(n)]

    plot_interpolation(x, y, x_equal, y_inter_nodes, y_interpolated, 'Mount Everest (Equal)', 'Longitude', 'Latitude')

    # Lagrange's interpolation with Chebyshev points

    indices_chebyshev = chebyshev_indices(len(x), chebyshev_nodes)

    x_chebyshev = x[indices_chebyshev]
    y_chebyshev = y[indices_chebyshev]

    # Vandermonde matrix

    n = len(x_chebyshev)
    V = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            V[i][j] = x_chebyshev[i] ** (n - j - 1)
    print(V)

    # Solve the system of equations

    p = np.linalg.solve(V, y_chebyshev)  # coefficients

    # Interpolated function plot

    y_interpolated = [sum([p[j] * x[i] ** (n - j - 1) for j in range(n)]) for i in range(n_org)]
    y_inter_nodes = [sum([p[j] * x_chebyshev[i] ** (n - j - 1) for j in range(n)]) for i in range(n)]

    plot_interpolation(x, y, x_chebyshev, y_inter_nodes, y_interpolated, 'Mount Everest (Chebyshev)', 'Longitude', 'Latitude')


# Main
evaluate_polynomial('paths/MountEverest.csv', 'Mount Everest', 15, 25)
