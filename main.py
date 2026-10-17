"""Entry point for BlindCaneOCR."""

if __name__=='__main__':
    print('BlindCaneOCR project initialized')
"""
main.py
--------------------------------------------------
Smart Blind Cane OCR - Initial Demonstration

Complete pipeline:

    Camera
       ↓
    Image
       ↓
    Preprocessing
       ↓
    PaddleOCR
       ↓
    Text Processing
       ↓
    Text-to-Speech

Author : Ayush Padalkar
"""

import cv2

from camera_ocr import Camera
from src.preprocess import ImagePreprocessor
from src.detector import OCRDetector
from src.recognizer import TextRecognizer
from src.tts import TextToSpeech

from src.logger import logger
from src.exceptions import (
    CameraError,
    ImageProcessingError,
    OCRError,
    RecognitionError,
    SpeechError,
)


class SmartBlindCaneOCR:
    """
    Main controller for the Smart Blind Cane OCR system.
    """

    def __init__(self):

        logger.info(
            "Initializing Smart Blind Cane OCR..."
        )

        self.camera = Camera()

        self.preprocessor = ImagePreprocessor()

        self.detector = OCRDetector()

        self.recognizer = TextRecognizer()

        self.tts = TextToSpeech()

        logger.info(
            "Smart Blind Cane OCR initialized successfully."
        )

    # ==========================================================
    # RUN CAMERA
    # ==========================================================

    def run_camera(self):

        """
        Start camera and capture an image.

        Returns
        -------
        frame
            Captured OpenCV image.
        """

        try:

            self.camera.start()

            logger.info(
                "Camera ready."
            )

            frame, image_path = (
                self.camera.preview()
            )

            if frame is None:

                logger.warning(
                    "No image captured."
                )

                return None

            logger.info(
                f"Image captured: {image_path}"
            )

            return frame

        except Exception as error:

            logger.exception(
                "Camera operation failed."
            )

            raise CameraError(
                f"Camera operation failed: {error}"
            ) from error

    # ==========================================================
    # PROCESS IMAGE
    # ==========================================================

    def process_image(self, image):

        """
        Process a captured image through
        preprocessing → OCR → text processing → speech.
        """

        # ------------------------------------------------------
        # PREPROCESSING
        # ------------------------------------------------------

        try:

            logger.info(
                "Starting image preprocessing..."
            )

            processed_image = (
                self.preprocessor.process(image)
            )

            logger.info(
                "Image preprocessing completed."
            )

        except Exception as error:

            logger.exception(
                "Image preprocessing failed."
            )

            raise ImageProcessingError(
                f"Preprocessing failed: {error}"
            ) from error

        # ------------------------------------------------------
        # OCR
        # ------------------------------------------------------

        try:

            logger.info(
                "Starting PaddleOCR..."
            )

            results = self.detector.detect(
                processed_image
            )

            detections = (
                self.detector.extract_details(
                    results
                )
            )

            logger.info(
                f"OCR detections: "
                f"{len(detections)}"
            )

        except Exception as error:

            logger.exception(
                "OCR processing failed."
            )

            raise OCRError(
                f"OCR failed: {error}"
            ) from error

        # ------------------------------------------------------
        # DRAW OCR BOXES
        # ------------------------------------------------------

        try:

            # Convert grayscale processed image
            # back to BGR for visualization.

            if len(processed_image.shape) == 2:

                display_image = cv2.cvtColor(
                    processed_image,
                    cv2.COLOR_GRAY2BGR
                )

            else:

                display_image = (
                    processed_image.copy()
                )

            annotated_image = (
                self.detector.draw_boxes(
                    display_image,
                    detections
                )
            )

            self.detector.save_result(
                annotated_image
            )

        except Exception as error:

            logger.warning(
                f"Could not create annotated image: "
                f"{error}"
            )

        # ------------------------------------------------------
        # TEXT PROCESSING
        # ------------------------------------------------------

        try:

            processed_detections = (
                self.recognizer.process(
                    detections
                )
            )

            final_text = (
                self.recognizer.combine_text(
                    processed_detections
                )
            )

        except Exception as error:

            logger.exception(
                "Text recognition failed."
            )

            raise RecognitionError(
                f"Text processing failed: {error}"
            ) from error

        # ------------------------------------------------------
        # DISPLAY TEXT
        # ------------------------------------------------------

        print("\n")
        print("=" * 60)
        print("RECOGNIZED TEXT")
        print("=" * 60)

        if final_text:

            print(final_text)

        else:

            print(
                "No readable text detected."
            )

        print("=" * 60)

        # ------------------------------------------------------
        # TEXT TO SPEECH
        # ------------------------------------------------------

        if final_text:

            try:

                self.tts.speak(
                    final_text
                )

            except Exception as error:

                logger.exception(
                    "Speech failed."
                )

                raise SpeechError(
                    f"Speech failed: {error}"
                ) from error

        else:

            self.tts.speak(
                "I could not detect any readable text."
            )

        return final_text

    # ==========================================================
    # MAIN APPLICATION
    # ==========================================================

    def run(self):

        """
        Run the complete Smart Blind Cane OCR system.
        """

        logger.info(
            "Starting Smart Blind Cane OCR demo."
        )

        print()
        print("=" * 60)
        print("       SMART BLIND CANE OCR")
        print("=" * 60)
        print()
        print("Controls:")
        print("SPACE → Capture image and read text")
        print("ESC   → Exit")
        print()
        print("=" * 60)

        try:

            while True:

                # ------------------------------------------------
                # Start camera
                # ------------------------------------------------

                self.camera.start()

                while True:

                    ret, frame = (
                        self.camera.camera.read()
                    )

                    if not ret:

                        logger.error(
                            "Failed to read camera frame."
                        )

                        break

                    cv2.imshow(
                        "Smart Blind Cane Camera",
                        frame
                    )

                    key = cv2.waitKey(1) & 0xFF

                    # --------------------------------------------
                    # ESC → EXIT
                    # --------------------------------------------

                    if key == 27:

                        logger.info(
                            "Exit requested."
                        )

                        return

                    # --------------------------------------------
                    # SPACE → CAPTURE
                    # --------------------------------------------

                    if key == 32:

                        logger.info(
                            "Capture button pressed."
                        )

                        captured_frame = (
                            frame.copy()
                        )

                        # Save image
                        self.camera.save_frame(
                            captured_frame
                        )

                        break

                # ------------------------------------------------
                # Process captured image
                # ------------------------------------------------

                if captured_frame is not None:

                    self.process_image(
                        captured_frame
                    )

                    print()
                    print(
                        "Press SPACE to scan again."
                    )
                    print(
                        "Press ESC to exit."
                    )

                    # --------------------------------------------
                    # Wait for next action
                    # --------------------------------------------

                    while True:

                        key = (
                            cv2.waitKey(1)
                            & 0xFF
                        )

                        if key == 27:

                            return

                        if key == 32:

                            break

        except KeyboardInterrupt:

            logger.info(
                "Application interrupted by user."
            )

        finally:

            self.camera.release()

            cv2.destroyAllWindows()

            logger.info(
                "Smart Blind Cane OCR stopped."
            )


# ==============================================================
# PROGRAM ENTRY POINT
# ==============================================================

def main():

    try:

        application = SmartBlindCaneOCR()

        application.run()

    except CameraError as error:

        print(
            f"\nCamera Error: {error}"
        )

    except ImageProcessingError as error:

        print(
            f"\nImage Processing Error: {error}"
        )

    except OCRError as error:

        print(
            f"\nOCR Error: {error}"
        )

    except RecognitionError as error:

        print(
            f"\nRecognition Error: {error}"
        )

    except SpeechError as error:

        print(
            f"\nSpeech Error: {error}"
        )

    except Exception as error:

        logger.exception(
            "Unexpected application error."
        )

        print(
            f"\nUnexpected Error: {error}"
        )


# ==============================================================
# START PROGRAM
# ==============================================================

if __name__ == "__main__":

    main()