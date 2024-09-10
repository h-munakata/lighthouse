"""
Copyright $today.year LY Corporation

LY Corporation licenses this file to you under the Apache License,
version 2.0 (the "License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at:

  https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""
import ffmpeg
import math
from typing import Optional, Dict, Union, Tuple

def convert_to_float(
    frac_str: str) -> float:
    try:
        return float(frac_str)
    except ValueError:
        try:
            num, denom = frac_str.split('/')
        except ValueError:
            raise ValueError(f'frac_str should be like fraction form, but frac_str={frac_str}.')
        try:
            leading, num = num.split(' ')
        except ValueError:
            return float(num) / float(denom)
        if float(leading) < 0:
            sign_mult = -1
        else:
            sign_mult = 1
        return float(leading) + sign_mult * (float(num) / float(denom))


class BaseLoader:
    def __init__(
    self,
    framerate: float,
    size: int,
    device: str,
    centercrop: bool = True) -> None:
        self._framerate = framerate
        self._size = size
        self._device = device
        self._centercrop = centercrop
        self._clip_len = int(1 / framerate)

    def _video_info(
        self,
        video_path: str) -> Optional[Dict[str, Union[int, float]]]:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams']
                             if stream['codec_type'] == 'video'), None)
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        fps = math.floor(convert_to_float(video_stream['avg_frame_rate']))
        
        try:
            frames_length = int(video_stream['nb_frames'])
            duration = float(video_stream['duration'])
        
        except Exception:
            return None
        
        info = {
            "duration": duration,
            "frames_length": frames_length,
            "fps": fps,
            "height": height,
            "width": width
        }
        return info

    def _output_dim(
        self,
        h: int,
        w: int) -> Tuple[int, int]:
        if isinstance(self.size, tuple) and len(self.size) == 2:
            return self.size
        elif h >= w:
            return int(h * self.size / w), self.size
        else:
            return self.size, int(w * self.size / h)