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
            facetsWindowHandler.open_new_claim(clipContents, self.stateManager)
        
    
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
    logging.basicConfig(level=4)
    logging.debug("Starting controller.py")
    
    if 0:
        screenReading.create_rectangle_from_two_clicks({"copyToClipboard": True})
        os._exit(0)
        
    stateManager = StateManager()
    
    stateManager.add_or_update_state("facetsLocation", (0,0, 1910, 1070))
    stateManager.add_or_update_state("afterFunctionActions", [
        sleep(1),
    ])

    controller = Controller(stateManager)
    controller.open_new_claim_from_clipboard()
    