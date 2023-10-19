import os
from sys import path
path.append('..')

import pyperclip
import re
import logging

from time import sleep

from ScopeCreep.screenReading import screenReading
from ScopeCreep.stateManager.stateManager import StateManager

import facetsWindowHandler

class Controller:
    def __init__(self, stateManager: StateManager = None):
        self.stateManager = stateManager
    
    def open_new_claim_from_clipboard(self):
        """
        Opens a new claim from the clipboard
        """
        clipContents = pyperclip.paste()
        
        if self._validate_claim_number(clipContents):
            if facetsWindowHandler.open_new_claim(clipContents, self.stateManager):
                logging.debug("Claim opened")
            else:
                raise Exception("Claim not opened")

        
    
    def _validate_claim_number(self, number: int) -> bool:
        
        re_12_digits = re.compile(r"\d{12}")
        re_2_chars = re.compile(r"\d{5}[A-Z]{2}\d{5}")

        logging.debug(f"Validating claim number: {number}")
        if re_12_digits.match(number):
            logging.debug("Claim number is 12 digits")
            return True
        elif re_2_chars.match(number):
            logging.debug("Claim number is modified 2 character")
            return True
        else:
            logging.debug("Claim number is invalid")
            return False


if __name__ == "__main__":
    logging.addLevelName(4, "DEBUG")
    logging.addLevelName(5, "ERROR")
    logging.basicConfig(level=5, format="%(levelname)s: %(message)s")

    # logging.disable(5)
    logging.disable(4)

    logging.debug("Starting controller.py")
    
    
    if 0:
        screenReading.create_rectangle_from_two_clicks({"copyToClipboard": True})
        os._exit(0)
        
    stateManager = StateManager()
    
    stateManager.add_or_update_state("facetsLocation", (0,0, 1920, 1080))
    stateManager.add_or_update_state("afterFunctionActions", [lambda: sleep(1), ])
    logging.error(f"State manager id: {stateManager.return_object()}")

    controller = Controller(stateManager)
    controller.open_new_claim_from_clipboard()
    