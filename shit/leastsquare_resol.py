# https://stackoverflow.com/questions/20546182/how-to-perform-coordinates-affine-transformation-using-python-part-2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import readOpenPoseJson
import calcTransformationMatrix
import util




def evaluateError(max_error, sum_error):
    #Zeker fout, geen match
    if(max_error>=0.09 or sum_error>=0.8):
        return "no_match"
    #Zeker juist, wel een match
    elif(max_error<=0.055 or sum_error<=0.37):
        return "match!"
    else: return "no_conclusion"



def matchPose(modelP, inputP):
    modelFoto = modelP  #"foto3"
    inputFoto = inputP  #"foto1"

    # plot vars
    markersize = 3

    im_model = plt.imread('Pictures/' + modelFoto + '.jpg')
    print("res: " , im_model.shape[0])
    # portrait foto, gsm jochen
    resolutieX_model = im_model.shape[1]  # 1440
    resolutieY_model = im_model.shape[0]  # 1920

    im_input = plt.imread('Pictures/' + inputFoto + '.jpg')
    # rendered foto
    resolutieX = im_input.shape[1]  # 1440 #1280
    resolutieY = im_input.shape[0]  # 1920 #720

    # 2D array. Elke entry is een coordinatenkoppel(joint-point) in 3D , z-coordinaat wordt nul gekozen want we werken in 2D
    # Voorbeeld;
    # primary = np.array([[11,4,0],
    #                     [18,7,0],
    #                     [3,11,0],
    #                     [11, 11, 0],
    #                     [12, 19, 0],
    #                     [17, 26, 0],
    #                     [5, 26, 0]])
    # Bevat 18 coordinatenkoppels want openpose returnt 18 joint-points
    primary = readOpenPoseJson.readJsonFile('json_data/' + modelFoto + '.json')

    secondary = readOpenPoseJson.readJsonFile('json_data/' + inputFoto + '.json')
    # secondary = np.array([[35,3,0],
    #                     [46,20,0],
    #                     [22,13,0],
    #                     [35, 13, 0],
    #                     [35, 24, 0],
    #                     [43,34, 0],
    #                     [26, 35, 0]])

    #FILTERING & STRIPPING OF UNDETECTED JOINTS
    #Check if all joints are detected. Undetected joints are undefinded (0,0)
    #Remove undetected joints from matrix
    for i in range(0,17):
        if i < secondary.shape[0]:
            if(secondary[i][0] == 0 and secondary[i][1] ==0):
                print("no_joint! ")
                secondary = np.delete(secondary, (i), axis=0)
                primary = np.delete(primary, (i), axis=0)
                i = i-1


    #enkel subarrays
    #primary = primary[8:14]
    #secondary = secondary[8:14]

    (modelTransform, A) = calcTransformationMatrix.calcTransformationMatrix(primary, secondary)

    print("A- transformatie matrix:")
    print(A)
    print("Input:")
    print(secondary)
    print("Result- transformatie van model:")
    print(modelTransform)

    #print("eerste kolom:")
    #print(modelTransform[:,0])

    #bereken correlatie tussen 2 matrixen
    print("###correlation: ")
    print(np.corrcoef(modelTransform[:,0]/resolutieX, secondary[:,0]/resolutieY))
    print(np.corrcoef(modelTransform[:, 1]/resolutieX, secondary[:, 1]/resolutieY))

    print("matric correlation: " )
    print(util.corr2_coeff(modelTransform, secondary).min())



    # Gewoon  MAX[  xi-x'i  en  yi-y'i ]
    maxError = np.abs(secondary - modelTransform)
    print("Max error:", maxError.max())
    # print(maxError)

    # np.sqrt(np.sum((maxError[:,0] - maxError[:,1]) ** 2))
    euclDis = ((maxError[:, 0]) ** 2 + maxError[:, 1] ** 2) ** 0.5
    euclDisNorm = ((maxError[:, 0] / resolutieX) ** 2 + (maxError[:, 1] / resolutieY) ** 2) ** 0.5

    # Euclidean distance boven gwn coordinaten verschil want eucl dis is ne cirkel
    # print("euclidean dis: ", euclDis)
    max_euclDis = max(euclDis)
    print("\n--------     Euclidean dis      -------")
    print("Max euclidean dis: ", max_euclDis)
    print("Body part: ", util.getBodyPartByIndex(np.argmax(euclDis, axis=None)))

    max_euclDis_norm = max(euclDisNorm)
    sum_max_euclDis_norm = np.sum(euclDisNorm)
    print("\n----- Euclidean dis genormaliseeerd -----")
    print("euclid dis NORM; ", euclDisNorm)
    print("Max euclidean dis norm resolutie: ", max_euclDis_norm)
    print("Sum euclidean dis: ", sum_max_euclDis_norm)
    print("Body part: ", util.getBodyPartByIndex(np.argmax(euclDisNorm, axis=None)))

    # plot img

    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, sharey=True, figsize=(14, 6))
    implot = ax1.imshow(im_model)
    ax1.set_title(modelFoto + '(model)')
    ax1.plot(*zip(*primary), marker='o', color='r', ls='', label='model', ms=markersize)  # ms = markersize
    red_patch = mpatches.Patch(color='red', label='model')
    ax1.legend(handles=[red_patch])

    ax2.set_title(inputFoto)
    ax2.imshow(im_input)
    ax2.plot(*zip(*secondary), marker='o', color='b', ls='', ms=markersize)
    ax2.legend(handles=[mpatches.Patch(color='blue', label='input')])

    ax3.set_title('Transformation of model')
    ax3.imshow(im_input)
    ax3.plot(*zip(*modelTransform), marker='o', color='y', ls='', ms=markersize)
    ax3.legend(handles=[mpatches.Patch(color='yellow', label='Transformation of model')])

    ax4.set_title('Transformatie + input')
    ax4.imshow(im_input)
    ax4.plot(*zip(*secondary), marker='o', color='b', ls='', ms=markersize)
    ax4.plot(*zip(*modelTransform), marker='o', color='y', ls='', ms=markersize)

    print("Evaluation poses: ", evaluateError(max_euclDis_norm, sum_max_euclDis_norm))
    plt.show()


    return (max_euclDis, max_euclDis_norm, sum_max_euclDis_norm);
