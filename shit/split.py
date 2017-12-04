# https://stackoverflow.com/questions/20546182/how-to-perform-coordinates-affine-transformation-using-python-part-2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import readOpenPoseJson
import calcTransformationMatrix
import util


# probleem:
# foto5 & jochen_foto4 => LEGS geeft vrij defitge transformatie, maar benen zijn wel gedraaid => rotatie/hoek zoeken

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def evaluateError(max_error, sum_error, transformation_matrix):
    # Zeker fout, geen match
    if (max_error >= 0.06 or sum_error >= 0.25):
        return bcolors.FAIL + "no_match" + bcolors.ENDC + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
    # Zeker juist, wel een match
    elif (max_error <= 0.042 or sum_error <= 0.13):
        rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
        rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
        if (max([rotation_1, rotation_2]) > 20):
            return bcolors.WARNING + "match, but rotation to high: " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
        else:
            return bcolors.OKGREEN + "match! " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
    else:
        return "no_conclusion" + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)


def evaluateError_face(max_error, sum_error, transformation_matrix):
    # Zeker fout, geen match
    if (max_error >= 0.06 or sum_error >= 0.25):
        return bcolors.FAIL + "no_match  max_error: " + bcolors.ENDC + str(max_error) + "   sum: " + str(sum_error)
    # Zeker juist, wel een match
    elif (max_error <= 0.042 or sum_error <= 0.13):
        rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
        rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
        if (max([rotation_1, rotation_2]) > 65):
            return bcolors.WARNING + "match, but rotation to high: " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
        else:
            return bcolors.OKGREEN + "match! " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
    else:
        return "no_conclusion" + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)


def evaluateMSE(input, model_transformation):
    # https://stackoverflow.com/questions/16774849/mean-squared-error-in-numpy
    # The effect of each error on RMSD is proportional to the size of the squared error thus larger errors have a disproportionately large effect on RMSD.
    # Consequently, RMSD is sensitive to outliers.[2][3]

    #laatste 0 kolom verwijderen
    input = input[:, :-1]
    model_transformation = model_transformation[:, :-1]
    #print(input - model_transformation)
    #rint(((input - model_transformation) ** 2))
    print(((input - model_transformation) ** 2).mean(axis=1))
    #print()
    mse = (((input - model_transformation) ** 2).mean(axis=1)) **(1/2)
    mse_max = max(mse)

    if mse_max > 350:
        return "no match  mse_max: " + str(mse_max) + "  mse: " + str(mse)
    else:
        return "match  mse_max: " + str(mse_max) + "  mse: " + str(mse)


modelFoto = "jochen_foto8"  # "foto3"
inputFoto = "jochen_foto2"  # "foto1"

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

# enkel subarrays
# NEK WORDT MOMENTEEL NIET GEBRUIKT, geeft minder nauwkeurige resultaten ??
primary_torso = primary[2:8]
secondary_torso = secondary[2:8]

primary_legs = primary[8:14]
secondary_legs = secondary[8:14]

primary_face = np.vstack([primary[0], primary[14:18]])
secondary_face = np.vstack([secondary[0], secondary[14:18]])

(modelTransform_torso, A_torso) = calcTransformationMatrix.calcTransformationMatrix(primary_torso, secondary_torso)
(modelTransform_legs, A_legs) = calcTransformationMatrix.calcTransformationMatrix(primary_legs, secondary_legs)
(modelTransform_face, A_face) = calcTransformationMatrix.calcTransformationMatrix(primary_face, secondary_face)


# print("--MSE torso: ", (((secondary_torso - modelTransform_torso) ** 2).mean(axis=1)) ** 1 / 2)
# print("-MSE legs: ", (((secondary_legs - modelTransform_legs) ** 2).mean(axis=1)) ** 1 / 2)
# print("--MSE torso: ", ((secondary_torso - modelTransform_torso) ** 2).mean(axis=None))
# print("-MSE legs: ", ((secondary_legs - modelTransform_legs) ** 2).mean(axis=None))
# mse_torso_sum =  ((secondary_torso - modelTransform_torso) ** 2).mean(axis=None)
# psnr_torso = np.log10([19940**2, mse_torso_sum])
# print("PSNR: " , psnr_torso)

print("A- transformatie matrix: FACE")
print(A_face)
# print("a: " , A_legs[0][0])
# print("a: " , A_legs[0][1])
# print("Input:")
# print(secondary)
# print("Result- transformatie van model:")
# print(modelTransform)

# Gewoon  MAX[  xi-x'i  en  yi-y'i ]
maxError_torso = np.abs(secondary_torso - modelTransform_torso)
print("Max error torso:", maxError_torso.max())

maxError_legs = np.abs(secondary_legs - modelTransform_legs)
print("Max error legs:", maxError_legs.max())

maxError_face = np.abs(secondary_face - modelTransform_face)
print("Max error legs:", maxError_face.max())
# print(maxError)

# np.sqrt(np.sum((maxError[:,0] - maxError[:,1]) ** 2))
euclDis_torso = ((maxError_torso[:, 0]) ** 2 + maxError_torso[:, 1] ** 2) ** 0.5
euclDisNorm_torso = ((maxError_torso[:, 0] / resolutieX) ** 2 + (maxError_torso[:, 1] / resolutieY) ** 2) ** 0.5
print("@@@@@Eucl dis TORSO: ", euclDis_torso)

euclDis_legs = ((maxError_legs[:, 0]) ** 2 + maxError_legs[:, 1] ** 2) ** 0.5
euclDisNorm_legs = ((maxError_legs[:, 0] / resolutieX) ** 2 + (maxError_legs[:, 1] / resolutieY) ** 2) ** 0.5
print("@@@@@Eucl dis LEGS: " , euclDis_legs)


euclDis_face = ((maxError_face[:, 0]) ** 2 + maxError_face[:, 1] ** 2) ** 0.5
euclDisNorm_face = ((maxError_face[:, 0] / resolutieX) ** 2 + (maxError_face[:, 1] / resolutieY) ** 2) ** 0.5

# Euclidean distance boven gwn coordinaten verschil want eucl dis is ne cirkel
# print("euclidean dis: ", euclDis)
# max_euclDis_torso = max(euclDis_torso)
# print("\n--------     Euclidean dis TORSO      -------")
# print("Max euclidean dis: ", max_euclDis_torso)

max_euclDis_norm_torso = max(euclDisNorm_torso)
sum_max_euclDis_norm_torso = np.sum(euclDisNorm_torso)
print("\n----- Euclidean dis genormaliseeerd  TORSO -----")
print("euclid dis NORM; ", euclDisNorm_torso)
print("Max euclidean dis norm resolutie: ", max_euclDis_norm_torso)
print("Sum euclidean dis: ", sum_max_euclDis_norm_torso)

# max_euclDis_legs = max(euclDis_legs)
# print("\n--------     Euclidean dis  LEGS    -------")
# print("Max euclidean dis: ", max_euclDis_legs)

max_euclDis_norm_legs = max(euclDisNorm_legs)
sum_max_euclDis_norm_legs = np.sum(euclDisNorm_legs)
print("\n----- Euclidean dis genormaliseeerd  LEGS -----")
print("euclid dis NORM; ", euclDisNorm_legs)
print("Max euclidean dis norm resolutie: ", max_euclDis_norm_legs)
print("Sum euclidean dis: ", sum_max_euclDis_norm_legs)

max_euclDis_norm_face = max(euclDisNorm_face)
sum_max_euclDis_norm_face = np.sum(euclDisNorm_face)
print("\n----- Euclidean dis genormaliseeerd  FACE -----")
print("euclid dis NORM; ", euclDisNorm_face)
print("Max euclidean dis norm resolutie: ", max_euclDis_norm_face)
print("Sum euclidean dis: ", sum_max_euclDis_norm_face)

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

ax3.set_title('Transformation of model')
ax3.imshow(im_input)
ax3.plot(*zip(*modelTransform_torso), marker='o', color='y', ls='', ms=markersize)
ax3.plot(*zip(*modelTransform_legs), marker='o', color='y', ls='', ms=markersize)
ax3.plot(*zip(*modelTransform_face), marker='o', color='y', ls='', ms=markersize)
ax3.legend(handles=[mpatches.Patch(color='yellow', label='Transformation of model')])

ax4.set_title('Transformatie + input')
ax4.imshow(im_input)
ax4.plot(*zip(*secondary_torso), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*secondary_legs), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*secondary_face), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_torso), marker='o', color='y', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_legs), marker='o', color='y', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_face), marker='o', color='y', ls='', ms=markersize)

print(bcolors.HEADER + "Evaluation TORSO: " + bcolors.ENDC,
      evaluateError(max_euclDis_norm_torso, sum_max_euclDis_norm_torso, A_torso))
print(bcolors.HEADER + "Evaluation LEGS:  " + bcolors.ENDC,
      evaluateError(max_euclDis_norm_legs, sum_max_euclDis_norm_legs, A_legs))
print(bcolors.HEADER + "Evaluation FACE:  " + bcolors.ENDC,
      evaluateError_face(max_euclDis_norm_face, sum_max_euclDis_norm_face, A_face))

print("")

print(bcolors.OKBLUE + "Evaluation MSE TORSO: " + bcolors.ENDC, evaluateMSE(secondary_torso, modelTransform_torso))
print(bcolors.OKBLUE + "Evaluation MSE LEGS: " + bcolors.ENDC, evaluateMSE(secondary_legs, modelTransform_legs))
plt.show()
