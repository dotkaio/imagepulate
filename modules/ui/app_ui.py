"""Main UI class for the Gradio application."""

import gradio as gr
from gradio_i18n import Translate, gettext as _
from typing import Dict, Any
import os
import argparse

from modules.html_constants import HEADER, CSS
from modules.paths import I18N_YAML
from modules.constants import (
    AUTOMATIC_MODE, BOX_PROMPT_MODE, PIXELIZE_FILTER,
    COLOR_FILTER, DEFAULT_COLOR, DEFAULT_PIXEL_SIZE
)
from modules.ui.components import UIComponents
from modules.ui.event_handlers import EventHandlers
from modules.utils.config_manager import get_config_manager
from modules.utils import open_folder
from modules.logger_util import get_logger

logger = get_logger()


class AppUI:
    """Handles Gradio UI creation and layout."""
    
    def __init__(self, args: argparse.Namespace, sam_inference):
        """
        Initialize the UI.
        
        Args:
            args: Command line arguments
            sam_inference: SamInference instance
        """
        self.args = args
        self.sam_inf = sam_inference
        self.i18n = Translate(I18N_YAML)
        
        # Get configuration
        self.config_manager = get_config_manager()
        
        # Initialize UI components and event handlers
        self.ui_components = UIComponents(
            self.config_manager,
            sam_inference.available_models
        )
        self.event_handlers = EventHandlers(sam_inference)
        
        # UI settings
        self.image_modes = [AUTOMATIC_MODE, BOX_PROMPT_MODE]
        self.default_mode = BOX_PROMPT_MODE
        self.filter_modes = [PIXELIZE_FILTER, COLOR_FILTER]
        self.default_filter = COLOR_FILTER
        self.default_color = DEFAULT_COLOR
        self.default_pixel_size = DEFAULT_PIXEL_SIZE
    
    def create_video_segmentation_tab(self) -> None:
        """Create the video segmentation tab UI."""
        mask_hparams = self.config_manager.mask_hparams
        
        with gr.TabItem(_("Video Segmentation")):
            with gr.Column():
                # Create input components
                inputs = self.ui_components.create_video_segmentation_inputs(
                    self.default_filter
                )
                
                with gr.Row(equal_height=True):
                    with gr.Column(scale=9):
                        file_vid_input = inputs['file_input']
                        vid_frame_prompter = inputs['frame_prompter']
                        sld_frame_selector = inputs['frame_slider']
                        img_preview = inputs['preview_image']
                    
                    with gr.Column(scale=1):
                        dd_models = inputs['model_dropdown']
                        dd_filter_mode = inputs['filter_dropdown']
                        cp_color_picker = inputs['color_picker']
                        nb_pixel_size = inputs['pixel_size']
                        dd_output_mime_type = inputs['output_format']
                        cb_invert_mask = inputs['invert_mask']
                        btn_generate_preview = gr.Button(_("GENERATE PREVIEW"))
            
            with gr.Row():
                btn_generate = gr.Button(_("GENERATE VIDEO"), variant="primary")
            
            # Create output components
            outputs = self.ui_components.create_video_segmentation_outputs()
            
            with gr.Row():
                vid_output = outputs['video_output']
                with gr.Column(scale=2):
                    output_file = outputs['file_output']
                    btn_open_folder = gr.Button(_("📁 Open Output folder"), scale=1)
            
            # Wire up event handlers
            file_vid_input.change(
                fn=self.event_handlers.on_video_model_change,
                inputs=[dd_models, file_vid_input],
                outputs=[vid_frame_prompter, sld_frame_selector]
            )
            
            dd_models.change(
                fn=self.event_handlers.on_video_model_change,
                inputs=[dd_models, file_vid_input],
                outputs=[vid_frame_prompter, sld_frame_selector]
            )
            
            sld_frame_selector.change(
                fn=self.event_handlers.on_frame_change,
                inputs=[sld_frame_selector],
                outputs=[vid_frame_prompter]
            )
            
            dd_filter_mode.change(
                fn=self.event_handlers.on_filter_mode_change,
                inputs=[dd_filter_mode],
                outputs=[cp_color_picker, nb_pixel_size, dd_output_mime_type]
            )
            
            preview_params = [
                vid_frame_prompter, dd_filter_mode, sld_frame_selector,
                nb_pixel_size, cp_color_picker, cb_invert_mask
            ]
            
            video_params = [
                vid_frame_prompter, dd_filter_mode, sld_frame_selector,
                nb_pixel_size, cp_color_picker, dd_output_mime_type, cb_invert_mask
            ]
            
            btn_generate_preview.click(
                fn=self.sam_inf.add_filter_to_preview,
                inputs=preview_params,
                outputs=[img_preview]
            )
            
            btn_generate.click(
                fn=self.sam_inf.create_filtered_video,
                inputs=video_params,
                outputs=[vid_output, output_file]
            )
            
            btn_open_folder.click(
                fn=lambda: open_folder(os.path.join(self.args.output_dir, "filter")),
                inputs=None,
                outputs=None
            )
    
    def create_layer_divider_tab(self) -> None:
        """Create the layer divider tab UI."""
        mask_hparams = self.config_manager.mask_hparams
        
        with gr.TabItem(_("Layer Divider")):
            with gr.Row():
                # Create input components
                inputs = self.ui_components.create_layer_divider_inputs(
                    self.default_mode
                )
                
                with gr.Column(scale=5):
                    img_input = inputs['image_input']
                    img_input_prompter = inputs['image_prompter']
                
                with gr.Column(scale=5):
                    dd_input_modes = inputs['mode_dropdown']
                    dd_models = inputs['model_dropdown']
                    cb_invert_mask = inputs['invert_mask']
                    
                    with gr.Accordion(
                        _("Mask Parameters"),
                        open=False,
                        visible=self.default_mode == AUTOMATIC_MODE
                    ) as acc_mask_hparams:
                        mask_hparams_component = self.ui_components.create_mask_parameters(
                            mask_hparams
                        )
                    
                    cb_multimask_output = inputs['multimask_output']
            
            with gr.Row():
                btn_generate = gr.Button(_("GENERATE PSD"), variant="primary")
            
            # Create output components
            outputs = self.ui_components.create_layer_divider_outputs()
            
            with gr.Row():
                gallery_output = outputs['gallery_output']
                with gr.Column():
                    output_file = outputs['file_output']
                    btn_open_folder = gr.Button(_("📁 Open PSD folder"), scale=1)
            
            # Combine input parameters
            input_params = [
                img_input, img_input_prompter, dd_input_modes,
                dd_models, cb_invert_mask
            ]
            input_params += mask_hparams_component + [cb_multimask_output]
            
            # Wire up event handlers
            btn_generate.click(
                fn=self.sam_inf.divide_layer,
                inputs=input_params,
                outputs=[gallery_output, output_file]
            )
            
            btn_open_folder.click(
                fn=lambda: open_folder(os.path.join(self.args.output_dir, "psd")),
                inputs=None,
                outputs=None
            )
            
            dd_input_modes.change(
                fn=self.event_handlers.on_mode_change,
                inputs=[dd_input_modes],
                outputs=[img_input, img_input_prompter, acc_mask_hparams]
            )
    
    def create_interface(self) -> gr.Blocks:
        """
        Create the complete Gradio interface.
        
        Returns:
            Gradio Blocks demo
        """
        demo = gr.Blocks(theme=self.args.theme, css=CSS)
        
        with demo:
            with self.i18n:
                md_header = gr.Markdown(HEADER, elem_id="md_header")
                md_prompt_guide = gr.Markdown(_("If you don't know how to prompt"))
                
                with gr.Tabs():
                    self.create_video_segmentation_tab()
                    self.create_layer_divider_tab()
        
        return demo
