"""3D Turtle implementation for use in tree generation module, also extends
Blender Vector class with some useful methods"""

import math
import random

import mathutils
from mathutils import Quaternion


class Vector(mathutils.Vector):
    """Extension of the standard Vector class with some useful methods"""

    @staticmethod
    def random():
        """Normalised vector containing random entries in all dimensions"""
        vec = Vector([random.random(), random.random(), random.random()])
        vec.normalize()
        return vec

    def rotated(self, rotation):
        vec = self.copy()
        vec.rotate(rotation)
        return vec

    def declination(self):
        """Calculate declination of vector in degrees"""
        return math.degrees(math.atan2(math.sqrt(self.x ** 2 + self.y ** 2), self.z))


class CHTurtle(object):
    """3D turtle implementation for use in both L-Systems and Parametric tree
    generation schemes"""
    dir = Vector([0.0, 0.0, 1.0])
    pos = Vector([0.0, 0.0, 0.0])
    right = Vector([1.0, 0.0, 0.0])
    width = 0.0

    def __init__(self, other=None):
        """Copy Constructor"""
        if other is not None:
            self.dir = other.dir.copy()
            self.pos = other.pos.copy()
            self.right = other.right.copy()
            self.width = other.width

    def __str__(self):
        return 'Turtle at %s, direction %s, right %s' % (self.pos, self.dir, self.right)

    def turn_right(self, angle):
        """Turn the turtle right about the axis perpendicular to the direction
        it is facing"""
        axis = (self.dir.cross(self.right))
        axis.normalize()
        self.dir.rotate(Quaternion(axis, math.radians(angle)))
        self.dir.normalize()
        self.right.rotate(Quaternion(axis, math.radians(angle)))
        self.right.normalize()

    def turn_left(self, angle):
        """Turn the turtle left about the axis perpendicular to the direction it
        is facing"""
        self.turn_right(-angle)

    def pitch_up(self, angle):
        """Pitch the turtle up about the right axis"""
        self.dir.rotate(Quaternion(self.right, math.radians(angle)))
        self.dir.normalize()

    def pitch_down(self, angle):
        """Pitch the turtle down about the right axis"""
        self.pitch_up(-angle)

    def roll_right(self, angle):
        """Roll the turtle right about the direction it is facing"""
        self.right.rotate(Quaternion(self.dir, math.radians(angle)))
        self.right.normalize()

    def roll_left(self, angle):
        """Roll the turtle left about the direction it is facing"""
        self.roll_right(-angle)

    def move(self, distance):
        """Move the turtle in the direction it is facing by specified distance"""
        self.pos += self.dir * distance

    def set_width(self, width):
        """Set the width stored by the turtle"""
        self.width = width
