import os
import cv2
import numpy as np
import tensorflow as tf

# --- Constants ---
KEYPOINT_NAMES = [
    "wither", "sole", "bwdt2", "back", "shoulder",
    "hip1", "ground", "chest", "bwdt1"
]
CLASS_NAMES = ["cattle", "buffalo"]

# --- Main Service Class ---
class AnalysisService:

    def _init_(self):
        """Initialize service and load ML models once."""
        object_detection_model_path = "models/object_detection.tflite"
        pose_estimation_model_path = "models/pose_estimation.tflite"

        try:
            self.object_detector = tf.lite.Interpreter(model_path=object_detection_model_path)
            self.object_detector.allocate_tensors()
            self.pose_estimator = tf.lite.Interpreter(model_path=pose_estimation_model_path)
            self.pose_estimator.allocate_tensors()
            print("✅ TFLite models loaded successfully.")
        except Exception as e:
            print(f"❌ FATAL: Error loading TFLite models: {e}")
            self.object_detector = None
            self.pose_estimator = None

    def _preprocess_image(self, image, size):
        """Resize and normalize image for models."""
        resized_image = cv2.resize(image, size)
        input_tensor = np.expand_dims(resized_image, axis=0).astype(np.float32)
        return input_tensor / 255.0

    def _detect_animal_with_tflite(self, image_path: str):
        """Run object detection and return best detection."""
        if not self.object_detector:
            raise Exception("Object detection model is not loaded.")
        
        image = cv2.imread(image_path)
        original_h, original_w, _ = image.shape
        input_tensor = self._preprocess_image(image, (640, 640))
        
        input_details = self.object_detector.get_input_details()[0]
        output_details = self.object_detector.get_output_details()
        self.object_detector.set_tensor(input_details['index'], input_tensor)
        self.object_detector.invoke()
        
        detections = self.object_detector.get_tensor(output_details[0]['index'])[0]

        best_detection = None
        best_score = 0.0

        # Iterate over detections (shape: [N, 6] → [ymin, xmin, ymax, xmax, class, score])
        for det in detections.T:  
            ymin, xmin, ymax, xmax, class_id_float, score = det[:6]
            class_id = int(class_id_float)
            if score > best_score and score > 0.5 and class_id < len(CLASS_NAMES):
                class_name = CLASS_NAMES[class_id]
                if class_name in ["cattle", "buffalo"]:
                    best_score = score
                    x1, y1 = int(xmin * original_w), int(ymin * original_h)
                    x2, y2 = int(xmax * original_w), int(ymax * original_h)
                    best_detection = {
                        "box": (x1, y1, x2, y2),
                        "class_name": class_name,
                        "score": float(score)
                    }

        return best_detection

    def _get_keypoints_with_tflite(self, cropped_image: np.ndarray) -> dict:
        """Run pose estimation and extract keypoints."""
        if not self.pose_estimator:
            raise Exception("Pose estimation model is not loaded.")
        
        h, w, _ = cropped_image.shape
        input_tensor = self._preprocess_image(cropped_image, (640, 640))
        input_details = self.pose_estimator.get_input_details()[0]
        output_details = self.pose_estimator.get_output_details()[0]
        self.pose_estimator.set_tensor(input_details['index'], input_tensor)
        self.pose_estimator.invoke()
        
        raw_output = self.pose_estimator.get_tensor(output_details['index'])

        # Handle different shapes safely
        if raw_output.ndim == 3:   # e.g. (1, N, 3)
            keypoints_output = raw_output[0]
        elif raw_output.ndim == 2: # e.g. (N, 3)
            keypoints_output = raw_output
        else:
            raise ValueError(f"Unexpected pose model output shape: {raw_output.shape}")

        keypoints_dict = {}
        for i, name in enumerate(KEYPOINT_NAMES):
            if i < len(keypoints_output):
                y, x, conf = keypoints_output[i]
                if conf > 0.1:
                    abs_x, abs_y = int(x * w), int(y * h)
                    keypoints_dict[name] = {
                        'coords': (abs_x, abs_y),
                        'confidence': float(conf)
                    }
        return keypoints_dict

    def _calculate_atp_scores(self, keypoints: dict) -> dict:
        """Compute ATP scores from keypoints."""
        trait_scores_list = []
        for name in KEYPOINT_NAMES:
            keypoint_data = keypoints.get(name)
            score = keypoint_data['confidence'] if keypoint_data else 0.0
            trait_scores_list.append({
                "trait_name": name.capitalize(),
                "score": round(score, 2)
            })

        valid_scores = [item['score'] for item in trait_scores_list if item['score'] > 0]
        overall_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
        
        return {
            "overall_score": float(round(overall_score, 2)),
            "trait_scores": trait_scores_list
        }

    def run_full_analysis(self, image_path: str) -> dict:
        """Main pipeline: detect → crop → pose → score."""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from path: {image_path}")
        
        detection_result = self._detect_animal_with_tflite(image_path)
        if detection_result is None:
            return {
                "error": "No cattle or buffalo detected with enough confidence."
            }
        
        x1, y1, x2, y2 = detection_result["box"]
        class_name = detection_result["class_name"]
        score = detection_result["score"]

        cropped_image = image[y1:y2, x1:x2]
        if cropped_image.size == 0:
            raise ValueError("Failed to crop image.")
        
        keypoints = self._get_keypoints_with_tflite(cropped_image)
        scores = self._calculate_atp_scores(keypoints)

        # Annotated image
        annotated_image = image.copy()
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 3)
        base, _ = os.path.splitext(os.path.basename(image_path))
        annotated_filename = f"{base}-annotated.jpg"
        annotated_image_path = os.path.join("uploads", annotated_filename)
        cv2.imwrite(annotated_image_path, annotated_image)
        
        return {
            "scores": scores,
            "annotated_image_path": annotated_image_path,
            "class_name": class_name,
            "detection_confidence": score
        }