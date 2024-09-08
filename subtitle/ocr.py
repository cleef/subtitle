# -*- coding: utf-8 -*-

import cv2
from easyocr import Reader


def sort_by_yx(results, y_threshold=10):
    # First sort by Y-coordinate, then by X-coordinate if they are on the same line
    results_sorted = sorted(results, key=lambda r: (round(r[0][0][1] / y_threshold), r[0][0][0]))
    return results_sorted


def merge_text(results):
    sorted_results = sort_by_yx(results)
    merged_text = ' '.join([text for (_, text, _) in sorted_results])
    return merged_text


class OCR:
    def __init__(self, gpu=True):
        self.reader = Reader(['en'], gpu=gpu)

    def read_text(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray_frame.shape
        roi = gray_frame[int(h*0.7):h, :]  # Adjust the region as needed
        results = self.reader.readtext(roi)
        merged_text = merge_text(results)
        return merged_text
    

    def read_text_from_video(self, video_path, subtitle_file, start_time=0, end_time=None):
        # Load video
        cap = cv2.VideoCapture(video_path)

        # Get the video frame rate
        fps = 0.5  # Extract text every second
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = round(video_fps / fps)  # Process every 'fps' frames per second

        # Calculate start and end frames
        start_frame = int(start_time * video_fps)
        end_frame = int(end_time * video_fps) if end_time else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(frame_interval)

        recognized_text = []
        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame_number > end_frame:
                break

            if frame_number >= start_frame and frame_number % frame_interval == 0:
                text = self.read_text(frame)
                if text.strip():
                    recognized_text.append(f'{text}\n')
                print(f'Processed {frame_number/round(video_fps)} seconds of video')

            del frame
            frame_number += 1

        cap.release()
        with open(subtitle_file, 'w') as f:
            f.writelines(recognized_text)