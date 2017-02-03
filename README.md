Automatic Turntable Addon
================
Version 0.3
-----------
(c) Mark Fitzgibbon 2017

Description
-----------
Automatically focus camera to rotate around a selected object in a scene.
Will default to camera named "Camera", using render settings set for this camera.
Script is provided as-is

Download
--------
User can pull, fork, or download this tool's source code from 
[Blender-Automatic-Turntable Repository](https://github.com/ibbolia/blender-automatic-turntable)

Requirements
------------
Requires Blender, v2.78 preferred.
Code is not intended nor designed to work as a standalone Python program.

Install
-------
User wishing to install as and addon to blender should perform the following:
1. Zip folder (if not already done) 
2. Open Blender program
3. Navigate to File > User Preferences > Add-ons
4. Install from file

Alternatively, User can install addon files directly in Blender's addon folder
Add-on is only in "Testing" supported level

Usage
--------
Addon is accessible through Render>Automatic Turntable
Automatic turntable will not manage render settings automaticaly
User should confirm camera parameters (e.g. clipping, FOV) befre execution

User will be presented with a dialog box and the following parameters:
- Iterations: The total amount of renders to be made
- Increments: The angle (in degrees) between iterations
- Margin: Minimum amount of space (percent) between the object and edge of render
- Camera: Name of Camera object to be utilized (defaults to Active)
- File Pat: Directory renders will be saved to

User can then press OK to start render process

Significant Known Issues
------------
- 6: Object with too much Y length cropped
	- Addresses issue caused by Y length exceeding X length
	- Suggested temporary workaround: No known workaround exists at this time

To Do
--------
- GUI interface
- More iteration control

Notes
--------
- [Camera distance formula](http://photo.stackexchange.com/questions/12434/how-do-i-calculate-the-distance-of-an-object-in-a-photo)

Contact
-------
- [Github](https://github.com/ibbolia)
- Twitter: [@ibbolia](https://twitter.com/ibbolia)
- Gmail: mwfitzgibbon