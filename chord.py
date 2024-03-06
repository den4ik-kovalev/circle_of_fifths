from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Chord:
    root: str
    is_major: bool = True

    def __str__(self):
        return self.sharp_name

    @property
    def sharp_name(self) -> str:
        name = {
            "C": "C",
            "C#": "C#", "Db": "C#",
            "D": "D",
            "D#": "D#", "Eb": "D#",
            "E": "E",
            "F": "F",
            "F#": "F#", "Gb": "F#",
            "G": "G",
            "G#": "G#", "Ab": "G#",
            "A": "A",
            "A#": "A#", "Bb": "A#",
            "B": "B"
        }[self.root]
        if not self.is_major:
            name += "m"
        return name

    @property
    def flat_name(self) -> str:
        name = {
            "C": "C",
            "C#": "Db", "Db": "Db",
            "D": "D",
            "D#": "Eb", "Eb": "Eb",
            "E": "E",
            "F": "F",
            "F#": "Gb", "Gb": "Gb",
            "G": "G",
            "G#": "Ab", "Ab": "Ab",
            "A": "A",
            "A#": "Bb", "Bb": "Bb",
            "B": "B"
        }[self.root]
        if not self.is_major:
            name += "m"
        return name

    @classmethod
    def all_triads(cls) -> (list[Chord], list[Chord]):
        return (
            [
                Chord("C"),
                Chord("F"),
                Chord("A#"),
                Chord("D#"),
                Chord("G#"),
                Chord("C#"),
                Chord("F#"),
                Chord("B"),
                Chord("E"),
                Chord("A"),
                Chord("D"),
                Chord("G")
            ],
            [
                Chord("A", False),
                Chord("D", False),
                Chord("G", False),
                Chord("C", False),
                Chord("F", False),
                Chord("A#", False),
                Chord("D#", False),
                Chord("G#", False),
                Chord("C#", False),
                Chord("F#", False),
                Chord("B", False),
                Chord("E", False),
            ],
        )
