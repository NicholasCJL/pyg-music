from typing import Dict, Tuple

from pygaudio import PygAudio
import pygaudio.envelopes as env
import pygaudio.waveforms as wave

from basetuner import BaseTuner


class Instrument:
    def __init__(self, tuner: BaseTuner):
        self.tuner = tuner
        self.audio = PygAudio()

    def play_notes(self, notes: Dict[str, Tuple[float, float]]):
        # get timing of last note
        latest_time = 0
        for times in notes.values():
            end_time = times[0] + times[1]
            if end_time > latest_time:
                latest_time = end_time

        # construct time
        self.audio.construct_time(seconds=latest_time)

        for note, times in notes.items():
            freq = self.tuner.translate([note])[0]
            start_offset = self.audio.time_to_offset(times[0])
            stop_offset = self.audio.time_to_offset(sum(times))
            self.audio.create_wave(wave_func=wave.sin,
                                   frequency=freq,
                                   amplitude=1,
                                   vol_func=env.constant_envelope,
                                   start_offset=start_offset,
                                   stop_offset=stop_offset)

        self.audio.play_sound()