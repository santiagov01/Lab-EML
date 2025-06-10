import serial
import numpy as np
import cv2

ser = serial.Serial('COM7', 9600, timeout=1)
kNumRows = 96
kNumCols = 96

def read_image_from_serial(ser):
    image_data = []
    in_image = False
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "<image>":
            in_image = True
            image_data = []
        elif line == "</image>":
            if in_image:
                break
        elif in_image:
            image_data.extend([int(x) for x in line.split(',') if x])
    return np.array(image_data, dtype=np.int8).reshape((kNumRows, kNumCols))

while True:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
    if line == "<image>":
        # Read image data
        image_data = []
        while True:
            img_line = ser.readline().decode('utf-8', errors='ignore').strip()
            if img_line == "</image>":
                break
            image_data.extend([int(x) for x in img_line.split(',') if x])
        if len(image_data) == kNumRows * kNumCols:
            img = np.array(image_data, dtype=np.int8).reshape((kNumRows, kNumCols))
            img_disp = ((img.astype(np.int16) + 128)).astype(np.uint8)
            # Resize image for display
            img_resized = cv2.resize(img_disp, (768, 768), interpolation=cv2.INTER_NEAREST)
            cv2.imshow('Arduino Image', img_resized)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Warning: Incomplete image data received.")
    elif line:
        print(line)

cv2.destroyAllWindows()