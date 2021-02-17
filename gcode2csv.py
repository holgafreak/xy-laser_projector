import numpy as np
import cv2
import sys
import argparse

myperse = argparse.ArgumentParser()
myperse.add_argument('-i','--input',type=str,required=True,help='input fname')
myperse.add_argument('-o','--output',type=str,required=True,help='output file')
myperse.add_argument('-p','--power',type=float,default=0.8,help='laser power (0.8)')
myperse.add_argument('-s','--speed',type=float,default=0.001,help='delay between points')
myperse.add_argument('-d','--display',action='store_true',default=False,help='show svg')
args = myperse.parse_args()

 
#import xylaser as xy
#dac = xy.Dac()
#laser = xy.Laser()

fo = open(args.output,'wt')
with open(args.input,'rt') as f:
    spede = args.speed
    
    line = 'M0'
    oldline = 'something'
    x = 0
    y = 0
    F = 0
    color = (0,0,0)
    line = f.readline()
    if line.startswith('( bounds'):
        values = line.split()
        xmin = float(values[2])
        ymin = float(values[3])
        xmax = float(values[4])
        ymax = float(values[5])
    else:
        raise ValueError('bounds out of bounds')
    distance =1
    maxl = 800
    scalex = maxl/(xmax-xmin)
    scaley = maxl/(ymax-ymin)
    if scalex > scaley:
        scale = scaley
        scaleV = 2.047/(ymax-ymin)/scale
    else:
        scale = scalex
        scaleV = 2.047/(xmax-xmin)/scale
    print(f'XY  {scale} V {scaleV:}') #.format(scale,scaleV))
    color=(255,0,0)
    circleim = np.zeros((maxl,maxl,3),dtype=np.uint8)
    lzr = args.power
    pwr = 0
    firstG0 = False
    while line != '':
        line=f.readline()
        if line == oldline:
            continue
        oldline = line
        if line.startswith('G1'):
            
            cmds = line.split()
            xval = 0.0
            yval = 0.0
            fval = 0
            for i in range(len(cmds)):
                if cmds[i].startswith('X'): 
                    xval = float(cmds[i].strip('X'))
                if cmds[i].startswith('Y'):
                    yval = float(cmds[i].strip('Y'))
                if cmds[i].startswith('F'):
                    fval = int(cmds[i].strip('F'))
           
            #xval -= xmin
            #yval -= ymin
            #xval *= scale
            #yval *= scale
            xval *= scale
            yval *= scale
            d = np.sqrt((x-xval)**2+(y-yval)**2)
            if d < 1:
                continue
            angle = np.arctan2(yval-y,xval-x)
            nsplit = int(d/1);
            #print(nsplit)
            if nsplit > 1:
                steps = np.linspace(0,d,nsplit,endpoint=False)
                xsteps = np.cos(angle)*steps+x
                ysteps = np.sin(angle)*steps+y
            else:
                xsteps = [xval]
                ysteps = [yval]
                nsplit = 1
            for i in range(nsplit):
                try:
                    xpt = np.floor(xsteps[i])
                    ypt = np.floor(ysteps[i])
                    #print(f'x {xpt} y {ypt}')
                    xdac = xsteps[i]*scaleV
                    ydac = ysteps[i]*scaleV
                    if xdac > 2.047:
                        xdac = 2.047 # 2.047
                    if ydac > 2.047:
                        ydac = 2.047
                    if ydac < 0:
                        ydac = 0
                    if xdac < 0:
                        xdac = 0
                except IndexError:
                    raise IndexError('idx = {} len = {}'.format(i,len(xsteps)))
                xyline =f'{xdac: 1.6f},{ydac: 1.6f},{lzr},{spede}\n' #.format(xdac,ydac,lzr)
                fo.write(xyline)
                #dac.dacwrite((xdac,ydac))
                cv2.circle(circleim,(int(xpt),int(ypt)),1,(0,255,0),-1)
                cv2.imshow('G',circleim)
                k = cv2.waitKey(5)
                if k == 27:
                    exit(0)
            x = xsteps[-1]
            y = ysteps[-1]
            
        if line.startswith('G0'):
            cmds = line.split()
            if 'M' in line:
                continue
            #print('g0')
            xval = 0.0
            yval = 0.0
            for i in range(len(cmds)):
                if cmds[i].startswith('X'): 
                    xval = float(cmds[i].strip('X'))
                if cmds[i].startswith('Y'):
                    yval = float(cmds[i].strip('Y'))
            xval *= scale
            yval *= scale
            xdac = xval*scaleV
            ydac = yval*scaleV
            xpt = int(xval)
            ypt = int(yval)
            xyline =f'{xdac: 1.6f},{ydac: 1.6f},0.0,0.001\n'
            fo.write(xyline)
            x = xval
            y = yval
            cv2.circle(circleim,(xpt-1,ypt-1),1,(0,0,255),-1)
                    
            color=(0,255,255) #laser.laser(100)
            #lzr = pwr
        elif line.startswith('M8'):
            color = (255,255,0)
            lzr = 0
        elif line.startswith('G05'):
            pwr =100 # int(line.split()[1].strip('P'))
'''
img = cv2.imread(str(sys.argv[1]),1)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_,thr = cv2.threshold(imgray,127,255,0)
_,contours,hierarchy = cv2.findContours(thr,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#for i in range(0,len(contours)):
#    print('len ith {} {}'.format(i,len(contours[i])))
#print(' cont len {} h len {}'.format(len(contours[4]),len(hierarchy)))
#laser.laser(100)
#cc = contours[4]*2.047/np.max(contours[4])
#print(cc[0][0])
ig = np.zeros((img.shape))
#cn = contours[2]
cv2.drawContours(ig,contours,-1,(0,255,255),3)
cv2.imshow('CC',ig)
cv2.waitKey(10)
ii=np.zeros((800,800,3),dtype=np.uint8);
while True:
    for i in range(0,len(contours)):
        cc = contours[i]*800/np.max(contours[i])
        l = len(cc)
        color = (int(255/(l+1)),255,0)
        for j in range(0,len(cc)):
            #dac.dacwrite((cc[j][0][0],cc[j][0][1]))
            cv2.circle(ii,(int(cc[j][0][0]),int(cc[j][0][1])),1,color,-1)
    cv2.imshow('C',ii)
    cv2.waitKey(-1)
    break
'''
#laser.laser(0)
#laser.laser_end()

#cv2.drawContours(img,contours,3,
print('Done')
cv2.waitKey(-1)
f.close()
fo.close()

exit(0)

                
        
        
