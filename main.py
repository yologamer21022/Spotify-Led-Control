import color
import name_get
import downloader
import time
#----------------------Arduino Setup----------#
import serial
import serial.tools.list_ports
arduino_name = "USB Serial Device"
arduino_port = "COM5"
ports = list(serial.tools.list_ports.comports())

connected = 0
def connecting():
    global arduino
    global connected
    try:
        for p in ports:
            if arduino_port in p.device:
                port = p.name
                print(p.name)

                arduino = serial.Serial(port, 9600)
                connected = 1
            # else:
            #     connected = 0
    except:
        connected = 0
connecting()
#-----------------------------------------#

name_cache = ""
img_pth = "cache/album_image.jpg"
colors = []

while True:
    
    if connected == 0:
        connecting()
        print("con")
    else:

        song = name_get.get_info_windows("song") + " " + name_get.get_info_windows("artist")
        if song != name_cache and "Spotify Free" not in song:
            time.sleep(.1)
            song = name_get.get_info_windows("song") + " " + name_get.get_info_windows("artist")
            if song != name_cache and "Spotify Free" not in song:
                downloader.main(song)
                print(song)

                colors = color.get_dominant_colors(img_pth, 1, 320, 320)

                name_cache = song
                raw_data = ""
                data = ""
                delimeter = "|"
                for i in colors:
                    raw_data = str(i) + delimeter + raw_data
                    data = raw_data.rstrip(delimeter)
                arduino.write(str(data).encode())      

    time.sleep(1)    