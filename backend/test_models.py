import cv2
import numpy as np
import tensorflow as tf

# --- CONFIGURATION ---
# 1. Place your buffalo image in the backend/ folder.
# 2. Change this filename to match your image.
TEST_IMAGE_PATH = "backend/buffalo.jpg"

# 3. These must match your analysis_service.py file.
MODEL_PATH = "backend/models/object_detection.tflite"
IMG_SIZE = (640, 640)
CLASS_NAMES = ["cattle", "buffalo"]

def main():
    print("--- Starting Model Diagnostic Test ---")
    
    # 1. Load the model
    try:
        detector = tf.lite.Interpreter(model_path=MODEL_PATH)
        detector.allocate_tensors()
        print("✅ Object detection model loaded successfully.")
    except Exception as e:
        print(f"❌ ERROR: Failed to load model at '{MODEL_PATH}'. Error: {e}")
        return

    # 2. Load and preprocess the image
    image = cv2.imread(TEST_IMAGE_PATH)
    if image is None:
        print(f"❌ ERROR: Cannot find the test image at '{TEST_IMAGE_PATH}'.")
        return

    h, w, _ = image.shape
    resized_image = cv2.resize(image, IMG_SIZE)
    input_tensor = np.expand_dims(resized_image, axis=0).astype(np.float32) / 255.0

    # 3. Run inference
    input_details = detector.get_input_details()[0]
    output_details = detector.get_output_details()
    detector.set_tensor(input_details['index'], input_tensor)
    detector.invoke()
    print("✅ Model inference complete.")

    # 4. Analyze and print the results
    print("\n--- MODEL OUTPUT ---")

    raw_output = detector.get_tensor(output_details[0]['index'])[0]  # shape (6, 8400)
    detections = np.transpose(raw_output)  # shape (8400, 6)

    found_anything = False
    for i, det in enumerate(detections[:100]):  # check first 100 anchors only
        x, y, box_w, box_h, confidence, class_prob = det
        score = confidence * class_prob  # combine object confidence + class prob

        if score > 0.3:  # threshold for printing
            found_anything = True
            class_id = 0 if class_prob < 0.5 else 1   # crude classification
            class_name = CLASS_NAMES[class_id]

            # Convert YOLO-style (x,y,w,h) → pixel box
            x1 = int((x - box_w / 2) * w)
            y1 = int((y - box_h / 2) * h)
            x2 = int((x + box_w / 2) * w)
            y2 = int((y + box_h / 2) * h)

            print(f"\nDetection #{i+1}:")
            print(f"  - Confidence Score: {score:.2f}")
            print(f"  - Detected Class: '{class_name}'")
            print(f"  - Box: ({x1}, {y1}), ({x2}, {y2})")

    if not found_anything:
        print("\nThe model did not detect any objects with confidence > 0.3.")

    print("\n--- DIAGNOSIS ---")
    print("Check the 'Confidence Score' above. If it is below ~0.50, the app may reject it.")
    print("Check if 'Detected Class' is correct. It must be 'cattle' or 'buffalo'.")
    print("-----------------")

if _name_ == "_main_":
    main()