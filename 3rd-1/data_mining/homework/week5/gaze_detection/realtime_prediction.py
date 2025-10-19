import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import joblib
import logging
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)


class GazePredictor:
    """Real-time gaze prediction using webcam."""

    def __init__(self, model_path, scaler_path, face_model_path, eye_blink_threshold=0.5):
        """
        Initialize the gaze predictor.

        Args:
            model_path: Path to trained SVM model
            scaler_path: Path to feature scaler
            face_model_path: Path to MediaPipe face landmarker model
            eye_blink_threshold: Threshold for detecting closed eyes
        """
        logging.info("Loading models...")

        # Load SVM model and scaler
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.eye_blink_threshold = eye_blink_threshold

        # Create FaceLandmarker
        base_options = python.BaseOptions(model_asset_path=face_model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1,
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

        # Feature names (must match training)
        self.eye_gaze_features = [
            'eyeLookUpLeft', 'eyeLookUpRight',
            'eyeLookDownLeft', 'eyeLookDownRight',
            'eyeLookInLeft', 'eyeLookInRight',
            'eyeLookOutLeft', 'eyeLookOutRight'
        ]
        self.head_rotation_features = ['head_pitch', 'head_yaw', 'head_roll']

        # Smoothing with moving average
        self.prediction_history = deque(maxlen=10)  # Last 10 predictions

        logging.info("Models loaded successfully!")

    def extract_features(self, frame):
        """
        Extract features from a single frame.

        Args:
            frame: RGB image frame

        Returns:
            features: Feature vector (11 features) or None if no face detected
            eyes_closed: Boolean indicating if eyes are closed
            blendshapes_dict: Dictionary of all blendshapes for debugging
        """
        # Convert to MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Detect face
        detection_result = self.detector.detect(mp_image)

        if not detection_result.face_blendshapes:
            return None, True, {}

        # Extract blendshapes
        blendshapes = detection_result.face_blendshapes[0]
        blendshapes_dict = {bs.category_name: bs.score for bs in blendshapes}

        # Check if eyes are closed
        eye_blink_left = blendshapes_dict.get('eyeBlinkLeft', 1.0)
        eye_blink_right = blendshapes_dict.get('eyeBlinkRight', 1.0)
        eyes_closed = (eye_blink_left > self.eye_blink_threshold or
                      eye_blink_right > self.eye_blink_threshold)

        # Extract eye gaze features
        eye_features = [blendshapes_dict.get(feat, 0.0) for feat in self.eye_gaze_features]

        # Extract head rotation from transformation matrix
        if detection_result.facial_transformation_matrixes:
            matrix = np.array(detection_result.facial_transformation_matrixes[0]).reshape(4, 4)
            R = matrix[:3, :3]

            # Calculate Euler angles (pitch, yaw, roll)
            pitch = np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2))
            yaw = np.arctan2(R[1, 0], R[0, 0])
            roll = np.arctan2(R[2, 1], R[2, 2])

            head_features = [pitch, yaw, roll]
        else:
            head_features = [0.0, 0.0, 0.0]

        # Combine features
        features = np.array(eye_features + head_features).reshape(1, -1)

        return features, eyes_closed, blendshapes_dict

    def predict(self, features):
        """
        Predict if user is watching screen.

        Args:
            features: Feature vector

        Returns:
            prediction: 0 (not watching) or 1 (watching)
            probability: Probability of watching screen
        """
        # Scale features
        features_scaled = self.scaler.transform(features)

        # Predict
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]

        return prediction, probability

    def get_smoothed_prediction(self, prediction):
        """
        Apply moving average to smooth predictions.

        Args:
            prediction: Current prediction (0 or 1)

        Returns:
            smoothed_prediction: Smoothed prediction
        """
        self.prediction_history.append(prediction)

        # Return majority vote
        if len(self.prediction_history) == 0:
            return prediction

        avg = np.mean(self.prediction_history)
        return 1 if avg >= 0.5 else 0

    def draw_ui(self, frame, prediction, probability, eyes_closed, smoothed_prediction):
        """
        Draw UI elements on frame.

        Args:
            frame: Image frame
            prediction: Raw prediction (0 or 1)
            probability: Prediction probabilities [no, yes]
            eyes_closed: Boolean
            smoothed_prediction: Smoothed prediction

        Returns:
            frame: Frame with UI drawn
        """
        height, width = frame.shape[:2]

        # Create semi-transparent overlay for status
        overlay = frame.copy()

        # Determine status color and text
        if eyes_closed:
            status_text = "EYES CLOSED"
            status_color = (128, 128, 128)  # Gray
            bg_color = (64, 64, 64)
        elif smoothed_prediction == 1:
            status_text = "WATCHING SCREEN"
            status_color = (0, 255, 0)  # Green
            bg_color = (0, 128, 0)
        else:
            status_text = "NOT WATCHING"
            status_color = (0, 0, 255)  # Red
            bg_color = (0, 0, 128)

        # Draw status bar at top
        cv2.rectangle(overlay, (0, 0), (width, 80), bg_color, -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Draw status text
        cv2.putText(frame, status_text, (20, 50),
                   cv2.FONT_HERSHEY_DUPLEX, 1.5, status_color, 3)

        # Draw probability bar
        if not eyes_closed:
            prob_yes = probability[1]
            prob_no = probability[0]

            # Background bar
            bar_x, bar_y, bar_w, bar_h = 20, 90, width - 40, 30
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h),
                         (50, 50, 50), -1)

            # Probability bar
            prob_width = int(bar_w * prob_yes)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + prob_width, bar_y + bar_h),
                         (0, 255, 0), -1)

            # Text
            prob_text = f"Watching: {prob_yes*100:.1f}% | Not Watching: {prob_no*100:.1f}%"
            cv2.putText(frame, prob_text, (bar_x, bar_y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Draw instructions at bottom
        instructions = [
            "Press 'q' to quit",
            "Press 's' to save screenshot",
            "Press 'r' to reset history"
        ]

        y_offset = height - 80
        for i, text in enumerate(instructions):
            cv2.putText(frame, text, (20, y_offset + i*25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # Draw raw vs smoothed indicator
        indicator_text = f"Raw: {'YES' if prediction == 1 else 'NO'} | " \
                        f"Smoothed: {'YES' if smoothed_prediction == 1 else 'NO'}"
        cv2.putText(frame, indicator_text, (20, 140),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        return frame

    def run(self):
        """Run real-time prediction from webcam."""
        logging.info("Starting webcam...")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            logging.error("Failed to open webcam!")
            return

        # Set camera resolution
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        logging.info("Webcam started! Press 'q' to quit.")

        frame_count = 0
        screenshot_count = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logging.error("Failed to read frame from webcam")
                    break

                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)

                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Extract features
                features, eyes_closed, blendshapes = self.extract_features(rgb_frame)

                if features is not None and not eyes_closed:
                    # Predict
                    prediction, probability = self.predict(features)
                    smoothed_prediction = self.get_smoothed_prediction(prediction)
                else:
                    prediction = 0
                    probability = np.array([1.0, 0.0])
                    smoothed_prediction = 0

                # Draw UI
                frame = self.draw_ui(frame, prediction, probability, eyes_closed, smoothed_prediction)

                # Display frame
                cv2.imshow('Gaze Detection - Press q to quit', frame)

                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    logging.info("Quitting...")
                    break
                elif key == ord('s'):
                    # Save screenshot
                    screenshot_path = f'screenshot_{screenshot_count:03d}.png'
                    cv2.imwrite(screenshot_path, frame)
                    logging.info(f"Screenshot saved: {screenshot_path}")
                    screenshot_count += 1
                elif key == ord('r'):
                    # Reset prediction history
                    self.prediction_history.clear()
                    logging.info("Prediction history reset")

                frame_count += 1

        finally:
            cap.release()
            cv2.destroyAllWindows()
            logging.info(f"Processed {frame_count} frames")


def main():
    """Main function."""
    # Configuration
    model_path = 'svm_results/best_svm_model.pkl'
    scaler_path = 'svm_results/scaler.pkl'
    face_model_path = 'face_landmarker.task'
    eye_blink_threshold = 0.5

    # Create predictor and run
    predictor = GazePredictor(
        model_path=model_path,
        scaler_path=scaler_path,
        face_model_path=face_model_path,
        eye_blink_threshold=eye_blink_threshold
    )

    predictor.run()


if __name__ == "__main__":
    main()
