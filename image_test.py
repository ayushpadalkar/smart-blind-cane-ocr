from pathlib import Path

from src.detector import OCRDetector
from src.recognizer import TextRecognizer
from src.tts import TextToSpeech
from src.preprocess import load_image


IMAGE_PATH = Path(
    "assets/images/images.png"
)


def main():

    print("=" * 60)
    print("SMART BLIND CANE - OCR TEST")
    print("=" * 60)

    # =====================================================
    # LOAD IMAGE
    # =====================================================

    print("\nLoading image...")

    image = load_image(
        IMAGE_PATH
    )

    print(
        f"Image loaded: "
        f"{image.shape[1]} x "
        f"{image.shape[0]}"
    )

    # =====================================================
    # LOAD OCR
    # =====================================================

    detector = OCRDetector()

    recognizer = TextRecognizer()

    # =====================================================
    # OCR
    # =====================================================

    print("\nRunning OCR...")

    detections = detector.detect(
        image
    )

    # =====================================================
    # PROCESS RESULTS
    # =====================================================

    detections = recognizer.process(
        detections
    )

    # =====================================================
    # DISPLAY TEXT
    # =====================================================

    print("\n" + "=" * 60)
    print("DETECTED TEXT")
    print("=" * 60)

    if not detections:

        print("No text detected.")

        return

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

    # =====================================================
    # COMBINE TEXT
    # =====================================================

    final_text = (
        recognizer.combine_text(
            detections
        )
    )

    print("\n" + "=" * 60)
    print("FINAL TEXT")
    print("=" * 60)

    print(final_text)

    # =====================================================
    # DRAW RESULT
    # =====================================================

    annotated = detector.draw_boxes(
        image,
        detections
    )

    detector.save_result(
        annotated
    )

    # =====================================================
    # TEXT TO SPEECH
    # =====================================================

    if final_text:

        print(
            "\nSpeaking detected text..."
        )

        tts = TextToSpeech()

        tts.speak(
            final_text
        )

    else:

        print(
            "\nNo text detected."
        )


if __name__ == "__main__":
    main()