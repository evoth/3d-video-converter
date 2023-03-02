from typing import Any, Dict

import ffmpeg
from cv2 import CAP_PROP_FPS, VideoCapture


def convert_3d(
    in_video: str,
    in_type: str,
    out_video: str,
    out_type: str,
    out_ffmpeg_options: Dict[str, Any] = {"c:v": "libx264", "crf": 18},
) -> None:
    """
    Given a 3D video and its type of 3D, converts to a 3D video of a different
    type (see https://ffmpeg.org/ffmpeg-filters.html#stereo3d for available
    input and output type strings). For example, to convert a full-width
    parallel view video to full color red/cyan anaglyph, the `in_type` would be
    `"sbsl"` and the `out_type` would be `"arcc"`.

    Optionally, export settings can be adjusted
    via `out_ffmpeg_options`, which are passed to the ffmpeg-python output
    function.
    """

    stream = ffmpeg.input(in_video)
    audio = stream.audio
    if in_type != out_type:
        filter_options = {"in": in_type, "out": out_type}
        stream = ffmpeg.filter(stream, "stereo3d", **filter_options)
    stream = ffmpeg.output(stream, audio, out_video, **out_ffmpeg_options)
    ffmpeg.run(stream)


def convert_2d_to_3d(
    in_video_left: str,
    in_video_right: str,
    use_audio_left: bool,
    use_audio_right: bool,
    out_video: str,
    out_type: str,
    out_ffmpeg_options: Dict[str, Any] = {"c:v": "libx264", "crf": 18},
    offset: float = 0,
    overwrite: bool = False,
) -> None:
    """
    Given two separate stereo videos of identical dimensions and constant
    framerates, combines into a 3D video of the specified type (see
    https://ffmpeg.org/ffmpeg-filters.html#stereo3d for available output type
    strings). For example, to combine the videos into a full-width parallel view
    video, the `out_type` would be `"sbsl"`.

    The audio from either or both videos may be used, depending on the value of
    `use_audio_left` and `use_audio_right`. If both are `True`, mixes audio down
    into mono or stereo, depending on the input files. However, if using audio
    from both videos, there may be slight echoing artifacts.

    Additionally, the offset between `in_video_left` and `in_video_right` can be
    specified by setting `offset` to the number of seconds `in_video_right` is
    delayed from `in_video_left` (or vice versa for a negative value).

    Optionally, export settings can be adjusted
    via `out_ffmpeg_options`, which are passed to the ffmpeg-python output
    function. Set `overwrite` to `True` to automatically overwrite files.
    """

    # Apply offset by trimming beginning of video that starts earlier
    in_options_left = {}
    if offset > 0:
        in_options_left["ss"] = offset
    stream_left = ffmpeg.input(in_video_left, **in_options_left)
    in_options_right = {}
    if offset < 0:
        in_options_right["ss"] = offset
    stream_right = ffmpeg.input(in_video_right, **in_options_right)

    # Create parallel view video which can be converted to another type
    stream = ffmpeg.filter(
        [stream_left.video, stream_right.video], "hstack", inputs=2, shortest=1
    )

    # Convert parallel view to another type
    in_type = "sbsl"
    if in_type != out_type:
        filter_options = {"in": in_type, "out": out_type}
        stream = ffmpeg.filter(stream, "stereo3d", **filter_options)

    # Process audio
    if use_audio_left and use_audio_right:
        audio = ffmpeg.filter(
            [stream_left.audio, stream_right.audio], "amerge", inputs=2
        )
        out_ffmpeg_options["ac"] = 2
    elif use_audio_left:
        audio = stream_left.audio
    elif use_audio_right:
        audio = stream_right.audio

    # Get framerate
    cap = VideoCapture(in_video_left)
    fps = cap.get(CAP_PROP_FPS)

    # Configure output
    out_ffmpeg_options["fps_mode"] = "cfr"
    out_ffmpeg_options["r"] = fps
    if use_audio_left or use_audio_right:
        stream = ffmpeg.output(stream, audio, out_video, **out_ffmpeg_options)
    else:
        stream = ffmpeg.output(stream, out_video, **out_ffmpeg_options)

    ffmpeg.run(stream, overwrite_output=overwrite)
