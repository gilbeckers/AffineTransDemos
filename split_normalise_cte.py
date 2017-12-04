# https://stackoverflow.com/questions/20546182/how-to-perform-coordinates-affine-transformation-using-python-part-2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import readOpenPoseJson
import calcTransformationMatrix
import util
import normalising
import calcEucldError

# probleem:
# foto5 & jochen_foto4 => LEGS geeft vrij defitge transformatie, maar benen zijn wel gedraaid => rotatie/hoek zoeken
from testcase_split_crop import calc_final_match


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


modelFoto = "emma1"  # "foto3
inputFoto = "foto1"  # "foto1"

calc_final_match(modelFoto, inputFoto)

# plot vars
markersize = 3

im_model = plt.imread('Pictures/' + modelFoto + '.jpg')
# print("res: ", im_model.shape[0])
# portrait foto, gsm jochen
resolutieX_model = im_model.shape[1]  # 1440
resolutieY_model = im_model.shape[0]  # 1920

im_input = plt.imread('Pictures/' + inputFoto + '.jpg')
# rendered foto
resolutieX = im_input.shape[1]  # 1440 #1280
resolutieY = im_input.shape[0]  # 1920 #720

# 2D array. Elke entry is een coordinatenkoppel(joint-point) in 3D , z-coordinaat wordt nul gekozen want we werken in 2D
# Bevat 18 coordinatenkoppels want openpose returnt 18 joint-points
primary = readOpenPoseJson.readJsonFile('json_data/' + modelFoto + '.json')
secondary = readOpenPoseJson.readJsonFile('json_data/' + inputFoto + '.json')

calcEucldError.norm_cte(secondary, primary)


A = np.array([[1,1,0],[5,7,0]])
B = np.array([[8,11,0],[8,9,0]])
(transA, A) = calcTransformationMatrix.calcTransformationMatrix(A, B)
print("transformatie matrix: " , A)
print("transform result: "  , transA)

# enkel subarrays
# NEK WORDT MOMENTEEL NIET GEBRUIKT, geeft minder nauwkeurige resultaten ??
primary_torso = primary[2:8]
secondary_torso = secondary[2:8]
primary_legs = primary[8:14]
secondary_legs = secondary[8:14]
primary_face = np.vstack([primary[0], primary[14:18]])
secondary_face = np.vstack([secondary[0], secondary[14:18]])

#Zoek transformatie om input af te beelden op model
#Returnt transformatie matrix + afbeelding/image van input op model (enkel voor plotten, echte error wordt hierboven berekend)
(modelTransform_torso, A_torso) = calcTransformationMatrix.calcTransformationMatrix(secondary_torso, primary_torso)
(modelTransform_legs, A_legs) = calcTransformationMatrix.calcTransformationMatrix(secondary_legs, primary_legs)
(modelTransform_face, A_face) = calcTransformationMatrix.calcTransformationMatrix(secondary_face, primary_face)

# plot img

f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=True, figsize=(14, 6))
implot = ax1.imshow(im_model)
ax1.set_title(modelFoto + '(model)')
ax1.plot(*zip(*primary_torso), marker='o', color='r', ls='', label='model', ms=markersize)  # ms = markersize
ax1.plot(*zip(*primary_legs), marker='o', color='c', ls='', label='model', ms=markersize)  # ms = markersize
ax1.plot(*zip(*primary_face), marker='o', color='orange', ls='', label='model', ms=markersize)  # ms = markersize
red_patch = mpatches.Patch(color='red', label='model')
ax1.legend(handles=[red_patch])

ax2.set_title(inputFoto)
ax2.imshow(im_input)
ax2.plot(*zip(*secondary_torso), marker='o', color='b', ls='', ms=markersize)
ax2.plot(*zip(*secondary_legs), marker='o', color='b', ls='', ms=markersize)
ax2.plot(*zip(*secondary_face), marker='o', color='b', ls='', ms=markersize)
ax2.legend(handles=[mpatches.Patch(color='blue', label='input')])

ax3.set_title('Transformation of input')
ax3.imshow(im_model)
ax3.plot(*zip(*modelTransform_torso), marker='o', color='y', ls='', ms=markersize)
ax3.plot(*zip(*modelTransform_legs), marker='o', color='y', ls='', ms=markersize)
ax3.plot(*zip(*modelTransform_face), marker='o', color='y', ls='', ms=markersize)
ax3.legend(handles=[mpatches.Patch(color='yellow', label='Transformation of model')])

ax4.set_title('Transformatie + model')
ax4.imshow(im_model)
ax4.plot(*zip(*primary_torso), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*primary_legs), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*primary_face), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_torso), marker='o', color='y', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_legs), marker='o', color='y', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_face), marker='o', color='y', ls='', ms=markersize)

plt.show()
