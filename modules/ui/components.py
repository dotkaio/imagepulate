"""UI component creation for the Gradio interface."""

import gradio as gr
from gradio_i18n import gettext as _
from gradio_image_prompter import ImagePrompter
from typing import Dict, List, Optional, Any

from modules.constants import (
    AUTOMATIC_MODE, BOX_PROMPT_MODE, PIXELIZE_FILTER, 
    COLOR_FILTER, TRANSPARENT_COLOR_FILTER, TRANSPARENT_VIDEO_FILE_EXT,
    SUPPORTED_VIDEO_FILE_EXT, DEFAULT_COLOR, DEFAULT_PIXEL_SIZE,
    IMAGE_FILE_EXT, VIDEO_FILE_EXT
)
from modules.model_downloader import DEFAULT_MODEL_TYPE


class UIComponents:
    """Factory class for creating Gradio UI components."""
    
    def __init__(self, config_manager, available_models: List[str]):
        """
        Initialize UI components factory.
        
        Args:
            config_manager: Configuration manager instance
            available_models: List of available model names
        """
        self.config_manager = config_manager
        self.available_models = available_models
        self.mask_hparams = config_manager.mask_hparams
    
    def create_mask_parameters(self, hparams: Optional[Dict] = None) -> List[gr.components.Component]:
        """
        Create mask generation parameter components.
        
        Args:
            hparams: Optional hyperparameters dictionary
            
        Returns:
            List of Gradio components for mask parameters
        """
        if hparams is None:
            hparams = self.mask_hparams
        
        return [
            gr.Number(
                label="points_per_side",
                value=hparams["points_per_side"],
                interactive=True
            ),
            gr.Number(
                label="points_per_batch",
                value=hparams["points_per_batch"],
                interactive=True
            ),
            gr.Slider(
                label="pred_iou_thresh",
                value=hparams["pred_iou_thresh"],
                minimum=0,
                maximum=1,
                interactive=True
            ),
            gr.Slider(
                label="stability_score_thresh",
                value=hparams["stability_score_thresh"],
                minimum=0,
                maximum=1,
                interactive=True
            ),
            gr.Slider(
                label="stability_score_offset",
                value=hparams["stability_score_offset"],
                minimum=0,
                maximum=1
            ),
            gr.Number(
                label="crop_n_layers",
                value=hparams["crop_n_layers"]
            ),
            gr.Slider(
                label="box_nms_thresh",
                value=hparams["box_nms_thresh"],
                minimum=0,
                maximum=1
            ),
            gr.Number(
                label="crop_n_points_downscale_factor",
                value=hparams["crop_n_points_downscale_factor"]
            ),
            gr.Number(
                label="min_mask_region_area",
                value=hparams["min_mask_region_area"]
            ),
            gr.Checkbox(
                label="use_m2m",
                value=hparams["use_m2m"]
            )
        ]
    
    def create_video_segmentation_inputs(self, default_filter: str) -> Dict[str, gr.components.Component]:
        """
        Create input components for video segmentation tab.
        
        Args:
            default_filter: Default filter mode
            
        Returns:
            Dictionary of named Gradio components
        """
        return {
            'file_input': gr.File(
                label=_("Upload Input Video"),
                file_types=IMAGE_FILE_EXT + VIDEO_FILE_EXT
            ),
            'frame_prompter': ImagePrompter(
                label=_("Prompt image with Box & Point"),
                type='pil',
                interactive=True,
                scale=5
            ),
            'frame_slider': gr.Slider(
                label=_("Frame Index"),
                interactive=False
            ),
            'preview_image': gr.Image(
                label=_("Preview"),
                interactive=False,
                scale=5
            ),
            'model_dropdown': gr.Dropdown(
                label=_("Model"),
                value=DEFAULT_MODEL_TYPE,
                choices=self.available_models
            ),
            'filter_dropdown': gr.Dropdown(
                label=_("Filter Modes"),
                interactive=True,
                value=default_filter,
                choices=[PIXELIZE_FILTER, COLOR_FILTER, TRANSPARENT_COLOR_FILTER]
            ),
            'color_picker': gr.ColorPicker(
                label=_("Solid Color"),
                interactive=True,
                visible=default_filter == COLOR_FILTER,
                value=DEFAULT_COLOR
            ),
            'pixel_size': gr.Number(
                label=_("Pixel Size"),
                interactive=True,
                minimum=1,
                visible=default_filter == PIXELIZE_FILTER,
                value=DEFAULT_PIXEL_SIZE
            ),
            'output_format': gr.Dropdown(
                label=_("Video File Format"),
                choices=TRANSPARENT_VIDEO_FILE_EXT if default_filter == TRANSPARENT_COLOR_FILTER 
                        else SUPPORTED_VIDEO_FILE_EXT,
                value=TRANSPARENT_VIDEO_FILE_EXT[0] if default_filter == TRANSPARENT_COLOR_FILTER 
                      else SUPPORTED_VIDEO_FILE_EXT[0]
            ),
            'invert_mask': gr.Checkbox(
                label=_("invert mask"),
                value=self.mask_hparams["invert_mask"]
            )
        }
    
    def create_video_segmentation_outputs(self) -> Dict[str, gr.components.Component]:
        """
        Create output components for video segmentation tab.
        
        Returns:
            Dictionary of named Gradio components
        """
        return {
            'video_output': gr.Video(
                label=_("Output Video"),
                interactive=False,
                scale=7
            ),
            'file_output': gr.File(
                label=_("Downloadable Output File"),
                scale=9
            )
        }
    
    def create_layer_divider_inputs(self, default_mode: str) -> Dict[str, gr.components.Component]:
        """
        Create input components for layer divider tab.
        
        Args:
            default_mode: Default input mode
            
        Returns:
            Dictionary of named Gradio components
        """
        return {
            'image_input': gr.Image(
                label=_("Input image here"),
                visible=default_mode == AUTOMATIC_MODE
            ),
            'image_prompter': ImagePrompter(
                label=_("Prompt image with Box & Point"),
                type='pil',
                visible=default_mode == BOX_PROMPT_MODE
            ),
            'mode_dropdown': gr.Dropdown(
                label=_("Image Input Mode"),
                value=default_mode,
                choices=[AUTOMATIC_MODE, BOX_PROMPT_MODE]
            ),
            'model_dropdown': gr.Dropdown(
                label=_("Model"),
                value=DEFAULT_MODEL_TYPE,
                choices=self.available_models
            ),
            'invert_mask': gr.Checkbox(
                label=_("invert mask"),
                value=self.mask_hparams["invert_mask"]
            ),
            'multimask_output': gr.Checkbox(
                label=_("multimask_output"),
                value=self.mask_hparams["multimask_output"]
            )
        }
    
    def create_layer_divider_outputs(self) -> Dict[str, gr.components.Component]:
        """
        Create output components for layer divider tab.
        
        Returns:
            Dictionary of named Gradio components
        """
        return {
            'gallery_output': gr.Gallery(
                label=_("Output images will be shown here")
            ),
            'file_output': gr.File(
                label=_("Generated psd file"),
                scale=9
            )
        }
