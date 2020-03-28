import pygame 
import math

def findnoise2(x,y):
	n = int(x) + int(y) * 57
	allf = 0xFFFFFFFF
	an = (n << 13) & allf
	n = (an ^ n) & allf
	nn = (n*(n*n*60493+19990303)+1376312589)&0x7fffffff
	return 1.0-(float(nn)/1073741824.0);

def interpolate( a, b, x):
	ft = float(x * 3.1415927)
	f = float((1.0-math.cos(ft))* 0.5)
	return a*(1.0-f)+b*f;

def noise(x,y):
    floorx = float(int(x))
    floory = float(int(y))
    s=findnoise2(floorx,floory) 
    t=findnoise2(floorx+1,floory)
    u=findnoise2(floorx,floory+1) 
    v=findnoise2(floorx+1,floory+1)
    int1=interpolate(s,t,x-floorx) 
    int2=interpolate(u,v,x-floorx)
    return interpolate(int1,int2,y-floory) 

