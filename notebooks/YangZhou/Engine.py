from copy import deepcopy
from itertools import combinations

import numpy as np


def get_surrounding_vectors(core):
    """ Get the VECTORS that moves the core to the COORDINATES that form the 3^d object around it """

    values = [-1, 0, 1]
    new_surroundings = [[-1], [0], [1]]

    for i in range(len(core) - 1):
        old_surroundings = deepcopy(new_surroundings)
        new_surroundings = list()

        for surrounding in old_surroundings:
            for value in values:
                new_surroundings.append(
                    [surrounding[i] if i < len(surrounding) else value for i in range(len(surrounding) + 1)])

    return new_surroundings


def get_surrounding_coordinates(core, surrounding_vectors, num_arg_val):
    """ Use surrounding VECTORS to find surrounding COORDINATES """

    assert len(surrounding_vectors) >= 0
    assert len(surrounding_vectors[0]) == len(core)

    surrounding_coords = list()
    for i in range(len(surrounding_vectors)):
        new_coord = new_coordinates(core, surrounding_vectors[i], num_arg_val)
        if new_coord is not False:
            surrounding_coords.append(new_coord)

    return surrounding_coords


def new_coordinates(core, vector, num_arg_val):
    """ Get particular COORDINATE using a move in direction of VECTOR from particular CORE """

    assert len(core) == len(vector)

    new_coord = list()
    for i in range(len(vector)):
        val = core[i] + vector[i]
        if val > num_arg_val[i] or val <= 0:
            return False
        new_coord.append(val)

    return new_coord


def cond_prod(lst):
    """ special conditional probability """
    if len(lst) > 0:
        return np.prod(lst)
    else:
        return 1


def find_horizontal(surrounding_coordinates, core):
    """ Find the treatment and nulls block from a 'Horizontal' vector move """

    treatment = list()
    null = list()
    direction = list()

    for i in range(len(core)):

        for move in [-1, 1]:
            treatment_target = core[i] + move
            null_target = core[i]

            treatment_tmp = list()
            null_tmp = list()

            for vector in surrounding_coordinates:
                if vector[i] == treatment_target:
                    treatment_tmp.append(vector)
                elif vector[i] == null_target:
                    null_tmp.append(vector)

            treatment.append(treatment_tmp)
            null.append(null_tmp)
            direction.append([move if j == i else 0 for j in range(len(core))])

    return treatment, null, direction


def pick_x(i, core):
    """ Pick all combinations of range(len(core)) for indexing when getting diagonal treatments """

    return list(combinations(list(range(len(core))), i))


def get_indices(core):
    """ Get combinations of index to be used to find diagonal treatments: part of special algorithm """

    indices = list()
    for i in range(1, len(core) + 1):
        for obj in pick_x(i, core):
            indices.append(obj)

    return indices


def find_diagonal(surrounding_vectors, core, indices, num_arg_val):
    """ Find the treatment and nulls block from a 'Diagonal' vector move (effectively interaction of all params) """

    treatment = list()
    null = list()

    diagonals = get_diagonals(surrounding_vectors)

    for diagonal in diagonals:
        treatment.append(get_diagonal_treatment(core, diagonal, indices, num_arg_val))

        null.append(get_diagonal_null(core, surrounding_vectors, diagonal, num_arg_val))

    return treatment, null, diagonals


def get_diagonals(surrounding_vectors):
    """ Find all the diagonal vectors """

    return [obj for obj in surrounding_vectors if 0 not in obj]


def get_diagonal_treatment(core, diagonal, indices, num_arg_val):
    """ Find all diagonal treatments of this diagonal direction - any vector that has from 1 to d elements in same
    direction diagonal, and all other vector positions 0 """
    treatment = get_surrounding_coordinates(core, get_diag_treatment_vectors(indices, diagonal), num_arg_val)

    return treatment


def get_diag_treatment_vectors(indices, diagonal):
    """ Find all vectors for diagonal treatments (orthogonal to direction or 0 vector) """

    diag_vectors = list()

    for index in indices:
        tmp = [0 for i in range(len(diagonal))]
        for i in index:
            tmp[i] = diagonal[i]
        diag_vectors.append(tmp)

    return diag_vectors


def get_diagonal_null(core, surrounding_vectors, diagonal, num_arg_val):
    """ Find all diagonal nulls of this diagonal direction - any vector that is orthogonal to the current direction """

    null = list()
    for surrounding_vector in surrounding_vectors:
        if np.dot(surrounding_vector, diagonal) == 0:
            new_coord = new_coordinates(core, surrounding_vector, num_arg_val)
            if new_coord is not False:
                null.append(new_coord)

    return null


def get_blocks(core, surrounding_coordinates, surrounding_vectors, indices, num_arg_val):
    """ Get all blocks' treatments and nulls (in respective lists) (both horizontal and diagonal) """

    treatment = list()
    null = list()
    direction = list()

    hor_treatment, hor_null, hor_dir = find_horizontal(surrounding_coordinates, core)

    diag_treatment, diag_null, vert_dir = find_diagonal(surrounding_vectors, core, indices, num_arg_val)

    treatment.extend(hor_treatment)
    treatment.extend(diag_treatment)

    null.extend(hor_null)
    null.extend(diag_null)

    direction.extend(hor_dir)
    direction.extend(vert_dir)

    return treatment, null, direction


def flatten_coordinates_h(coord, num_arg_val):
    """ TIANJIXING """
    """ System to create data into the right format when making synthetic data """
    assert len(coord) == len(num_arg_val)

    new_num_arg_val = [num_arg_val[1], num_arg_val[0]]
    new_coord = [coord[1], coord[0]]
    if len(num_arg_val) >= 2:
        new_num_arg_val.extend(num_arg_val[2:])
        new_coord.extend(coord[2:])

    out = 0
    for i in range(len(new_coord)):
        out += (new_coord[i] - 1) * cond_prod(new_num_arg_val[:i])

    return out


def recreate_coordinates_h(out, num_arg_val):
    """ TIANJIXING """
    """ Converts 1d list index to multi dimensional coordinates """
    coordinate = [0 for i in range(len(num_arg_val))]
    length = len(num_arg_val)

    new_num_arg_val = [num_arg_val[1], num_arg_val[0]]
    if len(num_arg_val) >= 2:
        new_num_arg_val.extend(num_arg_val[2:])

    for i in range(length):
        cond_product = cond_prod(new_num_arg_val[:length - i - 1])

        coordinate[length - i - 1] = (out // cond_product) + 1
        out = (out % cond_product)

    new_coordinates = [coordinate[1], coordinate[0]]
    if len(coordinate) > 2:
        new_coordinates.extend(coordinate[2:])

    return new_coordinates


def recreate_coordinates_v(out, num_arg_val):
    """ TIANJIXING """
    """ Converts 1d list index to multi dimensional coordinates """
    coordinate = [0 for i in range(len(num_arg_val))]
    length = len(num_arg_val)

    for i in range(length):
        cond_product = cond_prod(num_arg_val[:length - i - 1])

        coordinate[length - i - 1] = (out // cond_product) + 1
        out = (out % cond_product)

    return coordinate


def flatten_coordinates_v(coord, num_arg_val):
    """ TIANJIXING """
    """ System to help navigate around 1d list to store values using multidimensional indices"""
    assert len(coord) == len(num_arg_val)

    out = 0
    for i in range(len(coord)):
        out += (coord[i] - 1) * cond_prod(num_arg_val[:i])

    return out


def get_treat_or_null_scores(treat_or_null, num_arg_val, found):
    """ Return as the relevant scores as a list to be used for t_test """

    treat_or_null_score = dict()

    for coord in treat_or_null:
        index = flatten_coordinates_h(coord, num_arg_val)
        treat_or_null_score[str(coord).strip('[]')] = found[index]

    return treat_or_null_score


def make_coord(str_coord):
    """ make coordinate (list form) from string """
    return [int(index) for index in str_coord.split(',')]


def dict_arg_max(dic):
    """ find key of maximum dict value """
    max_val = 0
    for key in dic:
        if dic[key] > max_val:
            max_val = dic[key]
            max_key = key

    return make_coord(max_key), max_val
