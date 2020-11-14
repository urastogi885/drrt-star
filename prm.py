from scipy.spatial import cKDTree
import random
import mapUtils


# No. of sample points
N_SAMPLE_POINTS = 100


def get_sample_points(start_point, goal_point, robot_size, obstacle_points, obstacle_tree):
    sample_x, sample_y = [], []

    max_x, max_y = max(obstacle_points[1]), max(obstacle_points[2])
    min_x, min_y = min(obstacle_points[1]), min(obstacle_points[2])

    while len(sample_x) <= N_SAMPLE_POINTS:
        tx = (random.random() * (max_x - min_x)) + min_x
        ty = (random.random() * (max_y - min_y)) + min_y

        dist, index = obstacle_tree.query([tx, ty])

        if dist >= robot_size:
            sample_x.append(tx)
            sample_y.append(ty)

    sample_x.append(start_point[1])
    sample_y.append(start_point[2])
    sample_x.append(goal_point[1])
    sample_y.append(goal_point[2])

    return sample_x, sample_y


def get_obstacle_tree(map_file_name):
    obstacles_x, obstacles_y = [], []
    map = mapUtils.readMap(map_file_name)
    print(len(map))


if __name__ == "__main__":
    get_obstacle_tree("map.txt")
