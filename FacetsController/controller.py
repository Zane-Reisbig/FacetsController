import os
from sys import path
path.append('..')

import pyperclip
import re
import logging
import keyboard
import win32
import win32gui

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
        
        afterClaimActions = self.stateManager.check_if_state_exists("afterClaimActions")
        if afterClaimActions is not None:
            self.stateManager._call_functionType_list(afterClaimActions)

    def initialize_claim_for_processing(self, openClaim: bool = True):
        """
        Initializes a claim for processing
        :openClaim: if True, opens a new claim from the clipboard
        """
        if openClaim:
            self.open_new_claim_from_clipboard()
            
        # make sure we are at the top of the claim ✅
        # navigate down 1 submenu using ctrl+down ✅
        # adjudicate claim and make sure window responds to keypresses -
        # - before continuing
        # claim is ready to be processed
        
        self._navigate_to_indicitive_submenu()
        self._hit_key_n_times("ctrl+down", 1)
        self.adjuciate_claim()
        
    def adjuciate_claim(self):
        self._hit_key_n_times("f3")
        facetsWindowHandler.activateFacetsWindow("Additonal Modifiers")
        
    
    def _wait_for_window_to_respond(self):
        while True:
            pass
    
    def _check_top_window_name(self, windowName:str, fuzzy:bool = False):
        topMostWindow = win32gui.GetForegroundWindow()
        topMostWindowName = win32gui.GetWindowText(topMostWindow)
        
        if fuzzy:
            return windowName in topMostWindowName
        
        return windowName == topMostWindowName
    
    def _navigate_to_indicitive_submenu(self):
        """
        Navigates to the indicitive submenu
        """
        self._hit_key_n_times("ctrl+up", 6) 
    
    def _write_sentence(self, sentence: str):
        """
        writes a sentence
        """
        keyboard.write(sentence)
        sleep(0.1)
    
    def _hit_key_n_times(self, key: str, n: int = 1):
        """
        Hits a key n times
        :key: the key to hit
        :n: the number of times to hit the key
        """
        for _ in range(n):
            keyboard.press_and_release(key)
            sleep(0.1)
    
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
    # controller.open_new_claim_from_clipboard()
    controller.initialize_claim_for_processing()
    