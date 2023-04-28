#!/usr/bin/env python3

import sys

from visual_midi import Plotter
from visual_midi import Preset
from pretty_midi import PrettyMIDI

# Loading a file on disk using PrettyMidi, and show
pm = PrettyMIDI("./example.mid")
plotter = Plotter()
plotter.show(pm, "./example-01.html")

# Converting to PrettyMidi from another library, like Magenta note-seq
import magenta.music as mm
pm = mm.midi_io.note_sequence_to_pretty_midi(sequence)
plotter = Plotter()
plotter.show(pm, "/tmp/example-02.html")
