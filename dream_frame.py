import os
import cv2
import torch
from PIL import Image
import numpy as np
from segment_anything import sam_model_registry, SamPredictor
from ultralytics import YOLO
from diffusers import StableDiffusionInpaintPipeline
import requests

def download_if_missing(url, dest_path):
    if not os.path.exists(dest_path):
        print(f"[INFO] Downloading {os.path.basename(dest_path)}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"[INFO] Downloaded to {dest_path}")
    else:
        print(f"[INFO] {os.path.basename(dest_path)} already exists.")

#*************************************************************************************
# Use YOLOv8 to detect the person
#*************************************************************************************

def detect_person_yolo(frame):
    # Load YOLOv8 model (nano version for speed, can use 's', 'm', 'l', 'x' for larger models)
    print("[INFO] Detecting person with YOLOv8...")
    yolo_model = YOLO('./model/yolov8n.pt')
    # Run YOLOv8 detection
    results = yolo_model(frame)
    boxes = results[0].boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
    classes = results[0].boxes.cls.cpu().numpy()  # class indices
    # Find the largest 'person' box (class 0 in COCO)
    person_boxes = [box for box, cls in zip(boxes, classes) if int(cls) == 0]
    if not person_boxes:
        print("[ERROR] No person detected!")
        raise Exception("No person detected!")
    person_box = max(person_boxes, key=lambda b: (b[2]-b[0])*(b[3]-b[1]))
    return person_box

#*************************************************************************************
# Generate masks with SAM
#*************************************************************************************

def segment_person_sam(frame, person_box):  
    print("[INFO] Using SAM with YOLO bounding box...")
    sam = sam_model_registry["vit_b"](
        checkpoint="./model/sam_vit_b_01ec64.pth",
    ).to('cpu')

    predictor = SamPredictor(sam)
    predictor.set_image(frame)

    input_box = np.array(person_box).astype(int)[None, :]
    masks, scores, logits = predictor.predict(
        box=input_box,
        multimask_output=True
    )
    best_mask = masks[np.argmax([m.sum() for m in masks])]
    combined_mask = best_mask
    print("[INFO] Mask generated using SAM and YOLO bounding box.")
    return best_mask

#*************************************************************************************
# Générer un nouveau fond avec Stable Diffusion InpaintPipeline
#*************************************************************************************

def inpaint_background(original_image, mask, prompt, model_path, output_dir):
    print("[INFO] Generating new background with Stable Diffusion...")
    # Préparer le masque binaire pour l'inpainting (le fond doit être blanc, le sujet noir)
    # Ici, on inverse le masque: le fond (False) devient 255, le sujet (True) devient 0
    mask_pil = Image.fromarray((~mask * 255).astype("uint8"))
    # Redimensionner le masque si besoin (doit avoir la même taille que l'image)
    mask_pil = mask_pil.resize(original_image.size)

    # Charger le pipeline d'inpainting
    inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        #torch_dtype=torch.float16, #commented to make it work on cpu
        safety_checker=None,
        cache_dir=model_path
    ).to("cpu")
    # Générer l'image avec le nouveau fond
    with torch.no_grad():
        out_image = inpaint_pipe(
            prompt=prompt,
            image=original_image,
            mask_image=mask_pil,
            strength=0.9,
            generator=torch.Generator("cpu").manual_seed(7)
        ).images[0]

    # Sauvegarder et afficher le résultat
    output_path = os.path.join(output_dir, "output_inpaint.png")
    out_image.save(output_path)
    print(f"[INFO] Final image saved as {output_path}.")
    out_image.show()
    print("[INFO] Processing complete!")
    out_image.save(output_path)

def generate_image(prompt, output_path, input_image_path):
    # Paths
    grand_parent_dir = os.path.dirname(os.getcwd())
    model_path = os.path.join(grand_parent_dir, "model")
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"[INFO] Using prompt: {prompt}")
    
    # Load and resize the uploaded image
    frame = cv2.imread(input_image_path)
    frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_LANCZOS4)
    
    # 2. YOLO
    person_box = detect_person_yolo(frame)

    sam_url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
    sam_path = os.path.join("model", "sam_vit_b_01ec64.pth")
    download_if_missing(sam_url, sam_path)

    # 3. SAM
    combined_mask = segment_person_sam(frame, person_box)

    # 4. PNG transparent
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgba = np.dstack([frame_rgb, combined_mask.astype(np.uint8) * 255])
    output_dir = os.path.dirname(output_path)
    Image.fromarray(rgba).save(os.path.join(output_dir, "mask.png"))
    print(f"[INFO] Transparent PNG saved as {os.path.join(output_dir, 'mask.png')}")

    # 5. Inpainting
    original_image = Image.fromarray(frame_rgb)
    inpaint_background(original_image, combined_mask, prompt, model_path, output_dir)

    print("[INFO] Processing complete!")