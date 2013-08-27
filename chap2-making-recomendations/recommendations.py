# A dictionary of movie critics and theis ratigs of a small set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5}, 'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5} }

from math import sqrt

# Return a distance based similarity score for person1 and person2
def sim_distance(prefs, person1, person2):
    # Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum( [pow(prefs[person1][item] - prefs[person2][item], 2) for item in si] )
    return 1/ (1+ sqrt(sum_of_squares) )

