from random import Random

class SeededRandomNumberGenerator(Random):
    def __init__(self, rng: Random):
        self.setstate(rng.getstate())

    def n11(self):
        """
        A Shorthand to get a random value between negative 1 and 1.
        """
        return self.rng.uniform(-1, 1)

    # TODO: Add some more convenience functions which are RL specific. e.g.
    #  direction
    #  angular velocity
