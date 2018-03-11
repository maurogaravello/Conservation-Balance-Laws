#!/usr/bin/env python

#######################################
# LaxFr.py
#
# Functions implementig the Lax-Friedrichs
# method (only the convective step)
# for the numerical simulation
#
# u_i^{n+1} = 1/2 (u_{i+1}^n - u_{i-1}^n)
#           - 1/2 (dt/dx) [f(u_{i+1}^n) - f(u_{i-1}^n)]
#
#######################################

import numpy

### C_step: Convective step
def C_step(u, u_boundary, f, dt_dx):
    """
    :param u: numpy array with two ghost cells for the initial state
    :param u_boundary: tuple (ul, ur) giving the density boundary condition
                       ul = 'f' -> free flow (otherwise a scalar)
                       ur = 'f' -> free flow (otherwise a scalar)
    :param f: flux class ...numpy vector of the same size of u 
    :param dt_dx: scalar giving dt/dx
    """
    
    (ul, ur) = u_boundary
    flow = f.flux(u)
    unew = numpy.array([0.])
     
    unew = numpy.append(unew,
                        0.5 * (u[:-2] + u[2:] + (dt_dx) * (flow[:-2] - flow[2:])))

    if ul == 'f':
        unew[0] = 2. * unew[1] - unew[2]
    else:
        unew[0] = ul

    if ur == 'f':
        unew = numpy.append(unew, 2. * unew[-1] - unew[-2])
    else:
        unew = numpy.append(unew, [ur])
            
    return unew

