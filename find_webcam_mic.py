import pyaudio

def get_switch_audio():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        #print(f"Index {i}: {info['name']}")
        if info['name'] == "Microphone (USB Audio Device)":
            p.terminate()
            return i
    p.terminate()
    exit()