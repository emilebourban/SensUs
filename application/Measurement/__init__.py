import skimage
from skimage import measure
import os
import re
import numpy as np

class Measure:

    def __init__(self, path, spot_position = (0,0)):
        self.path = path
        self.spot_position = (0,0)
        self.threshold = 12

    def binarize(threshold,img):
        return img < threshold

    def count(list1, l, r):
        return len(list(x for x in list1 if l <= x <= r))

    def count_particle_one_image(self, img, spot_position, radius, threshold):
        total_particle = []

        for i in range(len(circle_coor)):
            coordinate_0 = circle_coor[i][0]
            coordinate_1 = circle_coor[i][1]
            new_img = img[coordinate_0-radius:coordinate_0+radius,coordinate_1-radius:coordinate_1+radius]
            new_img = new_img/255
            b = binarize(threshold,new_img)
            all_labels = measure.label(b,neighbors=4)
            some_props = measure.regionprops(all_labels)
            areas = [p.area for p in some_props]
            particle = count(areas,8,30)
            total_particle.append(particle)

        return(sum(total_particle)/len(total_particle))

    def count_particle(imgs,circle_coor,radius,n,threshold):

        particles = [count_particle_one_image(imgs[i],circle_coor,radius,threshold) for i in range(n)]
        return particles



    #fait appel aux placements de cercle dans layer
    def spot_dectection(self):
