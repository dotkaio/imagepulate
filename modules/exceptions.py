"""Custom exceptions for the Imagepulate application."""


class ImagepulateError(Exception):
    """Base exception for all Imagepulate errors."""
    pass


class SamInferenceError(ImagepulateError):
    """Base exception for SAM inference errors."""
    pass


class ModelLoadError(SamInferenceError):
    """Raised when model loading fails."""
    pass


class ModelNotFoundError(ModelLoadError):
    """Raised when a model file is not found."""
    pass


class MaskGenerationError(SamInferenceError):
    """Raised when mask generation fails."""
    pass


class VideoProcessingError(ImagepulateError):
    """Raised when video processing fails."""
    pass


class FrameExtractionError(VideoProcessingError):
    """Raised when frame extraction from video fails."""
    pass


class VideoCreationError(VideoProcessingError):
    """Raised when video creation fails."""
    pass


class ImageProcessingError(ImagepulateError):
    """Raised when image processing fails."""
    pass


class FileOperationError(ImagepulateError):
    """Raised when file operations fail."""
    pass


class ConfigurationError(ImagepulateError):
    """Raised when configuration loading or parsing fails."""
    pass
