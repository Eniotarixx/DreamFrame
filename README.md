# DreamFrame

**DreamFrame** is a Python script that lets you capture an image from your webcam, automatically segment a person, and generate a new realistic background using AI (Stable Diffusion Inpainting).  
Everything runs locally—no need to upload your images to an external server.

---

## Features

- Capture a centered square image from your webcam.
- Automatic person detection with YOLOv8.
- Precise subject segmentation with SAM (Segment Anything Model).
- Realistic new background generation with Stable Diffusion Inpainting.
- Automatic saving of results in the `output/` folder.

---

## Installation

1. **Clone the repository and move into the folder:**
   ```bash
   git clone https://github.com/Eniotarixx/DreamFrame
   cd DreamFrame
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv dream_frame_env
   source dream_frame_env/bin/activate
   ```

---

## Usage

1. **Run the main script:**
   ```bash
   python dream_frame.py
   ```

2. **On-screen instructions:**
   - A webcam window will open. Press `Space` to capture an image, or `Esc` to quit.
   - Enter a text prompt to describe the new background you want to generate (English works best).

3. **Results:**
   - Generated images are saved in the `output/` folder:
     - `opencv_frame.png`: the image captured from the webcam
     - `mask.png`: the subject cut out with transparency
     - `output_inpaint.png`: the final image with the new background

---

## Models Used

Required weights are downloaded automatically if missing:
- `model/yolov8n.pt` (YOLOv8 Nano, person detection)
- `model/sam_vit_b_01ec64.pth` (Segment Anything Model, segmentation)
- Stable Diffusion Inpainting (downloaded via HuggingFace Diffusers)

---

## Notes

- **First run:** Downloading models may take some time.
- **Compatibility:** Works on Mac (MPS).

---

## Customization

- You can change the prompt to generate different types of backgrounds.
- The script can be adapted for other types of segmentation or inpainting.

---

## Main Dependencies

- torch
- opencv-python
- Pillow
- numpy
- segment-anything
- ultralytics
- diffusers
- transformers
- accelerate
- requests

---

## Author

- Eniotarixx

---

Feel free to open an issue or pull request for suggestions or improvements!
