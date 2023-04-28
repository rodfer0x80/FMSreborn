from IPython.display import Audio
from pretty_midi import PrettyMIDI

sf2_path = '/usr/share/soundfonts/freepats-general-midi.sf2'  # path to sound font file
midi_file = './results/edm256_1.mid'

music = PrettyMIDI(midi_file=midi_file)
waveform = music.fluidsynth(sf2_path=sf2_path)
Audio(waveform, rate=44100)
