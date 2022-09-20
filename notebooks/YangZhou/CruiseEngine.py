from YangZhou.Engine import *
from scipy.spatial.distance import cdist
import statistics as s

def find_gaps(split, gap):
    """ find the size of jumps between each element of the final cruise indices, as evenly split as possible with jump size <= 5 """

    if split > 0:
        jump = [gap//(split+1) for i in range(split+1)]
        diff = gap - sum(jump)
        if diff:
            for i in range(diff):
                jump[i] += 1
    else:
        jump = [gap]

    return jump


def find_cruise_indices(jump):
    """ find the actual cruise_indices based on gaps """

    cruise_indices = [1]
    for i in range(len(jump)):
        cruise_indices.append(1+sum(jump[:i+1]))

    return cruise_indices


def get_cruise_indices(d_val, max_jump = 5):
    """ Returns the appropriate cruise indices based on the number of values in dimension. Second argument controls maximum split size, defaulted to 5 """

    assert type(d_val) is int and type(max_jump) is int, "Error: type of input(s) is not int"
    assert d_val >= 2, "Error: argument 1 (number of values in this dimension) must be >= 2"
    assert max_jump >= 1, "Error: max_jump must be >= 1"

    gap = d_val - 1
    split = ((gap-1)//max_jump)

    jump = find_gaps(split, gap)

    cruise_indices = find_cruise_indices(jump)

    return cruise_indices


def get_cruise_indices_values(arguments, num_arg):
    """ get cruise indices values of each dimension which serves as building blocks for cruise coordinates """

    cruise_indices = dict()
    for arg in arguments:
        cruise_indices[arg] = (get_cruise_indices(num_arg[arg]))

    ##TODO: Can toggle with get_cruise_indices!!!! should add parameter to do so!!
    cruise_indices_values = list(cruise_indices.values())

    return cruise_indices_values, cruise_indices


def get_cruise_coordinate_indices(cruise_indices):
    """ get the coordinate indices required to build the cruise coordinates (in order to achieve 'every pair' out of all possible values in each dimension """
    cruise_num_arg = {arg:len(cruise_indices[arg]) for arg in cruise_indices}
    cruise_num_arg_val = list(cruise_num_arg.values())

    cruise_coordinates_indices = list()
    for i in range(cond_prod(cruise_num_arg_val)):
        cruise_coordinates_indices.append(recreate_coordinates_h(i, cruise_num_arg_val))

    return cruise_coordinates_indices


def get_cruise_coordinates(cruise_indices_values, cruise_coordinates_indices):
    """ create all the actual cruise coordinates """
    dimension = len(cruise_indices_values)
    cruise_coordinates = list()
    for i in range(len(cruise_coordinates_indices)):
        cruise_coord = list()
        for j in range(dimension):
            cruise_coord.append(cruise_indices_values[j][cruise_coordinates_indices[i][j]-1])
        cruise_coordinates.append(cruise_coord)

    return cruise_coordinates


def sort_cruise_coordinates(cruise_coordinates, max_combo):
    """ sort the cruise coordinates based on distance from current max"""

    ##TODO: In future could update this!

    edist = list(cdist([max_combo], cruise_coordinates).flatten())
    ordered_cruise_coordinates = [(cruise_coordinates[i], edist[i]) for i in range(len(cruise_coordinates))]

    ordered_cruise_coordinates.sort(reverse=True, key=lambda x: x[1])

    sorted_cruise_coordinates = [ordered_cruise_coordinates[i][0] for i in range(len(ordered_cruise_coordinates))]

    return sorted_cruise_coordinates


def get_sorted_cruise_coordinates(arguments, num_arg, max_combo):
    """ use a series of functions to get the sorted_cruise_coordinates from just arguments and num_arg"""

    ##TODO: just need to do this once

    cruise_indices_values, cruise_indices = get_cruise_indices_values(arguments, num_arg)
    cruise_coordinates_indices = get_cruise_coordinate_indices(cruise_indices)
    cruise_coordinates = get_cruise_coordinates(cruise_indices_values, cruise_coordinates_indices)

    sorted_cruise_coordinates = sort_cruise_coordinates(cruise_coordinates, max_combo)

    return sorted_cruise_coordinates


def get_max_surrounding_mean_sd(max_combo, max_accuracy, surrounding_vectors, num_arg_val, found):

    max_surrounding_coordinates = get_surrounding_coordinates(max_combo, surrounding_vectors, num_arg_val)
    max_surrounding_accuracies = [max_accuracy]
    for coord in max_surrounding_coordinates:
        index = flatten_coordinates_h(coord, num_arg_val)
        max_surrounding_accuracies.append(found[index])

    max_surrounding_mean = s.mean(max_surrounding_accuracies)
    max_surrounding_sd = s.stdev(max_surrounding_accuracies)

    return max_surrounding_mean, max_surrounding_sd





