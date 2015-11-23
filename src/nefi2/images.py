# -*- coding: utf-8 -*-
"""
A class that represents an image object.
Used to handle io operations on image files and set various attributes.
"""
import ntpath
import cv2


class Image:
    def __init__(self, fpath):
        _head, _tail = ntpath.split(fpath)
        self.name = _tail or ntpath.basename(_head)
        self.signature = ''
        self.processed = False
        self.result = self.read_image(fpath)
        print '> Image: initialized, processed: %s' % self.processed

    def get_status(self):
        print '> Image: "%s" processed: %s' % (self.name, self.processed)

    def read_image(self, img_path):
        """
        Read in an image using its relative path.

        Args:
            img_path -- relative path to the image.
        Returns:
            numpy.ndarray -- numpy array of the image representation.
        """
        print '> Image: "%s" image loaded.' % self.name
        return cv2.imread(img_path, cv2.CV_LOAD_IMAGE_COLOR)


    @property
    def processed(self):
        return self.processed

    @processed.setter
    def processed(self, status):
        self.processed = status

    def save(self, output):
        """Save the result of algorithm processing."""
        self.result = output

    def sign(self, *signature):
        """Save the name of the algorithm that processed the image and its
        settings."""
        self.signature = signature


if __name__ == '__main__':
    pass
