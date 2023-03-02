from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="3d-video-converter",
    packages=["video_converter_3d"],
    version="0.0.2",
    author="Ethan Voth",
    author_email="ethanvoth7@gmail.com",
    url="https://github.com/evoth/3d-video-converter",
    description="FFMPEG-based tool for converting either two separate stereo videos or an existing 3D video into a wide range of 3D video formats.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "ffmpeg-python",
        "opencv-python",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
