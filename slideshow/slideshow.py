"""This module is used to play a slide show of images using PIL"""
import PIL.Image
import json
import time


class SlideShow:
    def __init__(self, queue = list):
        if type(queue) != type(list):
            queue = list()
        self.queue = queue


    def add_image(self, img: object):
        """
        This module add an image or list of images to the slide show queue
        :param img: Image to add to the slide show
        :return: None
        """
        self.queue.append(img)


    def play(self):
        """
        This module plays the slide show using pillow
        :return: None
        """
        for image in self.queue:
            PIL.Image.open(image)
            time.sleep(10)

