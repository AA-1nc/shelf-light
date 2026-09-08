import sys
from PySide6.QtWidgets import QApplication
from gui import mainWindow

app = QApplication(sys.argv)

window = mainWindow()
window.show()

sys.exit(app.exec())