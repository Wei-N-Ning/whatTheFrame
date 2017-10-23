

class SmartInt(int):

    _cache = dict()

    def __str__(self):
        return 'SmartInt<{}>'.format(int(self))

    def __add__(self, other):
        cache_key = (str(self), str(other))
        if cache_key in self._cache:
            return self._cache[cache_key]
        result = SmartInt(int(self) + int(other))
        self._cache[cache_key] = result
        return result

    def optimized_mult(self, other):
        if other == 2:
            return SmartInt(self << 1)
        if other == 4:
            return SmartInt(self << 2)
        if other == 8:
            return SmartInt(self << 3)
        return SmartInt(self * other)



