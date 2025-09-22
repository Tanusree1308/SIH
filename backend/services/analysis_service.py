import os
import cv2
import numpy as np
import tensorflow as tf

# --- 1. Load Your TFLite Models ---
try:
    object_detector = tf.lite.Interpreter(model_path="backend/models/object_detection.tflite")
    object_detector.allocate_tensors()
    pose_estimator = tf.lite.Interpreter(model_path="backend/models/pose_estimation.tflite")
    pose_estimator.allocate_tensors()
    print("TFLite models loaded successfully.")
except Exception as e:
    print(f"Error loading TFLite models: {e}")
    object_detector = None
    pose_estimator = None

# --- 2. Define Model Input/Output Details ---
OBJECT_DETECTION_IMG_SIZE = (640, 640)
POSE_ESTIMATION_IMG_SIZE = (640, 640)

KEYPOINT_NAMES = [
    "wither", "sole", "bwdt2", "back", "shoulder", 
    "hip1", "ground", "chest", "bwdt 1"
]
CLASS_NAMES = ["cattle", "buffalo"] 

def preprocess_image(image, size):
    resized_image = cv2.resize(image, size)
    input_tensor = np.expand_dims(resized_image, axis=0).astype(np.float32)
    input_tensor = input_tensor / 255.0
    return input_tensor

def detect_animal_with_tflite(image_path: str):
    if not object_detector:
        raise Exception("Object detection model is not loaded.")
        
    image = cv2.imread(image_path)
    original_h, original_w, _ = image.shape
    input_tensor = preprocess_image(image, OBJECT_DETECTION_IMG_SIZE)
    
    input_details = object_detector.get_input_details()[0]
    output_details = object_detector.get_output_details()
    object_detector.set_tensor(input_details['index'], input_tensor)
    object_detector.invoke()
    
    detections = object_detector.get_tensor(output_details[0]['index'])[0]

    for detection in detections:
        box_and_class_info = detection[:6]
        if len(box_and_class_info) < 6:
            continue
            
        ymin, xmin, ymax, xmax, class_id_float, score = box_and_class_info
        class_id = int(class_id_float)

        if score > 0.01: # Confidence threshold
            if class_id < len(CLASS_NAMES):
                class_name = CLASS_NAMES[class_id]
                if class_name in ["cattle", "buffalo"]:
                    x1, y1 = int(xmin * original_w), int(ymin * original_h)
                    x2, y2 = int(xmax * original_w), int(ymax * original_h)
                    return {"box": (x1, y1, x2, y2), "class_name": class_name}
    return None

def get_keypoints_with_tflite(cropped_image: np.ndarray) -> dict:
    if not pose_estimator:
        raise Exception("Pose estimation model is not loaded.")
    h, w, _ = cropped_image.shape
    input_tensor = preprocess_image(cropped_image, POSE_ESTIMATION_IMG_SIZE)
    input_details = pose_estimator.get_input_details()[0]
    output_details = pose_estimator.get_output_details()[0]
    pose_estimator.set_tensor(input_details['index'], input_tensor)
    pose_estimator.invoke()
    raw_output = pose_estimator.get_tensor(output_details['index'])
    keypoints_output = raw_output.reshape(-1, 3)
    keypoints_dict = {}
    for i, name in enumerate(KEYPOINT_NAMES):
        if i < len(keypoints_output):
            y, x, conf = keypoints_output[i]
            if conf > 0.1:
                abs_x, abs_y = int(x * w), int(y * h)
                # Convert confidence score to a standard Python float
                keypoints_dict[name] = {'coords': (abs_x, abs_y), 'confidence': float(conf)}
    return keypoints_dict

def calculate_atp_scores(keypoints: dict) -> dict:
    trait_scores_list = []
    
    for name in KEYPOINT_NAMES:
        keypoint_data = keypoints.get(name)
        score = keypoint_data['confidence'] if keypoint_data and keypoint_data['confidence'] > 0.1 else 0.0
        trait_scores_list.append({"trait_name": name.capitalize(), "score": round(score, 2)})

    valid_scores = [item['score'] for item in trait_scores_list if item['score'] > 0]
    overall_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
    
    return {
        # Convert overall score to a standard Python float
        "overall_score": float(round(overall_score, 2)),
        "trait_scores": trait_scores_list
    }

def run_full_analysis(image_path: str) -> dict:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image from path: {image_path}")
    
    detection_result = detect_animal_with_tflite(image_path)
    if detection_result is None:
        return None
    
    x1, y1, x2, y2 = detection_result["box"]
    class_name = detection_result["class_name"]
    
    cropped_image = image[y1:y2, x1:x2]
    if cropped_image.size == 0:
        raise ValueError("Failed to crop image.")
    
    keypoints = get_keypoints_with_tflite(cropped_image)
    scores = calculate_atp_scores(keypoints)

    annotated_image = image.copy()
    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.putText(annotated_image, class_name.capitalize(), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    for name, data in keypoints.items():
        if data['confidence'] > 0.1:
            x_rel, y_rel = data['coords']
            abs_x, abs_y = x1 + x_rel, y1 + y_rel
            cv2.circle(annotated_image, (abs_x, abs_y), 7, (0, 0, 255), -1)

    base, _ = os.path.splitext(os.path.basename(image_path))
    annotated_filename = f"{base}-annotated.jpg"
    annotated_image_path = os.path.join("backend", "uploads", annotated_filename)
    cv2.imwrite(annotated_image_path, annotated_image)
    
    return {
        "scores": scores,
        "annotated_image_path": annotated_image_path,
        "class_name": class_name
    }

