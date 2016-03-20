#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main nefi2 startup script.
It loads extension loader and initializes UI.
It also enables console batch processing mode.
"""
from nefi2.model.ext_loader import ExtensionLoader
from nefi2.model.pipeline import Pipeline
from nefi2.view.main_controller import MainView

import sys
import argparse
import ctypes
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
import qdarkstyle


__authors__ = {"Pavel Shkadzko": "p.shkadzko@gmail.com",
               "Dennig Groß": "gdennis91@googlemail.com",
               "Philipp Reichert": "prei@me.com"}


def gui_mode():
    """
    Start NEFI2 GUI
    """
    myappid = 'nefi2.0' # arbitrary string
    if sys.platform == 'win32' or sys.platform == 'win64':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    extloader = ExtensionLoader()
    pipeline = Pipeline(extloader.cats_container)
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setQuitOnLastWindowClosed(True)
    app.setWindowIcon(QtGui.QIcon("./icons/nefi2.ico"))
    wnd = MainView(pipeline)
    wnd.load_dark_theme(app)
    wnd.show()
    sys.exit(app.exec_())


def batch_mode(args):
    """
    Process images in console mode

    Args:
        | *args* (dict) : argument dict returned by ArgumentParser

    """
    extloader = ExtensionLoader()
    pipeline = Pipeline(extloader.cats_container)
    # processing args values
    if args.pipeline:
        # load the specified pipeline file
        # default url
        pipeline.load_pipeline_json(args.pipeline)
    if args.dir:
        # load the images from the specified source dir
        pipeline.set_input(args.dir)
    elif args.file:
        # load a single image
        pipeline.set_input(args.file)
    if args.out:
        pipeline.set_output_dir(args.out)
    pipeline.process_batch()


def main(args):
    """
    Load all available categories and algorithms into the pipeline.

    Args:
        | *args* : a Namespace object of supplied command-line arguments
    """
    if args.dir or args.file:
        batch_mode(args)
    else:
        gui_mode()


if __name__ == '__main__':
    prs = argparse.ArgumentParser(description="""NEFI2 is a tool created to
    extract networks from images. Given a suitable 2D image of a network as
    input, NEFI2 outputs a mathematical representation of the structure of the
    depicted network as a weighted undirected planar graph.""")
    prs.add_argument('-p', '--pipeline',
                     help='Specify a saved pipeline xml file.',
                     required=False)
    prs.add_argument('-d', '--dir',
                     help='Specify a directory with images '
                          'for batch processing.',
                     required=False)
    prs.add_argument('-f', '--file',
                     help='Specify an image file to process.',
                     required=False)
    prs.add_argument('-o', '--out',
                     help='Specify output directory.',
                     required=False)
    arguments = prs.parse_args()

    main(arguments)
