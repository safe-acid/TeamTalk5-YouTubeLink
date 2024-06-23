import sys, os, platform, ctypes

script_dir = os.path.dirname(os.path.abspath(__file__))
system = platform.system()
   # Construct the full path to the dynamic library file MAC/Linux/Win
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
    library_path = os.path.join(library_dir, "TeamTalk5.dll")
    print("run on Windows")
else:
    print(f"Unsupported system: {system}")
    sys.exit(1)
    
# Load the dynamic library using ctypes
try:
    ctypes.cdll.LoadLibrary(library_path)
except OSError as e:
    print(f"Error loading the library: {e}")
    sys.exit(1)
    

from sdk.Library.TeamTalkPy import TeamTalk5
from sdk.Library.TeamTalkPy.TeamTalk5 import *