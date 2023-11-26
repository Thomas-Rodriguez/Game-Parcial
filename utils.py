import pygame
import os

BASE_IMAGE_PATH = "data/images/"

def load_image(path):
    #convert() turns the internal representation of the imag in pygame more efficent to render
    img = pygame.image.load(BASE_IMAGE_PATH + path).convert()
    img.set_colorkey((0, 0, 0)) #makes the background of the png, that is already black a semi transparent
    return img

def load_images(path):
    images = []
    #for img_name in os.listdir(BASE_IMAGE_PATH + path): taking into account its looking into the files in alphabetic order 0 first, 8 last
    for img_name in sorted(os.listdir(BASE_IMAGE_PATH + path)):
        images.append(load_image(path + "/" + img_name))

    return images

class Animation:
    def __init__(self, images, duration = 5, loop = True) :
        self.images = images
        self.loop = loop
        self.duration = duration
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.duration * len(self.images) - 1)
            if self.frame >= self.duration * len(self.images) - 1:
                self.done = True 
            #min() takes two values and return the lower one of inside a list/tuple/dict/set ect

    def get_img(self):
        return self.images[int(self.frame / self.duration)]
    
    
