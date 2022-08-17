import cv2
from ..config.config import Config


is_debug = Config.is_debug()
debug_folder = Config.debug_folder()

class ImageLogger():

    @staticmethod
    def log_image(name, img):
        if is_debug:
            cv2.imwrite(debug_folder + name, img)