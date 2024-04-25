import numpy as np


def initialize_centroids_forgy(data, k):
    # TODO implement random initialization

    ids = np.random.choice(data.shape[0], size=k, replace=False)

    return np.array(data[ids])


def initialize_centroids_kmeans_pp(data, k):
    # TODO implement kmeans++ initialization

    centroids = [data[np.random.choice(len(data))].tolist()]

    for i in range(k-1):
        max_distance = -1
        data_to_add = None
        for data_point in data:
            data_point_list = data_point.tolist()
            if data_point_list not in centroids:
                dist = sum([np.sum((centroid - data_point)**2) for centroid in centroids])
                if dist > max_distance:
                    max_distance = dist
                    data_to_add = data_point_list
        centroids.append(data_to_add)

    return np.array(centroids)


def assign_to_cluster(data, centroids):
    assignments = np.zeros(data.shape[0], dtype=int)
    for i in range(data.shape[0]):
        min_distance = np.inf
        for j in range(centroids.shape[0]):
            distance = np.sum((centroids[j] - data[i])**2)
            if distance < min_distance:
                min_distance = distance
                assignments[i] = j
    return assignments


def update_centroids(data, assignments):
    # TODO find new centroids based on the assignments
    new_centroids = []
    for k in range(len(np.unique(assignments))):
        cluster_data = data[assignments == k]
        new_centroids.append(cluster_data.mean(axis=0))

    return np.array(new_centroids)


def mean_intra_distance(data, assignments, centroids):
    return np.sqrt(np.sum((data - centroids[assignments, :]) ** 2))


def k_means(data, num_centroids, kmeansplusplus=False):
    # centroids initialization
    if kmeansplusplus:
        centroids = initialize_centroids_kmeans_pp(data, num_centroids)
    else:
        centroids = initialize_centroids_forgy(data, num_centroids)

    assignments = assign_to_cluster(data, centroids)
    for i in range(100):  # max number of iteration = 100
        # print(f"Intra distance after {i} iterations: {mean_intra_distance(data, assignments, centroids)}")
        centroids = update_centroids(data, assignments)
        new_assignments = assign_to_cluster(data, centroids)
        if np.all(new_assignments == assignments):  # stop if nothing changed
            break
        else:
            assignments = new_assignments

    return new_assignments, centroids, mean_intra_distance(data, new_assignments, centroids)
