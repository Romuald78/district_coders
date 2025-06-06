import sys

from medias.exercises.libDC.genDC import GenDC


class GenExercice(GenDC):

    def __get_N_values(self):
        return self.randint(10, 20)

    def __get_next_value(self):
        return self.randint(-999, 999)

    def __init__(self, argv):
        super().__init__(argv)

    def _generate(self):
        # reinit seed
        self.reinit_seed()
        # get N data
        N = self.__get_N_values()
        print(N)
        # print N times a value between -999 / +999
        for i in range(N):
            v = self.__get_next_value()
            print(v)

        return True

    def _verify(self):
        result = True
        # reinit seed
        self.reinit_seed()
        # get N data
        N = self.__get_N_values()

        # get all values from user and get mini / maxi
        v = self.__get_next_value()
        mini = v
        maxi = v
        for i in range(N-1):
            v = self.__get_next_value()
            mini = min(mini, v)
            maxi = max(maxi, v)

        result = result and self.read_and_compare_next_int(mini)
        if result:
            result = result and self.read_and_compare_next_int(maxi)

        return result


if __name__ == '__main__':

    exo = GenExercice(sys.argv)
    exo.run()
