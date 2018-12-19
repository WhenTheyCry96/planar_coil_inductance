# -*- coding: utf-8 -*- 

class Planarcoil():
    def __init__(self):
        self.inductance=0
        self.get_input()


    def get_input(self):
        print('\n\n' + "="*20)
        print("     Enter parameters of planar coil     ")
        print("                unit : [mm]              ")

        print("="*20 + '\n\n')
        while True:
            turn = input('\n'+"Input Coil Turns : ")
            if turn.isnumeric() and int(turn) > 0:
                self.turn = int(turn)
                break
            else:
                print('\n' + "!!!!Input Error!!!!" + '\n')
        while True:
            wire_width = input('\n'+"Input Wire Width : ")
            if float(wire_width) > 0:
                self.wire_width = float(wire_width)
                break
            else:
                print('\n' + "!!!!Input Error!!!!" + '\n')
        while True:
            wire_distance = input('\n'+"Input Wire Distance : ")
            if float(wire_width) > 0:
                self.wire_distance = float(wire_distance) 
                break
            else:
                print('\n' + "!!!!Input Error!!!!")
        while True:
            height = input('\n'+"Input Height : ")
            if float(height) > 0:
                self.height = float(height)
                break
            else:
                print('\n' + "!!!!Input Error!!!!")
        self.height = height


    def calc_inductance(self):
        print('\n\n' + "="*20)
        print("Inducatnce calculation")
        print("="*20 + '\n\n')


if __name__ == "__main__":
    # Execute only if run as a script
    ex_planar = Planarcoil()
