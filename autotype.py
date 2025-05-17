#!/usr/bin/python3
'''
Author: Ethan Ashley
Version: 2.3

This script in intended to take input from the user in some way and type it out as if the user was typing it
This started out as something I wrote in about 30-40 minutes out of necessity
It has since been rewritten as part of a course project to make it a lot better
All features from V1 are here, plus some
It is intended to be extendable and customizable
'''


from evdev import uinput, ecodes as e
from time import sleep
import tempfile
import os
from subprocess import call

DEBUG = False  # Enable debug messages
INPUT_METHOD = 'editor'  # Desired input method to use, checked by a switch case
DELAY_CHAR = 0.05  # Seconds between each character
DELAY_LINE = 0.3  # Seconds waited after a newline
DELAY_START = 3  # Seconds before the program starts to type
CONVERT_CHARS = True  # Whether or not to process user input and convert any characters to other characters

# Mapping for characters that require the shift key
mapCharsShift = {
    '!': e.KEY_1,
    '@': e.KEY_2,
    '#': e.KEY_3,
    '$': e.KEY_4,
    '%': e.KEY_5,
    '^': e.KEY_6,
    '&': e.KEY_7,
    '*': e.KEY_8,
    '(': e.KEY_9,
    ')': e.KEY_0,
    '_': e.KEY_MINUS,
    '+': e.KEY_EQUAL,
    '{': e.KEY_LEFTBRACE,
    '}': e.KEY_RIGHTBRACE,
    '|': e.KEY_BACKSLASH,
    ':': e.KEY_SEMICOLON,
    '"': e.KEY_APOSTROPHE,
    '<': e.KEY_COMMA,
    '>': e.KEY_DOT,
    '?': e.KEY_SLASH,
    '~': e.KEY_GRAVE,
}
# Mapping for characters that do not require the shift key and do not have an automatic mapping
mapCharsNoShift = {
    ' ': e.KEY_SPACE,
    '\n': e.KEY_ENTER,
    '\t': e.KEY_TAB,
    '[' : e.KEY_LEFTBRACE,
    ']' : e.KEY_RIGHTBRACE,
    '\\': e.KEY_BACKSLASH,
    ';' : e.KEY_SEMICOLON,
    '\'': e.KEY_APOSTROPHE,
    '.' : e.KEY_DOT,
    ',' : e.KEY_COMMA,
    '/' : e.KEY_SLASH,
    '`' : e.KEY_GRAVE,
    '-' : e.KEY_MINUS,
    '=' : e.KEY_EQUAL,
}

# Convert characters which require the shift key
conv_mapCharsShift = {
    '‘' : e.KEY_APOSTROPHE,  # This is a open smart quote. I am not sure why office programs insist on these, but IMO they should just be single quotes and there is no purpose for a new character
    '’' : e.KEY_APOSTROPHE,  # This is a close smart quote. See above
}

# Convert characters which do not require the shift key
conv_mapCharsNoShift = {
    '–' : e.KEY_MINUS,  # This is an en-dash. Textbooks and office programs insist that these are used instead of dashes, and I am not a fan
}


def initialize():
    if CONVERT_CHARS:
        setCharacterConversions()
        
    #TODO autodetect the enviroment so we may type accordingly
    global ENVIRONMENT
    ENVIRONMENT = 'linux:wayland' 
    
    #TODO create a system of passing arguments to the program to override hardcoded settings
    
    global EDITOR
    EDITOR = os.environ.get('EDITOR') #TODO handle the case where this is not defined and a default must be used
    EDITOR = 'nano'

# Print messages to the console only when debugging is on
def message(msg: str):
    if DEBUG: print(msg)
    
# Modify the character mappings to contain mappings that are untrue
# Used as a means to covnert characters inputted by the user into other characters
def setCharacterConversions():
    mapCharsShift.update(conv_mapCharsShift)
    mapCharsNoShift.update(conv_mapCharsNoShift)

# Fetches input from the user using various methods
def getInput():
    message(INPUT_METHOD)
    match INPUT_METHOD:
        case 'test':
            userInput = 'Hello World! 1234567890 !@#$%^&*()_+{}|:"<>?~\''
            userInput += '\n'  # Required since the last newline is always removed. Causes a bug otherwise.
        case 'basic':  # Only does a single line. Not capable of multiple lines, but will always work.
            userInput = input("Enter the string to be typed: ")
        case 'pure':  # A Method of fetching multi-line input from the user in a pure python way. 
            print("Enter or Paste your content. Ctrl-D (linux) or Ctrl-Z (windows) to end.")
            userInput = ''
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                userInput += line
                userInput += '\n'
        case 'editor':
            with tempfile.NamedTemporaryFile(suffix=".tmp", delete=True, mode='w+') as tf:
                message(tf.name)
                # Open the file with the text editor
                call([EDITOR, tf.name])
                # Read the file data into a variable
                userInput = tf.read()
        case 'clipboard':
            print('INPUT METHOD NOT YET CREATED')
            exit()
        case 'file':
            print('INPUT METHOD NOT YET CREATED')
            exit()
        case _:
            print(f"INPUT_METHOD variable is not properly defined. \n\tINPUT_METHOD = {INPUT_METHOD}")
            exit()
    # Remove only the last newline which gets added on automatically
    if userInput.endswith("\n"): userInput = userInput[:-1]
    message(repr(userInput))
    return userInput

# Convert a character into a key code
def char_to_keycode(char):
    # Letters
    if char.isalpha():
        if char.isupper():
            return (getattr(e, f'KEY_{char.upper()}'), True)
        else:
            return (getattr(e, f'KEY_{char.upper()}'), False)
    # Numbers
    elif char.isdigit():
        return (getattr(e, f'KEY_{char}'), False)
    # Shift-less characters which cannot be done automatically
    elif char in mapCharsNoShift:
        return (mapCharsNoShift[char], False)
    # Shift characters which cannot be done automatically
    elif char in mapCharsShift:
        return (mapCharsShift[char], True)
    # Cry if a character cannot be converted
    else:
        print('A character in the input cannot be mapped to a keycode')
        raise ValueError(f"Unsupported character: {char}")

def typeKeycodes(keycodes):
    match ENVIRONMENT:
        case 'linux:wayland':  #TODO This may work on XOrg as well, I have not checked
            with uinput.UInput() as ui:
                sleep(1)
                DELAY_CHAR_RATIO = 0.01
                for keycode, use_shift in keycodes:
                    message(f"{keycode} {use_shift}")
                    if use_shift:  # Activate shift if required
                        ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 1)
                    # Press the desired character
                    ui.write(e.EV_KEY, keycode, 1)
                    sleep(DELAY_CHAR*DELAY_CHAR_RATIO)
                    ui.write(e.EV_KEY, keycode, 0)
                    if use_shift:
                        ui.write(e.EV_KEY, e.KEY_LEFTSHIFT, 0)
                    # Signal to the system that new events are available
                    ui.syn()
                    # Delay between key presses
                    if keycode == e.KEY_ENTER:
                        sleep(DELAY_LINE)
                    sleep(DELAY_CHAR - (DELAY_CHAR*DELAY_CHAR_RATIO))
        case _:  #TODO Add more environments
            print(f"Unknown detected environment: {ENVIRONMENT}")
            exit()

###############################################################################

# Setup the program
initialize()

# Get the input
inputString = getInput()

if inputString == '':
    print('No input provided, exiting...')
    exit()

# Convert all characters into an array of key codes
inputKeycodes = [char_to_keycode(char) for char in inputString]
message(inputKeycodes)

print(f"Typing in {DELAY_START} seconds...")
sleep(DELAY_START-1) # There is a 1 second delay for setup in the typeKeycodes function

# Type the string
typeKeycodes(inputKeycodes)


''' REFERENCES
https://codereview.stackexchange.com/questions/190865/call-a-text-editor-from-within-a-python-script-to-get-user-input
https://python-evdev.readthedocs.io/en/latest/usage.html

'''
