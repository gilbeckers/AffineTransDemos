import readOpenPoseJson
import calcEucldError

def calc_match(modelFoto, inputFoto):
    # 2D array. Elke entry is een coordinatenkoppel(joint-point) in 3D , z-coordinaat wordt nul gekozen want we werken in 2D
    # Bevat 18 coordinatenkoppels want openpose returnt 18 joint-points
    primary = readOpenPoseJson.readJsonFile('json_data/' + modelFoto + '.json')
    secondary = readOpenPoseJson.readJsonFile('json_data/' + inputFoto + '.json')

    #parameters van functie zijn slecht gekozen => secondary = input  &&   primary = model
    result = calcEucldError.norm_cte(secondary, primary)

    return result


def calc_final_match(modelFoto, inputFoto):
    primary = readOpenPoseJson.readJsonFile('json_data/' + modelFoto + '.json')
    secondary = readOpenPoseJson.readJsonFile('json_data/' + inputFoto + '.json')

    #parameters van functie zijn slecht gekozen => secondary = input  &&   primary = model
    result = calcEucldError.norm_cte_decide_match_or_not(secondary, primary)

    print("Match or not: ", result)
    return result

#calc_match("1", "24")
#print("---")
#calc_final_match("pose4", "pose4_fout")



