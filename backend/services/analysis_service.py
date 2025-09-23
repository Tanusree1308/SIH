import tensorflow as tf
import numpy as np
import cv2
import os
from fastapi import HTTPException

# --- Keypoint Mapping ---
# IMPORTANT: You MUST verify this mapping matches your pose estimation model's output.
# This is an example for a 9-keypoint model.
KEYPOINT_DICT = {
    'Nose': 0,
    'Withers': 1,      # Top of the shoulders
    'Shoulder': 2,
    'Hip': 3,
    'TailBase': 4,
    'FrontHoof': 5,
    'RearHoof': 6,
    'ChestBottom': 7,
    'HipHeightPoint': 8 # A point vertically above the hip for height measurement
}

class AnalysisService:
    def __init__(self):
        """
        Initialize object detection and pose estimation TFLite models.
        """
        # --- Load Object Detection Model ---
        object_model_path = "backend/models/object_detection.tflite"
        if not os.path.exists(object_model_path):
            raise FileNotFoundError(f"❌ Object detection model not found at {object_model_path}")

        self.object_detector = tf.lite.Interpreter(model_path=object_model_path)
        self.object_detector.allocate_tensors()

        self.obj_input_details = self.object_detector.get_input_details()
        self.obj_output_details = self.object_detector.get_output_details()

        # --- Load Pose Estimation Model ---
        pose_model_path = "backend/models/pose_estimation.tflite"
        if not os.path.exists(pose_model_path):
            raise FileNotFoundError(f"❌ Pose estimation model not found at {pose_model_path}")

        self.pose_estimator = tf.lite.Interpreter(model_path=pose_model_path)
        self.pose_estimator.allocate_tensors()

        self.pose_input_details = self.pose_estimator.get_input_details()
        self.pose_output_details = self.pose_estimator.get_output_details()

        print("✅ Models loaded successfully!")

    def preprocess_image(self, image_path, input_shape):
        """
        Loads and preprocesses an image for the model.
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"❌ Could not read image: {image_path}")

        height, width = input_shape[1], input_shape[2]
        image_resized = cv2.resize(image, (width, height))
        input_data = np.expand_dims(image_resized, axis=0).astype(np.float32)
        return input_data

    def run_object_detection(self, image_path):
        """
        Runs object detection on the given image. Returns the highest-scoring detection.
        """
        input_data = self.preprocess_image(image_path, self.obj_input_details[0]['shape'])

        self.object_detector.set_tensor(self.obj_input_details[0]['index'], input_data)
        self.object_detector.invoke()

        boxes = self.object_detector.get_tensor(self.obj_output_details[0]['index'])
        classes = self.object_detector.get_tensor(self.obj_output_details[1]['index'])
        scores = self.object_detector.get_tensor(self.obj_output_details[2]['index'])
        
        if scores[0].any():
            best_score_index = np.argmax(scores[0])
            return {
                "boxes": [boxes[0][best_score_index].tolist()],
                "classes": [classes[0][best_score_index].tolist()],
                "scores": [scores[0][best_score_index].tolist()]
            }
        return {"boxes": [], "classes": [], "scores": []}

    def run_pose_estimation(self, image_path):
        """
        Runs pose estimation on the given image.
        """
        input_data = self.preprocess_image(image_path, self.pose_input_details[0]['shape'])

        self.pose_estimator.set_tensor(self.pose_input_details[0]['index'], input_data)
        self.pose_estimator.invoke()

        keypoints = self.pose_estimator.get_tensor(self.pose_output_details[0]['index'])
        return {"keypoints": keypoints.tolist()}

    def calculate_distance(self, keypoints, point1_name, point2_name):
        """Calculates the Euclidean distance between two keypoints by name."""
        p1_index = KEYPOINT_DICT[point1_name]
        p2_index = KEYPOINT_DICT[point2_name]
        
        p1 = keypoints[0][0][p1_index]
        p2 = keypoints[0][0][p2_index]

        # Keypoint format is often [y, x, confidence]. Check confidence score.
        # Assuming confidence is the 3rd element. If your model doesn't provide it, check p1[0] > 0
        if len(p1) < 3 or len(p2) < 3 or p1[2] == 0 or p2[2] == 0:
            return 0

        # Note: TFLite models often output (y, x). We use them as is.
        distance = np.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
        return distance

    def score_trait(self, measured_distance, ideal_distance, acceptable_range_percent=0.10):
        """Converts a measured distance into a 1-5 score."""
        if measured_distance == 0:
            return 1.0

        deviation = abs(measured_distance - ideal_distance)
        acceptable_range = ideal_distance * acceptable_range_percent
        
        if deviation <= acceptable_range:
            return 5.0
        
        # Scale score down based on how far it deviates from the ideal
        score = 5.0 - (deviation / ideal_distance) * 4.0
        return round(max(1.0, min(5.0, score)), 1)

    def calculate_atp_score(self, pose_results):
        """
        Calculates the ATP score based on keypoint distances.
        """
        keypoints = pose_results["keypoints"]

        # --- DEFINE IDEAL MEASUREMENTS (in pixels) ---
        # ❗IMPORTANT: You MUST tune these values by measuring sample images of high-quality animals.
        IDEAL_BODY_LENGTH = 250  # Distance from Withers to Hip
        IDEAL_WITHERS_HEIGHT = 220 # Distance from Withers to Front Hoof
        IDEAL_HIP_HEIGHT = 215 # Distance from Hip to Rear Hoof
        
        # --- 1. Calculate Actual Distances ---
        body_length = self.calculate_distance(keypoints, 'Withers', 'Hip')
        withers_height = self.calculate_distance(keypoints, 'Withers', 'FrontHoof')
        hip_height = self.calculate_distance(keypoints, 'Hip', 'RearHoof')

        # --- 2. Score Each Trait ---
        body_length_score = self.score_trait(body_length, IDEAL_BODY_LENGTH)
        withers_height_score = self.score_trait(withers_height, IDEAL_WITHERS_HEIGHT)
        hip_height_score = self.score_trait(hip_height, IDEAL_HIP_HEIGHT)

        # --- 3. Calculate Overall Score (example: weighted average) ---
        weights = {'length': 0.4, 'height': 0.6}
        avg_height_score = (withers_height_score + hip_height_score) / 2
        overall_score = (body_length_score * weights['length']) + (avg_height_score * weights['height'])
        
        return {
            "overall_score": round(max(1.0, overall_score), 1),
            "trait_scores": [
                {"trait_name": "Body Length", "score": body_length_score},
                {"trait_name": "Withers Height", "score": withers_height_score},
                {"trait_name": "Hip Height", "score": hip_height_score},
            ]
        }

    def run_full_analysis(self, image_path):
        """
        Runs the full analysis pipeline.
        """
        try:
            detection_results = self.run_object_detection(image_path)
            if not detection_results["scores"]:
                raise ValueError("No animal detected in the image.")

            pose_results = self.run_pose_estimation(image_path)
            if not pose_results["keypoints"]:
                raise ValueError("Could not perform pose estimation.")

            scores = self.calculate_atp_score(pose_results)

            class_id = int(detection_results["classes"][0][0])
            class_names = ['cow', 'buffalo'] # Adjust as needed
            animal_type = class_names[class_id] if class_id < len(class_names) else 'unknown'

            # Combine all results into the final dictionary
            final_result = {
                "status": "success",
                "animal_type": animal_type,
                "annotated_image_path": image_path, # Placeholder for now
            }
            final_result.update(scores) # Add overall_score and trait_scores to the dictionary
            return final_result

        except Exception as e:
            return {"status": "error", "message": str(e)}