import cv2

from src.detector import OCRDetector
from src.recognizer import TextRecognizer
from src.tts import TextToSpeech


def main():

    print("=" * 60)
    print("SMART BLIND CANE - REAL-TIME OCR")
    print("=" * 60)

    # --------------------------------------------------
    # CAMERA
    # --------------------------------------------------

    print("\nOpening camera...")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open camera.")
        return

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------

    print("\nLoading OCR model...")

    detector = OCRDetector()
    recognizer = TextRecognizer()

    # --------------------------------------------------
    # TTS
    # --------------------------------------------------

    print("\nInitializing Text-to-Speech...")

    tts = TextToSpeech()

    print("\nSystem ready.")
    print("Press SPACE to capture and read text.")
    print("Press Q to quit.")

    # --------------------------------------------------
    # LIVE CAMERA
    # --------------------------------------------------

    while True:

        ret, frame = camera.read()

        if not ret:
            print("ERROR: Could not read camera frame.")
            break

        # Display live camera
        cv2.imshow(
            "Smart Blind Cane - Camera",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # --------------------------------------------------
        # QUIT
        # --------------------------------------------------

        if key == ord("q"):

            break

        # --------------------------------------------------
        # CAPTURE + OCR
        # --------------------------------------------------

        if key == ord(" "):

            print("\n" + "=" * 60)
            print("CAPTURED FRAME")
            print("=" * 60)

            print("\nRunning OCR...")

            detections = detector.detect(
                frame
            )

            detections = recognizer.process(
                detections
            )

            # ----------------------------------------------
            # NO TEXT
            # ----------------------------------------------

            if not detections:

                print("\nNo text detected.")

                tts.speak(
                    "No text detected."
                )

                continue

            # ----------------------------------------------
            # DISPLAY DETECTED TEXT
            # ----------------------------------------------

            print("\nDETECTED TEXT")
            print("-" * 60)

            for index, detection in enumerate(
                detections,
                start=1
            ):

                print(
                    f"{index}. "
                    f"{detection['text']} "
                    f"| Confidence: "
                    f"{detection['confidence']:.2f}"
                )

            # ----------------------------------------------
            # COMBINE TEXT
            # ----------------------------------------------

            final_text = recognizer.combine_text(
                detections
            )

            print("\nFINAL TEXT")
            print("-" * 60)

            print(final_text)

            # ----------------------------------------------
            # DRAW BOUNDING BOXES
            # ----------------------------------------------

            annotated = detector.draw_boxes(
                frame,
                detections
            )

            # Show OCR result
            cv2.imshow(
                "OCR Result",
                annotated
            )

            # ----------------------------------------------
            # SPEAK TEXT
            # ----------------------------------------------

            print("\nSpeaking detected text...")

            tts.speak(
                final_text
            )

            print("\nReady for next capture.")

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------

    camera.release()

    cv2.destroyAllWindows()

    print("\nCamera closed.")
    print("Program ended.")


if __name__ == "__main__":
    main()