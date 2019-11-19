#!/usr/bin/python3
import board
import neopixel
import neoAlphabet as neo
import time
import sys

# Addresses on NeoPixel are 0-255, sequential, serpentine from top left down.
# Map pixels to an 8x32 grid for ease of use
def initGrid():
    pxct=0 # pixel counter
    neoGrid=[] # mapping grid
    dorp=[] # dummy column
    rvs=False # False=top to bottom, True=bottom to top
    for i in range(256):
        pxct+=1
        dorp.append(i)
        if pxct==8:
            pxct=0
            if rvs:
                dorp.reverse()
                rvs=False
            else:
                rvs=True
            neoGrid.append(dorp)
            dorp=[]
    return neoGrid

# return an empty grid
def initBlankGrid():
    return [[0,0,0,0,0,0,0,0] for i in range(32)]

# Build a matrix by calling the bitmap for each character in the message
# and appending each column of it to the output matrix.
# Character bitmap definitions are in neoAlphabet.py and imported above
def genMessageGrid(message):
    thisMessage=[]
    for character in message:
        for column in neo.letterDict[character]:
            thisMessage.append(column)
    return thisMessage

# Take current 8x32 matrix to be displayed and write it to the NeoPixel
# object (assigned to 'p' below).
# RGB colors assignable, functionality to play with this possibly to be
# written in the future
# NOTE: writing 0 to a pixel is acceptable, don't need to write (0,0,0)
def genOutputGrid(thisGrid):
    for i in range(len(thisGrid)):
        for j in range(8):
            if thisGrid[i][j]==0:
                p[neoGrid[i][j]]=0
            else:
                p[neoGrid[i][j]]=(r,g,b)

# Scroll the message across the LED panel from right to left
def genScroll(thisGrid):

    # Make every message at least 32 columns by adding null columns at end
    if len(thisGrid)<32:
        for i in range(32-len(thisGrid)):
            thisGrid.append([0,0,0,0,0,0,0,0])

    # initial scroll-in
    for i in range(-1,-33,-1):
        thisSlice=initBlankGrid()
        ct=0
        for j in range(i,0,1):
            thisSlice[j]=thisGrid[ct]
            ct+=1
        genOutputGrid(thisSlice)
        p.show()
        time.sleep(delay)
        
    # middle section scrolling window
    # for messages that are longer than 32 columns, this just
    # creates a 32-column sliding window across the message matrix
    if len(thisGrid)>32:
        for i in range(1,len(thisGrid)-31,1):
            thisSlice=thisGrid[i:i+32]
            genOutputGrid(thisSlice)
            p.show()
            time.sleep(delay)
            
    # final scroll-off
    # This just progressively left-shifts the final frame,
    # appending null columns on the right until it's blank
    for i in range(32):
        for j in range(31):
            thisSlice[j]=thisSlice[j+1]
        thisSlice[-1]=[0,0,0,0,0,0,0,0]
        genOutputGrid(thisSlice)
        p.show()
        time.sleep(delay)

# stock code from Adafruit to cycle colors, not being used
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b)

# stock code from Adafruit to make random rainbow patterns, not being used
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(256):
            pixel_index = (i * 256 // 256) + j
            p[i] = wheel(pixel_index & 255)
        p.show()
        time.sleep(wait)
        

delay=float(sys.argv[2]) # 0.01 seems optimal
p=neopixel.NeoPixel(board.D18,256,auto_write=False) # object that writes to panel
neoGrid=initGrid()
r,g,b=20,20,20
thisMessage=genMessageGrid(sys.argv[1])
genScroll(thisMessage)
p.fill(0)
p.show()

