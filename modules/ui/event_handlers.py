"""Event handlers for Gradio UI components."""

import gradio as gr
from gradio_i18n import gettext as _
from gradio_image_prompter import ImagePrompter
from gradio_image_prompter.image_prompter import PromptValue
from typing import Dict, List, Any, Optional

from modules.constants import (
    AUTOMATIC_MODE, BOX_PROMPT_MODE, PIXELIZE_FILTER,
    COLOR_FILTER, TRANSPARENT_COLOR_FILTER, TRANSPARENT_VIDEO_FILE_EXT,
    SUPPORTED_VIDEO_FILE_EXT
)
from modules.video_utils import get_frames_from_dir
from modules.paths import TEMP_DIR
from modules.logger_util import get_logger

logger = get_logger()


class EventHandlers:
    """Handles all Gradio event callbacks."""

    def __init__(self, sam_inference):
        """
        Initialize event handlers.

        Args:
            sam_inference: SamInference instance for processing
        """
        self.sam_inf = sam_inference

    @staticmethod
    def on_mode_change(mode: str) -> List[gr.components.Component]:
        """
        Handle input mode change event.

        Args:
            mode: Selected input mode (AUTOMATIC_MODE or BOX_PROMPT_MODE)

        Returns:
            List of updated components with visibility settings
        """
        return [
            gr.Image(visible=mode == AUTOMATIC_MODE),
            ImagePrompter(visible=mode == BOX_PROMPT_MODE),
            gr.Accordion(visible=mode == AUTOMATIC_MODE),
        ]

    @staticmethod
    def on_filter_mode_change(mode: str) -> List[gr.components.Component]:
        """
        Handle filter mode change event.

        Args:
            mode: Selected filter mode

        Returns:
            List of updated components with visibility settings
        """
        return [
            gr.ColorPicker(visible=mode == COLOR_FILTER),
            gr.Number(visible=mode == PIXELIZE_FILTER),
            gr.Dropdown(
                choices=TRANSPARENT_VIDEO_FILE_EXT if mode == TRANSPARENT_COLOR_FILTER
                else SUPPORTED_VIDEO_FILE_EXT,
                value=TRANSPARENT_VIDEO_FILE_EXT[0] if mode == TRANSPARENT_COLOR_FILTER
                else SUPPORTED_VIDEO_FILE_EXT[0]
            )
        ]

    def on_video_model_change(
        self,
        model_type: str,
        vid_input: Optional[str],
        progress: gr.Progress = gr.Progress()
    ) -> List[gr.components.Component]:
        """
        Handle video model or input change event.

        Args:
            model_type: Selected model type
            vid_input: Path to input video file
            progress: Gradio progress indicator

        Returns:
            List of updated components (prompter and frame slider)
        """
        if not vid_input or vid_input is None:
            return [
                ImagePrompter(
                    label=_("Prompt image with Box & Point"),
                    type='pil',
                    interactive=True,
                    scale=5
                ),
                gr.Slider(label=_("Frame Index"), interactive=False)
            ]

        progress(0, desc=_("Extracting frames..."))

        self.sam_inf.init_video_inference_state(
            vid_input=vid_input,
            model_type=model_type
        )

        frames = get_frames_from_dir(vid_dir=TEMP_DIR)
        initial_frame = frames[0]
        max_frame_index = len(frames) - 1
        i_value = PromptValue(image=initial_frame, points=[])

        return [
            ImagePrompter(
                label=_("Prompt image with Box & Point"),
                value=i_value
            ),
            gr.Slider(
                label=_("Frame Index"),
                value=0,
                interactive=True,
                step=1,
                minimum=0,
                maximum=max_frame_index
            )
        ]

    @staticmethod
    def on_frame_change(frame_idx: int) -> ImagePrompter:
        """
        Handle frame selection change event.

        Args:
            frame_idx: Selected frame index

        Returns:
            Updated ImagePrompter with the selected frame
        """
        frames = get_frames_from_dir(vid_dir=TEMP_DIR)
        selected_frame = frames[frame_idx]
        n_value = PromptValue(image=selected_frame, points=[])
        return ImagePrompter(
            label=_("Prompt image with Box & Point"),
            value=n_value
        )

    @staticmethod
    def on_prompt_change(prompt: Dict[str, Any]) -> gr.Image:
        """
        Handle prompt change event.

        Args:
            prompt: Dictionary containing image and points

        Returns:
            Updated Image component with the prompted image
        """
        image = prompt["image"]
        return gr.Image(label=_("Preview"), value=image)
