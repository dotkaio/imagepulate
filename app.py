"""Main application entry point for Imagepulate."""

import argparse

from modules.logger_util import get_logger
from modules.html_constants import DEFAULT_THEME
from modules.sam_inference import SamInference
from modules.paths import OUTPUT_DIR, MODELS_DIR
from modules.ui.app_ui import AppUI

logger = get_logger()


class App:
    """Main application class - simplified orchestrator."""
    
    def __init__(self, args: argparse.Namespace):
        """
        Initialize the application.
        
        Args:
            args: Command line arguments
        """
        self.args = args
        
        # Initialize SAM inference engine
        self.sam_inf = SamInference(
            model_dir=self.args.model_dir,
            output_dir=self.args.output_dir
        )
        logger.info(f'Device "{self.sam_inf.device}" detected')
        
        # Create UI
        self.ui = AppUI(args, self.sam_inf)
        self.demo = self.ui.create_interface()
    
    def launch(self):
        """Launch the Gradio application."""
        auth = (self.args.username, self.args.password) if self.args.username and self.args.password else None
        
        self.demo.queue().launch(
            inbrowser=self.args.inbrowser,
            share=self.args.share,
            server_name=self.args.server_name,
            server_port=self.args.server_port,
            root_path=self.args.root_path,
            auth=auth
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', type=str, default=MODELS_DIR,
                        help='Model directory for segment-anything-2')
    parser.add_argument('--output_dir', type=str, default=OUTPUT_DIR,
                        help='Output directory for the results')
    parser.add_argument('--inbrowser', type=bool, default=True, nargs='?', const=True,
                        help='Whether to automatically start Gradio app or not')
    parser.add_argument('--share', type=bool, default=False, nargs='?', const=True,
                        help='Whether to create a public link for the app or not')
    parser.add_argument('--theme', type=str, default=None,
                        help='Gradio Blocks theme')
    parser.add_argument('--server_name', type=str,
                        default=None, help='Gradio server host')
    parser.add_argument('--server_port', type=int,
                        default=None, help='Gradio server port')
    parser.add_argument('--root_path', type=str,
                        default=None, help='Gradio root path')
    parser.add_argument('--username', type=str, default=None,
                        help='Gradio authentication username')
    parser.add_argument('--password', type=str, default=None,
                        help='Gradio authentication password')
    args = parser.parse_args()

    demo = App(args=args)
    demo.launch()
