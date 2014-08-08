'''
Created on 17-Jul-2014

@author: nikita
'''

from datetime import datetime
import psutil
   
    
import os

nw = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
myProcess = psutil.Process(os.getpid())
tim = datetime.fromtimestamp(myProcess.create_time()).strftime("%Y-%m-%d %H:%M:%S")
#a = time.strptime(nw,"%Y-%m-%d %H:%M:%S")    
#b = time.strptime(tim,"%Y-%m-%d %H:%M:%S")  
print nw
print tim
d1 = datetime.strptime(nw, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(tim, "%Y-%m-%d %H:%M:%S")
print abs((d2 - d1))

#print abs((b - a).days)
    
    
    
