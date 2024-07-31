# import time
from collections import Counter, deque

import flet as ft
import numpy as np
import pyaudio
import pyperclip

from .constants import *
from .utils import frequency_to_note, get_frequency


class Notes:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.bgcolor = ft.colors.DEEP_PURPLE_800
        self.notes_played = []
        self.max_freq = 0
        # self.current_note_start_time = time.time()

        # shd = ft.ShakeDetector(
        #     minimum_shake_count=2,
        #     shake_slop_time_ms=300,
        #     shake_count_reset_time_ms=1000,
        #     on_shake=lambda _: self.toggle(),
        # )
        # page.overlay.append(shd)

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.last_was_silence = False

        self.history = ft.Column(
            [],
            width=300,
            expand=True,
            tight=True,
            scroll=ft.ScrollMode.HIDDEN,
            auto_scroll=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        container_history = ft.Container(
            self.history,
            width=300,
            height=300,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor=ft.colors.DEEP_PURPLE_900,
        )

        # stacked = ft.Stack(
        #     [
        #         container_history,
        #         ft.Container(
        #             width=300,
        #             height=400,
        #             gradient=ft.LinearGradient(
        #                 colors=[
        #                     ft.colors.DEEP_PURPLE_800,
        #                     ft.colors.with_opacity(0, ft.colors.DEEP_PURPLE_800),
        #                     ft.colors.DEEP_PURPLE_800,
        #                     ft.colors.DEEP_PURPLE_800,
        #                 ],
        #                 begin=ft.alignment.bottom_center,
        #                 end=ft.alignment.top_center,
        #             ),
        #         ),
        #     ],
        # )

        self.note_text = ft.Text(
            "💜",
            size=60,
            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
        )

        self.chart = ft.LineChart(
            data_series=self.create_chart(),
            width=300,
            height=100,
        )

        container_chart = ft.Container(
            self.chart,
            width=300,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor=ft.colors.DEEP_PURPLE_900,
        )

        buttons = ft.Row(
            [
                ft.IconButton(icon=ft.icons.REPLAY, on_click=self.clear_history),
                ft.IconButton(icon=ft.icons.MIC, on_click=self.toggle),
                # ft.IconButton(icon=ft.icons.PLAY_ARROW, on_click=self.play),
                ft.IconButton(icon=ft.icons.COPY, on_click=self.copy),
                # ft.IconButton(icon=ft.icons.SHARE, on_click=self.share),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        container_button = ft.Container(
            buttons,
            width=300,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
            padding=ft.Padding(20, 20, 20, 20),
            bgcolor=ft.colors.DEEP_PURPLE_900,
        )

        page.add(
            ft.Row(
                controls=[
                    ft.Column(
                        [
                            container_history,
                            self.note_text,
                            container_chart,
                            container_button,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback,
        )
        self.stream.start_stream()

        self.note_buffer = deque(maxlen=10)
        self.current_note = ""

    def start(self):
        self.stream.start_stream()
        self.note_text.update()

    def toggle(self, event: ft.ControlEvent):
        if not self.stream.is_stopped():
            event.control.icon = ft.icons.MIC_OFF
            event.control.update()
            self.stop()
        else:
            event.control.icon = ft.icons.MIC
            event.control.update()
            self.start()

    def stop(self):
        self.stream.stop_stream()
        self.note_text.update()

    def share(self, _):
        notes = "\n".join([f"{note}" for note, freq in self.notes_played])
        ...

    def copy(self, _):
        notes = "\n".join([f"{note}" for note, freq in self.notes_played])
        pyperclip.copy(notes)

    def clear_history(self, _):
        self.notes_played = []
        self.max_freq = 0
        self.note_text.value = "💜"
        self.history.controls = []
        self.chart.data_series = self.create_chart()
        self.page.update()

    # audio callback
    def callback(self, in_data, frame_count, time_info, status):
        # self.current_note_start_time = time.time()
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        if np.max(np.abs(audio_data)) < THRESHOLD:
            self.update_note()
            return (in_data, pyaudio.paContinue)

        freq = get_frequency(audio_data)
        note = frequency_to_note(freq)
        self.max_freq = max(self.max_freq, freq)
        self.update_note(note, freq)
        return (in_data, pyaudio.paContinue)

    def update_note(self, new_note="", freq=0):
        self.note_buffer.append(new_note)

        # only update the displayed note if it's consistent for a majority of recent readings
        most_common_note = Counter(self.note_buffer).most_common(1)[0][0]
        if most_common_note != self.current_note:
            self.current_note = most_common_note

            # current_time = time.time()
            # duration = current_time - self.current_note_start_time
            self.notes_played.append(
                (
                    self.current_note,
                    freq,
                )
            )

            if freq and new_note:

                self.note_text.value = f"{self.current_note}"
                self.note_text.update()
                self.chart.data_series = self.create_chart()
                self.chart.update()
                self.history.controls.append(
                    ft.Text(
                        f"{self.current_note}",
                        size=20,
                        style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                    )
                )
                self.history.update()
                self.last_was_silence = False
            else:
                if not self.last_was_silence:
                    self.history.controls.append(ft.Text(size=20))
                    self.history.update()
                    self.last_was_silence = True

    def create_chart(self):
        data_points = []
        cutoff = 20

        for i, (note, note_freq) in enumerate(self.notes_played[-cutoff:]):
            if note_freq:
                data_points.append(
                    ft.LineChartDataPoint(
                        x=i,
                        y=min(note_freq / self.max_freq, 1),
                        tooltip=note,
                        tooltip_align=ft.alignment.bottom_center,
                    )
                )

        chart_data = [
            ft.LineChartData(
                data_points=data_points,
                color=ft.colors.LIGHT_GREEN,
                stroke_width=4,
                curved=True,
                stroke_cap_round=True,
            )
        ]

        return chart_data
