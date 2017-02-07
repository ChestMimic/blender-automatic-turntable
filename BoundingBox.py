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

		self.mini = self.mx * Vector((xMin, yMin, zMin))
		print("Min: " + str(self.mini))
		self.maxi = self.mx * Vector((xMax, yMax, zMax))
		print("Max: " + str(self.maxi))

class BoundingBox:
	def __init__(self, lst=[]):
		xMax = -math.inf
		yMax = -math.inf
		zMax = -math.inf

		xMin = math.inf
		yMin = math.inf
		zMin = math.inf

		boxen = []
		#Obtain bounding box in an object's local space
		for ob in lst:
			boxen.append(BBox(ob))

		for b in boxen:
			xMax = max(xMax, b.maxi[0])
			yMax = max(yMax, b.maxi[1])
			zMax = max(zMax, b.maxi[2])

			xMin = min(xMin, b.mini[0])
			yMin = min(yMin, b.mini[1])
			zMin = min(zMin, b.mini[2])

		xMid = (xMin + xMax)/2
		yMid = (yMin + yMax)/2
		zMid = (zMin + zMax)/2

		self.minimum = (xMin, yMin, zMin)
		self.maximum = (xMax, yMax, zMax)
		self.midpoint = (xMid, yMid, zMid)
		print(self.midpoint)

	def getAxisLength(self, ax):
		return self.maximum[ax] - self.minimum[ax]