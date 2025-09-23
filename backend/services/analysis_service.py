import tensorflow as tf
import numpy as np
import cv2
import os


class AnalysisService:
    def _init_(self):
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
        Runs object detection on the given image.
        """
        input_data = self.preprocess_image(image_path, self.obj_input_details[0]['shape'])

        self.object_detector.set_tensor(self.obj_input_details[0]['index'], input_data)
        self.object_detector.invoke()

        boxes = self.object_detector.get_tensor(self.obj_output_details[0]['index'])
        classes = self.object_detector.get_tensor(self.obj_output_details[1]['index'])
        scores = self.object_detector.get_tensor(self.obj_output_details[2]['index'])

        return {
            "boxes": boxes.tolist(),
            "classes": classes.tolist(),
            "scores": scores.tolist()
        }

    def run_pose_estimation(self, image_path):
        """
        Runs pose estimation on the given image.
        """
        input_data = self.preprocess_image(image_path, self.pose_input_details[0]['shape'])

        self.pose_estimator.set_tensor(self.pose_input_details[0]['index'], input_data)
        self.pose_estimator.invoke()

        keypoints = self.pose_estimator.get_tensor(self.pose_output_details[0]['index'])
        return {"keypoints": keypoints.tolist()}

    def calculate_atp_score(self, detection_results, pose_results):
        """
        Dummy ATP scoring function.
        Replace with your own scoring logic later.
        """
        detection_confidence = np.mean(detection_results["scores"]) if detection_results["scores"] else 0
        pose_quality = np.mean(pose_results["keypoints"]) if pose_results["keypoints"] else 0

        # Normalize values between 0–100
        detection_score = float(min(100, detection_confidence * 100))
        pose_score = float(min(100, pose_quality * 10))  # scaled differently

        overall_score = round((detection_score * 0.6 + pose_score * 0.4), 2)

        return {
            "overall_score": overall_score,
            "trait_scores": {
                "detection_score": detection_score,
                "pose_score": pose_score
            }
        }

    def run_full_analysis(self, image_path):
        """
        Runs both object detection and pose estimation on the image.
        Returns ATP scoring results.
        """
        try:
            detection_results = self.run_object_detection(image_path)
            pose_results = self.run_pose_estimation(image_path)
            scores = self.calculate_atp_score(detection_results, pose_results)

            return {
                "status": "success",
                "class_name": str(detection_results["classes"][0]) if detection_results["classes"] else "unknown",
                "scores": scores,
                "object_detection": detection_results,
                "pose_estimation": pose_results,
                "annotated_image_path": image_path  # Later you can save annotated image
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }