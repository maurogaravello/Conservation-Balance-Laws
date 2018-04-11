#################################################
# cbl.py
#
# Class for the integration of
# hyperbolic conservation and/or balance laws
#
#################################################

from __future__ import print_function, division
import numpy as np
import logging


# base class Cbl
class Cbl(object):
    def __init__(self):
        """
        Initializatium function for the class.

        """

        # domain
        self.x = None
        self.dx = None
        self.y = None
        self.dy = None
        self.dimension = None
        self.points = None

        # Initial density
        self.initial_density = None

        # Method for integrating the conservation law
        self.method = None

    #
    # Method for creating the numerical domain
    #
    def create_domain(self, start, end, points):
        """
        This function creates the grid for the domain of integration. It works
        only in the case of 1 or 2 dimensional domains.

        param start: tuple. Start point for the domain.
        param end: tuple. End point for the domain.
        param points: tuple. Number of points for the numerical domain.

        output: tuple. 
                If dimension is one, then (self.x, self.dx, self.grid).
                If dimension is two, then (self.x, self.dx, self.y, self.dy, self.grid).


        Examples
        ========

        >>> create_domain((0,), (1,), (100,))
        >>> create_domain((0,0), (1,2), (100,150))

 
        """

        _check_domain(start, end, points)

        self.dimension = len(start)
        self.points = points

        self.x, self.dx = np.linspace(start[0], end[0], points[0], retstep = True)

        if dimension == 1:
            self.grid = self.x
            return (self.x, self.dx, self.grid)

        # dimension is 2
        self.y, self.dy = np.linspace(start[1], end[1], points[1], retstep = True)
        self.grid = np.meshgrid(self.x, self.y)
        return (self.x, self.dx, self.y, self.dy, self.grid)


    #
    # Function for creating the intial datum
    #
    def create_initial_datum(self, InitialDatum_rho):
        """
        This function creates a 2d-arrays for the initial datum for the population.

        :param InitialDatum_rho: function. It gives the initial datum.

        It creates self.initial_density.
        """
        self.initial_density = InitialDatum_rho(self.grid)

    #
    # Function for setting the method for the integration
    #
    def set_numerical_method(self, **method):
        
        self.possible_methods = ['Godunov', 'Lax-Friedrics']
        lax_f = method.get('Lax-Friedrics', True)
        godunov = method.get('Godunov', None)
        # to be finished!!!!!!!!

    #
    # Function for creating the printing mesh
    #
    def create_print_mesh(self):
        """
        This function creates the print mesh.
        
        self.time = numpy vector starting from 0, ending to self.time_of_simulation
        self.dt = the time step

        """
        K = int(float(len(self.time))/self.pictures) + 1
        self.printing = np.zeros_like(self.time, dtype= bool)
        self.printing[::K] = True
        self.printing[-1] = True


#
# Function for checking the domain is feasible.
#
def _check_domain(start, end, points):

    try:
        assert len(start) == len(end) == len(points) == (1 or 2)
        assert isinstance(start, tuple) and isinstance(end, tuple) and isinstance(points, tuple)

    except: ### What error???
        print('Dimension error: start, end, points should be tuple of the same
        dimension. The dimension should be 1 or 2')
        logging.info('Dimension error: start, end, points should be tuple of the same
        dimension. The dimension should be 1 or 2')
        exit()

    dimension = len(points)
    for i in range(dimension):
        if start[i] >= end[i]:
            print('Error: wrong boundary data for the domain')
            logging.info('Error: wrong boundary data for the domain')
            exit()

        if not isinstance(points[i], int) or points[i] <= 1:
            print('Error: the number of points for the domain is not correct')
            logging.info('Error: the number of points for the domain is not correct')
            exit()
