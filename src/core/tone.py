from __future__ import annotations


# twelve tone row
TTR_SHARP = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
TTR_FLAT = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]


class Tone:

    def __init__(self, idx: int):
        self._idx = idx % 12

    def __eq__(self, other):
        return self._idx == other.idx

    @classmethod
    def by_idx(cls, idx: int) -> Tone:
        return cls(idx)

    @classmethod
    def by_name(cls, name: str) -> Tone:
        if name in TTR_SHARP:
            return cls(TTR_SHARP.index(name))
        if name in TTR_FLAT:
            return cls(TTR_SHARP.index(name))
        raise ValueError

    @classmethod
    def twelve_tone_row(cls) -> list[Tone]:
        return [cls.by_idx(i) for i in range(12)]

    @property
    def idx(self) -> int:
        return self._idx

    @property
    def sharp_name(self) -> str:
        return TTR_SHARP[self._idx]

    @property
    def flat_name(self) -> str:
        return TTR_FLAT[self._idx]
