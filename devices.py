import library 
from library import ttstr
tt = library.TeamTalk5.TeamTalk()

def defaultAudioDevices():
        msg = "\n\nDefault Audio Input Devices:\n"
        for device in tt.getSoundDevices():
            msg += f"Device ID: {device.nDeviceID},\n" \
               f"Sound System: {device.nSoundSystem},\n" \
               f"Device Name: {ttstr(device.szDeviceName)},\n\n " \

        print(msg)
        
if __name__ == "__main__":
    defaultAudioDevices()