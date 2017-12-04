import testcase2_fixedonly_none

import matplotlib.pyplot as plt


#First element=model
#Second element= input
#Third element= match(1) or not(0)
dataset = [
    ["foto1", "foto2", 1],
    ["foto1", "foto6", 1],
    ["foto6", "foto2", 1],
    ["foto6", "foto4", 1],
    ["foto4", "foto2", 1],
    ["foto4", "foto1", 1],
    ["foto4", "foto8", 1],
    ["foto8", "foto2", 1],
    ["foto8", "foto2", 1],
    ["foto1", "jochen_foto1", 1],
    ["foto1", "jochen_foto2", 1],
    ["foto4", "jochen_foto2", 1],
    ["foto4", "jochen_foto2", 1],
    ["jochen_foto1", "foto2", 1],
    ["jochen_foto2", "foto2", 1],
    ["foto6", "jochen_foto1", 1],
    ["foto6", "jochen_foto2", 1],
    ["mama1", "jochen_foto7", 1],
    ["jochen_foto4", "jochen_foto9", 1],
    ["jochen_foto1", "jochen_foto2", 1],
    ["jochen_foto5", "jochen_foto6", 1],
    ["jochen_foto8", "jochen_foto7", 1], #tot hier matches
    ["foto5", "jochen_foto2", 0],
    ["foto5", "jochen_foto1", 0],
    ["foto5", "jochen_foto7", 0],
    ["foto3", "jochen_foto4", 0],
    ["foto3", "jochen_foto5", 0],
    ["foto3", "jochen_foto7", 0],
    ["jochen_foto6", "jochen_foto7", 0],
    ["foto5", "foto6", 0],
    ["foto5", "foto8", 0],
    ["foto5", "foto4", 0],
    ["foto5", "foto3", 0],
    ["foto5", "foto2", 0],
    ["foto5", "foto1", 0],
    ["foto7", "foto1", 0],
    ["foto7", "foto2", 0],
    ["foto7", "foto3", 0],
    ["foto7", "foto4", 0],
    ["mama1", "jochen_foto6", 0],
    ["mama1", "jochen_foto9", 0],
    ["mama1", "jochen_foto5", 0],
    ["mama1", "jochen_foto4", 0],
    ["mama1", "jochen_foto2", 0],
    ["mama1", "jochen_foto1", 0],
    ["mama2", "jochen_foto1", 0],
    ["mama2", "jochen_foto2", 0],
    ["mama2", "jochen_foto4", 0],
    ["mama2", "jochen_foto7", 0],
    ["mama2", "jochen_foto8", 0],
    ["mama2", "jochen_foto6", 1],  #twijfel gevalleke
]

dataset_small = [
    ["foto1", "foto6", 1],
    ["foto6", "foto2", 1],
    ["foto1", "jochen_foto1", 1],
    ["foto1", "jochen_foto2", 1],
    ["foto6", "jochen_foto1", 1],
    ["foto6", "jochen_foto2", 1],
    ["mama1", "jochen_foto7", 1],
    ["jochen_foto4", "jochen_foto9", 1],
]


class Match_result:
    def __init__(self, eucl_max, sum_eucl, match):
        self.eucl_max = eucl_max
        self.sum_eucl = sum_eucl
        self.match = match

result_set = []
for pose_set in dataset:
    result = testcase2_fixedonly_none.doCalc(pose_set[0], pose_set[1])
    result_set.append(Match_result(result[0], result[1], pose_set[2]))


fig, ax = plt.subplots()
counter = 0
for x in result_set:
    #MATCH
    if x.match == 1:
        ax.scatter(x.eucl_max, x.sum_eucl, c='b')
    #N0 MATCH
    else:
        ax.scatter(x.eucl_max, x.sum_eucl, c='r')

    ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
    counter = counter+1

plt.show()