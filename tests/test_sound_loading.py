import unittest
import librosa
import random
import numpy

from aupyom import Sampler, Sound
from aupyom.util import example_audio_file


class TestSoundLoading(unittest.TestCase):
    def setUp(self):
        self.sampler = Sampler()
        self.audio_file = example_audio_file()

    def test_load_sound(self):
        s1 = Sound.from_file(self.audio_file)

        y, sr = librosa.load(self.audio_file)
        s2 = Sound(y, sr)

        self.assertTrue(numpy.all(s1.y == s2.y))

        s3 = Sound(numpy.random.rand(random.randint(1, 100000)),
                   random.choice((88200, 44100, 22050, 11025)))

    def play_sound_only_if_correct_sr(self):
        sr = random.choice(88200, 44100, 11025)
        s = Sound.from_file(self.audio_file, sr=sr)

        with self.assertRaises():
            self.sampler.play(s)

if __name__ == '__main__':
    unittest.main()
