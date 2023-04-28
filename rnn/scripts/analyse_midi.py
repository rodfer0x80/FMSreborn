#!/usr/bin/env python3

import sys

import pretty_midi
import numpy as np
# For plotting
import mir_eval.display
import librosa.display
import matplotlib.pyplot as plt

def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
        # Use librosa's specshow function for displaying the piano roll
        librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                                 hop_length=1, sr=fs, x_axis='time', y_axis='cqt_note',
                                 fmin=pretty_midi.note_number_to_hz(start_pitch))


def main():
    # We'll load in the example.mid file distributed with pretty_midi
    pm = pretty_midi.PrettyMIDI('example.mid')
    
    #plt.figure(figsize=(12, 4))
    #plot_piano_roll(pm, 24, 84)
    plt.figure(figsize=(1, 100))
    plot_piano_roll(pm, 0, 1000)

    # Let's look at what's in this MIDI file
    print('There are {} time signature changes'.format(len(pm.time_signature_changes)))
    print('There are {} instruments'.format(len(pm.instruments)))
    print('Instrument 3 has {} notes'.format(len(pm.instruments[0].notes)))
    #print('Instrument 4 has {} pitch bends'.format(len(pm.instruments[4].pitch_bends)))
    #print('Instrument 5 has {} control changes'.format(len(pm.instruments[5].control_changes)))
   
    times, tempo_changes = pm.get_tempo_changes()
    plt.plot(times, tempo_changes, '.')
    plt.xlabel('Time')
    plt.ylabel('Tempo');

    # Get and downbeat times
    beats = pm.get_beats()
    downbeats = pm.get_downbeats()
    # Plot piano roll
    plt.figure(figsize=(12, 4))
    plot_piano_roll(pm, 24, 84)
    ymin, ymax = plt.ylim()
    # Plot beats as grey lines, downbeats as white lines
    mir_eval.display.events(beats, base=ymin, height=ymax, color='#AAAAAA')
    mir_eval.display.events(downbeats, base=ymin, height=ymax, color='#FFFFFF', lw=2)
    # Only display 20 seconds for clarity
    plt.xlim(25, 45);
    
    return 0


if __name__ == '__main__':
    sys.exit(main())


# https://notebook.community/craffel/pretty-midi/Tutorial
