#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  getc.py The universal char reader for Python
#  Local Mini Opensource AI. Prototype 1 version.
#  
#  Contributors:
#  Felipe Ruiz Peixoto a.k.a eitabyte <eitabytegamer@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#   

# This function can be used with:
# from getc import getc
# char = getc()
# Return the character or None if something wrong
# In some cases, input()[0] will be called as a fallback option.
# Please, keep this code minimal, well-documented and with many try-except blocks
# to avoid main program's break. 
# The order of code blocks for each system type should remain from the smallest
# to the largest code block.
def getc():
    # Import to discover the actual operating system
    try:
        from platform import system
    except ImportError:
        print("Your system dont have the platform module to use getc.py")
        return None
    except:
        print("Error importing platform module for getc.py")
        return None
    # Detecting actual operating system
    sysname = system()
    # - - - WINDOWS SYSTEM
    if "windows" in sysname.lower():
        # Necessary import
        try:
            from msvcrt import getch
        except ImportError:
            print("Your system dont have msvcrt to use getc.py")
            return None
        except:
            print("Error importing msvcrt module for getc.py")
            return None
        # Using the function getch from msvcrt
        try:
            return getch().decode('utf-8')
        except:
            print("Error using getch() for getc.py")
            return None
    # - - - POSIX *NIX SYSTEMS
    elif (
    "linux" in sysname.lower()
    or "darwin" in sysname.lower()
    or "bsd" in sysname.lower()
    ):
        # Necessary imports to configure Linux terminal with fallback
        try:
            from sys import stdin
        except ImportError:
            print("Your system dont have the sys module to use getc.py")
            return None
        except:
            print("Error importing sys module for getc.py")
            return None
        try:
            from termios import tcgetattr, tcsetattr, ICANON, ECHO, TCSADRAIN
        except ImportError:
            print("Your system dont have the termios module to use getc.py")
            print("If you are on Android, make sure you have real terminal acess")
            print("and termios module installed.")
            return None
        except:
            print("Error importing termios module for getc.py")
            return None
        # Get the standard input file descriptor integer
        file_descriptor_int = stdin.fileno()
        # Get the actual terminal input settings to be recovered
        old_terminal = tcgetattr(file_descriptor_int)
        # Copy the actual terminal settings to be changed
        new_terminal = old_terminal.copy()
        # Change the actual terminal settings to non canonical mode
        # with echo off, keeping the other bit flags untouched
        new_terminal[3] &= ~ICANON & ~ECHO
        # Setting the terminal to non canonical mode
        tcsetattr(file_descriptor_int, TCSADRAIN, new_terminal)
        try:
            # Try to get the user character input
            return stdin.read(1)
        except:
            print("Error with stdin at getc.py.")
            return None
        finally:
            # Recover the old terminal settings 
            tcsetattr(file_descriptor_int, TCSADRAIN, old_terminal)
    # - - - NOT SUPPORTED SYSTEM
    else:
        print("Operating system not supported by getc.py yet")
        return None
        
# FOR TESTING ONLY
testvar = getc()
print("You pressed: "+testvar)
testvar = input("Now, test normal input: ")
print("You writed: "+testvar)

# - - - DOCUMENTATION
# The termios module for Linux uses a list of terminal settings:
# [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
#  iflag at position [0] controls the input processing with the bit flags:
#  * IGNBRK: Ignore break conditions
#  * BRKINT: Send SIGINT to break conditions
#  * ICRNL: Change CR to NL in input
#  * INLCR: Change NL to CR in input
#  * ISTRIP: Clear the 8th bit
#  oflag at position [1] controls the output processing:
#  * OPOST: Turn on output processing
#  * ONLCR  Change NL to CR-NL on output
#  * OCRNL Change CR to NL on output
#  cflag at position [2] is hardware settings:
#  * CSIZE: CS5, CS6, CS7 and CS8 bit sizes
#  * CSTOPB: 2 stop bits
#  * CREAD: Allows reception
#  * PARENB: Allows parity
#  * CLOCAL: Ignore modem's control lines
#  lflag at position [3] control the local settings:
#  * ICANON: Control's the line buffer (pressing enter to process entire line)
#  * ECHO: Control the echo (show what user is writing)
#  * ECHOE: Erase characters with backspace
#  * ISIG: Control's signals (CTRL+Z, CTRL+C)
#  * IEXTEN: Control's extended functions
#  ispeed at position [4] and ospeed at position[5] is obsolete
#  cc at position [6] is an array with special characters and timeouts
# The msvcrt for Windows is more direct and have the getch function that return
# the byte of the character.
