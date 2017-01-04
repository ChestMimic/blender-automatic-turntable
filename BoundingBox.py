from mathutils import Vector

class BoundingBox:
	def __init__(self, lst=[], globalPos = (0.0,0.0,0.0)):
		xMin = None
		xMax = None
		yMin = None
		yMax = None
		zMin = None
		zMax = None

		#Obtain bounding box in an object's local space
		for ob in lst:
			for b in ob.bound_box:
				loc, rot, scale = ob.matrix_world.decompose();

				globalPos = lambda i: Vector(b)[i] + loc[i]

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