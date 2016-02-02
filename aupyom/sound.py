import numpy
import librosa


class Sound(object):
    """ Sound object which can be read chunk by chunk. """

    def __init__(self, y, sr, chunk_size=1024):
        """
        :param array y: numpy array representing the audio data
        :param int sr: samplerate
        :param int chunk_size: size of each chunk (default 1024)

        """
        self.y, self.sr = y.astype(dtype='float32'), sr
        self.chunk_size = chunk_size


    def resample(self, target_sr):
        """ Returns a new sound with a samplerate of target_sr. """
        y_hat = librosa.core.resample(self.y, self.sr, target_sr)
        return Sound(y_hat, sr)

    # IO methods

    def as_ipywidget(self):
        """ Provides an IPywidgets player that can be used in a notebook. """
        from IPython.display import Audio

        return Audio(data=self.y, rate=self.sr)

    @classmethod
    def from_file(cls, filename, sr=22050):
        """ Loads an audiofile, uses sr=22050 by default. """
        y, sr = librosa.load(filename, sr=sr)
        return cls(y, sr)

    # Chunk iterator

    @property
    def playing(self):
        """ Whether the sound is currently played. """
        return self._playing

    @playing.setter
    def playing(self, value):
        if value and hasattr(self, '_it'):
            del self._it

        self._playing = value

    @property
    def chunks(self):
        """ Returns a chunk iterator over the sound. """
        if not hasattr(self, '_it'):
            class ChunkIterator(object):
                def __init__(iter):
                    iter.i = 0

                def next(iter):
                    chunk = self._next_chunk(iter.i)

                    if len(chunk) != self.chunk_size:
                        raise StopIteration

                    iter.i += self.chunk_size
                    return chunk

            self._it = ChunkIterator()

        return self._it

    def _next_chunk(self, i):
        return self.y[i: i + self.chunk_size]
