import unittest
import random
import numpy
import copy
import time

from aupyom import Sound, Sampler
from aupyom.util import example_audio_file


class TestTimeStretch(unittest.TestCase):
    def setUp(self):
        self.s1 = Sound.from_file(example_audio_file())

        freq, dt, sr = 440.0, 10.0, 22050
        t = numpy.linspace(0, dt, sr * dt)
        self.s2 = Sound(numpy.sin(2 * numpy.pi * freq * t), sr)

        self.sounds = [self.s1, self.s2, copy.deepcopy(self.s1)]

        self.sampler = Sampler(backend='dummy')

    def test_sampling(self):
        for s in self.sounds:
            self.sampler.play(s)
            time.sleep(random.random())
            s.pitch_shift = random.random() * 24 - 12
            time.sleep(random.random())
            s.stretch_factor = random.random() * 5

        while self.sampler.sounds:
            time.sleep(.1)


if __name__ == '__main__':
    unittest.main()
