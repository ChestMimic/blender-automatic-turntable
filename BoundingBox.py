from mathutils import Vector

class BoundingBox:
	def __init__(self, lst=[], globalPos = (0.0,0.0,0.0)):
		self.xMin = None
		self.xMax = None
		self.yMin = None
		self.yMax = None
		self.zMin = None
		self.zMax = None

		#Obtain bounding box in an object's local space
		for ob in lst:
			for b in ob.bound_box:
				print(ob.location)

				if self.xMax is None or ((Vector(b)[0] + ob.location[0]) > self.xMax):
					self.xMax = Vector(b)[0] + ob.location[0]
				if self.xMin is None or ((Vector(b)[0] + ob.location[0]) < self.xMin):
					self.xMin = Vector(b)[0] + ob.location[0]

				if self.yMax is None or ((Vector(b)[1] + ob.location[1]) > self.yMax) :
					self.yMax = Vector(b)[1] + ob.location[1]
				if self.yMin is None or ((Vector(b)[1] + ob.location[1]) < self.yMin):
					self.yMin = Vector(b)[1] + ob.location[1]

				if self.zMax is None or ((Vector(b)[2] + ob.location[2]) > self.zMax):
					self.zMax = Vector(b)[2] + ob.location[2]
				if self.zMin is None or ((Vector(b)[2] + ob.location[2]) < self.zMin):
					self.zMin = Vector(b)[2] + ob.location[2]

		self.xMid = (self.xMin + self.xMax)/2
		self.yMid = (self.yMin + self.yMax)/2
		self.zMid = (self.zMin + self.zMax)/2

		self.minimum = (self.xMin, self.yMin, self.zMin)
		self.maximum = (self.xMax, self.yMax, self.zMax)
		self.midpoint = (self.xMid, self.yMid, self.zMid)