#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
The main nefi2 startup script.
It loads extension loader and initializes UI.
It also enables console batch processing mode.
"""


from ext_loader import ExtensionLoader


def main():
    """Start the main pipeline and UI"""
    exloader = ExtensionLoader()
    # init_UI()  # not yet implemented!


if __name__ == '__main__':
    main()