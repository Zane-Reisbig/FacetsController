import json
import os
import sys
import mouse
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

def activate(windowName:str, stateManager: StateManager = None):
    """
    Activates the window with the given name
    :windowName: the name of the window to activate
        - windows {
            "Open",
            "Facets",
            
        }
    """
        
    def openOpenWindow(stateManager: StateManager = None):
        """
        Opens the open window
        """
        activateFacets()
        keyboard.press_and_release("ctrl+o")
        
        logging.debug(f"Facets Location: {_get_config(stateManager, 'facetsLocation', None)}")
        
        foundInactiveOpenWindow = screenReading.image_matches_known_active_window_state(
            Image.open(r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\openWindow.Title.InActive.png"),
            _get_config(stateManager, "facetsLocation", (0, 0, 1920, 1080))
        )
        
        foundActiveOpenWindow = screenReading.image_matches_known_active_window_state(
            Image.open(r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\openWindow.Title.Active.png"),
            _get_config(stateManager, "facetsLocation", (0, 0, 1920, 1080))
        )
        
        if foundInactiveOpenWindow:
            mouse.move(100, 100, absolute=True, duration=0.1)
            mouse.click(button="left")
        
        if foundActiveOpenWindow:
            mouse.move(100, 100, absolute=True, duration=0.1)
            mouse.click(button="left")


        print(f"Found inactive open window?: {foundInactiveOpenWindow}")
        print(f"Found active open window?: {foundActiveOpenWindow}")
    
    def activateFacets():
        mouse.move(10, 10, absolute=True, duration=0.1)
        mouse.click(button="left")
        
        
        
    match windowName:
        case "Open":
            openOpenWindow()
        case "Facets":
            activateFacets()
        case _:
            raise ValueError(f"Window name {windowName} is not valid")

    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    logging.debug(f"Action list: {actionList}")
    if actionList is not [None]:
        stateManager._call_functionType_list(actionList)


def open_new_claim(claimNumber: int, stateManager: StateManager = None):
    """
    Opens a new claim
    :claimNumber: the claim number to open
    """
    activate('Open', stateManager)
    openWindowClaimIDInputBox = screenReading.image_matches_known_active_window_state(
        Image.open(
            r"C:\Users\zan61897\OneDrive - Corewell Health\Desktop\Garbage\USE THIS FOR NEW PROJECTS PLEASE\FacetsController\.venv\FacetsController\FacetsWindowHandlerData\openWindow.ClaimID.InputBox.png"
        ),
        _get_config(stateManager.return_object(), "facetsLocation", (0, 0, 1920, 1080)),
    )
    
    actionList = stateManager.check_if_state_exists("afterFunctionActions")
    if actionList is not None:
        stateManager._call_functionType_list(actionList)
        
    
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
