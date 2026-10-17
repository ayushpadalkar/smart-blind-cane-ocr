"""
exceptions.py
---------------------------------------

Custom Exceptions for Smart Blind Cane OCR

Author : Ayush Padalkar
"""


class BlindCaneOCRError(Exception):
    """
    Base Exception for the OCR Project
    """
    pass


class CameraError(BlindCaneOCRError):
    """
    Raised when camera initialization or image capture fails.
    """
    pass


class ImageProcessingError(BlindCaneOCRError):
    """
    Raised when preprocessing fails.
    """
    pass


class OCRError(BlindCaneOCRError):
    """
    Raised when PaddleOCR fails.
    """
    pass


class RecognitionError(BlindCaneOCRError):
    """
    Raised when recognized text cannot be processed.
    """
    pass


class SpeechError(BlindCaneOCRError):
    """
    Raised when Text-To-Speech fails.
    """
    pass


class FileNotFoundErrorOCR(BlindCaneOCRError):
    """
    Raised when an image or file is missing.
    """
    pass


class ConfigurationError(BlindCaneOCRError):
    """
    Raised when configuration values are invalid.
    """
    pass


if __name__ == "__main__":

    try:
        raise CameraError("Camera could not be opened.")

    except BlindCaneOCRError as error:
        print(error)