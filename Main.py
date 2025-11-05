import sys
import json
import sys
import json
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IMPACT Ramp Builder")
        self.setGeometry(100, 100, 500, 280)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.lumber_prices = self.load_lumber_prices()
        self.create_form_layout()

    def load_lumber_prices(self, file_path='Lumber_Prices.json'):
        """Reads the JSON file and returns the list of lumber prices."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get('lumber_prices', [])
        except FileNotFoundError:
            print(f"Error: JSON file not found at {file_path}")
            return []
        except json.JSONDecodeError:
            print("Error: Could not parse JSON data. Check file formatting.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []
    
    def create_form_layout(self):
        # Main Wrapper
        master_layout = QHBoxLayout(self.central_widget)

        # Form
        form_container_layout = QVBoxLayout()
        form_grid = QGridLayout()
        
        #Basic Info
        self.heading_label = QLabel("<h1>Basic Info</h1>")
        form_grid.addWidget(self.heading_label, 0, 0)

        self.client_label = QLabel("Client Name:")
        self.client_input = QLineEdit()
        form_grid.addWidget(self.client_label, 1, 0)
        form_grid.addWidget(self.client_input, 1, 1)

        self.site_label = QLabel("Site Number:")
        self.site_input = QLineEdit()
        form_grid.addWidget(self.site_label, 2, 0)
        form_grid.addWidget(self.site_input, 2, 1)
        
        #Deck
        self.heading_label = QLabel("<h1>Deck/Porch Info</h1>")
        form_grid.addWidget(self.heading_label, 3, 0)

        self.inch_label = QLabel("Input unit inches? :") ######## True False BOOL
        self.inch_input = QCheckBox()
        form_grid.addWidget(self.inch_label, 4, 0)
        form_grid.addWidget(self.inch_input, 4, 1)

        self.length_label = QLabel("Length (Foot):")
        self.length_input = QLineEdit()
        self.length_input.setValidator(QIntValidator(0, 99999, parent=self))
        form_grid.addWidget(self.length_label, 5, 0)
        form_grid.addWidget(self.length_input, 5, 1)

        self.width_label = QLabel("Width: (Foot)")
        self.width_input = QLineEdit()
        self.width_input.setValidator(QIntValidator(0, 99999, parent=self))
        form_grid.addWidget(self.width_label, 6, 0)
        form_grid.addWidget(self.width_input, 6, 1)

        self.Stair_Label = QLabel("Number of Stairs:")
        self.Stair_input = QLineEdit()
        self.Stair_input.setValidator(QIntValidator(0, 4, parent=self))
        form_grid.addWidget(self.Stair_Label, 7, 0)
        form_grid.addWidget(self.Stair_input, 7, 1)
        
        #Ramp
        self.heading_label = QLabel("<h1>Ramp Info</h1>")
        form_grid.addWidget(self.heading_label, 8, 0)

        self.ramp_desc_label = QLabel("Ramp :")
        self.ramp_desc_input = QLineEdit()
        self.ramp_desc_input.setMinimumSize(250,40)
        form_grid.addWidget(self.ramp_desc_label, 9, 0)
        form_grid.addWidget(self.ramp_desc_input, 9, 1)

        self.flat_label = QLabel("Ending flat? :") ######## True False BOOL
        self.flat_input = QCheckBox()
        form_grid.addWidget(self.flat_label, 10, 0)
        form_grid.addWidget(self.flat_input, 10, 1)

        self.heading_label = QLabel("<h3>Slope:</h3>")
        form_grid.addWidget(self.heading_label, 11, 0)
        
        self.drop_label = QLabel("Drop (Inches) :")
        self.drop_input = QLineEdit()
        self.drop_input.setValidator(QIntValidator(0, 10, parent=self))
        form_grid.addWidget(self.drop_label, 12, 0)
        form_grid.addWidget(self.drop_input, 12, 1)

        self.degree_label = QLabel("Degree (Angle) :")
        self.degree_input = QLineEdit()
        self.degree_input.setValidator(QIntValidator(0, 10, parent=self))
        form_grid.addWidget(self.degree_label, 13, 0)
        form_grid.addWidget(self.degree_input, 13, 1)
        
        #Mesh
        self.heading_label = QLabel("<h1>Gen Info</h1>")
        form_grid.addWidget(self.heading_label, 14, 0)

        self.point_label = QLabel("Point Cloud Post Set (optional):")
        self.point_display = QLineEdit()
        self.point_pick = QPushButton("Browse...")
        self.point_display.setReadOnly(True)
        form_grid.addWidget(self.point_label, 15, 0)
        form_grid.addWidget(self.point_display, 15, 1) 
        form_grid.addWidget(self.point_pick, 15, 2)
        self.point_pick.clicked.connect(self.open_file_dialog)
        
        self.post_label = QLabel("Normal Post Set:")
        self.post_input = QCheckBox()
        form_grid.addWidget(self.post_label, 16, 0)
        form_grid.addWidget(self.post_input, 16, 1)

         # Submit Button
        self.submit_button = QPushButton("Submit Data")
        self.submit_button.clicked.connect(self.submit_form) # Connect the button

        form_container_layout.addLayout(form_grid)
        form_container_layout.addWidget(self.submit_button)
        form_container_layout.addStretch(1)
        # Cost
        cost_group = QGroupBox("Current Lumber Costs (USD)")
        cost_layout = QGridLayout(cost_group)
        cost_row = 0 # Location of cost sheet

        if not self.lumber_prices:
            error_label = QLabel("Error loading prices from file.")
            error_label.setStyleSheet("color: red;")
            cost_layout.addWidget(error_label, 0, 0, 1, 2)
        else:
            # Loop through the loaded JSON data and create widgets
            for item_data in self.lumber_prices:
                item_name = item_data.get('item', 'Unknown Item')
                item_price = item_data.get('price_usd', 0.0)
                item_label = QLabel(f"{item_name} Cost:")
                price_input = QLineEdit()
                price_input.setReadOnly(True)
                price_input.setText(f"${item_price:.2f}")

                #Store the widgets if you need to reference them later
                setattr(self, f"cost_{item_name.replace(' ', '_').lower()}_label", item_label)
                setattr(self, f"cost_{item_name.replace(' ', '_').lower()}_input", price_input)
                cost_layout.addWidget(item_label, cost_row, 0)
                cost_layout.addWidget(price_input, cost_row, 1)
                
                cost_row += 1

            master_layout.addLayout(form_container_layout)
            master_layout.addSpacing(100)
            master_layout.addWidget(cost_group)
            
        # Assemble the Layout

    def open_file_dialog(self):
        # This opens the native file selection dialog.
        # getOpenFileName returns a tuple: (file_path, filter_string)
        file_path, _ = QFileDialog.getOpenFileName(
            self,                                    # Parent window
            "Select a Point Cloud File",                    # Dialog title
            "",                                      # Starting directory (empty for user's home)
            "Point Cloud (*.E57);; Polygon File Format (*.ply);;All Files (*.*)" # Filters
        )

        # Check if a file was selected (i.e., the user didn't hit cancel)
        if file_path:
            # Set the selected file path into the QLineEdit
            self.point_display.setText(file_path)
            print(f"File selected: {file_path}")
        else:
            print("File selection canceled.")

    def submit_form(self):
        deck=False
        ramp=False
        # Retrieve and process data
        # Client
        Client_Name = self.client_input.text()
        Site_Number = self.site_input.text()

        # Deck
        Inches_Deck = self.inch_input.isChecked()
        Deck_Length = self.length_input.text()
        Deck_Width = self.width_input.text()
        Stair_Number = self.Stair_input.text()

        # Ramp
        Ramp_Desc = self.ramp_desc_input.text()
        Flat_Bool = self.flat_input.isChecked()
        Drop_Slope = self.drop_input.text()
        Drop_Angle = self.degree_input.text()

        # Point
        Point_Cloud = self.point_display.text()
        No_Tech_Bool = self.post_input.isChecked()

        ## ERROR CHECK
        errors = []
        
        if not Client_Name:
            errors.append("Client Name cannot be empty.")
        if not Site_Number:
            errors.append("Site Number cannot be empty.")

        if Deck_Length != "" or Deck_Width != "" or Stair_Number != "":
            deck=True
            if not Deck_Length:
                errors.append("Deck Length is required.")
            if not Deck_Width:
                errors.append("Deck Width is required.")
            if not Stair_Number:
                errors.append("Number of Stairs is required.")

        if Ramp_Desc != "" or Drop_Slope != "" or Drop_Angle != "":
            ramp=True
            if not Ramp_Desc:
                errors.append("Ramp Description cannot be empty.")
            
            if not Drop_Slope and not Drop_Angle:
                errors.append("Either 'Drop (Inches)' or 'Degree (Angle)' must be provided for the ramp slope.")
            elif Drop_Slope and Drop_Angle:
                 errors.append("Please provide only one value for the ramp slope: either 'Drop (Inches)' or 'Degree (Angle)'.")
        if errors:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please correct the following errors before submitting:\n\n" + "\n".join(f"* {e}" for e in errors)
            )
            return # Stop the submission process
        
        #

        Deck_Length = int(Deck_Length)
        Deck_Width = int(Deck_Width)
        Stair_Number = int(Stair_Number)
        
        # Only attempt conversion if the string is not empty // based on the XOR logic
        Drop_Slope = int(Drop_Slope) if Drop_Slope else None
        Drop_Angle = int(Drop_Angle) if Drop_Angle else None

        if Deck_Length > 0 and Deck_Width > 0:
            # We use self.deck_designer_window to hold a reference to the window
            # This prevents the window from being garbage collected and closing immediately.
            self.deck_designer_window = DeckDesignerWindow(Deck_Length, Deck_Width, Stair_Number, Inches_Deck, parent=self)
            self.deck_designer_window.show()
            print("Launched Deck Designer Window.")
            

# deck break out
class DeckDesignerWindow(QMainWindow):
    """
    A separate window for designing the deck and ramp placement.
    """
    def __init__(self, deck_length, deck_width, stair_count, inch, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Deck Designer - {deck_length} x {deck_width}")
        self.setGeometry(200, 200, 1000, 800)

        self.inch_unit=inch
        self.deck_length = deck_length
        self.deck_width = deck_width
        self.stair_count = stair_count # Storing this new value
        
        self.stair_items = []

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.master_layout = QVBoxLayout(self.central_widget)
        
        self.create_design_space()
        
    def create_design_space(self):
        # 1. Title
        title_label = QLabel("<h2>Deck and Ramp Placement (Top View)</h2>")
        self.master_layout.addWidget(title_label)
        
        # 2. Control Area (NEW)
        control_group = QGroupBox("Design Controls")
        control_layout = QHBoxLayout(control_group)
        
        # House Side Prompt
        house_label = QLabel("House Facing Side:")
        self.house_side_combo = QComboBox()
        self.house_side_combo.addItems(["Top", "Bottom", "Left", "Right"])
        # Connect the change to the update function
        self.house_side_combo.currentTextChanged.connect(self.update_house_label)
        
        control_layout.addWidget(house_label)
        control_layout.addWidget(self.house_side_combo)
        control_layout.addStretch(1) # Push widgets to the left
        
        self.master_layout.addWidget(control_group) # Add the control group to the master layout
        
        # 3. Graphics View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.master_layout.addWidget(self.view)
        
        # 4. Draw the initial deck and components
        self.draw_deck()
        self.add_components()
        
        # 5. Initialize the house label after all components are ready
        self.house_label_item = None
        self.update_house_label(self.house_side_combo.currentText()) # Initial draw
    def update_house_label(self, side: str):
        """
        Draws a text label on the selected side of the deck to indicate the house's position.
        """
        if self.house_label_item:
            self.scene.removeItem(self.house_label_item)
            self.house_label_item = None
        
        # Must run after draw_deck() has created self.deck_rect
        if not self.deck_rect:
            return

        deck_rect = self.deck_rect.rect()
        
        # Create the label text item
        label_text = "HOUSE"
        label = QGraphicsTextItem(label_text)
        label.setDefaultTextColor(QColor(255, 0, 0)) # Red color
        
        # Use a large font to make it clear
        font = label.font()
        font.setPointSize(20) # 20pt font
        font.setBold(True)
        label.setFont(font)
        
        # Get the label's dimensions for centering
        label_bounds = label.boundingRect()
        
        # Calculate position based on the selected side
        if side == "Top":
            x = deck_rect.left() + (deck_rect.width() - label_bounds.width()) / 2
            y = deck_rect.top() - label_bounds.height()
        elif side == "Bottom":
            x = deck_rect.left() + (deck_rect.width() - label_bounds.width()) / 2
            y = deck_rect.bottom()
        elif side == "Left":
            x = deck_rect.left() - label_bounds.width()
            y = deck_rect.top() + (deck_rect.height() - label_bounds.height()) / 2
            # Optional: Rotate the text for a vertical wall
            label.setRotation(-90)
            x += label_bounds.height() # Adjust position after rotation
        elif side == "Right":
            x = deck_rect.right()
            y = deck_rect.top() + (deck_rect.height() - label_bounds.height()) / 2
            # Optional: Rotate the text
            label.setRotation(90)
            y += label_bounds.width() # Adjust position after rotation
        else:
            return

        label.setPos(x, y)
        self.scene.addItem(label)
        self.house_label_item = label
        
        # Ensure the view updates to show the label if it's placed outside the deck (Top/Left/Right)
        self.view.ensureVisible(label.boundingRect())
    def draw_deck(self):
        self.scene.clear()
        
        # --- Start of Scaling Logic (Unchanged) ---
        if self.inch_unit:
            SCALE = 1
        else:
            # Let's use 10 for better visibility and calculation
            SCALE = 10 
        
        visual_length = self.deck_length * SCALE
        visual_width = self.deck_width * SCALE
        # --- End of Scaling Logic ---
        
        # --- Texture Map Modification ---
        try:
            # 1. Load the texture image
            texture_pixmap = QPixmap("Decking.png") # <<<<<< MAKE SURE THIS FILE EXISTS
            if texture_pixmap.isNull():
                print("Warning: Texture image 'Decking.png' not found or failed to load. Falling back to solid color.")
                deck_brush = QBrush(QColor(190, 190, 250, 100)) # Fallback light blue fill
            else:
                # **Crucial Step: Scale the QPixmap to the exact visual size**
                # Use SmoothTransformation for better quality scaling
                scaled_pixmap = texture_pixmap.scaled(
                    visual_length, 
                    visual_width, 
                    Qt.IgnoreAspectRatio, 
                    Qt.SmoothTransformation
                )
                
                # 2. Create the non-repeating brush from the scaled image
                deck_brush = QBrush(scaled_pixmap)
                
                # NOTE: For an image scaled to the exact size, using Qt.NoBrush
                # or similar might be more explicit, but QBrush(pixmap) is sufficient.
                # However, for an exact, non-repeating fit, you may not need the rect item's brush
                # if you switch to a QGraphicsPixmapItem as noted below.
                
        except Exception as e:
            # Catch other potential errors
            print(f"Error loading texture: {e}. Falling back to solid color.")
            deck_brush = QBrush(QColor(190, 190, 250, 100)) # Fallback light blue fill

        # deck outline
        self.deck_rect = QGraphicsRectItem(0, 0, visual_length, visual_width) # Store as instance variable
        #self.deck_rect.setPen(QPen(QColor(50, 50, 200), 2)) # Blue outline
        
        # 3. Apply the texture brush
        self.deck_rect.setBrush(deck_brush) 
        
        self.scene.addItem(self.deck_rect)
        
        # Label the deck (Unchanged)
        label = QGraphicsTextItem(f"Deck Area\n{self.deck_length} x {self.deck_width}")
        label.setDefaultTextColor(QColor(0, 0, 100))
        # Center the text
        label.setPos(visual_length / 2 - label.boundingRect().width() / 2, 
                     visual_width / 2 - label.boundingRect().height() / 2)
        self.scene.addItem(label)
        
        # Set the scene's bounding rect (Unchanged)
        self.scene.setSceneRect(QRectF(self.deck_rect.rect()).normalized().adjusted(-10, -10, 10, 10)) 
        
        # Fit the view to the new scene bounds (Unchanged)
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def add_components(self):
        # We now pass the deck item reference to the component constructors
        deck_item = self.deck_rect 
        
        # Add stairs if count > 0
        if self.stair_count > 0:
            initial_x_offset = 0
            # Loop to create multiple staircase objects
            for i in range(self.stair_count):
                # We also pass the index 'i' so the item can have a unique name
                stairs = StairsItem(self.inch_unit, index=i + 1, deck_item=deck_item) 
                
                # Place the stairs item next to the previous one for a simple initial layout
                stairs.setPos(initial_x_offset, 0)
                
                # Increment the offset for the next stair item
                # The total visual width of a StairsItem is its boundingRect().width()
                initial_x_offset += stairs.boundingRect().width()
                
                self.scene.addItem(stairs)
                self.stair_items.append(stairs) # Store the reference
        
        # Add ramp (Ramp Item logic remains the same)
        ramp = RampItem(self.inch_unit, deck_item=deck_item) 
        # Use the accumulated offset for the ramp's starting position
        ramp_x_pos = deck_item.rect().width() - ramp.boundingRect().width()
        ramp.setPos(ramp_x_pos, 0)
        self.scene.addItem(ramp)
        self.ramp_item = ramp # Store the reference
         
class DraggableItem(QGraphicsRectItem):
    """
    Base class for any item (Stairs, Ramp) that needs to be draggable 
    and snap to the 8 corner positions of the main deck item.
    """
    def __init__(self, rect, color, name="Item", deck_item=None, texture_path=None, parent=None):
        super().__init__(rect, parent)
        self.name = name
        self.deck_item = deck_item
        
        # Enable dragging for this item
        self.setFlag(QGraphicsRectItem.ItemIsMovable) 
        self.setCacheMode(QGraphicsRectItem.DeviceCoordinateCache)

        # --- MODIFIED: Handle Texture or Fallback Color ---
        brush = QBrush(QColor(color)) # Default brush
        
        if texture_path:
            try:
                texture_pixmap = QPixmap(texture_path)
                if not texture_pixmap.isNull():
                    # Scale the pixmap to the item's visual size
                    scaled_pixmap = texture_pixmap.scaled(
                        rect.width(), 
                        rect.height(), 
                        Qt.IgnoreAspectRatio, 
                        Qt.SmoothTransformation
                    )
                    brush = QBrush(scaled_pixmap)
                else:
                    print(f"Warning: Texture image '{texture_path}' not found or failed to load for {self.name}. Using solid color.")
            except Exception as e:
                print(f"Error loading texture for {self.name}: {e}. Using solid color.")

        self.setBrush(brush)
        self.setPen(QPen(QColor(0, 0, 0), 1))

        # Add the text label
        self.add_label()
        
    def add_label(self):
        """Creates and centers a text label on the item."""
        label = QGraphicsTextItem(self.name, parent=self)
        label.setDefaultTextColor(QColor(0, 0, 0)) # Black text

        # Get the item's bounding rectangle (local coordinates)
        item_rect = self.boundingRect()
        
        # Get the label's bounding rectangle
        label_bounds = label.boundingRect()

        # Calculate position to center the label within the item
        x = item_rect.width() / 2 - label_bounds.width() / 2
        y = item_rect.height() / 2 - label_bounds.height() / 2
        
        # Set the label position (relative to the DraggableItem)
        label.setPos(x, y)
    def mousePressEvent(self, event):
        # We need to call the base implementation to start the drag operation
        super().mousePressEvent(event)
        print(f"Clicked and dragging {self.name}")

    def get_snap_positions(self):
        """Calculates the 8 potential snap positions around the deck edges."""
        if not self.deck_item:
            return []

        # The deck rect is in scene coordinates (since it's at 0,0)
        deck_rect = self.deck_item.rect() 
        item_w = self.boundingRect().width()
        item_h = self.boundingRect().height()
        
        # Snap positions are defined by the top-left corner of the item when snapped.
        positions = []
        
        # 1. Top-Left Corner (Outside Top and Outside Left positions)
        positions.append(QPointF(deck_rect.left(), deck_rect.top() - item_h))      # Aligned Top
        positions.append(QPointF(deck_rect.left() - item_w, deck_rect.top()))      # Aligned Left

        # 2. Top-Right Corner (Outside Top and Outside Right positions)
        positions.append(QPointF(deck_rect.right() - item_w, deck_rect.top() - item_h)) # Aligned Top
        positions.append(QPointF(deck_rect.right(), deck_rect.top()))                 # Aligned Right

        # 3. Bottom-Right Corner (Outside Bottom and Outside Right positions)
        positions.append(QPointF(deck_rect.right() - item_w, deck_rect.bottom()))  # Aligned Bottom
        positions.append(QPointF(deck_rect.right(), deck_rect.bottom() - item_h)) # Aligned Right

        # 4. Bottom-Left Corner (Outside Bottom and Outside Left positions)
        positions.append(QPointF(deck_rect.left(), deck_rect.bottom()))            # Aligned Bottom
        positions.append(QPointF(deck_rect.left() - item_w, deck_rect.bottom() - item_h)) # Aligned Left
        
        return positions
        
    def mouseReleaseEvent(self, event):
        """When the mouse is released, snap the item to the nearest valid position."""
        super().mouseReleaseEvent(event)
        
        current_pos = self.pos()
        # **This is where 'snap_positions' is defined:**
        snap_positions = self.get_snap_positions()
        
        if not snap_positions:
            return

        min_distance_sq = float('inf')
        nearest_pos = current_pos # Initialize nearest_pos

        for snap_pos in snap_positions:
            # Calculate the squared distance (faster than calculating the square root)
            dx = snap_pos.x() - current_pos.x()
            dy = snap_pos.y() - current_pos.y()
            distance_sq = dx*dx + dy*dy
            
            if distance_sq < min_distance_sq:
                min_distance_sq = distance_sq
                nearest_pos = snap_pos
        
        # Snap the item to the nearest position
        self.setPos(nearest_pos)
        print(f"{self.name} snapped to: ({nearest_pos.x():.2f}, {nearest_pos.y():.2f})")
        
        # NOTE: Make sure the final line of your function is NOT just 'snap_positions'
        # The function should exit naturally after the setPos call.

class StairsItem(DraggableItem):
    # FIX: Add deck_item to the signature and pass it to super()
    # Added 'index' to the signature
    def __init__(self, scale, index=1, deck_item=None, parent=None):
        super().__init__(
                    QRectF(0, 0, 36, 36), # Positional 1: rect
                    QColor(255, 150, 50, 200), # Positional 2: color
                    f"STAIRS {index}", # Positional 3: name, now uses index
                    # --- START OF KEYWORD ARGUMENTS ---
                    deck_item=deck_item, # Keyword (Recommended)
                    texture_path="Stair_T.png", # Keyword
                    parent=parent# Keyword (Must be named because it follows texture_path)
                )
        
class RampItem(DraggableItem):
    # FIX: Add deck_item to the signature and pass it to super()
    def __init__(self,scale, deck_item=None, parent=None): 
        # Placeholder size: 10 units wide x 20 units long (100x200 pixels using SCALE=10)
            super().__init__(
                QRectF(0, 0, 48, 48), 
                QColor(50, 200, 50, 200),
                "RAMP", 
                # 
                deck_item=deck_item,            # Keyword (Recommended)
                texture_path="Ramp_T.png",        # Keyword
                parent=parent                   # Keyword (Must be named because it follows texture_path)
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec())
