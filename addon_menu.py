class OrbitalMenu(bpy.types.Menu):
	bl_idname = "OBJECT_MT_automatic_turntable"
	bl_label = "Automatic Turntable"

	def draw(self, context):
		layout = self.layout
		