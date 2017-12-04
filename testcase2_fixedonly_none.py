# https://stackoverflow.com/questions/20546182/how-to-perform-coordinates-affine-transformation-using-python-part-2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import readOpenPoseJson
import calcTransformationMatrix
import util



def doCalc(modelFoto, inputFoto):
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

    primary_fixed_points = np.vstack([primary[0:3], primary[5], primary[8], primary[11]])
    secondary_fixed_points = np.vstack([secondary[0:3], secondary[5], secondary[8], secondary[11]])

    (modelTransform_fixed_points, A_fixed_points) = calcTransformationMatrix.calcTransformationMatrix_fixed_points(secondary_fixed_points, primary_fixed_points, secondary)
    plot = False
    if plot:
        f, (ax1, ax2, ax4) = plt.subplots(1, 3, sharey=True, figsize=(14, 6))
        implot = ax1.imshow(im_model)
        ax1.set_title(modelFoto + '(model)')
        ax1.plot(*zip(*primary), marker='o', color='r', ls='', label='model', ms=markersize)  # ms = markersize
        ax1.plot(*zip(*primary_fixed_points), marker='o', color='g', ls='', label='model', ms=markersize)  # ms = markersize
        red_patch = mpatches.Patch(color='red', label='model')
        ax1.legend(handles=[red_patch])

        ax2.set_title(inputFoto)
        ax2.imshow(im_input)
        ax2.plot(*zip(*secondary), marker='o', color='b', ls='', ms=markersize)
        ax2.legend(handles=[mpatches.Patch(color='blue', label='input')])

        ax4.set_title('Transformatie + model')
        ax4.imshow(im_model)
        ax4.plot(*zip(*primary), marker='o', color='b', ls='', ms=markersize)
        ax4.plot(*zip(*modelTransform_fixed_points), marker='o', color='cyan', ls='', ms=markersize)
        plt.draw()
        plt.show()



    # Gewoon  MAX[  xi-x'i  en  yi-y'i ]
    maxError = np.abs(primary - modelTransform_fixed_points)
    # np.sqrt(np.sum((maxError[:,0] - maxError[:,1]) ** 2))
    euclDis = ((maxError[:, 0]) ** 2 + maxError[:, 1] ** 2) ** 0.5
    euclDisNorm = ((maxError[:, 0] / resolutieX_model) ** 2 + (maxError[:, 1] / resolutieY_model) ** 2) ** 0.5

    max_euclDis = max(euclDis)
    sum_max_euclDis= np.sum(euclDis)
    return [max_euclDis, sum_max_euclDis]

doCalc("foto4", "foto1")