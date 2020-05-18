import copy
import numpy as np
import distance
from jellyfish._jellyfish import damerau_levenshtein_distance
import unicodecsv


def DL_Distance(str1, str2):
    print(str1, str2)
    print("distance 1: ", distance.nlevenshtein(str1, str2))
    print("distance 2: ", damerau_levenshtein_distance(str1, str2))
    dls = (damerau_levenshtein_distance(str1, str2) / max(len(str1), len(str2)))
    print("distance 3: ", dls)

    print("distance 4: ", distance.jaccard(str1, str2))


str1 = "sdfs sdf sdf"
str2 = "asdf asf ghdfgfdg safs f"
DL_Distance(str1.upper(), str2.upper())