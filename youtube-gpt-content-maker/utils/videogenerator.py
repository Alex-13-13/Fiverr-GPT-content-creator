import os
import random
from typing import Tuple

import moviepy.editor as me
from moviepy.video.compositing.concatenate import concatenate_videoclips

class VideoGenerator:

    def __init__(
        self,
        video_folder: str = 'video',
        music_folder: str = 'music',
        duration: int = 20,
        size: Tuple[int, int] = (1080, 1920),
        channel_name: str = 'Motivation55'

    ) -> None:
        self.video_folder = video_folder
        self.music_folder = music_folder
        self.video_list = os.listdir(video_folder)
        self.music_list = os.listdir(music_folder)
        self.duration = duration
        self.size = size
        self.channel_name = channel_name

    def _pick_random_file(self, file_list: list[str]) -> str:
        return random.choice(file_list)

    def make_audio(self) -> me.AudioFileClip:
        music_file = f"./{self.music_folder}/{self._pick_random_file(self.music_list)}"
        return me.AudioFileClip(music_file).set_duration(self.duration)

    def make_video(self) -> me.VideoFileClip:
        video_file = f"./{self.video_folder}/{self._pick_random_file(self.video_list)}"
        return me.VideoFileClip(video_file).loop(duration= self.duration)


    def content(self, text: list, durationperpart:list) -> list:
        ### Text should spread over the video, not all text in ones. With duration each text clip of 5 sec for example
        textos=[]
        i=0
        for texto in text:
            if (texto!=' ' or texto!=''):
                textos.append(me.TextClip(
                texto,
                font='Amiri-Bold',
                fontsize=100,
                color='white',
                method='caption',
                size=(self.size[0]*0.8, None),
                stroke_color='black',
                stroke_width=4
                ).set_duration(durationperpart[i]).set_position("center"))
                i=i+1
        return textos

    def footer(self) -> me.TextClip:
        return me.TextClip(
            f'@{self.channel_name}',
            font='Helvetica-Bold',
            fontsize=60,
            color='white',
            method='label',
            stroke_color='black',
            stroke_width=2
        ).set_duration(self.duration).set_position(("center", self.size[1]*0.8))

    def _make_main_clip(self, text: list, durationperpart: list) -> me.CompositeVideoClip:
        video = self.make_video()
        # Overlay the music on the video
        video = video.set_audio(self.make_audio())
        # Resize
        video = video.resize(self.size)
        # Create a composition
        text_concat = concatenate_videoclips(self.content(text,durationperpart)).set_position("center")
        final = [video, text_concat, self.footer()]
        # Composing
        return me.CompositeVideoClip(final).set_duration(self.duration)

    def generate_video(self, text: list, durationperpart: list) -> me.CompositeVideoClip:
        return self._make_main_clip(text,durationperpart)
        # finalclip.write_videofile(f"1.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac") # NOQA
