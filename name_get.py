import win32gui
import win32process
import psutil
#Get Spotify Window Info

char = "-"
result = ""
spotify_pid = None
def get_info_windows(option):
    global char
    global result
    global spotify_pid

    pids = []
    try:
        result = ""
        for proc in psutil.process_iter(['name', 'pid']):
            if proc.name().lower() == 'spotify.exe':
                pids.append(proc.info["pid"])

        def callaback(hwnd, pid):
            global result
            global spotify_pid
            pid_list = win32process.GetWindowThreadProcessId(hwnd)
            if pid == pid_list[1]:
                if char in win32gui.GetWindowText(hwnd):
                    result = win32gui.GetWindowText(hwnd)
                    spotify_pid = pid
                    return
                elif win32gui.GetWindowText(hwnd) == "Spotify Free":
                    result = "Paused - Paused"
                    return

        for i in pids:
            win32gui.EnumWindows(callaback, i)
    except:
        print("Error while getting song info")
    
    parts = result.split(char)
    try:
        if option == "artist":
            return parts[0]
        if option == "song":
            return parts[1]
    except:
        return None