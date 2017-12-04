import normalising
import numpy as np
import calcTransformationMatrix

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
    if (max_error >= 0.057 or sum_error >= 0.21):
        return bcolors.FAIL + "no_match" + bcolors.ENDC + "  max_error: " + str(max_error) + " (" + str((1-(max_error/0.15)) *100 ) + "%) " + "   sum: " + str(sum_error)
    # Zeker juist, wel een match
    elif (max_error <= 0.052 or sum_error <= 0.17):
        rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
        rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
        if (max([rotation_1, rotation_2]) > 20):
            return bcolors.WARNING + "match, but rotation to high: " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + " (" + str( (1-(max_error/0.15)) *100 ) + "%) " + "   sum: " + str(sum_error)
        else:
            return bcolors.OKGREEN + "match! " + bcolors.ENDC + str(rotation_1) + " " + str(
                rotation_2) + "  max_error: " + str(max_error) + " (" + str((1-(max_error/0.15)) *100 ) + "%) " + "   sum: " + str(sum_error)
    else:
        return "no_conclusion" + "  max_error: " + str(max_error) + " (" + str((1-(max_error/0.15)) *100 ) + "%) " + "   sum: " + str(sum_error)


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

#Geeft final boolean terug= heel part (torso, legs of face) is match of geen match
#Geeft final boolean terug= heel part (torso, legs of face) is match of geen match
def evaluate_error_decide(max_error, sum_error, transformation_matrix, eucld_tresh, rotation_tresh):
    rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
    rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
    rot_max = max(rotation_2, rotation_1)

    print("max ecul: " , max_error)
    print("max rota: " , rot_max)
    # Zeker juist, dus match
    if (max_error <= eucld_tresh and rot_max <= rotation_tresh):
        return True

    #Geen match
    return False

#Geeft final boolean terug= heel part (torso, legs of face) is match of geen match
#Geeft final boolean terug= heel part (torso, legs of face) is match of geen match
def evaluate_error_decide_schouders_incl(max_error, transformation_matrix, eucld_tresh, rotation_tresh, max_schouders, schouder_tresh):
    rotation_1 = np.abs(np.math.atan2(-transformation_matrix[0][1], transformation_matrix[0][0]) * 57.3)
    rotation_2 = np.abs(np.math.atan2(transformation_matrix[1][0], transformation_matrix[1][1]) * 57.3)
    rot_max = max(rotation_2, rotation_1)

    print("max ecul torso: " , max_error)
    print("max rota torso: " , rot_max)
    print("max schouders: ", max_schouders)
    # Zeker juist, dus match
    if (max_error <= eucld_tresh and rot_max <= rotation_tresh):

        #Checken of schouders niet te veel afwijken
        if(max_schouders<schouder_tresh):
            return True
        else:
            print("!!!!!Schouder error te groot!!!!")

    #Geen match
    return False


def norm_cte(model, input):

    #Crop/cut => delen door Xmax & Ymax
    model = normalising.normalise_cte(model)
    input = normalising.normalise_cte(input)

    primary_torso = model[2:8]
    secondary_torso = input[2:8]
    primary_legs = model[8:14]
    secondary_legs = input[8:14]
    primary_face = np.vstack([model[0], model[14:18]])
    secondary_face = np.vstack([input[0], input[14:18]])

    (modelTransform_torso, A_torso) = calcTransformationMatrix.calcTransformationMatrix(primary_torso, secondary_torso)
    (modelTransform_legs, A_legs) = calcTransformationMatrix.calcTransformationMatrix(primary_legs, secondary_legs)
    (modelTransform_face, A_face) = calcTransformationMatrix.calcTransformationMatrix(primary_face, secondary_face)

    # Gewoon  MAX[  xi-x'i  en  yi-y'i ]
    maxError_torso = np.abs(secondary_torso - modelTransform_torso)
    maxError_legs = np.abs(secondary_legs - modelTransform_legs)
    maxError_face = np.abs(secondary_face - modelTransform_face)

    euclDis_torso = ((maxError_torso[:, 0]) ** 2 + maxError_torso[:, 1] ** 2) ** 0.5
    euclDis_legs = ((maxError_legs[:, 0]) ** 2 + maxError_legs[:, 1] ** 2) ** 0.5
    euclDis_face = ((maxError_face[:, 0]) ** 2 + maxError_face[:, 1] ** 2) ** 0.5

    max_euclDis_torso = max(euclDis_torso)
    sum_euclDis_torso = np.sum(euclDis_torso)
    #print("\n----- Euclidean dis genormaliseeerd  TORSO -----")
    #print("euclid dis NORM; ", euclDis_torso)
    #print("Max euclidean dis norm resolutie: ", max_euclDis_torso)
    #print("Sum euclidean dis: ", sum_max_euclDis_torso)

    max_euclDis_legs = max(euclDis_legs)
    sum_euclDis_legs = np.sum(euclDis_legs)
    #print("\n----- Euclidean dis genormaliseeerd  LEGS -----")
    #print("euclid dis NORM; ", euclDis_legs)
    #print("Max euclidean dis norm resolutie: ", max_euclDis_legs)
    #print("Sum euclidean dis: ", sum_max_euclDis_legs)

    max_euclDis_face = max(euclDis_face)
    sum_euclDis_face = np.sum(euclDis_face)
    #print("\n----- Euclidean dis genormaliseeerd  FACE -----")
    #print("euclid dis NORM; ", euclDis_face)
    #print("Max euclidean dis norm resolutie: ", max_euclDis_face)
    #print("Sum euclidean dis: ", sum_max_euclDis_face)

    # Evaluate errors => decide match or not
    #print(bcolors.HEADER + "Evaluation TORSO: " + bcolors.ENDC,
    #      evaluateError(max_euclDis_torso, sum_max_euclDis_torso, A_torso))
    #print(bcolors.HEADER + "Evaluation LEGS:  " + bcolors.ENDC,
    #          evaluateError(max_euclDis_legs, sum_max_euclDis_legs, A_legs))
    #print(bcolors.HEADER + "Evaluation FACE:  " + bcolors.ENDC,
    #      evaluateError_face(max_euclDis_face, sum_max_euclDis_face, A_face))

    #Rotatie
    rotation_1_torso = np.abs(np.math.atan2(-A_torso[0][1], A_torso[0][0]) * 57.3)
    rotation_2_torso = np.abs(np.math.atan2(A_torso[1][0], A_torso[1][1]) * 57.3)
    rotation_1_legs = np.abs(np.math.atan2(-A_legs[0][1], A_legs[0][0]) * 57.3)
    rotation_2_legs = np.abs(np.math.atan2(A_legs[1][0], A_legs[1][1]) * 57.3)
    rotation_1_face = np.abs(np.math.atan2(-A_face[0][1], A_face[0][0]) * 57.3)
    rotation_2_face = np.abs(np.math.atan2(A_face[1][0], A_face[1][1]) * 57.3)


    #Maak array met errors in
    #Eerst face dan torso dan legs
    #result = [[max_euclDis_face, sum_max_euclDis_face], [max_euclDis_torso, sum_max_euclDis_torso], [max_euclDis_legs, sum_max_euclDis_legs]]

    result = [[max_euclDis_face, max(rotation_1_face, rotation_2_face), sum_euclDis_face], [max_euclDis_torso, max(rotation_1_torso, rotation_2_torso), sum_euclDis_torso],
              [max_euclDis_legs, max(rotation_1_legs, rotation_2_legs), sum_euclDis_legs]]
    return result

def norm_cte_decide_match_or_not(model, input):

    #print("moooodel  " , model)

    #Crop/cut => delen door Xmax & Ymax
    model = normalising.normalise_cte(model)
    input = normalising.normalise_cte(input)

    #print("mooo: " , model)

    primary_torso = model[2:8]
    secondary_torso = input[2:8]
    primary_legs = model[8:14]
    secondary_legs = input[8:14]
    primary_face = np.vstack([model[0], model[14:18]])
    secondary_face = np.vstack([input[0], input[14:18]])

    (modelTransform_torso, A_torso) = calcTransformationMatrix.calcTransformationMatrix(primary_torso, secondary_torso)
    (modelTransform_legs, A_legs) = calcTransformationMatrix.calcTransformationMatrix(primary_legs, secondary_legs)
    (modelTransform_face, A_face) = calcTransformationMatrix.calcTransformationMatrix(primary_face, secondary_face)

    #print("input trans: " , modelTransform_torso)
    #print("aaaa:  ", A_torso)
    # Gewoon  MAX[  xi-x'i  en  yi-y'i ]
    maxError_torso = np.abs(secondary_torso - modelTransform_torso)
    maxError_legs = np.abs(secondary_legs - modelTransform_legs)
    maxError_face = np.abs(secondary_face - modelTransform_face)

    #print("maaax error tors; " , maxError_torso)

    euclDis_torso = ((maxError_torso[:, 0]) ** 2 + maxError_torso[:, 1] ** 2) ** 0.5
    euclDis_legs = ((maxError_legs[:, 0]) ** 2 + maxError_legs[:, 1] ** 2) ** 0.5
    euclDis_face = ((maxError_face[:, 0]) ** 2 + maxError_face[:, 1] ** 2) ** 0.5

    maxError_shouder = max([euclDis_torso[0], euclDis_torso[3]])

    print("Error schouder: " , maxError_shouder)
    print("Error torso: ", euclDis_torso)

    max_euclDis_torso = max(euclDis_torso)
    sum_max_euclDis_torso = np.sum(euclDis_torso)

    max_euclDis_legs = max(euclDis_legs)
    sum_max_euclDis_legs = np.sum(euclDis_legs)

    max_euclDis_face = max(euclDis_face)
    sum_max_euclDis_face = np.sum(euclDis_face)

    euclDis_tresh_torso = 0.05
    rotation_tresh_torso = 18
    euclDis_tresh_legs = 0.0395
    rotation_tresh_legs = 14

    schouder_tresh = 0.035

    #Return final match: alle delen moeten True geven ZONDER SCHOUDERS
    #return evaluate_error_decide(max_euclDis_torso, sum_max_euclDis_torso, A_torso, euclDis_tresh_torso, rotation_tresh_torso) and evaluate_error_decide(max_euclDis_legs, sum_max_euclDis_legs, A_legs, euclDis_tresh_legs, rotation_tresh_legs)

    #Met schouders
    return evaluate_error_decide_schouders_incl(max_euclDis_torso, A_torso, euclDis_tresh_torso,
                                 rotation_tresh_torso, maxError_shouder, schouder_tresh ) and evaluate_error_decide(max_euclDis_legs, sum_max_euclDis_legs,
                                                                                 A_legs, euclDis_tresh_legs,
                                                                                 rotation_tresh_legs)
