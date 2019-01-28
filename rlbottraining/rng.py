from random import Random

class SeededRandomNumberGenerator(Random):
    def __init__(self, rng: Random):
        super().__init__()
        self.setstate(rng.getstate())

    def n11(self):
        """
        A Shorthand to get a random value between negative 1 and 1.
        """
        return self.uniform(-1, 1)
