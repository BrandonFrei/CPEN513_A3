from copy import deepcopy
import os
import random
import numpy as np
import math
import matplotlib.pyplot as plt
import numpy as np


### Gain will be calculated from A's perspective

def parse_netlist(rel_path):
    """Parses the netlist

    Args:
        rel_path (string): relative path to location of the input file

    Returns:
        list: list version of netlist
    """
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

    abs_file_path = os.path.join(script_dir, rel_path)
    # reading in the file
    data = []
    with open(abs_file_path) as rfile:
        data_raw = rfile.readlines()
        for line in data_raw:
            data.append(line.strip())
    data = list(filter(('').__ne__, data))
    split_data = []
    for i in range(int(len(data))):
        temp = (data[i].split())
        temp = list(map(int, temp))
        split_data.append(temp)
    return split_data


def split_nodes(nodes):
    nodes_a = {}
    nodes_b = {}
    for i in range(len(nodes)):
        if (i % 2 == 0):
            nodes_a[i] = deepcopy(nodes[i])
        else:
            nodes_b[i] = deepcopy(nodes[i])
    return nodes_a, nodes_b


def split_nodes_random(nodes):
    nodes_a = {}
    nodes_b = {}
    num_nodes = len(nodes)
    node_locations = [i for i in range(num_nodes)]
    random.shuffle(node_locations)
    for i in range(len(nodes)):
        if (node_locations[i] % 2 == 0):
            nodes_a[i] = deepcopy(nodes[i])
        else:
            nodes_b[i] = deepcopy(nodes[i])
    return nodes_a, nodes_b

def get_cost(nodes_a, nodes_b, edges):
    for i in range(len(edges)):
        all_in_set_a = 0
        all_in_set_b = 0
        for j in range(len(edges[i][0])):
            edge = edges[i][0][j]
            if (edge in nodes_a):
                all_in_set_a = 1
            if (edge in nodes_b):
                all_in_set_b = 1
            if (all_in_set_a and all_in_set_b):
                break
        if (all_in_set_a and all_in_set_b):
            edges[i][1] = 1
        else:
            edges[i][1] = 0
    return edges
    # edges that cross the partition - # of edges that don't cross partition

def get_cost_hypernet(nodes_a, nodes_b, edges):
    for i in range(len(edges)):
        normalizing_factor = 1/(len(edges[i][0]) - 1)
        edges[i][1] = normalizing_factor
    return edges

def get_highest_cost(nodes):
    node_keys = list(nodes.keys())
    max_cost = -100000000
    highest_cost_node = -1
    for i in range(len(nodes)):
        if (nodes[node_keys[i]][2] == 1):
            continue
        if (nodes[node_keys[i]][1] > max_cost):
            max_cost = nodes[node_keys[i]][1]
            highest_cost_node = node_keys[i]
    return highest_cost_node

def get_highest_costs(nodes_a, nodes_b):
    high_cost_a = get_highest_cost(nodes_a)
    high_cost_b = get_highest_cost(nodes_b)
    return high_cost_a, high_cost_b

def calc_new_costs_vanilla(nodes_a, nodes_b, edges, swapped_node_1, swapped_node_2):
    delta_cost = 0
    edges_to_recalc = list(set(nodes_a[swapped_node_2][0] + nodes_b[swapped_node_1][0]))
    previous_cost = 0
    for i in range(len(edges_to_recalc)):
        node_a_cost = 0
        node_b_cost = 0

        for j in range(len(edges[edges_to_recalc[i]][0])):
            if (edges[edges_to_recalc[i]][0][j] in nodes_a):
                node_a_cost = 1
            if (edges[edges_to_recalc[i]][0][j] in nodes_b):
                node_b_cost = 1
            if (node_a_cost & node_b_cost):
                break
        if (node_a_cost & node_b_cost):
            if (edges[edges_to_recalc[i]][1] == 0):
                delta_cost += 1
            edges[edges_to_recalc[i]][1] = 1
        else:
            if (edges[edges_to_recalc[i]][1] == 1):
                delta_cost -= 1
            edges[edges_to_recalc[i]][1] = 0
    return edges, delta_cost


def calc_new_costs_modified(nodes_a, nodes_b, edges, swapped_node_1, swapped_node_2):
    delta_cost = 0
    edges_to_recalc = list(set(nodes_a[swapped_node_2][0] + nodes_b[swapped_node_1][0]))
    previous_cost = 0
    for i in range(len(edges_to_recalc)):
        node_a_cost = 0
        node_b_cost = 0

        for j in range(len(edges[edges_to_recalc[i]][0])):
            if (edges[edges_to_recalc[i]][0][j] in nodes_a):
                node_a_cost += 1
            if (edges[edges_to_recalc[i]][0][j] in nodes_b):
                node_b_cost += 1
            if (node_a_cost & node_b_cost):
                break
        # print("This_iteration")
        # print("len(edges[edges_to_recalc[i]][0]) - 1: " + str(len(edges[edges_to_recalc[i]][0])) + ", node_a_cost: " + str(node_a_cost))
        
        # if all of the nodes are in the correct side
        if (len(edges[edges_to_recalc[i]][0]) == node_a_cost or len(edges[edges_to_recalc[i]][0]) == node_b_cost):
            if (edges[edges_to_recalc[i]][1] == 1):
                delta_cost -= 1
            edges[edges_to_recalc[i]][1] = 0
        # if there is a single node on the wrong side of the partition,
        # and if both nodes are connected in the same net
        # effectively, by taking this move, we're not maximizing the best edge move we could be 
        elif ((len(edges[edges_to_recalc[i]][0]) - 1 == node_a_cost or len(edges[edges_to_recalc[i]][0]) - 1 == node_b_cost)
                # and if they are both in the same net
                and (swapped_node_1 in edges[edges_to_recalc[i]][0] and swapped_node_2 in edges[edges_to_recalc[i]][0])):
            print("hello")
            delta_cost += 1
            if (edges[edges_to_recalc[i]][1] == 0):
                delta_cost += 1
            edges[edges_to_recalc[i]][1] = 1

        else:
            if (edges[edges_to_recalc[i]][1] == 0):
                delta_cost += 1
            edges[edges_to_recalc[i]][1] = 1
    return edges, delta_cost


def calc_total_cost(edges):
    cost = 0
    for i in range(len(edges)):
        cost += edges[i][1]
    return cost

def calc_total_gain(nodes_a, nodes_b):
    # print("new cost calc")
    node_a_keys = list(nodes_a.keys())
    node_b_keys = list(nodes_b.keys())
    cost = 0
    for i in range(len(node_a_keys)):
        cost += nodes_a[node_a_keys[i]][1]
    for i in range(len(node_b_keys)):
        cost += nodes_b[node_b_keys[i]][1]
    return cost

def calc_each_gain_initial_vanilla(nodes_a, nodes_b, edges):
    node_a_keys = list(nodes_a.keys())
    for i in range(len(nodes_a)):
        cost = 0
        for j in range(len(nodes_a[node_a_keys[i]][0])):
            if (edges[nodes_a[node_a_keys[i]][0][j]][1] == 1):
                cost += 1
            else:
                cost -= 1
        nodes_a[node_a_keys[i]][1] += cost
    node_b_keys = list(nodes_b.keys())
    for i in range(len(nodes_b)):
        cost = 0
        for j in range(len(nodes_b[node_b_keys[i]][0])):
            if (edges[nodes_b[node_b_keys[i]][0][j]][1] == 1):
                cost += 1
            else:
                cost -= 1
        nodes_b[node_b_keys[i]][1] += cost
    return nodes_a, nodes_b

def calc_each_gain_initial(nodes_a, nodes_b, edges):
    # list of the keys, because it's essentially a gather scatter
    node_a_keys = list(nodes_a.keys())
    for i in range(len(nodes_a)):
        # if the node is locked
        if (nodes_a[node_a_keys[i]][2] == 1):
            continue
        node_a_cost = 0
        for j in range(len(nodes_a[node_a_keys[i]][0])):
            # add the contributing cost from each net associated to the node
            node_a_cost += edges[nodes_a[node_a_keys[i]][0][j]][1]
        nodes_a[node_a_keys[i]][1] = node_a_cost
    node_b_keys = list(nodes_b.keys())
    for i in range(len(nodes_b)):
        # if the node is locked
        if (nodes_b[node_b_keys[i]][2] == 1):
            continue
        node_b_cost = 0
        for j in range(len(nodes_b[node_b_keys[i]][0])):
            node_b_cost += edges[nodes_b[node_b_keys[i]][0][j]][1]
        nodes_b[node_b_keys[i]][1] = node_b_cost
    return nodes_a, nodes_b

def swap_nodes(nodes_a, nodes_b, node_to_swap_a, node_to_swap_b):
    temp = deepcopy(nodes_b[node_to_swap_b])
    del nodes_b[node_to_swap_b]
    nodes_a[node_to_swap_b] = temp
    temp = deepcopy(nodes_a[node_to_swap_a])
    nodes_b[node_to_swap_a] = temp
    del nodes_a[node_to_swap_a]
    # the 1 is a "lock", indicating that this node has been swapped on this pass
    nodes_a[node_to_swap_b][2] = 1
    nodes_b[node_to_swap_a][2] = 1
    return nodes_a, nodes_b

def unlock_nodes(nodes):
    node_a_keys = list(nodes.keys())
    for i in range(len(nodes)):
        nodes[node_a_keys[i]][2] = 0
    return nodes

def unlock_all_nodes(nodes_a, nodes_b):
    nodes_a = unlock_nodes(nodes_a)
    nodes_b = unlock_nodes(nodes_b)
    return nodes_a, nodes_b

def get_values(netlist):
    """gets descriptive values of netlist

    Args:
        netlist (list): list version of netlist

    Returns:
        num_blocks (int): number of blocks in netlist
        num_connections (int): number of connections between cells
        num_rows (int): number of grid rows for circuit to be placed
        num_columns (int): number of grid columns for circuit to be placed
        new_netlist (dict): the key is the net number, the 1st list associated is the respective net, the 2nd list
                            will contain the cost of the given net
    """
    num_blocks, num_connections, num_rows, num_columns = netlist[0]
    netlist = netlist[1:]
    new_netlist = {}
    for i in range(num_connections):
        new_netlist[int(i)] = []
        new_netlist[int(i)].append(netlist[i])
        # the 0 will represet that the node has not yet been moved (it is unlocked)
        new_netlist[int(i)].append(0)
    return num_blocks, num_connections, num_rows, num_columns, new_netlist

def init_cell_placements(num_blocks, num_rows, num_connections, num_columns, netlist):
    """Places cells into the nxm grid as specified by the input file (random locations)

    Args:
        num_blocks (int): [description]
        num_rows (int): number of rows in cell grid
        num_connections (int): number of nets in cell grid
        num_columns (int): number of columns in cell grid
        netlist (dict): the key is the net number, the 1st list associated is the respective net, the 2nd list
                        will contain the cost of the given net (left for init_cell_placement)

    Returns:
        dict: contains the locations of each block in the format of:
              block: [[current_cell_x, current_cell_y], [associated netlist nets]]
    """
    block_locations = {}
    avail_locations = []
    for i in range(num_rows):
        for j in range(num_columns):
            temp_loc = [i, j]
            avail_locations.append(temp_loc)
    random.shuffle(avail_locations)

    # after this, block locations looks like: block: [[current_cell_x, current_cell_y], [associated netlist nets]]
    for i in range(num_blocks):
        block_locations[int(i)] = []
        associated_nets = []
        for j in range(num_connections):
            if int(i) in netlist[j][0][:]:
                associated_nets.append(j)
        block_locations[int(i)].append(associated_nets)
        block_locations[int(i)].append(0)
        block_locations[int(i)].append(0)
    avail_locations = []
    # fill in blank block locations
    return block_locations


def main_function(input_file):
    # random.seed(9)
    edges = parse_netlist(input_file)
    num_blocks, num_connections, num_rows, num_columns, edges = get_values(edges)
    nodes = init_cell_placements(num_blocks, num_rows, num_connections, num_columns, edges)

    nodes_a, nodes_b = split_nodes_random(nodes)
    edges = get_cost(nodes_a, nodes_b, edges)

    fig, ax1 = plt.subplots()
    nodes_a, nodes_b, edges = loop_2(nodes_a, nodes_b, edges, num_blocks, fig, ax1)
    # plt.pause(5)
    node_keys = list(nodes_a.keys()) + list(nodes_b.keys())
    new_nodes = {}
    new_edges = get_cost(nodes_a, nodes_b, edges)
    new_cost = calc_total_cost(new_edges)
    print("new cost: " + str(new_cost))
    for i in range(num_blocks):
        if (node_keys[i] in nodes_a):
            new_nodes[node_keys[i]] = nodes[node_keys[i]][0]
        else:
            new_nodes[node_keys[i]] = nodes[node_keys[i]][0]
    print("NODES")
    old_nodes = {}
    for i in range(len(nodes)):
        old_nodes[i] = nodes[i][0]
    print("NEW_NODES")
    if (new_nodes == old_nodes):
        print("test passed :)")
    return nodes_a, nodes_b, edges


def loop_2(nodes_a, nodes_b, edges, num_blocks, fig, ax1):
    plt.title("Cost vs. Number of Steps")
    ax1.set_xlabel("Number of KL Iterations")
    ax1.set_ylabel("Cost (Total Cuts)", c="red")
    cost_array = []
    i = 0
    best_cut_a = deepcopy(nodes_a)
    best_cut_b = deepcopy(nodes_b)
    best_edges = deepcopy(edges)
    while (i < 6):
        nodes_a, nodes_b = unlock_all_nodes(nodes_a, nodes_b)
        is_change = 0
        nodes_a, nodes_b = calc_each_gain_initial_vanilla(nodes_a, nodes_b, edges)
        cost = calc_total_cost(edges)
        temp_cost = cost
        # print("current iteration: " + str(i))
        for j in range(int(num_blocks / 2)):
            
            highest_cost_node_a, highest_cost_node_b = get_highest_costs(nodes_a, nodes_b)
            # print("Node A highest cost: " + str(highest_cost_node_a) + ", Node B highest cost: " + str(highest_cost_node_b))
            nodes_a, nodes_b = swap_nodes(nodes_a, nodes_b, highest_cost_node_a, highest_cost_node_b)
            # print(nodes_a)
            # print(sorted(nodes_a))
            edges, delta_cost = calc_new_costs_modified(nodes_a, nodes_b, edges, highest_cost_node_a, highest_cost_node_b)
            # print("new-nodes:")
            # print(nodes_a)
            # print(sorted(nodes_a))
            temp_cost += delta_cost
            # print("temp costs: " + str(temp_cost))
            if (cost > temp_cost):
                cost = temp_cost
                best_cut_a = deepcopy(nodes_a)
                best_cut_b = deepcopy(nodes_b)
                best_edges = deepcopy(edges)
                # print(best_edges)
                # print(sorted(best_cut_a))
                is_change = 1

        cost_array.append(cost)
        ax1.scatter(i, cost, c="Red")
        ax1.plot(range(i+1), cost_array, c="red", linestyle='-')
        plt.pause(0.05)
        i = i + 1
        print(cost)
        if(is_change == 1):
            nodes_a = deepcopy(best_cut_a)
            nodes_b = deepcopy(best_cut_b)
            edges = deepcopy(best_edges)
        else:
            return best_cut_a, best_cut_b, best_edges
            break
        
    return nodes_a, nodes_b, edges
    