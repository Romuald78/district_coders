import sys


from medias.exercises.libDC.genDC import GenDC



class GenExercice(GenDC):

    def __init__(self, argv):
        super().__init__(argv)

    def _generate(self):
        # reinit seed
        self.reinit_seed()
        # get N data
        N = self.randint(5, 10)
        print(N)
        # print N times a value between -500 / +500
        for i in range(N):
            v = self.randint(-500, 500)
            print(v)

        return True

    def _verify(self):
        result = True
        # reinit seed
        self.reinit_seed()
        # get N data
        N  = self.randint(5, 10)
        # get all values from user and compare to expected result
        for i in range(N):
            v = self.randint(-500, 500)
            v = abs(v)
            try:
                u = input()
                try:
                    u = int(u)
                except ValueError:
                    print(f"Impossible to get the user output as an integer (input='{u}')", file=sys.stderr)
                    result = False
                    break
                if u != v:
                    print(f"Expected: '{v}' / Received: '{u}'", file=sys.stderr)
                    result = False
                    break
            except:
                print(f"Impossible to get the user output.\nExpected: '{v}' / Nothing received :(", file=sys.stderr)
                result = False
                break

        return result


if __name__ == '__main__':

    exo = GenExercice(sys.argv)
    exo.run()
