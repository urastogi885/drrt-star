from scipy.spatial import cKDTree
import random
import mapUtils
import numpy as np
import matplotlib.pyplot as plt
import math


# No. of sample points
N_SAMPLE_POINTS = 100
N_KNN = 10
MAX_EDGE_LEN = 30.0


def get_sample_points(start_point, goal_point, robot_size, obstacle_points, obstacle_tree):
    sample_x, sample_y = [], []

    max_x, max_y = max(obstacle_points[0]), max(obstacle_points[1])
    min_x, min_y = min(obstacle_points[0]), min(obstacle_points[1])

    while len(sample_x) <= N_SAMPLE_POINTS:
        tx = int((random.random() * (max_x - min_x)) + min_x)
        ty = int((random.random() * (max_y - min_y)) + min_y)

        dist, index = obstacle_tree.query([tx, ty])

        if dist >= robot_size:
            sample_x.append(tx)
            sample_y.append(ty)

    sample_x.append(start_point[0])
    sample_y.append(start_point[1])
    sample_x.append(goal_point[0])
    sample_y.append(goal_point[1])

    return sample_x, sample_y


def get_obstacle_points(map_file_name):
    obstacles_x, obstacles_y = [], []
    map_array = mapUtils.readMap(map_file_name)
    for i in range(len(map_array)):
        for j in range(len(map_array[0])):
            if map_array[i][j] == 1:
                obstacles_x.append(i), obstacles_y.append(j)
    return obstacles_x, obstacles_y


def get_obstacle_tree(obstacle_points):
    return cKDTree(np.vstack((obstacle_points[0], obstacle_points[1])).T)


def is_collision(sx, sy, gx, gy, robot_size, obstacle_tree):
    x = sx
    y = sy
    dx = gx - sx
    dy = gy - sy
    yaw = math.atan2(gy - sy, gx - sx)
    d = math.hypot(dx, dy)

    if d >= MAX_EDGE_LEN:
        return True
    n_step = round(d / robot_size)

    for i in range(n_step):
        dist, _ = obstacle_tree.query([x, y])
        if dist <= robot_size:
            return True  # collision
        x += robot_size * math.cos(yaw)
        y += robot_size * math.sin(yaw)

    # goal point check
    dist, _ = obstacle_tree.query([gx, gy])
    if dist <= robot_size:
        return True  # collision

    return False  # OK


def generate_roadmap(start_point, goal_point, robot_size=1, animation=False):
    vertices, edges = [], []
    obstacle_points = get_obstacle_points('map.txt')
    obstacle_tree = get_obstacle_tree(obstacle_points)
    sample_points = get_sample_points(start_point, goal_point, robot_size, obstacle_points, obstacle_tree)
    if animation:
        plt.plot(sample_points[0], sample_points[1], ".b")
        plt.show()

    n_sample = len(sample_points[0])
    sample_tree = cKDTree(np.vstack((sample_points[0], sample_points[1])).T)

    for (i, ix, iy) in zip(range(n_sample), sample_points[0], sample_points[1]):
        dists, indexes = sample_tree.query([ix, iy], k=n_sample)
        edge_i = []
        vertex_i = []
        if [ix, iy] in vertices:
            sample_node_idx = vertices.index([ix, iy])
        else:
            sample_node_idx = len(vertices)
            vertex_i.append([ix, iy])
        for ii in range(1, len(indexes)):
            nx = sample_points[0][indexes[ii]]
            ny = sample_points[1][indexes[ii]]
            # collision = is_collision(ix, iy, nx, ny, robot_size, obstacle_tree)
            if not is_collision(ix, iy, nx, ny, robot_size, obstacle_tree):
                if [nx, ny] not in vertices:
                    vertex_i.append([nx, ny])
                    edge_i.append([sample_node_idx, len(vertices) + len(vertex_i) - 1])
                else:
                    idx = vertices.index([nx, ny])
                    edge_i.append([sample_node_idx, idx])

            if len(edge_i) >= N_KNN:
                break
        if len(edge_i) > 0:
            vertices += vertex_i
            edges += edge_i

    #  plot_road_map(road_map, sample_x, sample_y)
    return vertices, edges


if __name__ == "__main__":
    generate_roadmap((5, 5), (95, 90), 2)
