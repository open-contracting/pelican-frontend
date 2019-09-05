
import random


class ReservoirSampler:
    def __init__(self, samples_cap):
        if samples_cap < 1:
            raise ValueError("samples_cap must be a positive integer")

        self._samples_cap = samples_cap
        self._samples = []
        self._index = 0

    def process(self, value):
        if self._index < self._samples_cap:
            self._samples.append(value)
        else:
            r = random.randint(0, self._index)
            if r < self._samples_cap:
                self._samples[r] = value

        self._index += 1

    def retrieve_samples(self):
        return self._samples
