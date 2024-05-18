import cv2

# Load the video file
cap = cv2.VideoCapture(r"C:\Users\eqbal\Downloads\WhatsApp Video 2024-05-03 at 21.47.24_f01f5427.mp4")

# The frame number you want to access
frame_number = 42

# Set the position of the next frame to be read or decoded in the video
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)

# Read the next frame from the video
ret, frame = cap.read()

if ret:
    # If the frame is read correctly, save it as an image file
    cv2.imwrite('frame42.jpg', frame)
else:
    print("Error: can't fetch the frame.")

# When everything done, release the capture
print(cap)