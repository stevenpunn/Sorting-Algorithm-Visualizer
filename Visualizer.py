import pygame
import random
from createVisuals import createVisuals
pygame.init()

def title(createList, sortingAlgorithmName, ascending):
    createList.window.fill(createList.backgroundColor)

    title = createList.font.render(f"{sortingAlgorithmName} - {'Ascending' if ascending else 'Descending'}", 1, createList.BLACK)
    createList.window.blit(title, (createList.width/2 - title.get_width()/2, 5))

    controls = createList.font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, createList.BLACK)
    createList.window.blit(controls, (createList.width/2 - controls.get_width()/2, 35))

    sortingAlgos = createList.font.render("1 - Bubble Sort | 2 - Insertion Sort | 3 - Quick Sort", 1, createList.BLACK)
    createList.window.blit(sortingAlgos, (createList.width/2 - sortingAlgos.get_width()/2, 55))

    drawBars(createList)
    pygame.display.update()

# generate a random list of values to be sorted
def generateList(n, min_val, max_val):
    myList = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        myList.append(val)
    return myList

# create a function to create different bars
def drawBars(createList, colorSwap={}, clearBackground = False):
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
                drawBars(createList, {j: createList.GREEN, j+1: createList.RED}, True)
                yield True                  # yield allows to iterate and pause sorting
    return myList

def insertionSort(createList, ascending = True):
    myList = createList.myList
    
    for i in range(1, len(myList)):
        key = myList[i]                 # stores current index in memory
        while True:
            ascending_sort = i > 0 and myList[i - 1] > key and ascending
            descending_sort = i > 0 and myList[i - 1] < key and not ascending

            if not ascending_sort and not descending_sort:
                break
            myList[i] = myList[i - 1]
            i = i - 1
            myList[i] = key
            drawBars(createList, {i:createList.GREEN, i - 1: createList.RED}, True)
            yield True
    return myList

def quickSort(createList, ascending = True):
    myList = createList.myList

    def partition(start, end, ascending):
        pivot = myList[end]
        i = start -1

        for j in range(start, end):
            if (myList[j] <= pivot and ascending) or (myList[j] >= pivot and not ascending):
                i += 1
                myList[i], myList[j] = myList[j], myList[i]
                drawBars(createList, {i: createList.GREEN, j: createList.RED}, True)
                yield True
        
        myList[i + 1], myList[end] = myList[end], myList[i + 1]
        drawBars(createList, {i + 1: createList.BLUE, end: createList.RED}, True)
        yield True
        return i+1
    
    def sorter(start, end, ascending):
        if start < end:
            pivotPosition = yield from partition(start, end, ascending)     # partition values to find pivot index]\
            yield from sorter(start, pivotPosition - 1, ascending)
            yield from sorter(pivotPosition + 1, end, ascending)
    yield from sorter(0, len(myList) -1, ascending)

def main():
    run = True
    runtime = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100

    myList = generateList(n, min_val, max_val)
    createList = createVisuals(800, 600, myList)
    sorting = False
    paused = False
    ascending = True
    sortingAlgorithmName = "Select Sorting Algorithm"
    sortingAlgorithms = None

    while run:
        runtime.tick(60)            # adjust speed of sorting
        if sorting and not paused:
            try:
                next(sortingAlgorithmGenerator)
            except StopIteration:
                    sorting = False
        else:
            title(createList, sortingAlgorithmName, ascending)

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
            elif event.key == pygame.K_SPACE:
                if sorting:
                    paused = not paused
                elif sortingAlgorithms is not None:
                    sorting = True
                    paused = False
                    sortingAlgorithmGenerator = sortingAlgorithms(createList, ascending)
                else:
                    print("No Sorting Algorithm Selected!")
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_1 and not sorting:
                sortingAlgorithms = bubbleSort
                sortingAlgorithmName = "Bubble Sort"
            elif event.key == pygame.K_2 and not sorting:
                sortingAlgorithms = insertionSort
                sortingAlgorithmName = "Insertion Sort"
            elif event.key == pygame.K_3 and not sorting:
                sortingAlgorithms = quickSort
                sortingAlgorithmName = "Quick Sort"

    pygame.quit()
    

if __name__ == "__main__":
    main()