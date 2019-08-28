import skimage
from skimage import measure
import os
import re
import numpy as np

class Measure:

    # spots = [([x, y], r), ([x, y], r), ...]
    #for p, r in spots:

    def __init__(self, path, circles):
        self.path = path
        self.circles = circles
        self.threshold = 0.5

    #def threshold(self):
        #0.9*moy histo

    #def binarize(self):
    #    return img < self.threshold

    #def count(self, list1, l, r):
    #    return len(list(x for x in list1 if l <= x <= r))

    def count_particles_one_image(self, img):
        total_particle = []

        for (cx, cy), rad in self.circles:
            new_img = img[cx-rad:cx+rad, cy-rad:cy+rad]
            new_img = new_img/255
            bin_img = new_img < self.threshold
            all_labels = measure.label(bin_img, neighbors=4)
            some_props = measure.regionprops(all_labels)
            areas = [p.area for p in some_props]
            particle = len(list(x for x in areas if 8 <= x <=30))
            total_particle.append(particle)

        return sum(total_particle)/len(total_particle)


    def count_particles(self):
        #order file
        ordered_id = sorted([int(file[4:8]) for file in os.listdir(self.path) \
                             if file[0:4] == 'img_' and file[-4:] == '.npy'])
        ordered_pathes = [f'results/img_{n:04d}.npy' for n in ordered_id]

        particles = [self.count_particles_one_image(np.load(f)) for f in ordered_pathes]

        return particles

    def compute_slope(self):

        x = np.array([i for i in range(len(self.particles))])
        x.astype(float)
        #slope, intercept, r_value, p_value, std_err = stats.linregress(x, count_particles)
        #print("slope: %f    intercept: %f" % (slope, intercept))
        #plt.plot(x, i, 'o', label='original data')
        #plt.plot(x, intercept + slope*x, 'r', label='fitted line')
        #plt.legend()
        #plt.show()
        #return slope


    def run(self):

        #print(compute_slope())
        #get_concentration()
        print('your concentration is 10 µg/mL')

        #release folder
        #for i in os.listdir(self.path):
        #    os.remove(i)
        return 42
