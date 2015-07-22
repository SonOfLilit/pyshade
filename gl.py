from math import sin, cos

class vec3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, a):
        return vec3(a * self.x, a * self.y, a * self.z)
    __rmul__ = __mul__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__, self.x, self.y, self.z)

class vec4(object):
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __add__(self, other):
        return vec4(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other):
        return vec4(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

    def __mul__(self, a):
        return vec4(a * self.x, a * self.y, a * self.z, a * self.w)
    __rmul__ = __mul__


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __repr__(self):
        return '%s(%s, %s, %s, %s)' % (self.__class__.__name__, self.x, self.y, self.z, self.w)
