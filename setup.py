import os, platform, sys, requests, shutil
from urllib.parse import urljoin
import py7zr

BASE_URL = "https://www.bearware.dk/teamtalksdk/"
SDK_VER  = os.getenv("TT_SDK_VER", "v5.19a")           # фиксируем 5.19a, можно переопределить
FLAVOR   = os.getenv("TT_SDK_FLAVOR", "tt5sdk")        # tt5sdk | tt5prosdk

def resolve_filename():
    sysname = platform.system()
    machine = platform.machine().lower()

    if sysname == "Linux":
        # arm64 → raspbian_arm64, иначе ubuntu22_x86_64
        if "aarch64" in machine or "arm64" in machine:
            return f"{FLAVOR}_{SDK_VER}_raspbian_arm64.7z"
        else:
            return f"{FLAVOR}_{SDK_VER}_ubuntu22_x86_64.7z"

    if sysname == "Darwin":
        return f"{FLAVOR}_{SDK_VER}_macos_universal.7z"

    if sysname == "Windows":
        return f"{FLAVOR}_{SDK_VER}_win64.7z"

    print(f"No SDK mapping for platform: {sysname} ({machine})")
    sys.exit(1)

def download_file(url, filename):
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    with open(filename, "wb") as f:
        for chunk in r.iter_content(1024 * 64):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {filename}")

def extract_archive(filename, extract_dir):
    os.makedirs(extract_dir, exist_ok=True)
    with py7zr.SevenZipFile(filename, mode="r") as z:
        z.extractall(path=extract_dir)
    print(f"Extracted to {extract_dir}")
    os.remove(filename)

def move_files_to_sdk(extracted_dir, sdk_dir):
    # берем первый подпапку внутри extracted_dir
    sub = next(
        os.path.join(extracted_dir, d)
        for d in os.listdir(extracted_dir)
        if os.path.isdir(os.path.join(extracted_dir, d))
    )
    for item in os.listdir(sub):
        s = os.path.join(sub, item)
        d = os.path.join(sdk_dir, item)
        shutil.move(s, d)
    shutil.rmtree(sub)
    print(f"Moved SDK content into {sdk_dir}")

def essential_sdk(sdk_dir):
    keep = {os.path.join(sdk_dir, "Library"), os.path.join(sdk_dir, "License.txt")}
    for item in os.listdir(sdk_dir):
        p = os.path.join(sdk_dir, item)
        if p not in keep:
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
    print("Kept essentials only")

def install_sdk():
    if os.path.exists("sdk"):
        print("SDK directory already exists. Skipping installation.")
        return

    sdk_dir = os.path.join(os.getcwd(), "sdk")
    os.makedirs(sdk_dir, exist_ok=True)

    fname = resolve_filename()
    url = urljoin(urljoin(BASE_URL, SDK_VER + "/"), fname)

    local = os.path.join(sdk_dir, fname)
    extract_dir = os.path.join(sdk_dir, "extracted_temp")

    download_file(url, local)
    extract_archive(local, extract_dir)
    move_files_to_sdk(extract_dir, sdk_dir)
    essential_sdk(sdk_dir)

    print("TeamTalk SDK installation complete!")
    print("Run: python radio.py --devices to get your Audio IDs")

if __name__ == "__main__":
    install_sdk()