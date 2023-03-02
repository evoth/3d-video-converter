# 3D Video Converter

A simple FFMPEG-based script for converting either two separate stereo videos or an existing 3D video into a wide range of 3D video formats.

## Installation

### Install `3d-video-converter`

From PyPI:

```bash
pip install 3d-video-converter
```

Or from the source on GitHub:

```bash
pip install "3d-video-converter @ git+https://github.com/evoth/3d-video-converter"
```

The package will be installed with the module name `video_converter_3d`.

### Install FFmpeg

This package depends on [ffmpeg-python](https://github.com/kkroening/ffmpeg-python), which means that [FFmpeg](https://ffmpeg.org/) must be installed and accessible via the `$PATH` environment variable. Please follow appropriate installation instructions for your platform.

To check if FFmpeg is installed, run the `ffmpeg` command from the terminal. If it is installed correctly, you should see version and build information.

## Usage examples

Convert a full-width parallel view video to full color red/cyan anaglyph:

```python
from video_converter_3d import convert_3d

convert_3d("video_parallel.mp4", "sbsl", "video_anaglyph.mp4", "arcc")
```

Combine two separate stereo videos into a full-width parallel view video, only keeping audio from the left video:

```python
from video_converter_3d import convert_2d_to_3d

convert_2d_to_3d(
    "video_left.mp4",
    "video_right.mp4",
    True,
    False,
    "video_parallel.mp4",
    "sbsl"
)
```
