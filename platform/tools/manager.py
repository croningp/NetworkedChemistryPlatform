import logging

from random import uniform, randint
import os, inspect, sys, json, time, threading


""" PATHS """   
HERE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.join(HERE, '..')) # Base Project folder

DATA_FOLDER = os.path.join(HERE, "..", "..", "platform_run", "data")


LOG = "FILEPATH_GOES_HERE"


""" Twitterbot Module Imports """
from board import board
from pumps import operation as op
from camera import spectroscopy2 as spec

from camera import img_analysis as analysis
from utils import folder_creator, json_utils


class Manager(object):
    """
    Manager class for controlling the operations of the Hexbot.
    Mostly consists of wrappers to other modules.
    """
    def __init__(self):
        # The root folder for this current reaction run
        self.xp_folder = self.create_base_folder(DATA_FOLDER)

        # Starts the video recorder
        self.camera = spec.VideoRecorder(0)

        # Adds a basic logging functionality
        self.logger = self.setup_logger()

        # Initialises the stirring of the reaction vessel
        self.start_stirring()


    def create_base_folder(self, root_path):
        """ See utils/folder_creator.py """
        return folder_creator.create_base_folder(root_path)

    def create_img_filename(self, root_path, count, choice, *vals):
        """ See utils/folder_creator.py """
        return folder_creator.create_img_filename(root_path, count, choice, *vals)

    def dispense(self, pump_name, volume):
        """
        Dispenses a volume into the reaction vessel.

        Args:
            pump_name (str): The name of the pump
            volume (int/float): The volume to be dispensed
        """
        self.log_info('{0}  pumping {1}ml'.format(pump_name, volume))
        op.disp(pump_name, volume)

    def clean(self):
        """ Cleans the reaction vessel """
        self.log_info('Cleaning')
        op.cln_cycle()

    def dirty_clean(self, counter):
        """ Cleans the reaction vessel but leaves some reagents in the vessel """
        self.log_info('Dirty clean')
        op.dirty_clean(counter)

    def start_stirring(self):
        """ Starts stirring the reaction vessel """
        self.log_info('Stirrer on')
        op.stir.on()

    def save_frame(self, filename):
        """
        Saves an image from the camera to a location:

        Args:
            filename (str): Path to save the image to.
        """
        self.log_info('Saving image to {0}'.format(filename))
        self.camera.save_frame(filename)


    def setup_logger(self):
        """
        Sets up the logger for logging information to a file

        Returns:
            logger (Logger): Logging object for logging. Say logger one more time...
        """
        logger = logging.getLogger('Hexbot')
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(filename=LOG)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s::%(levelname)s -- %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def log_info(self, msg):
        """ Logs a message to the logfile """
        message = time.strftime('[%x_%X] ') + msg
        print(message)
        self.logger.info(message)
