import numpy

from queue import Queue
from threading import Thread, Condition


class Sampler(object):
    """ Sampler used to play, stop and mix multiple sounds.

        .. warning:: A single sampler instance should be used at a time.

    """

    def __init__(self, sr=22050, backend='sounddevice'):
        """
        :param int sr: samplerate used - all sounds added to the sampler will automatically be resampled if needed (- his can be a CPU consumming task, try to use sound with all identical sampling rate if possible.
        :param str backend: backend used for playing sound. Can be either 'sounddevice' or 'dummy'.

        """
        self.sr = sr
        self.sounds = []

        self.chunks = Queue(1)
        self.chunk_available = Condition()

        if backend == 'dummy':
            from .dummy_stream import DummyStream
            self.BackendStream = DummyStream
        elif backend == 'sounddevice':
            from sounddevice import OutputStream
            self.BackendStream = OutputStream
        else:
            raise ValueError("Backend can either be 'sounddevice' or 'dummy'")

        # TODO: use a process instead?
        self.play_thread = Thread(target=self.run)
        self.play_thread.daemon = True
        self.play_thread.start()

    def play(self, sound):
        """ Adds and plays a new Sound to the Sampler.

            :param sound: sound to play

            .. note:: If the sound is already playing, it will restart from the beginning.

        """
        if self.sr != sound.sr:
            raise ValueError('You can only play sound with a samplerate of {} (here {}). Use the Sound.resample method for instance.', self.sr, sound.sr)

        if sound in self.sounds:
            self.remove(sound)

        with self.chunk_available:
            self.sounds.append(sound)
            sound.playing = True

            self.chunk_available.notify()

    def remove(self, sound):
        """ Remove a currently played sound. """
        with self.chunk_available:
            sound.playing = False
            self.sounds.remove(sound)

    # Play loop

    def next_chunks(self):
        """ Gets a new chunk from all played sound and mix them together. """
        with self.chunk_available:
            while True:
                playing_sounds = [s for s in self.sounds if s.playing]

                chunks = []
                for s in playing_sounds:
                    try:
                        chunks.append(next(s.chunks))
                    except StopIteration:
                        s.playing = False
                        self.sounds.remove(s)

                if chunks:
                    break

                self.chunk_available.wait()

            return numpy.mean(chunks, axis=0)

    def run(self):
        """ Play loop, i.e. send all sound chunk by chunk to the soundcard. """
        self.running = True

        def chunks_producer():
            while self.running:
                self.chunks.put(self.next_chunks())

        t = Thread(target=chunks_producer)
        t.start()

        with self.BackendStream(samplerate=self.sr, channels=1) as stream:
            while self.running:
                stream.write(self.chunks.get())
