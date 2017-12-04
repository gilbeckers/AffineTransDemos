import testcase_split_crop

import matplotlib.pyplot as plt
import pylab

#First element=model
#Second element= input
#Third element= match(1) or not(0)
dataset_torso = [
    ["jochen_foto9", "nina1", 0],
    ["jochen_foto9", "emma1", 0],
    ["gil1", "emma1", 0],
    ["gil1", "emma1", 0],
    ["jochen_foto1", "emma1", 0],
    ["jochen_foto2", "emma1", 0],
    ["gil1", "emma1", 0],
    ["foto1", "foto2", 1],
    ["foto1", "foto6", 1],
    ["foto6", "foto2", 1],
    ["foto1", "jochen_foto1", 1],
    ["foto1", "jochen_foto2", 1],
    ["jochen_foto1", "foto2", 1],
    ["jochen_foto2", "foto2", 1],
    ["foto6", "jochen_foto1", 1],
    ["foto6", "jochen_foto2", 1],
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
    ["mama2", "jochen_foto6", 0],#twijfel gevalleke
    ["mama1", "jochen_foto7", 0],

]







dataset_legs = [
    ["foto1", "jochen_foto1", 1],
    ["foto1", "foto2", 1],
    ["jochen_foto9", "nina1", 0],
    ["jochen_foto4", "nina1", 0],
    ["jochen_foto6", "jochen_foto7", 1],
    ["jochen_foto6", "jochen_foto8", 1],
    ["jochen_foto8", "jochen_foto7", 1],
    ["jochen_foto6", "jochen_foto5", 1],
    ["jochen_foto5", "jochen_foto7", 1],
    ["jochen_foto1", "jochen_foto2", 1],
    ["jochen_foto1", "foto7", 1],
    ["jochen_foto2", "foto7", 1],
    ["foto5", "foto7", 1],
    ["foto1", "jochen_foto9", 0],
    ["foto3", "jochen_foto9", 0],
    ["foto3", "foto1", 0],
    ["foto3", "foto2", 0],
    ["foto3", "foto4", 0],
    ["foto3", "foto5", 0],


]

dataset_face = [
    ["foto1", "foto2", 1],
    ["foto1", "foto3", 1],
    ["foto1", "foto5", 1],
    ["foto5", "foto3", 1],
    ["foto1", "foto2", 1],
    ["foto1", "foto4", 0],
    ["foto5", "foto4", 0],
    ["foto3", "foto4", 0],
    ["foto2", "foto4", 0],

]

class Match_result:
    def __init__(self, eucl_max, sum_eucl, match):
        self.eucl_max = eucl_max
        self.sum_eucl = sum_eucl
        self.match = match

result_set_face = []
result_set_torso = []
result_set_legs = []

for pose_set in dataset_torso:
    result = testcase_split_crop.calc_match(pose_set[0], pose_set[1])

    #result_set_face.append(Match_result(result[0][0], result[0][1], pose_set[2]))
    result_set_torso.append(Match_result(result[1][0], result[1][1], pose_set[2]))
    #result_set_legs.append(Match_result(result[2][0], result[2][1], pose_set[2]))

for pose_set in dataset_legs:
    result = testcase_split_crop.calc_match(pose_set[0], pose_set[1])

    #result_set_face.append(Match_result(result[0][0], result[0][1], pose_set[2]))
    #result_set_torso.append(Match_result(result[1][0], result[1][1], pose_set[2]))
    result_set_legs.append(Match_result(result[2][0], result[2][1], pose_set[2]))

for pose_set in dataset_face:
    result = testcase_split_crop.calc_match(pose_set[0], pose_set[1])

    result_set_face.append(Match_result(result[0][0], result[0][1], pose_set[2]))
    #result_set_torso.append(Match_result(result[1][0], result[1][1], pose_set[2]))
    #result_set_legs.append(Match_result(result[2][0], result[2][1], pose_set[2]))

fig, ax = plt.subplots()
ax.set_title("Torso")
ax.set_xlabel('MAX RMS')
ax.set_ylabel('Rotation')
ax.plot((0, 0.05), (30, 30), 'g')
ax.plot((0.05, 0.05), (0, 30), 'k-')
counter = 0
for x in result_set_torso:
    #MATCH
    if x.match == 1:
        ax.scatter(x.eucl_max, x.sum_eucl, c='b') #sum_eucl is rotation in dit geval ..
    #N0 MATCH
    else:
        ax.scatter(x.eucl_max, x.sum_eucl, c='r')

    ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
    counter = counter+1


fig, ax = plt.subplots()
ax.set_title("Legs")
ax.set_xlabel('MAX RMS')
ax.set_ylabel('Rotation')
counter = 0
for x in result_set_legs:
    #MATCH
    if x.match == 1:
        ax.scatter(x.eucl_max, x.sum_eucl, c='b')
    #N0 MATCH
    else:
        ax.scatter(x.eucl_max, x.sum_eucl, c='r')

    ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
    counter = counter+1

fig, ax = plt.subplots()
ax.set_title("Face")
ax.set_xlabel('MAX RMS')
ax.set_ylabel('Rotation')
counter = 0
for x in result_set_face:
    #MATCH
    if x.match == 1:
        ax.scatter(x.eucl_max, x.sum_eucl, c='b')
    #N0 MATCH
    else:
        ax.scatter(x.eucl_max, x.sum_eucl, c='r')

    ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
    counter = counter+1


plt.show()