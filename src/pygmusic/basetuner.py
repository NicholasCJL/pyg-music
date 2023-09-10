from abc import ABC, abstractmethod
import re
from typing import Dict, List, Tuple


class BaseTuner(ABC):
    chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A',
                       'A#', 'B']
    chromatic_span = [f"{note}{octave}"
                      for note in chromatic_scale
                      for octave in range(9)]

    def __init__(self,
                 reference_note: str,
                 reference_freq: float):
        self.note_to_freq: Dict[str, Tuple[float, float, float]] = {}
        self.ref_note = reference_note
        self.ref_freq = reference_freq

    @abstractmethod
    def build_scales(self):
        pass

    @abstractmethod
    def translate(self, notes: List[str]):
        pass

    def _parse_note(self, note: str) -> float:
        """
        Parses string in note format e.g. A#3 into frequency.
        :param note: String in note format.
        """
        # note exists
        if note in self.note_to_freq:
            return self.note_to_freq[note][1]

        # note does not exist
        # check if is valid format
        if not re.match(r"^[A-G][b#]?[0-8]$", note):
            raise ValueError(f"{note=} is not a valid note format.")

        # it's a differently notated sharp/flat e.g. F# vs Gb
        octave = note[-1]
        root = note[0]
        offset = 2 if note[1] == '#' else 0

        # retrieve root note and return the note offset from it
        base_note = root + octave

        return self.note_to_freq[base_note][offset]
