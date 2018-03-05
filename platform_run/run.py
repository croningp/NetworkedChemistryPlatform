"""
This is your surface level experiment script which you can mould to your own preferences.
Using the Manager class, you have access to pumps/camera/stirrer etc.
Use calls to the manager to obtain your desired functionality
"""
import os
import sys
import inspect

HERE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
platform_path = os.path.join(HERE, "..", "platform")
sys.path.append(platform_path)

from tools.manager import Manager

class RunPlatform(object):
    """
    Class for running the platform
    Populate with your own custom methods for experiment
    """
    def __init__(self):
        self.mgr = Manager()

    """
    Add your own methods below
    """

    