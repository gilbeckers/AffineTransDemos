from shit import leastsquare_resol

(max_euclDis, max_euclDis_norm, sum_euclDis_norm) = leastsquare_resol.matchPose("foto5", "foto7")


print("error: " , max_euclDis)