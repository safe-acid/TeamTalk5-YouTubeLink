import os
import platform
import sys
import requests
from urllib.parse import urljoin
import shutil
import py7zr
import platform

# Define base URL and list of file names (modify if needed)
BASE_URL = "http://www.bearware.dk/teamtalksdk/v5.15a/"
FILE_NAMES = {
    "Linux": "tt5sdk_v5.15a_ubuntu22_x86_64.7z",
    "Darwin": "tt5sdk_v5.15a_macos_x86_64.7z",
    "Windows": "tt5sdk_v5.15a_win64.7z"
}
# Windows-specific file download URL
# Determine the appropriate DLL file URL based on the system architecture
if platform.system() == "Windows":
    if platform.architecture()[0] == "64bit":
        DLL_FILE_URL = "https://sourceforge.net/projects/mpv-player-windows/files/libmpv/mpv-dev-x86_64-20240630-git-68a1a38.7z/download"
    else:
        DLL_FILE_URL = "https://sourceforge.net/projects/mpv-player-windows/files/libmpv/mpv-dev-i686-20240630-git-68a1a38.7z/download"


def download_file(url, filename):
    """Downloads a file from the specified URL and saves it locally."""
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise exception for failed downloads

    with open(filename, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print(f"Downloaded {filename} successfully.")


def extract_archive(filename, extract_dir):
    """Extracts the contents of an archive to the specified directory using py7zr."""
    os.makedirs(extract_dir, exist_ok=True)  # Create extraction directory if needed
    with py7zr.SevenZipFile(filename, mode='r') as archive:
        archive.extractall(path=extract_dir)
    print(f"Extracted {filename} to {extract_dir}.")
    os.remove(filename)  # Delete the archive file after extraction
    print(f"Deleted {filename}.")

def move_files_to_sdk(extracted_dir, sdk_dir):
    """Move files from extracted directory to sdk directory, preserving structure."""
    extracted_subdir = next(os.path.join(extracted_dir, d) for d in os.listdir(extracted_dir) if os.path.isdir(os.path.join(extracted_dir, d)))
    for item in os.listdir(extracted_subdir):
        s = os.path.join(extracted_subdir, item)
        d = os.path.join(sdk_dir, item)
        if os.path.isdir(s):
            shutil.move(s, d)
        else:
            shutil.move(s, sdk_dir)
    shutil.rmtree(extracted_subdir)  # Remove the now-empty extracted subdirectory
    print(f"Moved all files from {extracted_subdir} to {sdk_dir} and removed the extracted subdirectory.")

def essential_sdk(sdk_dir):
    """Keeps only the essential files and directories in the sdk directory."""
    essential_paths = [
        os.path.join(sdk_dir, "Library"),
        os.path.join(sdk_dir, "License.txt")
    ]
    
    for item in os.listdir(sdk_dir):
        item_path = os.path.join(sdk_dir, item)
        if item_path not in essential_paths:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    print(f"Kept only essential files and directories in {sdk_dir}.")

def install_dll_for_windows():
    """Download and extract specific DLL for Windows, then move the DLL to the project root and clean up."""
    if platform.system() == "Windows":
        print("Downloading MPV DLL for Windows")
        #using along with mpv 1.0.7
        filename = "mpv-dev-x86_64-v3-20240623-git-265056f.7z"
        local_path = os.path.join(os.getcwd(), filename)
        extract_dir = os.path.join(os.getcwd(), "extracted_dll")

        # Download and extract DLL
        download_file(DLL_FILE_URL, local_path)
        print("Extracting downloaded DLL")
        extract_archive(local_path, extract_dir)
        

        # Move DLL to project root and clean up
        dll_path = os.path.join(extract_dir, "libmpv-2.dll")
        if os.path.exists(dll_path):
            shutil.move(dll_path, os.getcwd())  # Move the DLL to the project root
            print(f"Moved 'libmpv-2.dll' to {os.getcwd()}.")
        else:
            print("DLL file not found after extraction.")

        # Remove the extracted directory
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
            print(f"Deleted {extract_dir} directory.")

        print("DLL installation complete!")
        
def install_sdk():
    print("Downloading SDK")
    """Downloads, extracts, and installs the TeamTalk SDK."""
     # Check if the 'sdk' directory exists
    if os.path.exists("sdk"):
        print("SDK directory already exists. Skipping installation.")
        return  # Exit the function if directory exists
    else:
        sdk_dir = os.path.join(os.getcwd(), "sdk")  # Create directory for downloaded SDKs
        os.makedirs(sdk_dir, exist_ok=True)

        # Determine the appropriate filename based on the platform
        system = platform.system()
        filename = FILE_NAMES.get(system)
        
        if not filename:
            print(f"No SDK available for the current platform: {system}")
            sys.exit(1)

        download_url = urljoin(BASE_URL, filename)
        local_path = os.path.join(sdk_dir, filename)
        extract_dir = os.path.join(sdk_dir, "extracted_temp")

        download_file(download_url, local_path)
        print("Extracting downloaded files")
        extract_archive(local_path, extract_dir)
        move_files_to_sdk(extract_dir, sdk_dir)  # Move files to sdk directory
        essential_sdk(sdk_dir)  # Keep only the essential files and directories

        print("TeamTalk SDK installation complete!")
        print("You can run command\n python devices.py")
        print("Define your input sound device and save ID in\n config.py")

if __name__ == "__main__":
    
    # Install the TeamTalk SDK
    install_sdk()
    install_dll_for_windows()