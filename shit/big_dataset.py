import testcase_split_crop
import matplotlib.pyplot as plt


import readOpenPoseJson
import calcEucldError

def calc_match_big_dataset(modelFoto, inputFoto):
    # 2D array. Elke entry is een coordinatenkoppel(joint-point) in 3D , z-coordinaat wordt nul gekozen want we werken in 2D
    # Bevat 18 coordinatenkoppels want openpose returnt 18 joint-points
    primary = readOpenPoseJson.readJsonFile('poses_dataset/' + modelFoto + '.json')
    secondary = readOpenPoseJson.readJsonFile('poses_dataset/' + inputFoto + '.json')

    #parameters van functie zijn slecht gekozen => secondary = input  &&   primary = model
    result = calcEucldError.norm_cte(secondary, primary)

    return result



class Match_result:
    def __init__(self, eucl_max, sum_eucl, match):
        self.eucl_max = eucl_max
        self.sum_eucl = sum_eucl
        self.match = match

model_nr = 1299
eind_nr = 1450

model = str(model_nr) + "_keypoints"
model = "jochen_foto1"
input_counter = model_nr +1

result_set_face = []
result_set_torso = []
result_set_legs = []

for i in range(input_counter, eind_nr):
    input_foto = str(i) + "_keypoints"
    result = calc_match_big_dataset(model, input_foto)
    print("result: " , result[1][0])

    result_set_torso.append(Match_result(result[1][0], result[1][1], 1))



fig, ax = plt.subplots()
ax.set_title("Torso")
ax.set_xlabel('MAX RMS')
ax.set_ylabel('Rotation')
counter = input_counter
for x in result_set_torso:
    #MATCH
    if x.match == 1:
        ax.scatter(x.eucl_max, x.sum_eucl, c='b') #sum_eucl is rotation in dit geval ..
    #N0 MATCH
    else:
        ax.scatter(x.eucl_max, x.sum_eucl, c='r')

    ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
    counter = counter+1


# fig, ax = plt.subplots()
# ax.set_title("Legs")
# ax.set_xlabel('MAX RMS')
# ax.set_ylabel('Rotation')
# counter = 0
# for x in result_set_legs:
#     #MATCH
#     if x.match == 1:
#         ax.scatter(x.eucl_max, x.sum_eucl, c='b')
#     #N0 MATCH
#     else:
#         ax.scatter(x.eucl_max, x.sum_eucl, c='r')
#
#     ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
#     counter = counter+1
#
# fig, ax = plt.subplots()
# ax.set_title("Face")
# ax.set_xlabel('MAX RMS')
# ax.set_ylabel('Rotation')
# counter = 0
# for x in result_set_face:
#     #MATCH
#     if x.match == 1:
#         ax.scatter(x.eucl_max, x.sum_eucl, c='b')
#     #N0 MATCH
#     else:
#         ax.scatter(x.eucl_max, x.sum_eucl, c='r')
#
#     ax.annotate(counter, (x.eucl_max, x.sum_eucl), fontsize=8)
#     counter = counter+1


plt.show()