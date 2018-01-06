import random


def filegrab(file):
    words = [line.rstrip('\n') for line in open(file)]
    return words


def choices(self, population, weights=None, k=1):
        random = self.random
        if cum_weights is None:
            if weights is None:
                _int = int
                total = len(population)
                return [population[_int(random() * total)] for i in range(k)]
            cum_weights = list(_itertools.accumulate(weights))
        elif weights is not None:
            raise TypeError('Cannot specify both weights and cumulative weights')
        if len(cum_weights) != len(population):
            raise ValueError('The number of weights does not match the population')
        bisect = _bisect.bisect
        total = cum_weights[-1]
        return [population[bisect(cum_weights,
                random() * total)] for i in range(k)]
