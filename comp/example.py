import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

# Define color range for the object you want to track (red example)
lower_color = np.array([0, 120, 70])
upper_color = np.array([10, 255, 255])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the selected color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Clean the mask (remove noise)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours (shapes) in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If at least one contour is found
    if contours:
        # Get the largest contour (most likely the object)
        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)

        if area > 500:  # ignore very small objects
            # Compute bounding box
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Compute object center
            cx = x + w//2
            cy = y + h//2
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

            # Display some info
            cv2.putText(frame, f"Tracking Object - Area: {int(area)}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    # Show results
    cv2.imshow("Mask", mask)
    cv2.imshow("Tracking", frame)

    # Quit on 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

