from shapely.geometry import Point, Polygon
from shapely.affinity import translate
import numpy as np
import math

def is_valid_corner(points, a, b, c):
    fig = Polygon(points)

    x, y = axis_ajust(a, b, c)
    xoff = -0.01 if x else 0.01
    yoff = -0.01 if y else 0.01

    if fig.covers(translate(Point(b), xoff=xoff, yoff=yoff)):
        return True
    return False

def three_points_angle(a, b, c):
    v0 = np.array(a) - np.array(b)
    v1 = np.array(c) - np.array(b)

    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return np.around(np.degrees(angle), 5)

def two_points_slope(v0, v1):
    theta = math.atan2(v1[1] - v0[1], v1[0] - v0[0])
    slope = math.degrees(theta)
            
    if slope < 0:
        slope = 360 + slope
        
    return np.around(slope, 5)



def axis_ajust(a, b, c):
    x = False
    y = False
        
    if c[0] > b[0] and a[1] < b[1] or a[1] < b[1] and c[1] > b[1]: # |-
        y = True
                
    if a[0] < b[0] and c[1] < b[1] or a[1] < b[1] and c[0] < b[0]: # -|
        x = True
        y = True
                
    if a[1] > b[1] and c[0] < b[0] or a[0] < b[0] and c[1] > b[1]: # _|
        x = True
        
    return x,y

def get_corner_from_index(index, points):
    a = points[index-1]
    b = points[index]
    c = points[index+1]
    
    if index == 0:
    	a = points[len(points) - 2]

    return a,b,c

def normalize(x, y):
    x = np.around(np.array(x) - min(x), 5)
    y = np.around(np.array(y) - min(y),5)
    
    return list(zip(x,y))

def get_unique_cuts(cuts):
    unique_cuts = []
    for cut in cuts:
        c = Polygon(cut)
        unique = True
        for uc in unique_cuts:
            if c.equals(uc[0]):
                uc[1] += 1
                unique = False
                break
        if unique:
            unique_cuts.append([c, 1])
            
    unique_cuts = [[list(cut.exterior.coords), count] for cut, count in unique_cuts]

    return unique_cuts

def get_optimized_cuts(cuts, ceramic):
    optimized_cuts = []	
    for cut in cuts:
    	points = cut.exterior.coords
    	
    	best_cut_boundary = 0
    	best_cut = cut
    	slopes = get_slopes(points)
    	
    	for slope in slopes:
    		cut_ = rotate(cut, -slope)
    		x,y = cut_.exterior.coords.xy
    		points = normalize(x, y)

    		cut_ = Polygon(points)
    		xmin, ymin, xmax, ymax = cut_.bounds
    		
    		if not cut_.within(ceramic):
    			continue
    		
    		i = 0
    		for i in range(0, len(points) - 1):
    			a,b,c = get_corner_from_index(i, points)

    			new_cut = cut_

    			if b[0] == xmin and b[1] == ymax:
    				new_cut = translate(cut_, xoff=-xmin, yoff=ceramic_height - ymax)

    			if b[0] == xmin and b[1] == ymin:
    				new_cut = translate(cut_, xoff=-xmin, yoff=-ymin) 

    			if b[0] == xmax and b[1] == ymax:
    				new_cut = translate(cut_, xoff=ceramic_width - xmax, yoff=ceramic_height - ymax)

    			if b[0] == xmax and b[1] == ymin:
    				new_cut = translate(cut_, xoff=ceramic_width - xmax, yoff=-ymin)
    			
    			boundary_intersection = ceramic.boundary.intersection(new_cut.boundary).length
    			if boundary_intersection > best_cut_boundary:
    				best_cut = new_cut
    				best_cut_boundary = boundary_intersection

    			i += 1

    	optimized_cuts.append(best_cut)	
    		
    return optimized_cuts

def get_slopes(points):
    slopes = set()
    for i in range(0, len(points) - 1):
        a,b,c = get_corner_from_index(i, points)
        slope = two_points_slope(a,b) % 90
        slopes.add(slope)
            
    return slopes
