from __future__ import division

import time


class DummyStream(object):
    """ A dummy stream used in case where PortAudio can not be instanciated. """

    def __init__(self, samplerate, **kwargs):
        self.sr = samplerate

    def __enter__(self):
        return self

    def write(self, chunk):
        time.sleep(len(chunk) / self.sr)

    def __exit__(self, type, value, traceback):
        pass
