import unittest
import random
import numpy
import copy

from aupyom import Sound
from aupyom.util import example_audio_file


class TestTimeStretch(unittest.TestCase):
    def setUp(self):
        self.s1 = Sound.from_file(example_audio_file())

        freq, dt, sr = 440.0, 10.0, 22050
        t = numpy.linspace(0, dt, sr * dt)
        self.s2 = Sound(numpy.sin(2 * numpy.pi * freq * t), sr)

        self.sounds = [self.s1, self.s2]

    def test_chunk_size_checking(self):
        for sf in self.speeds():
            s = copy.deepcopy(random.choice(self.sounds))
            s.stretch_factor = sf

            for c in s.chunks:
                self.assertTrue(len(c) == s.chunk_size)

    def test_number_of_chunks(self):
        for sf in self.speeds():
            s1 = copy.deepcopy(random.choice(self.sounds))

            s2 = copy.deepcopy(s1)
            s2.stretch_factor = sf

            c1 = len(list(s1.chunks))
            c2 = len(list(s2.chunks))

            error = abs((c1 - c2 * sf) / c1)
            self.assertTrue(error < 0.05, error)

    def speeds(self):
        speedup = 1 + 10 * random.random()
        slowdown = random.random()

        return speedup, slowdown

if __name__ == '__main__':
    unittest.main()
