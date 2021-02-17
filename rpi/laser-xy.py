import numpy as np
import xylaser as xy
import sys
from time import sleep
laser = xy.Laser()
dac = xy.Dac()

f = open(str(sys.argv[1]),'rt')
data = f.read()
data = data.split('\n')
while True:
    try:
        for i in range(0,len(data)):
            line = data[i]
            line = line.strip()
            if line == '':
                continue 
            d = line.split(',')
            #print(d)
            x = float(d[0])
            y = float(d[1])
            l = float(d[2])
            s = float(d[3])
            laser.laser(l)
            dac.dacwrite((x,y))
            sleep(s)
    except KeyboardInterrupt:
        laser.laser(0)
        laser.laser_end()
        f.close()
        exit(0)


                
        
        
