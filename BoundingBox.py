from mathutils import Vector
import math

class BBox:
	def __init__(self, obj):
		xMax = -math.inf
		yMax = -math.inf
		zMax = -math.inf

		xMin = math.inf
		yMin = math.inf
		zMin = math.inf

		self.mx = obj.matrix_world

		for b in obj.bound_box:
			xMax = max(xMax, b[0])
			yMax = max(yMax, b[1])
			zMax = max(zMax, b[2])

			xMin = min(xMin, b[0])
			yMin = min(yMin, b[1])
			zMin = min(zMin, b[2])

		self.mini = self.mx * Vector(xMin, yMin, zMin)
		self.maxi = self.mx * Vector(xMax, yMax, zMax)

class BoundingBox:
	def __init__(self, lst=[]):
		xMin = 9999999999999999999999
		xMax = -9999999999999999999999
		yMin = 9999999999999999999999
		yMax = -9999999999999999999999
		zMin = 9999999999999999999999
		zMax = -9999999999999999999999

		#Obtain bounding box in an object's local space
		for ob in lst:
			for b in ob.bound_box:
				mat = ob.matrix_world
				#loc, rot, scale = ob.matrix_world.decompose();

				globalPos = lambda i: (mat*Vector(b))[i]

				if xMax is None or (globalPos(0) > xMax):
					xMax = globalPos(0)
				if xMin is None or (globalPos(0) < xMin):
					xMin = globalPos(0)

				if yMax is None or (globalPos(1) > yMax) :
					yMax = globalPos(1)
				if yMin is None or (globalPos(1) < yMin):
					yMin = globalPos(1)

				if zMax is None or (globalPos(2) > zMax):
					zMax = globalPos(2)
				if zMin is None or (globalPos(2) < zMin):
					zMin = globalPos(2)

		xMid = (xMin + xMax)/2
		yMid = (yMin + yMax)/2
		zMid = (zMin + zMax)/2

		self.minimum = (xMin, yMin, zMin)
		self.maximum = (xMax, yMax, zMax)
		self.midpoint = (xMid, yMid, zMid)
		print(self.midpoint)

	def getAxisLength(self, ax):
		return self.maximum[ax] - self.minimum[ax]