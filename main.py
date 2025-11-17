import time

import supriya
from supriya import Envelope, synthdef
from supriya.ugens import EnvGen, Out, SinOsc, LFTri


NOTES = [ 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#' ]

BACH = ('q F2 A3 F2 C3 F2 ' +
        'F3 qq E3 D3 C3 D3 C3 A#3 A3 A#3 A3 G2 ' +
        'q F2 A3 C3 A3 F3 C3'
        )


def note_to_freq(note):
    octave = int(note[-1:])
    degree = NOTES.index(note[:-1])
    expt = octave + degree / 12
    return 55.0 * 2 ** expt


def parse_notes(score):
    out = []
    dur = 0.25
    for token in score.split():
        if token == 'q':
            dur = 0.25
        elif token == 'qq':
            dur = 0.125
        else:
            out += [(note_to_freq(token), dur)]
    return out


@synthdef()
def simple_sine(frequency=440, amplitude=0.1, gate=1):
    sine = SinOsc.ar(frequency=frequency) * amplitude
    tri = LFTri.ar(frequency=frequency/2, initial_phase=0.15)
    envelope = EnvGen.kr(envelope=Envelope.adsr(), gate=gate, done_action=2)
    Out.ar(bus=0, source=[sine * tri * envelope] * 2)


def play(server, note):
    (freq, dur) = note
    synth = server.add_synth(
        add_action=supriya.AddAction.ADD_TO_HEAD,
        amplitude=0.1,
        frequency=freq,
        synthdef=simple_sine,
        target_node=None)
    time.sleep(dur)
    synth.free()


def main():
    server = supriya.Server()
    server.boot()
    server.add_synthdefs(simple_sine)
    server.sync()
    for note in parse_notes(BACH):
        play(server, note)


if __name__ == "__main__":
    main()
