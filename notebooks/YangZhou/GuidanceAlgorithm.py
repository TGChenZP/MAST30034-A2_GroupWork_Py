from YangZhou.Engine import *
import numpy as np
from scipy import stats


def find_new_core1(treatment, null, direction, num_arg_val, found):
    """ Only positive mean and < 0.05 """
    assert len(treatment) == len(null)
    assert len(treatment) == len(direction)
    new_cores = list()

    appended_new_core = np.zeros(np.prod(num_arg_val))
    for i in range(len(treatment)):
        if len(treatment[i]) <= 1 or len(null[i]) <= 1:
            continue

        bool_inc = np.mean(list(get_treat_or_null_scores(treatment[i], num_arg_val, found).values())) > np.mean(
            list(get_treat_or_null_scores(null[i], num_arg_val, found).values()))
        p_val = stats.ttest_ind(list(get_treat_or_null_scores(treatment[i], num_arg_val, found).values()),
                                list(get_treat_or_null_scores(null[i], num_arg_val, found).values()),
                                equal_var=True).pvalue

        # print(direction[i])
        # print(bool_inc, '\t', p_val)

        arg_max, max_accuracy_in_this_dir = dict_arg_max(get_treat_or_null_scores(treatment[i], num_arg_val, found))
        if p_val < 0.05 and bool_inc:
            if not appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)]:
                new_cores.append(arg_max)
                appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)] = 1

    # print('\n')

    return new_cores


def find_new_core2(treatment, null, direction, num_arg_val, found, core):
    """ Experimental alternative find core """

    assert len(treatment) == len(null)
    assert len(treatment) == len(direction)

    new_cores = list()
    core_score = found[flatten_coordinates_h(core, num_arg_val)]

    appended_new_core = np.zeros(np.prod(num_arg_val))
    for i in range(len(treatment)):
        if len(treatment[i]) <= 1 or len(null[i]) <= 1:
            continue

        bool_inc = np.mean(list(get_treat_or_null_scores(treatment[i], num_arg_val, found).values())) > np.mean(
            list(get_treat_or_null_scores(null[i], num_arg_val, found).values()))
        p_val = stats.ttest_ind(list(get_treat_or_null_scores(treatment[i], num_arg_val, found).values()),
                                list(get_treat_or_null_scores(null[i], num_arg_val, found).values()),
                                equal_var=True).pvalue

        # print(direction[i])
        # print(bool_inc, '\t', p_val)

        arg_max, max_accuracy_in_this_dir = dict_arg_max(get_treat_or_null_scores(treatment[i], num_arg_val, found))
        if p_val < 0.05 and bool_inc:
            if not appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)]:
                new_cores.append(arg_max)
                appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)] = 1

        elif p_val >= 0.05:
            # TODO: 暂时没太好的方法区分negative and uncertain
            if max_accuracy_in_this_dir > core_score and not \
                    appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)]:
                new_cores.append(arg_max)
                appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)] = 1

        else:
            if max_accuracy_in_this_dir > core_score and not \
                    appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)]:
                new_cores.append(arg_max)
                appended_new_core[flatten_coordinates_h(arg_max, num_arg_val)] = 1

    # print('\n')

    return new_cores
