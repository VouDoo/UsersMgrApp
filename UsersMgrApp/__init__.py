#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UsersMrgApp
=========

Version: 1.0.0

Description: Python project for LP ASSR 4/4 - IUT Senart

Author: Maxence GRYMONPREZ
Email: maxgrymonprez@live.fr

Versions notes:

1.0.0
-----
Date: 2017-03-06
- First release
"""


def main(args):
    """
    :param args:
    :rtype: object

    """
    init_db()
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    # Libs are part of standard distribution for python 3
    import sys
    # Application libs
    from gui import *
    sys.exit(main(sys.argv))
