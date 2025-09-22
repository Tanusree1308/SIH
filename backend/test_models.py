import cv2
import numpy as np
import tensorflow as tf

# --- CONFIGURATION ---
# 1. Place your buffalo image in the `backend/` folder.
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
    
    detections = detector.get_tensor(output_details[0]['index'])[0]

    found_anything = False
    for i, detection in enumerate(detections[:5]):
        
        box_and_class_info = detection[:6]
        if len(box_and_class_info) < 6:
            continue
            
        _, _, _, _, class_id_float, score = box_and_class_info
        class_id = int(class_id_float)
        
        if score > 0.01: # Show anything with more than 1% confidence
            found_anything = True
            class_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else f"Unknown Class ID ({class_id})"
            print(f"\nDetection #{i+1}:")
            print(f"  - Confidence Score: {score:.2f}")
            print(f"  - Detected Class: '{class_name}' (ID: {class_id})")

    if not found_anything:
        print("\nThe model did not detect any objects with a confidence score above 1%.")
        
    print("\n--- DIAGNOSIS ---")
    print("Check the 'Confidence Score' above. If it is below 0.50, the app will reject it.")
    print("Also, check if the 'Detected Class' is correct. It must be 'cattle' or 'buffalo'.")
    print("-----------------")


if __name__ == "__main__":
    main()