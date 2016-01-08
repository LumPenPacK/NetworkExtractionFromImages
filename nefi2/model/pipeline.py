# -*- coding: utf-8 -*-
"""
This module contains the class Pipeline that represents a central control
mechanism over a sequential image processing pipeline. It controls all the
available image processing categories, handles processing results and works
as an mediator between the algorithms and UI.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.curdir, 'model'))
sys.path.insert(0, os.path.join(os.curdir, 'model', 'categories'))
sys.path.insert(0, os.path.join(os.curdir, 'model', 'algorithms'))
from _category import Category
from collections import OrderedDict
import demjson

__authors__ = {"Pavel Shkadzko": "p.shkadzko@gmail.com",
               "Dennis Groß": "gdennis91@googlemail.com"}


class Pipeline:
    def __init__(self, categories):
        """
        Args:
            *categories*: OrderedDict of category names and their instances

        public Attributes:
            | *available_cats* (dict): dict of {Category name: Category}
            | *executed_cats* (list): a list of Categories in the pipeline
            | *pipeline_path* (str): a path to a saved pipelines
            | *image_path* (str): a path to an image file
            | *out_dir* (str): a path where processing results are saved
            
        """
        self.available_cats = categories
        self.executed_cats = [v for v in self.available_cats.values()]
        self.pipeline_path = 'saved_pipelines'  # default dir
        self.image_path = 'IMAGE'
        self.out_dir = os.path.join(os.getcwd(), 'output')
        # debugging only
        # print(self.executed_cats)
        
    def new_category(self, name, position):
        """
        Create a new instance of Category.

        Args:
            | *name* (str): Category name
            | *position* (int): a category index in self.executed_cats
                
        """
        self.executed_cats.insert(position, Category(name))

    def move_category(self, origin_pos, destination_pos):
        """
        Move Category instance within the pipeline using indices.

        Args:
            | *origin_pos* (int): Category index number
            | *destination_pos* (int): new position for Category

        """
        self.executed_cats.insert(destination_pos,
                                  self.executed_cats[origin_pos])
        del self.executed_cats[origin_pos]

    def delete_category(self, position):
        """
        Remove Category from the pipeline.

        Args:
            *position* (int): Category index number

        """
        del self.executed_cats[position]

    def process(self):
        """
        Execute current pipeline starting from the first modified image
        processing category.

        Returns:
            *results* (list): a list of processing results

        """
        results = []
        image = self.image_path
        results.append(image)
        # find the first category which contains the modified algorithm
        for idx, cat in enumerate(self.executed_cats):
            if cat.active_algorithm.AlgBody().modified:
                start_from = idx, cat.name
                break
        # execute the pipeline from the category with the modified algorithm
        for num, cat in enumerate(self.executed_cats[idx:]):
            results.append(cat.process(results[num]))
        return results

    def change_algorithm(self, position, alg_name):
        """
        Set the algorithm of the category in position to modified = *True*

        Args:
            | *position*: list index of the category in the pipeline
            | *alg_name*: algorithm name
            
        """
        for v in self.executed_cats[position].available_algs.values()[0]:
            if alg_name == v.Body().get_name():
                v.Body().set_modified()

    def get_executed_cats(self):
        """
        Create and return a list of currently executed categories.
        
        *No cats are actually harmed during execution of this method >_<*

        Returns:
            *executed_cat_names*: list of Category names
            
        """
        executed_cat_names = [cat.get_name() for cat in self.executed_cats]
        return executed_cat_names

    def get_algorithm_list(self, position):
        """
        Get names of all available algorithms for the category in position.
        Sort the list and return.

        Args:
            *position* (int): Category index number

        Returns:
            *alg_names* (list): a sorted list of algorithm names
            
        """
        alg_names = self.available_cats.values()[position].alg_names
        alg_names.sort()
        return alg_names

    def get_image(self, img_path):
        """
        Receive and save the path to the image which will be processed.
        
        Args:
            *img_path* (str): image path
            
        """
        self.image_path = img_path

    def save_pipeline_xml(self, save_path):
        pass
    
    def set_input_dir(self, dir_path):
        """
        Set the directory where original images are located.
        <Used in console mode>.
        
        Args:
            *dir_path* (str): directory path of original images
        
        """
        self.input_dir = dir_path
        
    def set_output_dir(self, dir_path):
        """
        Create and set the directory where to save the results of processing.
        <Used in console mode>.
        
        Args:
            *dir_path* (str): directory path for processing results
        
        """
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        self.output_dir = dir_path

    def load_pipeline_json(self, url):
        """
        Loads the Pipeline from the url location and parses all data to
        create the corresponding executed_cats

        Args:
            | *url*: location identifier for the pipeline.json
            
        """
        try:
            json = demjson.decode_file(url, "UTF-8")
        except JSONError:
            e = sys.exc_info()[0]
            print("Unable to parse " + url + " trace: " + e)

        for alg in json.keys():
            alg_json = json[alg]
            cat = Category(alg_json["type"])
            cat.active_algorithm = cat._get_available_algorithms()[alg]
            self.executed_cats.append(cat)

            for (name, value) in alg.keys():
                cat.active_algorithm.find_ui_element(name).set_value(value)

    def save_pipeline_json(self, name,  url):
        """
        Goes trough the list of executed_cats and calls for every
        selected_algorithm its report_pip method. With the returned
        dictionary's, it builds the pipeline.json file and stores it
        at the given url location on the file system.

        Args:
            | *url*: location identifier for the pipeline.json
            
        """
        alg_reports = []

        for cat in self.get_executed_cats():
            alg = cat.active_algorithm
            name, alg_dic = alg.report_pip()
            alg_reports.append([name, alg_dic])

        with open(url + name + ".txt", "wb+") as outfile:
            ord_alg_reps = OrderedDict(alg_reports)
            outfile.write(bytes(demjson.encode(ord_alg_reps), "UTF-8"))


if __name__ == '__main__':
    pass
