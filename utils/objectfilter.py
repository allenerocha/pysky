import utils.astro_info

def emphemeries_filter(*args) -> list:
    """
    This function takes the passed list and filters out all the ephemeries bodies into another list
    :param arg: List of passed bodies
    :return: [[STARS], [EPHEMERIES BODIES]]
    """
    # Converts tuple to list
    celestial_objs = list(args)

    # Retrieves a list of all ephemeriers bodies in that list
    EPHEMERIES_BODIES = utils.astro_info.get_bodies(list(args))

    # Removes all ephemeries bodies from the list
    STARS = [celestial_obj for celestial_obj in celestial_objs if celestial_obj not in EPHEMERIES_BODIES]
    return [STARS, EPHEMERIES_BODIES]
