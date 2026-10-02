from numpy import sqrt


class Vector:
    num_of_vectors = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

        Vector.num_of_vectors += 1

    def __add__(self, b):
        return Vector(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Vector(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return Vector(b * self.x, b * self.y)

    def __rmul__(self, b):
        return Vector(b * self.x, b * self.y)

    def __truediv__(self, b):
        if b != 0:
            return Vector(self.x / b, self.y / b)
        else:
            return Vector(self.x / 0.001, self.y / 0.001)

    def dot(self, b):
        return self.x * b.x + self.y * b.y

    def mag(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        return self / self.mag()

    def coords(self):
        coord = (self.x, self.y)
        return coord