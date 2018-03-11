#!/usr/bin/env python

#######################################
# Godunov.py
#
# Functions implementig the Godunov
# method (only the convective step)
# for the numerical simulation in
# case of a concave flux
#
# u_i^{n+1} = u_i^n - (dt/dx) [F^n_{i+1/2} - F^n_{i-1/2}]
#
#######################################

import numpy


def trace(a, b, flux):
    """
    This function calculates the trace at interfaces.
    It is fundamental that the
    flux is strictly concave.
    
    It returns a couple, corresponding to the left and right
    traces at the interface.

    :param a: scalar. Left density.
    :param b: scalar. Right density.
    :param flux: flux class
    """
    if a < b and flux.flux(a) < flux.flux(b): # shock positive speed
        return (a,a)

    if a < b and flux.flux(a) > flux.flux(b): # shock negative speed
        return (b,b)

    if a < b and flux.flux(a) == flux.flux(b): # stationary shock
        return (a,b)

    if a == b: # no discontinuity
        return (a,b)

    if a < flux.theta: # rarefaction positive speed
        return (a,a)

    if b > flux.theta: # rarefaction negative speed
        return (b,b)

    return (flux.theta, flux.theta) 



def Godunov_Flux(u, f):
    """
    This function calculates the Godunov flux. It returns
    a numpy array given the Godunov flux. This numpy array has size
    equal to the size of u minus 1. It is fundamental that the
    flux is strictly concave.

    :param u: numpy array with two ghost cells. Density of the state
    :param f: flux class
  
    """

    f1 = f.flux(u)
    mask_sh_pos = (u[:-1] <= u[1:]) & (f1[:-1] <= f1[1:])
    mask_sh_neg = (u[:-1] <= u[1:]) & (f1[:-1] > f1[1:])

    mask_rar_neg = (u[:-1] > u[1:]) & (u[1:] >= f.theta)
    mask_rar_pos = (u[:-1] > u[1:]) & (u[:-1] <= f.theta)

    mask_pos = mask_sh_pos | mask_rar_pos
    mask_neg = mask_sh_neg | mask_rar_neg
    
    mask_theta = numpy.logical_not(mask_pos | mask_neg)

    return mask_theta * f.maximum + mask_pos * f1[:-1] + \
           mask_neg * f1[1:]

    
    

### C_step: Convective step
def C_step(u, u_boundary, f, dt_dx):
    """
    :param u: numpy array with two ghost cells for the initial state
    :param u_boundary: tuple (ul, ur) giving the density boundary condition
                       ul = 'f' -> free flow (otherwise a scalar)
                       ur = 'f' -> free flow (otherwise a scalar)
    :param f: flux class
    :param dt_dx: scalar giving dt/dx
    """
    
    (ul, ur) = u_boundary

    # adding two cells to u
    u_aug = numpy.append(numpy.array([0.]), numpy.append(u, [0.]))

    # assigning boundary data
    if ul == 'f':
        u_aug[0] = min(1., u_aug[1])
    else:
        u_aug[0] = ul

    if ur == 'f':
        u_aug[-1] = max(0., u_aug[-2])
    else:
        u_aug[-1] = ur

    # calculate Godunov flux
    flow = Godunov_Flux(u_aug, f)


    # unew = numpy.array([0.])
     
    # unew = numpy.append(unew,
    #                     u[1:-1] - (dt_dx) * (flow[1:] - flow[:-1]))

    unew = u_aug[1:-1] - (dt_dx) * (flow[1:] - flow[:-1])

           
    return unew

