# Lane Detection System 🚗🛣️

**Lane Detection System** is a Python-based application designed to detect lane markings on the road from video footage. The system processes both day and night driving videos, applying various computer vision techniques to accurately identify lane lines in different lighting conditions.

## Preview

![Lane Detection Preview](./lanedetection.gif)

## Overview

The **Lane Detection System** processes videos to detect lane lines, leveraging OpenCV and NumPy for image processing. Two separate Python scripts are available for day and night driving conditions. These scripts apply various techniques like Gaussian blurring, edge detection, and Hough Line Transformation to extract lane lines from video frames.

## Features

- **Lane Detection for Day and Night Drives:** Separate processing for videos filmed in different lighting conditions, improving accuracy.
- **Image Processing with OpenCV:** Techniques like Gaussian blurring, Canny edge detection, and Hough Line Transformation are used for lane line detection.
- **Error Handling for Missing Lines:** The system remembers the last detected lanes when lines are temporarily not visible in the frame.
- **Polygonal Overlay:** A trapezoid-shaped overlay highlights the lane area for better visual guidance.
- **Real-time Video Processing:** The system processes videos frame by frame and outputs the result with lane lines overlaid.

## Input Video Links

The system uses two different videos for lane detection, one for day driving and one for night driving:

### Day Drive:
- **Raw video download:** [Day Drive - Google Drive](https://drive.google.com/file/d/1qxNcqjQPsiqj5z1uzSbHO_hExGDDnk3F/view)
- **YouTube preview:** [Day Drive - YouTube](https://www.youtube.com/watch?v=uHCSfWnePP0)

### Night Drive:
- **Raw video download:** [Night Drive - Google Drive](https://drive.google.com/file/d/1jYsov9fi90QRxaFNu16AaLmIl77Y4H05/view)
- **YouTube preview:** [Night Drive - YouTube](https://www.youtube.com/watch?v=iV5cvtQZLwU)

## Technologies Used

- **Python**
- **OpenCV**
- **NumPy**

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Lane-Detection-System.git
```

2.Install the required dependencies:

```bash
pip install -r requirements.txt
```

3.Download the input video files from the links provided above.

4.Run the Python script for either day or night drive:

```bash
python day_drive.py
# or
python night_drive.py
```

## Project Structure

```bash
Lane-Detection-System/
│
├── day_drive_lane_detection.py          # Lane detection for day driving video
├── night_drive_lane_detection.py        # Lane detection for night driving video
├── requirements.txt                     # List of dependencies (e.g., OpenCV, NumPy)
└── README.md                            # Project documentation
```

## Techniques and Image Processing
- **Gaussian Blurring**: Reduces noise in the frames to make lane detection more accurate.
- **Canny Edge Detection**: Identifies edges in the frame, a crucial step before detecting lane lines.
- **Hough Line Transformation**: Detects straight lines in the frame based on the edges found.
- **Line Smoothing**: Slope and intercepts of detected lines are averaged to provide stable lane lines.
- **Polygon Overlay**: A trapezoid shape is drawn over the detected lanes to enhance the visibility of the road structure.

## Output Videos
Processed videos are saved as output files showing the detected lanes overlaid on the road:

- day-drive-output.avi
- night-drive-output.avi
