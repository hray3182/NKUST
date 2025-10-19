import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pandas as pd
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)


def extract_features(video_path, label, frame_interval, model_path, output_csv):
    """
    Extract face blendshapes and transformation matrices from video frames.

    Args:
        video_path: Path to input video file
        label: Label for this video (e.g., 'truth', 'lie')
        frame_interval: Process every nth frame
        model_path: Path to MediaPipe face landmarker model
        output_csv: Path to output CSV file
    """

    # Eye gaze features (8 features)
    eye_gaze_features = [
        "eyeLookUpLeft",
        "eyeLookUpRight",
        "eyeLookDownLeft",
        "eyeLookDownRight",
        "eyeLookInLeft",
        "eyeLookInRight",
        "eyeLookOutLeft",
        "eyeLookOutRight",
    ]

    # Eye blink features (2 features)
    eye_blink_features = ["eyeBlinkLeft", "eyeBlinkRight"]

    logging.info(f"Start extract feature from video {video_path}")

    # Create FaceLandmarker
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1,
    )

    detector = vision.FaceLandmarker.create_from_options(options)

    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Failed to open video: {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    logging.info(f"Video FPS: {fps}, Total frames: {total_frames}")

    # Storage for extracted data
    data_rows = []

    frame_count = 0
    processed_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every nth frame
        if frame_count % frame_interval != 0:
            frame_count += 1
            continue

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detect face landmarks
        detection_result = detector.detect(mp_image)

        # Initialize row data
        row_data = {
            "video_path": video_path,
            "label": label,
            "frame_number": frame_count,
            "timestamp": frame_count / fps,
        }

        # Extract blendshapes (only eye-related features)
        if detection_result.face_blendshapes:
            blendshapes = detection_result.face_blendshapes[0]

            # Extract only eye gaze and blink features
            desired_features = eye_gaze_features + eye_blink_features
            for blendshape in blendshapes:
                if blendshape.category_name in desired_features:
                    row_data[blendshape.category_name] = blendshape.score

        # Extract head rotation from transformation matrix (pitch, yaw, roll)
        if detection_result.facial_transformation_matrixes:
            # Get the 4x4 transformation matrix
            matrix = np.array(detection_result.facial_transformation_matrixes[0]).reshape(4, 4)

            # Extract rotation angles from rotation matrix (top-left 3x3)
            R = matrix[:3, :3]

            # Calculate Euler angles (pitch, yaw, roll) in radians
            pitch = np.arctan2(-R[2, 0], np.sqrt(R[2, 1]**2 + R[2, 2]**2))
            yaw = np.arctan2(R[1, 0], R[0, 0])
            roll = np.arctan2(R[2, 1], R[2, 2])

            row_data['head_pitch'] = pitch
            row_data['head_yaw'] = yaw
            row_data['head_roll'] = roll

        data_rows.append(row_data)
        processed_count += 1

        if processed_count % 100 == 0:
            logging.info(f"Processed {processed_count} frames")

        frame_count += 1

    cap.release()
    logging.info(f"Total frames processed: {processed_count}")

    # Convert to DataFrame and save
    if data_rows:
        df = pd.DataFrame(data_rows)
        df.to_csv(output_csv, index=False)
        logging.info(f"Saved features to {output_csv}")
        logging.info(f"Shape: {df.shape}")
        logging.info(f"Columns: {list(df.columns)}")
        return df
    else:
        logging.warning("No data extracted")
        return None


def batch_process_videos(video_list, model_path, output_dir, frame_interval=5):
    """
    Process multiple videos and save features.

    Args:
        video_list: List of tuples (video_path, label)
        model_path: Path to MediaPipe model
        output_dir: Directory to save CSV files
        frame_interval: Process every nth frame
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_dfs = []

    for video_path, label in video_list:
        video_name = Path(video_path).stem
        output_csv = output_dir / f"{video_name}_features.csv"

        df = extract_features(video_path, label, frame_interval, model_path, output_csv)
        if df is not None:
            all_dfs.append(df)

    # Optionally combine all videos into one CSV
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_csv = output_dir / "all_videos_features.csv"
        combined_df.to_csv(combined_csv, index=False)
        logging.info(f"Saved combined features to {combined_csv}")
        return combined_df

    return None


def process_dataset(dataset_dir, model_path, output_dir, frame_interval=5):
    """
    Process dataset with 'yes' and 'no' subdirectories.

    Args:
        dataset_dir: Path to dataset directory containing 'yes' and 'no' folders
        model_path: Path to MediaPipe model
        output_dir: Directory to save CSV files
        frame_interval: Process every nth frame
    """
    dataset_path = Path(dataset_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Collect all videos with labels
    video_list = []

    # Process 'yes' folder
    yes_folder = dataset_path / "yes"
    if yes_folder.exists():
        for video_file in yes_folder.glob("*.mp4"):
            video_list.append((str(video_file), "yes"))
        logging.info(
            f"Found {len(list(yes_folder.glob('*.mp4')))} videos in 'yes' folder"
        )

    # Process 'no' folder
    no_folder = dataset_path / "no"
    if no_folder.exists():
        for video_file in no_folder.glob("*.mp4"):
            video_list.append((str(video_file), "no"))
        logging.info(
            f"Found {len(list(no_folder.glob('*.mp4')))} videos in 'no' folder"
        )

    logging.info(f"Total videos to process: {len(video_list)}")

    # Process all videos
    all_dfs = []

    for idx, (video_path, label) in enumerate(video_list, 1):
        logging.info(f"\n{'=' * 60}")
        logging.info(
            f"Processing video {idx}/{len(video_list)}: {Path(video_path).name}"
        )
        logging.info(f"Label: {label}")
        logging.info(f"{'=' * 60}")

        video_name = Path(video_path).stem
        # Sanitize filename (remove special characters)
        safe_name = video_name.replace(" ", "_").replace("(", "").replace(")", "")
        output_csv = output_path / f"{label}_{safe_name}_features.csv"

        try:
            df = extract_features(
                video_path, label, frame_interval, model_path, output_csv
            )
            if df is not None:
                all_dfs.append(df)
        except Exception as e:
            logging.error(f"Error processing {video_path}: {e}")
            continue

    # Combine all videos into one CSV
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        combined_csv = output_path / "all_videos_combined.csv"
        combined_df.to_csv(combined_csv, index=False)
        logging.info(f"\n{'=' * 60}")
        logging.info(f"Processing complete!")
        logging.info(f"Saved combined features to {combined_csv}")
        logging.info(f"Total samples: {len(combined_df)}")
        logging.info(f"Yes samples: {len(combined_df[combined_df['label'] == 'yes'])}")
        logging.info(f"No samples: {len(combined_df[combined_df['label'] == 'no'])}")
        logging.info(f"{'=' * 60}")
        return combined_df
    else:
        logging.warning("No data extracted from any video")
        return None


# Example usage
if __name__ == "__main__":
    # Process your dataset structure
    dataset_dir = "dataset"  # Your dataset folder with 'yes' and 'no' subfolders
    model_path = "face_landmarker.task"
    output_dir = "output_features"
    frame_interval = 5  # Process every 5th frame (adjust based on your needs)

    process_dataset(dataset_dir, model_path, output_dir, frame_interval)

    # Alternative: Single video example
    # extract_features(
    #     video_path="dataset/yes/2025-10-18 21-15-40.mp4",
    #     label="yes",
    #     frame_interval=5,
    #     model_path=model_path,
    #     output_csv="single_video_features.csv"
    # )
