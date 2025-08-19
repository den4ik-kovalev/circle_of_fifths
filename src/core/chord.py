from __future__ import annotations
from abc import ABC, abstractmethod

from src.core.tone import Tone


class Chord(ABC):

    def __init__(self, root: Tone):
        self.root = root

    @property
    @abstractmethod
    def sharp_name(self) -> str:
        pass

    @property
    @abstractmethod
    def flat_name(self) -> str:
        pass

    @abstractmethod
    def tones(self) -> list[Tone]:
        pass


class MajorTriad(Chord):

    @property
    def sharp_name(self) -> str:
        return self.root.sharp_name

    @property
    def flat_name(self) -> str:
        return self.root.flat_name

    def tones(self) -> list[Tone]:
        root = self.root
        third = Tone.by_idx(root.idx + 4)
        fifth = Tone.by_idx(root.idx + 7)
        return [root, third, fifth]

    @classmethod
    def circle(cls) -> list[MajorTriad]:
        roots = ["C", "F", "A♯", "D♯", "G♯", "C♯", "F♯", "B", "E", "A", "D", "G"]
        return [cls(Tone.by_name(root)) for root in roots]


class MinorTriad(Chord):

    @property
    def sharp_name(self) -> str:
        return self.root.sharp_name + "m"

    @property
    def flat_name(self) -> str:
        return self.root.flat_name + "m"

    def tones(self) -> list[Tone]:
        root = self.root
        third = Tone.by_idx(root.idx + 3)
        fifth = Tone.by_idx(root.idx + 7)
        return [root, third, fifth]

    @classmethod
    def circle(cls) -> list[MinorTriad]:
        roots = ["A", "D", "G", "C", "F", "A♯", "D♯", "G♯", "C♯", "F♯", "B", "E"]
        return [cls(Tone.by_name(root)) for root in roots]
