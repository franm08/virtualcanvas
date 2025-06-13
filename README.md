# Interactive Vision Canvas

## Project Overview
**Interactive Vision Canvas** is a gesture-based drawing tool that transforms hand movements into creative strokes using MediaPipe and OpenCV. Designed for intuitive, touch-free interaction, users can draw, erase, and manipulate shapes in real-time—ideal for educational demos, accessibility tools, and creative applications.

Demo coming soon: **[Coming Soon]**

## Features

### 1. Gesture-Controlled Drawing
- Draw with hand movements using fingertip tracking.
- Fist gesture to pause drawing.

### 2. Brush & Shape Tools
- Circle, Square, and Spray brushes.
- Draw shapes: lines, rectangles, and circles.

### 3. Interactive UI
- On-screen buttons to switch tools, colors, and modes.
- Hover-based interaction, no clicks required.

### 4. Screenshot Capture
- Save your artwork with a gesture-based screenshot button.

### 5. Advanced Brushes
- Animated rainbow brushes and spray effects.
- Adjustable brush sizes and eraser tool.

### 6. Drawing Modes
- Freeform, Shape Drawing, and Grid Snap options.

## How It Works

### Step 1: Hand Tracking
- Captures webcam feed and uses MediaPipe to detect hand landmarks.
- Identifies index finger for cursor and fist for drawing toggle.

### Step 2: Drawing Logic
- Depending on mode, draws points, shapes, or patterns on a virtual canvas.
- Detects button hover with index finger and performs tool switches.

### Step 3: Canvas Overlay
- Combines drawing with live camera feed for real-time visual feedback.

## Future Enhancements
- Multi-hand support.
- Shape resizing via pinch gesture.
- Gesture-based undo/redo.
- Web deployment using Flask or Streamlit.

## Acknowledgements
- **Libraries:** MediaPipe, OpenCV, NumPy
- **Tools:** Python, OpenCV GUI
- **Inspiration:** ML + Human-Computer Interaction experiments

## License
This project is licensed under the **MIT License**. See `LICENSE` file for details.
