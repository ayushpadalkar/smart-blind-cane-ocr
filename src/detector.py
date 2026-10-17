from pathlib import Path

import cv2

from paddleocr import PaddleOCR

from .config import (
    OCR_CONFIDENCE,
    OCR_VERSION,
)


class OCRDetector:

    def __init__(self):

        print("Loading PaddleOCR PP-OCRv5 Mobile models...")

        self.ocr = PaddleOCR(
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",

            # We don't need these extra modules
            # for our basic OCR task.

            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,

            lang="en",
        )

        print(
            "PaddleOCR PP-OCRv5 Mobile "
            "models loaded successfully."
        )

    # =========================================================
    # OCR
    # =========================================================

    def detect(self, image):

        results = self.ocr.predict(
            image
        )

        detections = []

        for result in results:

            # PaddleOCR returns a result object
            # containing OCR information.

            try:
                data = result.json
            except Exception:
                data = None

            if data is None:
                continue

            # Some PaddleOCR versions expose
            # the result as a dictionary.

            if callable(data):
                data = data()

            if not isinstance(data, dict):
                continue

            ocr_data = data.get(
                "res",
                data
            )

            texts = ocr_data.get(
                "rec_texts",
                []
            )

            scores = ocr_data.get(
                "rec_scores",
                []
            )

            boxes = ocr_data.get(
                "rec_polys",
                []
            )

            for text, score, box in zip(
                texts,
                scores,
                boxes
            ):

                try:
                    score = float(score)
                except Exception:
                    score = 0.0

                if score < OCR_CONFIDENCE:
                    continue

                if not text:
                    continue

                box = [
                    [int(point[0]), int(point[1])]
                    for point in box
                ]

                detections.append(
                    {
                        "text": str(text),
                        "confidence": score,
                        "bbox": box,
                    }
                )

        return detections

    # =========================================================
    # DRAW BOXES
    # =========================================================

    def draw_boxes(
        self,
        image,
        detections
    ):

        annotated = image.copy()

        for detection in detections:

            box = detection["bbox"]

            text = detection["text"]

            confidence = detection[
                "confidence"
            ]

            

            # Convert to numpy array

            import numpy as np

            points = np.array(
                box,
                dtype=np.int32
            )

            cv2.polylines(
                annotated,
                [points],
                True,
                (0, 255, 0),
                2
            )

            x = int(
                points[0][0]
            )

            y = max(
                20,
                int(points[0][1]) - 10
            )

            label = (
                f"{text} "
                f"({confidence:.2f})"
            )

            cv2.putText(
                annotated,
                label,
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        return annotated

    # =========================================================
    # SAVE RESULT
    # =========================================================

    def save_result(
        self,
        image,
        filename="ocr_result.jpg"
    ):

        from .config import OUTPUT_DIR

        OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path = (
            OUTPUT_DIR /
            filename
        )

        cv2.imwrite(
            str(output_path),
            image
        )

        print(
            f"Saved result to: {output_path}"
        )