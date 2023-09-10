from typing import List
from basetuner import BaseTuner


class EqualTemperamentTuner(BaseTuner):
    def __init__(self,
                 reference_note: str,
                 reference_freq: float):
        super().__init__()
        self.ref_note = reference_note
        self.ref_freq = reference_freq

    def build_scales(self):
        step = 2 ** (1/12)

        # get position of the reference note
        index = self.chromatic_span.index(self.ref_note)

        # build down
        for i, note in enumerate(self.chromatic_span[index::-1]):
            self.note_to_freq[note] = (self.ref_freq * step ** (-i-1),
                                       self.ref_freq * step ** (-i),
                                       self.ref_freq * step ** (-i+1))

        # build up (shift index to account for 0-indexing)
        for i, note in enumerate(self.chromatic_span[index+1:]):
            self.note_to_freq[note] = (self.ref_freq * step ** i,
                                       self.ref_freq * step ** (i+1),
                                       self.ref_freq * step ** (i+2))

    def translate(self, notes: List[str]):
        return [self._parse_note(note) for note in notes]
