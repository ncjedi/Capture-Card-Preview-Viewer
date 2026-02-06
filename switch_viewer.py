import cv2
import pyaudio
import threading
from find_webcam_mic import get_switch_audio
import win32api
import time
from wakepy import keep

def hide_mouse():
    time.sleep(1)
    print("hi")

#thing to hide mouse
def mouse_evt(event, x, y, flags, param):
    """Callback function to hide the cursor."""
    win32api.SetCursor(None) # This hides the cursor

# 1. Setup Video Capture
cap = cv2.VideoCapture(0)

cv2.namedWindow('Webcam Feed', cv2.WINDOW_NORMAL)

#make it full screen
cv2.setWindowProperty('Webcam Feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#mouse hide thing call
cv2.setMouseCallback('Webcam Feed', mouse_evt)

#get index
index = get_switch_audio()

# 2. Setup Audio Capture (simplified)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, input_device_index=index, output_device_index=p.get_default_output_device_info()['index'], frames_per_buffer=1024)

def audio_preview():
    while True:
        data = stream.read(1024)
        stream.write(data)
        # Add audio processing/playback here
        pass

# Run audio in a separate thread
threading.Thread(target=audio_preview, daemon=True).start()

# 3. Main Loop for Video

with keep.presenting():
    while True:
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow('Webcam Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to exit
            break

cap.release()
cv2.destroyAllWindows()