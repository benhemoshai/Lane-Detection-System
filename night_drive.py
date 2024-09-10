import numpy as np
import cv2

# Global variables to store the last detected lines
last_left_line = None
last_right_line = None

# Finds the slope and intercept of the left and right lanes of each image
def average_slope_intercept(lines):
    if lines is None:
        return None, None
    
    left_lines = []    # (slope, intercept)
    left_weights = []  # (length,)
    right_lines = []   # (slope, intercept)
    right_weights = [] # (length,)
     
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:  # Skip vertical lines
                continue
            # Calculate slope and intercept
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))  # Line length
            if slope < 0:  # Left lane (negative slope)
                left_lines.append((slope, intercept))
                left_weights.append((length))
            else:  # Right lane (positive slope)
                right_lines.append((slope, intercept))
                right_weights.append((length))
    
    # Weighted average of left and right lane lines
    left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if len(left_weights) > 0 else None
    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
    return left_lane, right_lane

# Converts the slope and intercept of each line into pixel points
def pixel_points(y1, y2, line):
    if line is None:
        return None
    slope, intercept = line
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    y1 = int(y1)
    y2 = int(y2)
    return ((x1, y1), (x2, y2))

# Creates full-length lane lines from pixel points
def lane_lines(image, lines):
    global last_left_line, last_right_line
    
    left_lane, right_lane = average_slope_intercept(lines)
    
    # If current lines are not detected, use the last detected lines
    if left_lane is None and last_left_line is not None:
        left_lane = last_left_line
    if right_lane is None and last_right_line is not None:
        right_lane = last_right_line
        
    last_left_line = left_lane
    last_right_line = right_lane
    
    y1 = image.shape[0]  # Bottom of the image
    y2 = y1 * 0.58       # Slightly higher
    left_line = pixel_points(y1, y2, left_lane)
    right_line = pixel_points(y1, y2, right_lane)

    return left_line, right_line

# Draws lane lines and a trapezoid polygon on the input image
def draw_lane_lines(image, lines, color=[0, 0, 255], thickness=12):
    line_image = np.zeros_like(image)
    
    for line in lines:
        if line is not None:
            cv2.line(line_image, *line, color, thickness)
    
    # Adds trapezoid polygon
    global last_left_line, last_right_line
    
    left_lane, right_lane = last_left_line, last_right_line
    
    if left_lane is not None and right_lane is not None:
        y1 = image.shape[0]
        y2 = y1 * 0.58
        left_line = pixel_points(y1, y2, left_lane)
        right_line = pixel_points(y1, y2, right_lane)
        
        # Define trapezoid polygon based on the points of the lines
        left_top, left_bottom = left_line
        right_top, right_bottom = right_line
        points = np.array([[left_top, right_top, right_bottom, left_bottom]], dtype=np.int32)
        cv2.fillPoly(line_image, points, (0, 255, 0))
    
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

# Converts the image to grayscale
def gray_im(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Applies Gaussian Blur to reduce noise using a (5, 5) kernel
def gaus_blur(frame):
    return cv2.GaussianBlur(gray_im(frame), (5, 5), 0)

# Applies thresholding and crops the image to a trapezoid shape to minimize noise and focus on the road
def crop_im(frame):
    _, white_mask = cv2.threshold(gaus_blur(frame), 240, 255, cv2.THRESH_BINARY)

    height, width = frame.shape[:2]
    roi_vertices = np.array([[(width * 0.05, height), (width * 0.48, height * 0.4),
                              (width * 0.355, height * 0.4), (width * 0.9, height)]], dtype=np.int32)

    roi_mask = np.zeros_like(white_mask)
    cv2.fillPoly(roi_mask, roi_vertices, 255)

    masked_lane = cv2.bitwise_and(white_mask, roi_mask)

    return masked_lane

# Detects edges using Canny edge detection
def canny(frame):
    return cv2.Canny(crop_im(frame), 50, 150)

# Detects lines using Hough Line Transform
def hough_lines(frame):
    return cv2.HoughLinesP(canny(frame), 1, np.pi / 180, threshold=40, minLineLength=20, maxLineGap=200)

# Main function for processing the video and detecting lane lines
def main():
    vid = cv2.VideoCapture('./night-drive-input.mp4')

    if not vid.isOpened():
        print("Could not open video")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('night-drive-output.avi', fourcc, 20.0, (int(vid.get(3)), int(vid.get(4))))

    while True:
        ret, frame = vid.read()
        if not ret:
            break
   
        lines = hough_lines(frame)
        left_line, right_line = lane_lines(frame, lines)
        result = draw_lane_lines(frame, [left_line, right_line])
        out.write(result)
        cv2.imshow('Lane Detection', result)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    vid.release()
    out.release()
    cv2.destroyAllWindows()

# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
