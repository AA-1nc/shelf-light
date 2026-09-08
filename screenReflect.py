from mss import MSS
from PIL import Image
import numpy as np
import time
import colorsys
from PySide6.QtCore import QThread
from network import client

class ScreenReflectWorker(QThread):
    def __init__(self, client: client):
        super().__init__()
        self.client = client
        self.running = False
        self.sct = MSS()
        self.monitor = self.sct.monitors[1]
        self.frameTime = 1 / 24

    def run(self):
        self.running = True

        while self.running:
            img = np.array(self.sct.grab(self.monitor))
            
            small = Image.fromarray(img).resize((320, 180))
            img = np.array(small)
            
            grid = self.screenToGrid(img)
            
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    r, g, b = grid[row][col]
                    grid[row][col] = self.boostColorSaturation((int(r), int(g), int(b)))

            self.client.sendData('color2D', grid)
            
            time.sleep(self.frameTime)

    def stop(self):
        self.running = False

    def changeFps(self, fps):
        self.frameTime = 1 / fps

    def screenToGrid(self, img, rows=3, cols=3):
        height, width, _ = img.shape
        grid = []

        cellHeight = height // rows
        cellWidth = width // cols

        for row in range(rows):
            gridRow = []

            for col in range(cols):
                cell = img[row*cellHeight:(row+1)*cellHeight,
                        col*cellWidth:(col+1)*cellWidth,
                        :3]
                
                b, g, r = cell.mean(axis=(0, 1))
                gridRow.append((r, g, b))
            grid.append(gridRow)
        return grid

    def boostColorSaturation(self, color):
        r, g, b = color
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        s = min(1, s * 2)
        r, g, b, = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))