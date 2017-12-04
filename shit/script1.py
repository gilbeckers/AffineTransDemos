#https://stackoverflow.com/questions/8873462/how-to-perform-coordinates-affine-transformation-using-python?noredirect=1&lq=1
# => zonder least-square => geeft probleem hier omdat matrix niet inverteerbaar is ( nullen in 3e kolom)
import numpy as np

primary_system1 = (153,93,0)
primary_system2 = (414,91,0)
primary_system3 = (414,267,0)
primary_system4 = (153,267,0)

secondary_system1 = (74,327,0)
secondary_system2 = (561,327,0)
secondary_system3 = (561,567,0)
secondary_system4 = (74,567,0)


def solve_affine( p1, p2, p3, p4, s1, s2, s3, s4 ):
    x = np.transpose(np.matrix([p1,p2,p3,p4]))
    y = np.transpose(np.matrix([s1,s2,s3,s4]))
    # add ones on the bottom of x and y
    x = np.vstack((x,[1,1,1,1]))
    y = np.vstack((y,[1,1,1,1]))
    # solve for A2
    A2 = y * x.I
    print(A2)
    # return function that takes input x and transforms it
    # don't need to return the 4th row as it is
    return lambda x: (A2*np.vstack((np.matrix(x).reshape(3,1),1)))[0:3,:]

transformFn = solve_affine( primary_system1, primary_system2,
                            primary_system3, primary_system4,
                            secondary_system1, secondary_system2,
                            secondary_system3, secondary_system4 )


# test: transform primary_system1 and we should get secondary_system1
np.matrix(secondary_system1).T - transformFn( primary_system1 )
# np.linalg.norm of above is 0.02555