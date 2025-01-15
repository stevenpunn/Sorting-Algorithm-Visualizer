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

    sortingAlgos = createList.font.render("1 - Bubble Sort | 2 - Insertion Sort | 3 - Quick Sort | 4 - Selection Sort | 5 - Radix Sort", 1, createList.BLACK)
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

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):  # compare adjacent values
                myList[j], myList[j+1] = myList[j+1], myList[j]                 # swaps values if one is > than the other
                drawBars(createList, {j: createList.GREEN, j+1: createList.RED}, True)
                yield True                  # yield allows to iterate and pause sorting
    return myList

def insertionSort(createList, ascending = True):
    myList = createList.myList
    
    for i in range(1, len(myList)):
        key = myList[i]                 # current element being inserted into sorted list
        while True:
            ascending_sort = i > 0 and myList[i - 1] > key and ascending        # key < element to the left
            descending_sort = i > 0 and myList[i - 1] < key and not ascending   # key > element to the left

            if not ascending_sort and not descending_sort:
                break

            myList[i] = myList[i - 1]               # move larger element to the righ
            i = i - 1                         
            myList[i] = key 
            drawBars(createList, {i:createList.GREEN, i - 1: createList.RED}, True)     # green = current, red = compared
            yield True
    return myList

def quickSort(createList, ascending = True):
    myList = createList.myList

    #create dividing partition
    def partition(start, end, ascending):
        pivot = myList[end]
        i = start -1
        # determines whether an element belongs in the left or right half
        for j in range(start, end):
            if (myList[j] <= pivot and ascending) or (myList[j] >= pivot and not ascending):
                i += 1
                myList[i], myList[j] = myList[j], myList[i]
                drawBars(createList, {i: createList.GREEN, j: createList.RED}, True)        # green = i, red = j
                yield True
        
        myList[i + 1], myList[end] = myList[end], myList[i + 1]
        drawBars(createList, {i + 1: createList.BLUE, end: createList.RED}, True)           # red = original, blue = swapped
        yield True
        return i+1

    def sorter(start, end, ascending):
        if start < end:
            pivotPosition = yield from partition(start, end, ascending)     # partition values to find pivot index
            yield from sorter(start, pivotPosition - 1, ascending)          # sort the left half first
            yield from sorter(pivotPosition + 1, end, ascending)
    yield from sorter(0, len(myList) -1, ascending)

def selectionSort(createList, ascending = True):
    myList = createList.myList
    # i = current min, j = current item being traversed
    for i in range (len(myList)):
        currentMin = i
        for j in range(i+1, len(myList)):
            if (myList[j] < myList[currentMin] and ascending) or (myList[j] > myList[currentMin] and not ascending):
                currentMin = j 
            
            # create highlighted elements for selection bars
            drawBars(createList, {j: createList.RED, currentMin: createList.GREEN}, True)       # red = current element
            yield{j: createList.RED, currentMin: createList.GREEN}                              # green = current min    
        
        # swap new minumum with current minimum
        myList[i], myList[currentMin] = myList[currentMin], myList[i]
        # highlight swapped bars
        drawBars(createList, {i: createList.BLUE, currentMin: createList.GREEN}, True)          # blue = swapped bar
        yield{i: createList.BLUE, currentMin: createList.GREEN}
    # clears bars after finished execution    
    yield{}

def radixSort(createList, ascending = True):
    myList = createList.myList

    # Find max number 
    maxVal =  max(myList)
    maxDigits = len(str(maxVal))

    # Define sorting order
    order = 1 if ascending else -1

    # Perform counting sort for each digit
    place = 1       # start with least significant digit
    for _ in range(maxDigits):
        # create the buckets
        buckets = [[] for _ in range(10)]

        # Insert elements into buckets
        for num in myList:
            digit = (num // place) % 10
            buckets[digit].append(num)

        # Reconstruct list from buckets
        index = 0
        for bucket in (buckets if ascending else reversed(buckets)):
            for num in bucket:
                myList[index] = num
                index += 1
                drawBars(createList, {index: createList.GREEN}, True)
                yield True

            # Sort next significant digit
        place *= 10
    yield{}

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
    delay = 40                     # 100ms

    while run:
        runtime.tick(60)            # adjust speed of sorting

        if sorting and not paused:
            try:
                next(sortingAlgorithmGenerator)
                pygame.time.delay(delay)
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
            elif event.key == pygame.K_4 and not sorting:
                sortingAlgorithms = selectionSort
                sortingAlgorithmName = "Selection Sort"
            elif event.key == pygame.K_5 and not sorting:
                sortingAlgorithms = radixSort
                sortingAlgorithmName = "Radix Sort"
            elif event.key == pygame.K_UP:          # reduces delay, increases speed
                delay = max(10, delay - 10)         # min delay = 10ms
                print (f"Speed Increased: Delay = {delay} ms")
            elif event.key == pygame.K_DOWN:        # increase delay, slows down
                delay = min(500, delay + 10)        # max delay = 500ms 
                print (f"Speed Decreased: Delay = {delay} ms")

    pygame.quit()
    
if __name__ == "__main__":
    main()