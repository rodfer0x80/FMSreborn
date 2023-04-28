import os
import pretty_midi
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


def extract_notes(midi_file):
    """Extract notes and timing information from a MIDI file."""
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    notes = []
    for instrument in midi_data.instruments:
        for note in instrument.notes:
            notes.append((note.start, note.end, note.pitch))
    return notes


def quantize_notes(notes, time_step=0.1):
    """Quantize the timing information of notes into a fixed grid."""
    max_time = max([note[1] for note in notes])
    quantized_time = np.arange(0, max_time, time_step)
    piano_roll = np.zeros((128, len(quantized_time)))
    for note in notes:
        start, end, pitch = note
        start_index = int(start / time_step)
        end_index = int(end / time_step)
        piano_roll[pitch, start_index:end_index] = 1
    return piano_roll


def preprocess_midi_files(midi_folder):
    """Preprocess MIDI files in a folder for use with a transformer model."""
    midi_files = os.listdir(midi_folder)
    notes_list = []
    for midi_file in midi_files:
        if midi_file.endswith('.mid'):
            notes = extract_notes(os.path.join(midi_folder, midi_file))
            notes_list.append(notes)
    # Quantize notes into a fixed grid
    quantized_notes = [quantize_notes(notes) for notes in notes_list]
    # Standardize the data using z-score normalization
    scaler = StandardScaler()
    scaler.fit(np.concatenate(quantized_notes, axis=1).T)
    standardized_notes = [scaler.transform(
        notes.T).T for notes in quantized_notes]
    # Split the data into training and validation sets
    train_data, valid_data = train_test_split(
        standardized_notes, test_size=0.2, random_state=42)
    return train_data, valid_data, scaler
