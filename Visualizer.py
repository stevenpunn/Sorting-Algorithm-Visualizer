import pygame
import random
from createVisuals import createVisuals
pygame.init()

def draw(createList):
    createList.window.fill(createList.backgroundColor)

    controls = createList.font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, createList.BLACK)
    createList.window.blit(controls, (createList.width/2 - controls.get_width()/2, 5))

    sortingAlgos = createList.font.render("I - Insertion Sort | B - Bubble Sort | M - Merge Sort", 1, createList.BLACK)
    createList.window.blit(sortingAlgos, (createList.width/2 - sortingAlgos.get_width()/2, 35))

    draw_list(createList)
    pygame.display.update()

# generate a random list of values to be sorted
def generateList(n, min_val, max_val):
    myList = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        myList.append(val)
    return myList

# create a function to create different bars
def draw_list(createList, colorSwap={}, clearBackground = False):
    myList = createList.myList

    if clearBackground:
        clearRectangle = (createList.sidePadding//2, 
        createList.topPadding, 
        createList.width - createList.sidePadding, 
        createList.height - createList.topPadding)
        pygame.draw.rect(createList.window, createList.backgroundColor, clearRectangle)

    for i, val in enumerate(myList):
        x = createList.startHorizontal + i * createList.bar_width
        y = createList.height - (val - createList.min_val) * createList.bar_height

        color = createList.gradients[i % 3]      # alternates between different gradients

        if i in colorSwap:
            color = colorSwap[i]

        pygame.draw.rect(createList.window, color, (x, y, createList.bar_width, createList.height))
    
    if clearBackground:
        pygame.display.update()

def bubbleSort(createList, ascending = True):
    myList = createList.myList

    for i in range(len(myList) -1):
        for j in range(len(myList) - 1 -i):
            num1 = myList[j]
            num2 = myList[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                myList[j], myList[j+1] = myList[j+1], myList[j]
                draw_list(createList, {j: createList.GREEN, j+1: createList.RED}, True)
                yield True                  # yield allows to iterate and pause sorting
    return myList

def main():
    run = True
    runtime = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    myList = generateList(n, min_val, max_val)
    createList = createVisuals(800, 600, myList)
    sorting = False
    ascending = True

    sortingAlgorithms = bubbleSort
    sortingAlgorithmName = "Bubble Sort"
    sortingAlgorithmGenerator = None

    while run:
        runtime.tick(60)
        if sorting:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                    sorting = False
        else:
            draw(createList)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                myList = generateList(n, min_val, max_val)
                createList.set_list(myList)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sortingAlgorithmGenerator = sortingAlgorithms(createList, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sortingAlgorithms = bubbleSort
                sortingAlgorithmName = "Bubble Sort"

    pygame.quit()
    

if __name__ == "__main__":
    main()