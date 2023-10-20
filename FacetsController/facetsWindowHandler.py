import json
import os
import sys
from time import sleep
import mouse
import pyperclip
import screeninfo
import keyboard
import black
import logging

from PIL import ImageGrab, Image
from ScopeCreep.screenReading import screenReading
from ScopeCreep.stateManager.stateManager import StateManager
from monitorTypes import WindowSizes, MainWindowTabs


def check_if_duplicate(
    pytesspath: str, windowSize: WindowSizes, stateManager: StateManager = None
) -> bool:
    """
    Checks if the current claim is a duplicate
    :pytesspath: the path to pytesseract
    :windowSize: the size of desktop monitor
                - config in types.py
    :stateManager:? the state manager
        :stateKeys used: {
            "activeMainWindowTab",
            "isCurrentClaimDuplicate",
        }
    :return: True if the current claim is a duplicate, False otherwise
    """

    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file, "r") as f:
        config = json.load(f)

    activate_line_item_tab(windowSize)
    duplicate_claim_text = screenReading.get_text_from_rectangle(
        config[windowSize.value]["duplicateStaticAreaLocation"],
        pytesspath,
    )

    isDuplicate = duplicate_claim_text == "CDD _ Definite Duplicate Claim\n"

    stateManager.add_or_update_state("isCurrentClaimDuplicate", isDuplicate)
    stateManager.add_or_update_state("activeMainWindowTab", MainWindowTabs.lineItem.value)
    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    if actionList is not None:
        stateManager._call_functionType_list(actionList)

    return isDuplicate


def activate_line_item_tab(windowSize: WindowSizes, stateManager: StateManager = None):
    """
    Activates the line item tab
    :windowSize: the size of desktop monitor
                - config in types.py
    :stateManager:? the state manager
        :stateKeys used: {
            "activeMainWindowTab",
        }
    :return: None
    """
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file, "r") as f:
        config = json.load(f)

    mouse.move(
        config[windowSize.value]["lineItemTabPoint"][0],
        config[windowSize.value]["lineItemTabPoint"][1],
        absolute=True,
        duration=0.1,
    )
    mouse.click(button="left")

    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    if actionList is not None:
        stateManager._call_functionType_list(actionList)
    stateManager.add_or_update_state("activeMainWindowTab", MainWindowTabs.lineItem.value)


def activate_duplicate_claim_tab(
    windowSize: WindowSizes, stateManager: StateManager = None
):
    """
    Activates the duplicate claim tab
    :windowSize: the size of desktop monitor
                - config in types.py
    :stateManager:? the state manager
        :stateKeys used: {
            "activeMainWindowTab",
        }
    :return: None

    """
    config_file = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_file, "r") as f:
        config = json.load(f)

    mouse.move(
        config[windowSize.value]["duplicateTabPoint"][0],
        config[windowSize.value]["duplicateTabPoint"][1],
        absolute=True,
        duration=0.1,
    )
    mouse.click(button="left")

    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    if actionList is not None:
        stateManager._call_functionType_list(actionList)
    stateManager.add_or_update_state(
        "activeMainWindowTab", MainWindowTabs.duplicate.value
    )

def activateFacetsWindow(windowName:str, stateManager: StateManager = None):
    """
    Activates the window with the given name
    :windowName: the name of the window to activate
        - windows {
            "Open",
            "Facets",
            "Additional Modifiers",
            
        }
    """
    returnValue = None
    match windowName:
        case "Open":
            activateFacets()
            returnValue = openOpenWindow(stateManager)
        case "Additional Modifiers":
            returnValue = openAdditionalModifiersWindow(stateManager)
            
        case "Facets":
            activateFacets()
        case _:
            raise ValueError(f"Window name {windowName} is not valid")

    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    if actionList:
        stateManager._call_functionType_list(actionList)
    
    return returnValue

def openAdditionalModifiersWindow(stateManager: StateManager):
    keyboard.press_and_release("ctrl+t")
    logging.debug("Pressed ctrl+t")
    mouse.move(0,0)
    
    foundAdditionalModifiersWindow = screenReading.image_matches_known_active_window_state(
        Image.open(r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\additonalModifiers.Title.Active.png"),
        _get_config(stateManager.return_object(), "facetsLocation", (0, 0, 1920, 1080))
    )
    
    if foundAdditionalModifiersWindow:
        box = foundAdditionalModifiersWindow
        # box = _get_center_of_box(box)
        logging.debug(f"Found additional modifiers window at {box}")
        
        mouse.move(box[0], box[1], absolute=True, duration=0.1)
        mouse.click(button="left")
        return True
    
    return False
    
    
def activateFacets():
    mouse.move(300, 1000, absolute=True, duration=0.1)
    mouse.click(button="left")

def openOpenWindow(stateManager: StateManager):
    """
    Opens the open window
    """
    keyboard.press_and_release("ctrl+o")
    
    foundInactiveOpenWindow = screenReading.image_matches_known_active_window_state(
        Image.open(r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\openWindow.Title.InActive.png"),
        _get_config(stateManager.return_object(), "facetsLocation", (0, 0, 1920, 1080))
    )
    
    foundActiveOpenWindow = screenReading.image_matches_known_active_window_state(
        Image.open(r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\openWindow.Title.Active.png"),
        _get_config(stateManager.return_object(), "facetsLocation", (0, 0, 1920, 1080))
    )

    if foundInactiveOpenWindow or foundActiveOpenWindow:
        box = foundActiveOpenWindow if foundActiveOpenWindow else foundInactiveOpenWindow
        # box = _get_center_of_box(box)
        logging.debug(f"Found open window claim id input box at {box}")
        
        mouse.move(box[0], box[1], absolute=True, duration=0.1)
        mouse.click(button="left")
        return True

    return False

def open_new_claim(claimNumber: int, stateManager: StateManager):
    """
    Opens a new claim
    :claimNumber: the claim number to open
    """
    activateFacetsWindow('Open', stateManager)
    openWindowClaimIDInputBox = screenReading.image_matches_known_active_window_state(
        Image.open(r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\openWindow.ClaimID.Title.Active.png"),
        _get_config(stateManager.return_object(), "facetsLocation", (0, 0, 1920, 1080)),
    )
    
    if openWindowClaimIDInputBox:
        box = openWindowClaimIDInputBox
        box = _get_center_of_box(openWindowClaimIDInputBox)
        logging.debug(f"Found open window claim id input box at {box}")

        mouse.move(box[0], box[1] + 10, absolute=True, duration=0.1)
        mouse.click()
        sleep(0.1)
        keyboard.write(claimNumber)
        keyboard.press_and_release("enter")
    else:
        logging.debug("Could not find open window claim id input box")
        return False
    
    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    if actionList:
        stateManager._call_functionType_list(actionList)
    
    return True

def _get_center_of_box(box: tuple) -> tuple:
    return (
        box[0] + (box[2] / 2),
        box[1] + (box[3] / 2),
    )
    
def _get_config(options: object, key: str, default) -> object:
    """
    Gets a config value from the options object.
    :options: An object containing options.
    :key: The key of the config value.
    :default: The default value if the key is not found.
    :return: The value of the config.
    """
    if options:
        if key in options:
            return options[key]
    return default
