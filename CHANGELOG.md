#Change Log
All notable changes will be tracked in this file

##[Unreleased]
###Added
- AutomaticTurntableOperator class (To replace Orbital Operator)
- Turntable class (To replace Orbital)
- Keymaps variable
- AutomaticTurntableOperator UI via invoke_props_dialog

###Changed
- Register/Unregister takes effect on AutomaticTurntableOperator class

###Removed
- Active code referencing Orbital class

##[0.2.3] - 2017-01-16
###Fixed
- Issue 7: Camera rotation points now do not exceed final position
- Issue 8: Utilizes camera defined in script instead of active camera

##[0.2.2] - 2017-01-05
###Fixed
- Issue 5: Transforms no longer negatively affect render fitting

###Changed
- Bounding Box calculation now uses matrices directly on values

##[0.2.1] - 2017-01-04 
###Fixed
- Script is now able to account for global scale values of objects when determining bounds (Issue #5)

###Added
- Significan Known Issues section to readme

###Changed
- Classes seperated into individual files
- Modified specific methodology of corner calculation in BoundingBox.py
- (Above) Added Global Scale to calculation method for an individual bounding box
- Date markings in Readme

###Removed
- addon_menu.py: according to bpy documentation, this is the intent of an init file

##[0.2] - 2016-12-28
###Added
- RadialPoints.py file for determining position of camera during calculations
	-Some code exists for using spherical coordinates. It is not functional.
- addon_menu.py for setting up UI menu
- Altered calculation for bounding box 
	-(based on [boundingbox](https://github.com/ibbolia/blender-scripts/))
	-Calculation still utilizes "fit_view_to_selected" method, to be phased out

###Changed
- Functionality to use number of steps instead of degrees
- Camera radius from origin zoomed back around 10% from previous 
- Readme edits
	- Corrected link to github repository
	- Added link to twitter profile
	- Version number change


##[0.1] - 2016-12-14
###Added
- Base __init__.py file (from blender-scripts)