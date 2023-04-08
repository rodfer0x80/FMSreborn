#!/usr/bin/env python3


import os
import sys
import pickle

import numpy
from music21 import converter, instrument, note, chord, stream

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint


DATA = "./data"
WEIGHTS = "./weights"
NOTES = "./data/notes"
MIDI = "./data/midi"
if "data" not in os.listdir("."):
    os.mkdir(DATA)
if "midi" not in os.listdir(DATA):
    print("No midi files found to train")
    exit(1)
if "weights" not in os.listdir("."):
    os.mkdir(WEIGHTS)


def train_network():
    """ This function calls all other functions and trains the LSTM"""
    
    notes = get_notes()
    
    # get amount of pitch names
    n_vocab = len(set(notes))

    network_input, network_output = prepare_sequences(notes, n_vocab)

    model = create_network(network_input, n_vocab)

    train(model, network_input, network_output)


def get_notes():
    """ Extracts all notes and chords from midi files in the ./midi_songs 
    directory and creates a file with all notes in string format"""
    notes = []

    for file in os.listdir(MIDI):
        midi = converter.parse(f"{MIDI}/{file}")
        print("Parsing %s" % f"{MIDI}/{file}")
        notes_to_parse = None

        try:
            s2 = instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except:
            notes_to_parse = midi.flat.notes
        
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
        
        with open(NOTES, 'wb') as filepath:
            pickle.dump(notes, filepath)

    return notes

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences which are the inputs for the LSTM """
    
    # sequence length should be changed after experimenting with different numbers and music genres
    sequence_length = 30

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

    # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))

    # normalize input
    network_input = network_input / float(n_vocab)
    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)



def create_network(network_input, n_vocab):
    """ Creates the structure of the neural network """
    # TODO: convert to pytorch
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        return_sequences=True
    ))
    model.add(Dropout(0.3))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(512))
    model.add(Dense(256))
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model


def train(model, network_input, network_output):
    """ train the neural network """
    
    filepath = WEIGHTS+"/weights-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    # experiment with different epoch sizes and batch sizes
    model.fit(network_input, network_output, epochs=3, batch_size=64, callbacks=callbacks_list)


if __name__ == '__main__':
    train_network()
    sys.exit(0)
