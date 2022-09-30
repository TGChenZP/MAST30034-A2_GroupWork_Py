from scipy.stats import t

def cruise_warning_threshold1(max_accuracy, max_surrounding_sd, max_surrounding_n):
    """ max - halfwidth """

    qt = t.ppf(0.025, max_surrounding_n-1)
    halfwidth = max_surrounding_sd * qt

    # print('Max accuracy:', max_accuracy)
    # print('sd:', max_surrounding_sd)
    # print('Halfwidth:', halfwidth)
    # print('Threshold:', max_accuracy+halfwidth, '\n')

    return max_accuracy + halfwidth


def cruise_warning_threshold2(max_accuracy, max_surrounding_sd, max_surrounding_n):
    """ max - halfwidth (99% CI) """

    qt = t.ppf(0.005, max_surrounding_n-1)
    halfwidth = max_surrounding_sd * qt

    # print('Max accuracy:', max_accuracy)
    # print('sd:', max_surrounding_sd)
    # print('Halfwidth:', halfwidth)
    # print('Threshold:', max_accuracy+halfwidth, '\n')

    return max_accuracy + halfwidth


def cruise_warning_threshold3(max_surrounding_mean, max_surrounding_sd, max_surrounding_n):
    """ lower bound of 95 CI"""

    qt = t.ppf(0.025, max_surrounding_n-1)
    halfwidth = max_surrounding_sd * qt

    # print('Max accuracy:', max_accuracy)
    # print('sd:', max_surrounding_sd)
    # print('Halfwidth:', halfwidth)
    # print('Threshold:', max_surrounding_mean+halfwidth, '\n')

    return max_surrounding_mean + halfwidth


def cruise_warning_threshold4(max_surrounding_mean, max_surrounding_sd, max_surrounding_n):
    """ lower bound of 99 CI"""

    qt = t.ppf(0.005, max_surrounding_n-1)
    halfwidth = max_surrounding_sd * qt

    # print('Max accuracy:', max_accuracy)
    # print('sd:', max_surrounding_sd)
    # print('Halfwidth:', halfwidth)
    # print('Threshold:', max_surrounding_mean+halfwidth, '\n')

    return max_surrounding_mean + halfwidth