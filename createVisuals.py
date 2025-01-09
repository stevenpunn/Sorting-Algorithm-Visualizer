import pygame
import math
pygame.init()

# defining global values and create visualization blocks
class createVisuals:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    backgroundColor = WHITE
    sidePadding = 100
    topPadding = 100
    font = pygame.font.SysFont('Garamond', 20)
    largeFont = pygame.font.SysFont('Garamond', 30)
    gradients = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]
  
    def __init__(self, width, height, myList):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(myList)

    # adjust bar height and width depending on amount of values
    def set_list(self, myList):
        self.myList = myList
        self.min_val = min(myList)
        self.max_val = max(myList)
        
        self.bar_width = round((self.width - self.sidePadding) / len(myList))
        self.bar_height = math.floor((self.height - self.topPadding) / (self.max_val - self.min_val))
        self.startHorizontal = self.sidePadding // 2