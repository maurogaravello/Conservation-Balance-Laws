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

        # Method for integrating
        self.method = None

    #
    # Method for creating the numerical domain
    #
    def create_domain(self, start, end, points):
        """
        This function creates the grid for the domain of integration. It works
        only in the case of 1 or 2 dimensions

        param start: tuple. Start point for the domain.
        param end: tuple. End point for the domain.
        param points: tuple. Number of points for the numerical domain.

        output: tuple. 
                If dimension is one, then (self.x, self.dx, self.grid).
                If dimension is two, then (self.x, self.dx, self.y, self.dy, self.grid).


        Examples
        ========

 
        """

        assert len(start) == len(end) == len(points) == (1 or 2)
        assert isinstance(start, tuple) and isinstance(end, tuple) and isinstance(points, tuple)

        self.dimension = len(start)

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
    # Function for checking the domain is feasible.
    #
    def check_domain(self):
        if self.x_1 >= self.x_2:
            print('Error: x_1 should be less than x_2')
            logging.info('Error: x_1 should be less than x_2')
            exit()

        if self.y_1 >= self.y_2:
            print('Error: y_1 should be less than y_2')
            logging.info('Error: y_1 should be less than y_2')
            exit()

        if not isinstance(self.n_x, int) or not isinstance(self.n_y, int):
            print('Error: both n_x and n_y should be integers')
            logging.info('Error: both n_x and n_y should be integers')
            exit()

        if self.n_x == 0 or self.n_y == 0:
            print('Error: both n_x and n_y should be strictly positive')
            logging.info('Error: both n_x and n_y should be strictly positive')
            exit()

            

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

