import random
import sys
import time


class GenDC:

    def _generate(self):
        raise NotImplementedError('generate Method has not been implemented yet !')

    def _verify(self):
        raise NotImplementedError('generate Method has not been implemented yet !')

    def __init__(self, argv):
        # declaration
        self.__seed = None
        self.__cb   = None
        # get params
        for arg in argv:
            if arg.startswith('-s'):
                seed = arg.replace('-s', '')
                self.__seed = int(seed)
            elif arg == '-g':
                self.__cb = self._generate
            elif arg == '-v':
                self.__cb = self._verify

        if self.__cb is None:
            raise ValueError('Bad mode !')

        # set random seed using current time if no seed given
        if self.__seed is None:
            self.__seed = int(time.time() * 1000000)

    def reinit_seed(self):
        random.seed(self.__seed)

    def random(self):
        return random.random()

    def randint(self, mini, maxi):
        if mini > maxi:
            raise ValueError('GenDC::get_nb_data() -> mini value cannot be greater than maxi value')
        return random.randint(mini, maxi)

    def run(self):
        result = self.__cb()
        if not result:
            print('[ERROR]')
            sys.exit(1)
        print('[OK]')
        sys.exit(0)




