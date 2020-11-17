from PRM import generateRoadMap
from Node import Node
import random
import time
from copy import deepcopy


def get_graph(v):
    g_hat = []
    for i in v:
        for j in v:
            g_hat.append([i, j])
    return g_hat


def get_edge_list(graph, v, e):
    e_hat = []
    for i in range(len(graph)):
        for j in range(len(graph)):

            if graph[i] == graph[j]:
                pass
            elif graph[i][0] == graph[j][0]:
                index1 = v.index(graph[i][1])
                index2 = v.index(graph[j][1])
                if [index1, index2] in e or [index2, index1] in e:
                    e_hat.append([i, j])
            elif graph[i][1] == graph[j][1]:
                index1 = v.index(graph[i][0])
                index2 = v.index(graph[j][0])
                if [index1, index2] in e or [index2, index1] in e:
                    e_hat.append([i, j])
            else:
                index1 = v.index(graph[i][0])
                index2 = v.index(graph[j][0])
                index3 = v.index(graph[i][1])
                index4 = v.index(graph[j][1])
                if ([index1, index2] in e or [index2, index1] in e) and (
                        [index3, index4] in e or [index4, index3] in e):
                    e_hat.append([i, j])
    return e_hat

class DRRTStar:
    def __init__(self, graph, e_mat, start_points, target_points, exp_steps, n_robots):
        self.g_hat = graph
        self.e_hat = e_mat
        self.start_points = start_points
        self.target_points = target_points
        self.n_it = exp_steps
        self.n_robots = n_robots
        self.tree = [Node(start_points)]
        self.best_path = None
        self.last_vertices = Node(start_points)

    def connect_to_target(self):
        return self.best_path

    def drrt_star(self, time_limit=-1):
        # start_time = time.time()
        # while time.time() - start_time < time_limit:
        for _ in range(self.n_it):
            self.last_vertices = self.expand_drrt_star(self.last_vertices)
        path = self.connect_to_target()
        if path is not None and self.get_cost(path) < self.get_cost(self.best_path):
            self.best_path = deepcopy(path)
        return self.best_path

    def get_nearest_node(self, point):
        for i in range(len(self.tree)):
            self.tree[i].updateDistance(point)
        self.tree.sort(key=lambda x: x.distance)
        return self.tree[0]

    def get_neighbors(self, node):    # TODO: Fix this! Should return 2 nodes/vertices
        neighbors_index_list = []
        index = self.g_hat.index(node.env)
        for e in self.e_hat:
            if index in e:
                for p in e:
                    if p != index:
                        neighbors_index_list.append(p)

        neighbors_list = []
        for index in neighbors_index_list:
            neighbors_list.append(Node(self.g_hat[index]))
        return neighbors_list

    def informed_expansion(self, v_near, q_rand):
        neighbors = self.get_neighbors(v_near)
        if q_rand == self.target_points:
            for i in range(len(neighbors)):
                neighbors[i].updateDistance(self.target_points)
            neighbors.sort(key=lambda x: x.distance)
            return neighbors[0]

        return random.choice(neighbors)

    def expand_drrt_star(self, v_last):
        q_rand = []
        if v_last is None:
            # Get random points from the environment
            for _ in range(self.n_robots):
                q_rand.append([random.randrange(0, 100), random.randint(0, 100)])
            # Assign values to v_near
            v_near = deepcopy(self.get_nearest_node(q_rand))
        else:
            # Make random sample equal to target points
            for point in self.target_points:
                q_rand.append(point)
            # Assign values to v_near
            v_near = deepcopy(v_last)
        v_new = self.informed_expansion(v_near, q_rand)
        # Get neighbors to v_new that also lie in the tree
        neighbors = self.get_neighbors(v_new)
        for node in neighbors:
            if node not in self.tree:
                neighbors.remove(node)
        # TODO: Work on the section below
        # Get neighbors with minimum cost to connect with v_new
        n_best = self.get_best_neighbors(neighbors)
        if n_best is None:
            return None
        if self.get_cost(v_new) > self.get_cost(self.best_path):
            return None

        if v_new not in self.tree:
            v_new.parent = n_best
            self.tree.append(v_new)
        else:
            self.tree_rewire(v_new, n_best)
        # TODO: Start with Line 16
        return v_new

    def tree_rewire(self, node_parent, node):
        pass

    @staticmethod def get_best_neighbors(neighbors):
        return neighbors

    @staticmethod def get_cost(node):
        return 0


if __name__ == '__main__':
    start = [[51, 71], [50, 33]]
    target = [[46, 30], [47, 64]]
    expansion_steps = 300000

    fixed_nodes = [[60, 38], [51, 47], [50, 33], [51, 71], [69, 72], [36, 38], [19, 61], [5, 93], [5, 93], [26, 95],
                   [82, 96], [55, 97], [49, 16], [83, 37], [4, 5], [6, 22], [10, 37], [26, 34], [24, 10], [47, 5],
                   [27, 3],
                   [46, 30], [68, 3], [70, 20], [70, 32], [92, 6], [93, 27], [7, 61], [5, 79], [24, 73], [47, 64],
                   [36, 60],
                   [71, 59], [89, 59], [91, 78], [70, 87], [47, 89]]

    vertices, edges = generateRoadMap(0, 25, fixed_nodes)
    g_hat = get_graph(vertices)
    e_hat = get_edge_list(g_hat, vertices, edges)
    drrt_star = DRRTStar(g_hat, e_hat, start, target, expansion_steps, 2)
    start_time = time.time()
    final_path = drrt_star.drrt_star()
    print('Time taken: ', time.time() - start_time)
    # Print the final path
    for node in final_path:
        print(node.env)
