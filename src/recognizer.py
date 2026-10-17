import re

from .config import OCR_CONFIDENCE


class TextRecognizer:

    def clean_text(
        self,
        text
    ):

        if not text:
            return ""

        text = text.strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    def remove_duplicates(
        self,
        texts
    ):

        cleaned = []

        for text in texts:

            text = self.clean_text(
                text
            )

            if not text:
                continue

            if text not in cleaned:

                cleaned.append(
                    text
                )

        return cleaned

    # =========================================================
    # FILTER CONFIDENCE
    # =========================================================

    def filter_confidence(
        self,
        detections
    ):

        return [
            detection
            for detection in detections
            if detection.get(
                "confidence",
                0
            ) >= OCR_CONFIDENCE
        ]

    # =========================================================
    # SORT READING ORDER
    # =========================================================

    def sort_reading_order(
        self,
        detections
    ):

        return sorted(
            detections,
            key=lambda item: (
                item["bbox"][0][1],
                item["bbox"][0][0]
            )
        )

    # =========================================================
    # PROCESS
    # =========================================================

    def process(
        self,
        detections
    ):

        detections = (
            self.filter_confidence(
                detections
            )
        )

        detections = (
            self.sort_reading_order(
                detections
            )
        )

        for detection in detections:

            detection["text"] = (
                self.clean_text(
                    detection["text"]
                )
            )

        return detections

    # =========================================================
    # COMBINE TEXT
    # =========================================================

    def combine_text(
        self,
        detections
    ):

        texts = [
            detection["text"]
            for detection in detections
            if detection.get("text")
        ]

        return " ".join(
            texts
        )