# -*- coding: utf-8 -*- 
import math


class StraightCoil():
    def __init__(self, a, b, h, l):
        self.a = a
        self.b = b
        self.h = h
        self.l = l
        self.L_self = 0
    
    def self_inducatnce(self, length):
        # self inductance of straight rectangular conductors
        # for thin-high freq.
        L_self = 0.002*self.l*( math.log(2*self.l/(self.a+self.b)) + 0.25049 +(self.a+self.b)/(3*self.l) )
        return L_self 


class Planarcoil():
    def __init__(self):
        self.inductance=0
        # mu unit : [uH / cm]
        self.mu = 4 * math.pi * 1.0e-7 * 1.0e-4
        # number of conductor = how many pieces of straight conductors
        self.num_coil = 0
        self.get_input()

    def get_input(self):
        print('\n\n' + "="*40)
        print("     Enter parameters of planar coil     ")
        print("           Length unit : [cm]            ")
        print("         Inductance Unit : [uH]          ")
        print("="*40 + '\n\n')

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

        while True:
            relative_mu = input('\n'+"Input relative permeability : ")
            if float(relative_mu) > 0:
                self.mu = self.mu * float(relative_mu)
                break
            else:
                print('\n' + "!!!!Input Error!!!!")

        while True:
            print('\n'+"Choose Your Coil's Shape"+'\n')
            print('\n'+"phase means : angle difference of (I_final - I_init) in xy-plane"+'\n')
            choose = input(" 1] phase : 0* \n 2] phase : 270* \n 3] phase : 180* \n 4] phase : 90* \n ")
            if choose.isnumeric() and int(choose) > 0 and int(choose) < 5:
                self.num_coil = 4*self.turn + ( int(choose)%4 )
                print("\nTotal Straight Conductor Number : %d \n" %(self.num_coil))
                break
            else:
                print('\n' + "!!!!Input Error!!!!")

    def mutual_inductance(self, cond1, cond2):
        pass

    def calc_inductance(self):
        print('\n\n' + "="*20)
        print("Inducatnce calculation")
        print("="*20 + '\n\n')


if __name__ == "__main__":
    # Execute only if run as a script
    ex_planar = Planarcoil()
