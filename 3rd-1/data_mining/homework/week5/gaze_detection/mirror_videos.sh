#!/bin/bash

# Mirror all videos in dataset (horizontal flip)
# This script uses ffmpeg to create horizontally flipped versions of all videos

echo "=========================================="
echo "Video Dataset Mirror Script"
echo "=========================================="
echo ""

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "Error: ffmpeg is not installed!"
    echo "Please install ffmpeg first:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Arch: sudo pacman -S ffmpeg"
    echo "  macOS: brew install ffmpeg"
    exit 1
fi

# Create backup directory
BACKUP_DIR="dataset_backup"
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# Process yes folder
echo ""
echo "Processing 'yes' folder..."
echo "=========================================="

if [ -d "dataset/yes" ]; then
    yes_count=0
    for video in dataset/yes/*.mp4; do
        if [ -f "$video" ]; then
            filename=$(basename "$video")
            name="${filename%.*}"
            ext="${filename##*.}"

            # Create mirrored filename
            mirrored_file="dataset/yes/${name}_mirrored.${ext}"

            # Check if mirrored file already exists
            if [ -f "$mirrored_file" ]; then
                echo "  [SKIP] $mirrored_file already exists"
            else
                echo "  [PROCESSING] $filename -> ${name}_mirrored.${ext}"

                # Use ffmpeg to horizontally flip the video
                # -vf hflip: horizontal flip filter
                # -c:a copy: copy audio without re-encoding
                ffmpeg -i "$video" -vf hflip -c:a copy "$mirrored_file" -y -loglevel error

                if [ $? -eq 0 ]; then
                    echo "  [SUCCESS] Created $mirrored_file"
                    ((yes_count++))
                else
                    echo "  [ERROR] Failed to create $mirrored_file"
                fi
            fi
        fi
    done
    echo ""
    echo "Processed $yes_count new videos in 'yes' folder"
else
    echo "  'yes' folder not found!"
fi

# Process no folder
echo ""
echo "Processing 'no' folder..."
echo "=========================================="

if [ -d "dataset/no" ]; then
    no_count=0
    for video in dataset/no/*.mp4; do
        if [ -f "$video" ]; then
            filename=$(basename "$video")
            name="${filename%.*}"
            ext="${filename##*.}"

            # Create mirrored filename
            mirrored_file="dataset/no/${name}_mirrored.${ext}"

            # Check if mirrored file already exists
            if [ -f "$mirrored_file" ]; then
                echo "  [SKIP] $mirrored_file already exists"
            else
                echo "  [PROCESSING] $filename -> ${name}_mirrored.${ext}"

                # Use ffmpeg to horizontally flip the video
                ffmpeg -i "$video" -vf hflip -c:a copy "$mirrored_file" -y -loglevel error

                if [ $? -eq 0 ]; then
                    echo "  [SUCCESS] Created $mirrored_file"
                    ((no_count++))
                else
                    echo "  [ERROR] Failed to create $mirrored_file"
                fi
            fi
        fi
    done
    echo ""
    echo "Processed $no_count new videos in 'no' folder"
else
    echo "  'no' folder not found!"
fi

# Summary
echo ""
echo "=========================================="
echo "Summary:"
echo "=========================================="
echo "Total new mirrored videos created: $((yes_count + no_count))"
echo "  - Yes folder: $yes_count"
echo "  - No folder: $no_count"
echo ""

# Count total videos now
total_yes=$(ls dataset/yes/*.mp4 2>/dev/null | wc -l)
total_no=$(ls dataset/no/*.mp4 2>/dev/null | wc -l)

echo "Total videos in dataset:"
echo "  - Yes folder: $total_yes videos"
echo "  - No folder: $total_no videos"
echo "  - Total: $((total_yes + total_no)) videos"
echo ""
echo "Done!"
echo "=========================================="
