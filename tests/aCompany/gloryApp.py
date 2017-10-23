
from gloryLib.omgThreading.wtfCrashing import thisSucks
from gloryLib.smartCode.notSoSmart import patchMe
from gloryLib.winningApi.noFreedom import suicideCore


def run():

    def inline(*args, **kwargs):
        result = list()
        for i in xrange(20, 21):
            si = patchMe.SmartInt(i)
            si += suicideCore.convert_anything_to_float(si)
            first = suicideCore.take_whatever_comes_first(si)
            suicideCore.this_is_critical(first)
            result.append(si + first)
        return result

    return thisSucks.do_this(inline)


def main():

    start_ = 40
    end_ = 50

    def inline(*args, **kwargs):
        result = list()
        for i in xrange(start_, end_):
            si = patchMe.SmartInt(i)
            si += suicideCore.convert_anything_to_float(si)
            first = suicideCore.take_whatever_comes_first(si)
            suicideCore.this_is_critical(first)
            result.append(si + first)
        return result

    assert thisSucks.do_this(inline)

    start_ = 1
    end_ = 5

    thisSucks.do_this(inline)


# uncomment these lines and see the fun first...... you HAVE TO do this
# if __name__ == '__main__':
#     main()
