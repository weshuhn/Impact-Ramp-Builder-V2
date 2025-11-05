# 1. Import the necessary FreeCAD modules
import FreeCAD as App
import Part
import FreeCADGui as Gui

# 2. Create a new document (or get the active one)
# 'doc' will hold a reference to the new document
doc = App.newDocument("MyNewBoxModel")

# 3. Create a box shape using the Part module
# Part.makeBox(length, width, height)
box_shape = Part.makeBox(10.0, 10.0, 10.0)

# 4. Create a feature object in the document to display the shape
# This adds the object to the tree view
box_object = doc.addObject("Part::Feature", "MyBox")

# 5. Assign the shape to the feature object
box_object.Shape = box_shape

# 6. Recompute the document to make the object visible
doc.recompute()

# 7. (Optional) Adjust the view to fit the new object
Gui.activeDocument().activeView().viewAxonometric() # Set view to isometric
Gui.activeDocument().activeView().viewFit() # Zoom to fit the object