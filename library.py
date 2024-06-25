import sys
import os
import platform
import ctypes

script_dir = os.path.dirname(os.path.abspath(__file__))
system = platform.system()

# Load platform-specific dynamic library
if system == "Darwin":
    library_dir = os.path.join(script_dir, "sdk/Library/TeamTalk_DLL")
    library_path = os.path.join(library_dir, "libTeamTalk5.dylib")
    print("run on Darwin")
elif system == "Linux":
    library_dir = os.path.join(script_dir, "sdk/Library/TeamTalk_DLL")
    library_path = os.path.join(library_dir, "libTeamTalk5.so")
    print("run on Linux")
elif system == "Windows":
    library_dir = os.path.join(script_dir, "sdk/Library/TeamTalk_DLL")
    # Default TeamTalk DLL
    library_path = os.path.join(library_dir, "TeamTalk5.dll")
    # MPV DLL
    mpv_library_path = os.path.join(script_dir, "libmpv-2.dll")
    print("run on Windows")
else:
    print(f"Unsupported system: {system}")
    sys.exit(1)

# Load the dynamic library using ctypes
try:
    ctypes.cdll.LoadLibrary(library_path)
    if system == "Windows":
        # Additionally load the MPV library if on Windows
        ctypes.cdll.LoadLibrary(mpv_library_path)
except OSError as e:
    print(f"Error loading the library: {e}")
    sys.exit(1)

# TeamTalk Library
from sdk.Library.TeamTalkPy import TeamTalk5
from sdk.Library.TeamTalkPy.TeamTalk5 import *
