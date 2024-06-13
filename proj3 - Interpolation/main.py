import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_csv(file_name):
    df = pd.read_csv(file_name)
    x_csv = df['x'].tolist()
    y_csv = df['y'].tolist()
    return x_csv, y_csv


def plot(x_plot, y_plot, title, x_label, y_label):
    plt.plot(x_plot, y_plot, label='Original function')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig('plots/' + title + '.png')
    plt.show()


def plot_interpolation(x_org, y_org, x_inter_dot, y_inter_dot, y_inter, title, x_label, y_label):
    plt.plot(x_org, y_org, label='Original function')
    plt.plot(x_org, y_inter, label='Interpolated function')
    plt.scatter(x_inter_dot, y_inter_dot, color='red', label='Interpolation points')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.savefig('plots/' + title + '.png')
    plt.show()


def equal_indices(x_org, num_points):
    if num_points < 2:
        return [0]
    step = (len(x_org) - 1) / (num_points - 1)
    return [int(step * k) for k in range(num_points)]


def chebyshev_indices(x_org_len, num_points):
    if num_points < 2:
        return [0]
    chebyshev_tmp = [np.cos((2 * k + 1) * np.pi / (2 * num_points)) for k in range(num_points)]  # [-1,1]
    chebyshev_ids = [int((chebyshev_tmp[k] + 1) * (x_org_len - 1) / 2) for k in range(num_points)]  # [0, len(x_org)]
    return chebyshev_ids


def lagrange_function(val, x_inter, y_inter):
    out = 0
    for x_fi in range(len(x_inter)):
        tmp = 1
        for x_k in range(len(x_inter)):
            if x_fi != x_k and x_inter[x_fi] != x_inter[x_k]:
                tmp *= (val - x_inter[x_k]) / (x_inter[x_fi] - x_inter[x_k] + 1e-10)
        out += tmp * y_inter[x_fi]
    return out


def evaluate_csv(path, name, equal_nodes, chebyshev_nodes, cubic_nodes):
    # Read CSV

    x, y = read_csv(path)
    n_org = len(x)

    x = np.array(x)
    y = np.array(y)

    plot(x, y, name + ' original', 'Longitude', 'Latitude')

    # Lagrange's interpolation

    indices = equal_indices(x, equal_nodes)

    x_equal = x[indices]
    y_equal = y[indices]

    # Calculating values and plot them

    y_interpolated = [lagrange_function(x[i], x_equal, y_equal) for i in range(n_org)]
    y_inter_nodes = [lagrange_function(x_equal[i], x_equal, y_equal) for i in range(len(y_equal))]

    plot_interpolation(x, y, x_equal, y_inter_nodes, y_interpolated, name + ' (Equal, ' + str(equal_nodes) + ' nodes)', 'Longitude', 'Latitude')

    # Lagrange's interpolation with Chebyshev points

    indices_chebyshev = chebyshev_indices(len(x), chebyshev_nodes)

    x_chebyshev = x[indices_chebyshev]
    y_chebyshev = y[indices_chebyshev]

    # Interpolated function plot

    y_interpolated_chebyshev = [lagrange_function(x[i], x_chebyshev, y_chebyshev) for i in range(n_org)]
    y_inter_nodes_chebyshev = [lagrange_function(x_chebyshev[i], x_chebyshev, y_chebyshev) for i in
                               range(len(y_chebyshev))]

    plot_interpolation(x, y, x_chebyshev, y_inter_nodes_chebyshev, y_interpolated_chebyshev, name + ' (Chebyshev, ' + str(chebyshev_nodes) + ' nodes)',
                       'Longitude', 'Latitude')

    # Cubic spline interpolation

    indices_cubic = equal_indices(x, cubic_nodes)

    x_cubic = x[indices_cubic]
    y_cubic = y[indices_cubic]

    n_cubic = len(x_cubic)

    # Create system of equations

    n_equations = n_cubic - 1

    A = np.zeros((4 * n_equations, 4 * n_equations))
    b = np.zeros(4 * n_equations)
    p = np.zeros(4 * n_equations)

    # Fill up b vector

    b[0] = y_cubic[0]  # first point
    b[2 * n_equations - 1] = y_cubic[n_equations]  # last point

    for i in range(n_equations - 1):  # double points in the middle
        b[2 * i + 1] = y_cubic[i + 1]
        b[2 * i + 2] = y_cubic[i + 1]

    # Fill rest with zeros

    for i in range(2 * n_equations):
        p[2 * n_equations + i] = 0

    # Equals between ranges ( first 2 * n conditions )

    for i in range(n_equations):
        # f_i = f_i+1
        A[2 * i, 4 * i:4 * i + 4] = [x_cubic[i] ** 3, x_cubic[i] ** 2, x_cubic[i], 1]  # f_i
        A[2 * i + 1, 4 * i:4 * i + 4] = [x_cubic[i + 1] ** 3, x_cubic[i + 1] ** 2, x_cubic[i + 1], 1]  # f_i+1

    # First and second derivatives ( next 2 * (n - 1) conditions )

    for i in range(n_equations - 1):
        # d/dx (f_i) = d/dx (f_i+1)
        A[2 * n_equations + 2 * i, 4 * i:4 * i + 3] = [3 * x_cubic[i + 1] ** 2, 2 * x_cubic[i + 1], 1]  # d/dx (f_i)
        A[2 * n_equations + 2 * i, 4 * (i + 1):4 * (i + 1) + 3] = [-3 * x_cubic[i + 1] ** 2, -2 * x_cubic[i + 1],
                                                                   -1]  # -d/dx (f_i+1)

        # d^2/dx^2 (f_i) = d^2/dx^2 (f_i+1)
        A[2 * n_equations + 2 * i + 1, 4 * i:4 * i + 2] = [6 * x_cubic[i + 1], 2]  # d^2/dx^2 (f_i)
        A[2 * n_equations + 2 * i + 1, 4 * (i + 1):4 * (i + 1) + 2] = [-6 * x_cubic[i + 1], -2]  # -d^2/dx^2 (f_i+1)

    # 2 boundary conditions ( zeroing second derivatives at edges of the range )

    A[4 * n_equations - 2, 0:2] = [6 * x_cubic[0], 2]  # d^2/dx^2 (f_0) = 0
    A[4 * n_equations - 1, 4 * (n_equations - 1):4 * (n_equations - 1) + 2] = [6 * x_cubic[n_equations], 2]  # d^2/dx^2 (f_n) = 0

    # Solve system of equations

    p = np.linalg.solve(A, b)

    # Interpolated function values and plot

    cubic_functions = [[p[4 * i], p[4 * i + 1], p[4 * i + 2], p[4 * i + 3]] for i in range(n_equations)]

    # Interpolated values on original range

    y_interpolated_cubic = []

    for i in range(n_org):
        for j in range(n_equations):
            if x_cubic[j] <= x[i] <= x_cubic[j + 1]:
                y_interpolated_cubic.append(cubic_functions[j][0] * x[i] ** 3 +
                                            cubic_functions[j][1] * x[i] ** 2 +
                                            cubic_functions[j][2] * x[i] +
                                            cubic_functions[j][3])
                break

    # Interpolated values on interpolation points

    y_inter_nodes_cubic = []

    for i in range(n_equations):
        y_inter_nodes_cubic.append(cubic_functions[i][0] * x_cubic[i] ** 3 +
                                   cubic_functions[i][1] * x_cubic[i] ** 2 +
                                   cubic_functions[i][2] * x_cubic[i] +
                                   cubic_functions[i][3])

    y_inter_nodes_cubic.append(cubic_functions[n_equations - 1][0] * x_cubic[n_equations] ** 3 +
                               cubic_functions[n_equations - 1][1] * x_cubic[n_equations] ** 2 +
                               cubic_functions[n_equations - 1][2] * x_cubic[n_equations] +
                               cubic_functions[n_equations - 1][3])

    # Plot

    plot_interpolation(x, y, x_cubic, y_inter_nodes_cubic, y_interpolated_cubic, name + ' (Cubic, ' + str(cubic_nodes) + ' nodes)', 'Longitude',
                       'Latitude')


# Main
for n_nodes in [50, 100]:
    evaluate_csv('paths/MountEverest.csv', 'Mount Everest', n_nodes, n_nodes, n_nodes, )  # jedne wzniesienie

    evaluate_csv('paths/WielkiKanionKolorado.csv', 'Wielki Kanion Kolorado', n_nodes, n_nodes, n_nodes)  # jeden duży dołek i mniejsze dołki w nim

# evaluate_csv('paths/100.csv', '100', 10, 10, 10)  # wiele wzniesień

# Additional

# evaluate_csv('paths/Hel_yeah.csv', 'Hel Yeah', 15, 50, 50)  # jeden duży dołek i mniejsze dołki w nim

# evaluate_csv('paths/Obiadek.csv', 'Obiadek', 15, 50, 50)  # jeden duży dołek i mniejsze dołki w nim

# evaluate_csv('paths/Unsyncable_ride.csv', 'Unsyncable Ride', 15, 50, 50)  # wiele wzniesień

# evaluate_csv('paths/GlebiaChallengera.csv', 'Challenger Deep', 15, 50, 50)  # jeden duży dołek z łagodnym zboczem

# evaluate_csv('paths/Redlujjj.csv', 'Redlujj', 15, 50, 50)  # fajne
