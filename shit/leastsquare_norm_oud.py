#https://stackoverflow.com/questions/20546182/how-to-perform-coordinates-affine-transformation-using-python-part-2

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import readOpenPoseJson

resolutieX = 1440
resolutieY = 1920
modelFoto = "foto2"
inputFoto = "foto1_rendered"


#2D array. Elke entry is een coordinatenkoppel(joint-point) in 3D , z-coordinaat wordt nul gekozen want we werken in 2D
#Voorbeeld;
# primary = np.array([[11,4,0],
#                     [18,7,0],
#                     [3,11,0],
#                     [11, 11, 0],
#                     [12, 19, 0],
#                     [17, 26, 0],
#                     [5, 26, 0]])
#Bevat 18 coordinatenkoppels want openpose returnt 18 joint-points
primary = readOpenPoseJson.readJsonFile(modelFoto + '.json')


secondary = readOpenPoseJson.readJsonFile(inputFoto + '.json')
# secondary = np.array([[35,3,0],
#                     [46,20,0],
#                     [22,13,0],
#                     [35, 13, 0],
#                     [35, 24, 0],
#                     [43,34, 0],
#                     [26, 35, 0]])

#Zoek 2D affine transformatie matrix om scaling, rotatatie en translatie te beschrijven tussen model en input
#2x2 matrix werkt niet voor translaties
# Pad the data with ones, so that our transformation can do translations too
n = primary.shape[0]
pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))]) #horizontaal stacken
unpad = lambda x: x[:,:-1]

#padden:
#naar vorm [ x x 0 1]
X = pad(primary)
Y = pad(secondary)

print(X)
print(Y)

# Solve the least squares problem X * A = Y
# to find our transformation matrix A
A, res, rank, s = np.linalg.lstsq(X, Y)

transform = lambda x: unpad(np.dot(pad(x), A))
modelTransform = transform(primary)

A[np.abs(A) < 1e-10] = 0 # set really small values to zero
print("A:")
print(A)
print("Target:")
print(secondary)
print("Result:")
print(modelTransform)

##### normalize ####
print('#sec norm##')
l2norm = np.sqrt((secondary * secondary).sum(axis=1))
print(l2norm)

Secondary_genormd = secondary / l2norm.reshape(18,1)
print(Secondary_genormd)

print('modeltran norm:')
Modeltrans_genormd = modelTransform / (np.sqrt((modelTransform* modelTransform).sum(axis=1))).reshape(18,1)
print(Modeltrans_genormd)
####



maxError = np.abs(secondary - modelTransform)
print("Max error:", maxError.max())
print(maxError)

#np.sqrt(np.sum((maxError[:,0] - maxError[:,1]) ** 2))
euclDis = (maxError[:,0]**2 + maxError[:,1]**2)**0.5

#Euclidean distance boven gwn coordinaten verschil want eucl dis is ne cirkel
print("euclidean dis: ", euclDis)
print("Max euclidean dis: ", max(euclDis))


VerschilNorm = Secondary_genormd - Modeltrans_genormd
print("verschilnorm:")
print(np.abs(VerschilNorm))
NormEuclDis = (VerschilNorm[:,0]**2 + VerschilNorm[:,1]**2)**0.5
print("Norm Eucl dis")
print(NormEuclDis)
print(max(NormEuclDis))

#Plot secun
plt.figure()
plt.title("normSecun")
plt.axis([0, 1, 0, 1])
ax=plt.gca()                            # get the axis
ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis
ax.xaxis.tick_top()                     # and move the X-Axis
#ax.yaxis.set_ticks(np.arange(0, 16, 1)) # set y-ticks
ax.yaxis.tick_left()                    # remove right y-Ticks
modelplot = plt.plot(*zip(*Secondary_genormd), marker='o', color='r', ls='', label='model')

#Plot norm ModelTrans
plt.figure()
plt.title("norm model trans")
plt.axis([0, 1, 0, 1])
ax=plt.gca()                            # get the axis
ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis
ax.xaxis.tick_top()                     # and move the X-Axis
#ax.yaxis.set_ticks(np.arange(0, 16, 1)) # set y-ticks
ax.yaxis.tick_left()                    # remove right y-Ticks
modelplot = plt.plot(*zip(*Modeltrans_genormd), marker='o', color='r', ls='', label='model')


plt.figure()
plt.title(modelFoto)
plt.axis([0, resolutieX, 0, resolutieY])
ax=plt.gca()                            # get the axis
ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis
ax.xaxis.tick_top()                     # and move the X-Axis
#ax.yaxis.set_ticks(np.arange(0, 16, 1)) # set y-ticks
ax.yaxis.tick_left()                    # remove right y-Ticks



modelplot = plt.plot(*zip(*primary), marker='o', color='r', ls='', label='model')
red_patch = mpatches.Patch(color='red', label='Model')
plt.legend(handles=[red_patch])


plt.figure()
plt.title(inputFoto)
plt.axis([0, resolutieX, 0, resolutieY])
ax=plt.gca()                            # get the axis
ax.set_ylim(ax.get_ylim()[::-1])        # invert the axis
ax.xaxis.tick_top()                     # and move the X-Axis
#ax.yaxis.set_ticks(np.arange(0, 16, 1)) # set y-ticks
ax.yaxis.tick_left()                    # remove right y-Ticks

plt.plot(*zip(*secondary), marker='o', color='b', ls='')
plt.plot(*zip(*modelTransform), marker='o', color='g', ls='')

plt.legend(handles=[mpatches.Patch(color='blue', label='Input foto'), mpatches.Patch(color='green', label='Transformatie van model')])
plt.show()
