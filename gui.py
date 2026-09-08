from PySide6.QtCore import Qt, Signal, QPropertyAnimation
from PySide6.QtWidgets import *
from network import client
from screenReflect import ScreenReflectWorker

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ShelfLite')
        self.client = client()
        self.client.connect()

        layout = QVBoxLayout(self)

        # Connection Widget
        connectionWidget = QWidget()
        connectionLayout = QVBoxLayout(connectionWidget)
        connectionLayout.addWidget(QLabel("Connect to Strip"))

        connectionWidget.setObjectName('connectionWidget')
        connectionWidget.setStyleSheet(f"""
                        #connectionWidget {{
                        border: none;
                        border-bottom: 1px solid #3a3a3a;
                        border-radius: 8px;
                        padding: 8px;
                        text-align: left;
                    }}""")

        layout.addWidget(connectionWidget)

        # Light mode widgets
        manual = manualWidget(self.client)
        screenReflect = screenReflectWidget(self.client)

        self.dropdowns = []
        self.dropdowns.append(expandingDropdown('Manual', manual, 0))
        self.dropdowns.append(expandingDropdown('Screen Reflect', screenReflect, 1))

        for item in self.dropdowns:
            item.opened.connect(self.openNewDropdown)
            layout.addWidget(item, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addStretch()

        # Screen reflect thread creation
        self.worker = ScreenReflectWorker(self.client)
        screenReflect.startRequested.connect(self.worker.start)
        screenReflect.stopRequested.connect(self.worker.stop)
        screenReflect.fpsChanged.connect(self.worker.changeFps)

    def openNewDropdown(self, index):
        for i in range(len(self.dropdowns)):
            if i == index: continue
            if self.dropdowns[i].isOpen():
                self.dropdowns[i].toggle()

class manualWidget(QWidget):
    def __init__(self, client: client):
        super().__init__()
        self.client = client
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel('Manual'))

        grid = QGridLayout()
        grid.setSpacing(8)
        self.colors = [[(255, 255, 255) for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                cell = colorCell(row, col)
                cell.colorChanged.connect(self.updateColor)
                grid.addWidget(cell, row, col)

        gridWidget = QWidget()
        gridWidget.setLayout(grid)

        layout.addWidget(gridWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)

    def updateColor(self, row, col, color):
        self.colors[row][col] = color
        self.client.sendData('color2D', self.colors)

    def activate(self):
        self.client.sendData('color2D', self.colors)

    def deactivate(self):
        pass

class screenReflectWidget(QWidget):
    startRequested = Signal()
    stopRequested = Signal()
    fpsChanged = Signal(int)

    def __init__(self, client: client):
        super().__init__()
        self.client = client
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel('Screen Reflect'))

        self.fpsSelect = QComboBox()
        self.fpsSelect.addItems([ i + ' fps' for i in ['5', '10', '24', '30', '60']])
        self.fpsSelect.setCurrentIndex(2)
        self.fpsSelect.currentTextChanged.connect(self.changeFps)
        layout.addWidget(self.fpsSelect, alignment=Qt.AlignmentFlag.AlignLeft)

        self.setLayout(layout)

    def activate(self):
        self.startRequested.emit()

    def deactivate(self):
        self.stopRequested.emit()

    def changeFps(self):
        self.fpsChanged.emit(int(self.fpsSelect.currentText().split(' ')[0]))

# Custom Widgets

class colorCell(QPushButton):
    colorChanged = Signal(int, int, tuple)

    def __init__(self, row, col):
        super().__init__()

        self.row = row
        self.col = col

        self.color = (255, 255, 255)
        self.setFixedSize(70, 70)
        self.updateAppearance()
        self.clicked.connect(self.pickColor)
    
    def pickColor(self):
        color = QColorDialog.getColor()

        if not color.isValid():
            return
        
        self.color = (color.red(), color.green(), color.blue())
        self.colorChanged.emit(self.row, self.col, self.color)
        self.updateAppearance()
    
    def updateAppearance(self):
        r, g, b = self.color
        self.setStyleSheet(f'''
            QPushButton {{
                background-color: rgb({r}, {g}, {b});
                border: 2px solid #444;
                border-radius: 6px;
            }}

            QPushButton:hover {{
                border-color: white;
            }}
        ''')

class expandingDropdown(QWidget):
    opened = Signal(int)

    def __init__(self, text, content: QWidget, index):
        super().__init__()

        layout = QVBoxLayout()
        self.open = False
        self.index = index

        self.header = QToolButton()
        self.header.setText(text)
        self.header.setArrowType(Qt.ArrowType.RightArrow)
        self.header.clicked.connect(self.toggle)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.header.setStyleSheet("""
            QToolButton {
                border: none;
                border-bottom: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 8px;
                text-align: left;
            }

            QToolButton:hover {
                background-color: rgba(255,255,255,0.05);
            }
        """)

        self.content = content
        self.contentContainer = QWidget()

        containerLayout = QVBoxLayout()
        containerLayout.setContentsMargins(0, 0, 0, 0)
        containerLayout.addWidget(self.content)
        self.contentContainer.setLayout(containerLayout)

        self.contentContainer.setMaximumHeight(0)
        self.expandedHeight = self.contentContainer.sizeHint().height()
        self.contentContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            
        layout.addWidget(self.header)
        layout.addWidget(self.contentContainer)

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def toggle(self):
        self.open = not self.open
        if self.open:
            self.contentContainer.setMaximumHeight(self.contentContainer.sizeHint().height())

            self.opened.emit(self.index)
            self.content.activate()

            self.header.setArrowType(Qt.ArrowType.DownArrow)
        else:
            self.contentContainer.setMaximumHeight(0)

            self.content.deactivate()

            self.header.setArrowType(Qt.ArrowType.RightArrow)

    def isOpen(self):
        return self.open
        
