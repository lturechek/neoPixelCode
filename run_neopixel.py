import board
import neopixel
import neoAlphabet as neo
import time
import sys

def initGrid():
    pxct=0
    rowct=0
    neoGrid=[]
    dorp=[]
    rvs=False
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
            rowct+=1
    return neoGrid

def initBlankGrid():
    return [[0,0,0,0,0,0,0,0] for i in range(32)]
    
def genMessageGrid(message):
    thisMessage=[]
    for character in message:
        for column in neo.letterDict[character]:
            thisMessage.append(column)
    return thisMessage

def genOutputGrid(thisGrid):
    #print ("{} columns".format(len(thisGrid)))
    for i in range(len(thisGrid)):
        for j in range(8):
            if thisGrid[i][j]==0:
                p[neoGrid[i][j]]=0
            else:
                p[neoGrid[i][j]]=(r,g,b)

def genScroll(thisGrid):
    totalLength=len(thisGrid)+64
    if len(thisGrid)<32:
        for i in range(32-len(thisGrid)):
            thisGrid.append([0,0,0,0,0,0,0,0])
    #print(thisGrid)
    #print ('\n\n\n')

    # initial scroll-in
    for i in range(-1,-33,-1):
        #print (i)
        thisSlice=initBlankGrid()
        ct=0
        for j in range(i,0,1):
            thisSlice[j]=thisGrid[ct]
            ct+=1
        #print (thisSlice)
        genOutputGrid(thisSlice)
        p.show()
        time.sleep(delay)
        
    # middle section scrolling window
    if len(thisGrid)>32:
        for i in range(1,len(thisGrid)-31,1):
            thisSlice=thisGrid[i:i+32]
            genOutputGrid(thisSlice)
            p.show()
            time.sleep(delay)
            
    # final scroll-off
    for i in range(32):
        for j in range(31):
            thisSlice[j]=thisSlice[j+1]
        thisSlice[-1]=[0,0,0,0,0,0,0,0]
        genOutputGrid(thisSlice)
        p.show()
        time.sleep(delay)


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


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(256):
            pixel_index = (i * 256 // 256) + j
            p[i] = wheel(pixel_index & 255)
        p.show()
        time.sleep(wait)
        
#time.sleep(10)
delay=float(sys.argv[2])
p=neopixel.NeoPixel(board.D18,256,auto_write=False)
neoGrid=initGrid()
r,g,b=20,20,20
thisMessage=genMessageGrid(sys.argv[1])
#print (thisMessage)
#print (len(thisMessage))
genScroll(thisMessage)
#genOutputGrid(thisMessage)
p.fill(0)
p.show()
#rainbow_cycle(.001)
p.fill(0)
p.show()
#p.show()
#time.sleep(int(sys.argv[2]))
#p.fill(0)
#p.show()
