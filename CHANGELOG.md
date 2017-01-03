#Change Log
All notable changes will be tracked in this file

##[Unreleased]
###Changed
- Classes seperated into individual files

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