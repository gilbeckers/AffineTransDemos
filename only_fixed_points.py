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
    if (max_error >= 80 or sum_error >= 140):
        return bcolors.FAIL + "no_match" + bcolors.ENDC + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
    # Zeker juist, wel een match
    elif (max_error <= 75 or sum_error <= 110):
        rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
        rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
        if (max([rotation_1, rotation_2]) > 30):
            return bcolors.WARNING + "match, but rotation to high: " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
        else:
            return bcolors.OKGREEN + "match! " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
    else:
        return "no_conclusion" + "  max_error: " + str(max_error) + "   sum: " + str(sum_error)
def evaluateError_face(max_error, sum_error, transformation_matrix):
    # Zeker fout, geen match
    if (max_error >= 80 or sum_error >= 180):
        return bcolors.FAIL + "no_match  max_error: " + bcolors.ENDC + str(max_error) + "   sum: " + str(sum_error)
    # Zeker juist, wel een match
    elif (max_error <= 50 or sum_error <= 100):
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


modelFoto = "foto1"  # "foto3"
inputFoto = "midget1"  # "foto1"

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

primary_fixed_points = np.vstack([primary[1:3], primary[5], primary[8], primary[11]])
secondary_fixed_points = np.vstack([secondary[1:3], secondary[5], secondary[8], secondary[11]])

(modelTransform_fixed_points, A_fixed_points) = calcTransformationMatrix.calcTransformationMatrix_fixed_points(secondary_fixed_points, primary_fixed_points, secondary)


# Gewoon  MAX[  xi-x'i  en  yi-y'i ]
maxError = np.abs(primary - modelTransform_fixed_points)
print("Max error torso:", maxError.max())

# np.sqrt(np.sum((maxError[:,0] - maxError[:,1]) ** 2))
euclDis = ((maxError[:, 0]) ** 2 + maxError[:, 1] ** 2) ** 0.5
euclDisNorm = ((maxError[:, 0] / resolutieX_model) ** 2 + (maxError[:, 1] / resolutieY_model) ** 2) ** 0.5
print("@@@@@Eucl dis TORSO: ", euclDis)

max_euclDis = max(euclDis)
sum_max_euclDis= np.sum(euclDis)

# plot img

f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=True, figsize=(14, 6))
implot = ax1.imshow(im_model)
ax1.set_title(modelFoto + '(model)')
ax1.plot(*zip(*primary), marker='o', color='r', ls='', label='model', ms=markersize)  # ms = markersize
ax1.plot(*zip(*primary_fixed_points), marker='o', color='c', ls='', label='model', ms=markersize)  # ms = markersize
red_patch = mpatches.Patch(color='red', label='model')
ax1.legend(handles=[red_patch])

ax2.set_title(inputFoto)
ax2.imshow(im_input)
ax2.plot(*zip(*secondary), marker='o', color='b', ls='', ms=markersize)
ax2.plot(*zip(*secondary_fixed_points), marker='o', color='r', ls='', ms=markersize)
ax2.legend(handles=[mpatches.Patch(color='blue', label='input')])

ax3.set_title('Transformation of input')
ax3.imshow(im_model)
ax3.plot(*zip(*modelTransform_fixed_points), marker='o', color='y', ls='', ms=markersize)
ax3.legend(handles=[mpatches.Patch(color='yellow', label='Transformation of model')])

ax4.set_title('Transformatie + model')
ax4.imshow(im_model)
ax4.plot(*zip(*primary), marker='o', color='b', ls='', ms=markersize)
ax4.plot(*zip(*modelTransform_fixed_points), marker='o', color='y', ls='', ms=markersize)

print(bcolors.HEADER + "Evaluation BODY: " + bcolors.ENDC,
      evaluateError(max_euclDis, sum_max_euclDis, A_fixed_points))


plt.show()
