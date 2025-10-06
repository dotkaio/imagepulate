this is a Gradio based playground web UI using [facebook/segment-anything-2](https://github.com/facebookresearch/segment-anything-2) models.

## Feature

- Segment video for transparent background or pixelated object

<table>
  <tr>
    <td align="center"><strong>Transparent background</strong></td>
  </tr>
  <tr>
    <td>
      <video controls autoplay loop src="https://github.com/user-attachments/assets/23b7d8b0-8594-4def-b0dc-405bedd53c84" muted="false"></video>
    </td>
  </tr>
    <tr>
    <td align="center"><strong>Pixelate</strong></td>
  </tr>
  <tr>
    <td>
      <video controls autoplay loop src="https://github.com/user-attachments/assets/1749893b-cf90-4407-89d7-9aaf13234dcc" muted="false"></video>
    </td>
  </tr>
</table>

- Segment image to divide objects into layers and save them as PSD files.

See [PROMPT_GUIDE.md](https://github.com/dotkaio/imagepulate/blob/master/docs/PROMPT_GUIDE.md) to see how to prompt the segmentation parts of the image.

# Installation and Running

### Prerequisites

To run this Web UI, you need these prerequisites. If you don't have them, please install them in the following links :

- `git` : https://git-scm.com/downloads
- `python=>3.10` : https://www.python.org/downloads/
- `FFmpeg` : https://ffmpeg.org/download.html

After installing FFmpeg, **make sure to add the `FFmpeg/bin` folder to your system PATH!** <br>
And for CUDA, if you're not using an Nvidia GPU and CUDA 12.4, edit the [requirements.txt](https://github.com/dotkaio/imagepulate/blob/master/requirements.txt) to match your environment.

### Option 1 : Running with Shell / Batch Scripts

There's a set of shell / batch scripts for installation and running.

1. Download [`sam2-playground-portable.zip`](https://github.com/dotkaio/imagepulate/releases/tag/v1.0.0) with the file corresponding to your OS and extract its contents.
2. Run `install.bat` or `install.sh` to install dependencies. (It will create a `venv` directory and install dependencies there.)
3. Start WebUI with `start-webui.bat` or `start-webui.sh` (It will run `python app.py` after activating the `venv`)
4. To update, run `update.bat` or `update.sh` (It will run `git pull origin master`)

### Option 2: Docker

1. Clone the repository

```
git clone https://github.com/dotkaio/imagepulate.git
```

3. Build the image ( Image is about ~6 GB )

```
docker compose build
```

3. Run the container

```
docker compose up
```

4. Connect to `localhost:7860` with your browser.

If needed, update [`docker-compose.yaml`](https://github.com/dotkaio/imagepulate/blob/master/docker-compose.yaml) to match your environments.

### Option 3: Manual Setup

1. Clone the repository

```
git clone https://github.com/dotkaio/imagepulate.git
```

2. Create and activate a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements-macos.txt  # For macOS
# or
pip install -r requirements.txt        # For Windows/Linux with CUDA

```

4. Run the application

```bash
python app.py
```

5. Open your browser and go to `http://localhost:7860`

## Refactoring Progress

This project is undergoing a structured refactoring process to improve code quality, maintainability, and performance. Below is a summary of the completed steps and the next steps in the refactoring journey.
