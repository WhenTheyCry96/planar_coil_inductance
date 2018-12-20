# -*- coding: utf-8 -*- 
import math


class StraightCoil():
    def __init__(self, w, h, l):
        self.w = w
        self.h = h
        if l > 0:
            self.l = l
        else:
            print("\n\tERROR ERROR ERROR ERROR\n Invalid Straight Coil Length : %f \n\n" %(l))
            raise ValueError
        self.L_self = self.self_inducatnce()
        # print("cond w : %f cond h : %f cond l : %f cond L : %f" %(self.w,self.h,self.l,self.L_self))

    def self_inducatnce(self):
        # self inductance of straight rectangular conductors
        # for thin-high freq.
        # L_self [uH]
        L_self = 0.002*self.l*( math.log(2*self.l/(self.h+self.w)) + 
            0.50049 +(self.h+self.w)/(3*self.l) )
        return L_self 


class Planarcoil():
    def __init__(self):
        self.inductance=0
        # mu unit : [uH / cm]
        self.mu = 4 * math.pi * 1.0e-7 * 1.0e-4
        # number of conductor = how many pieces of straight conductors
        self.num_coil = 0
        self.get_input()
        self.generate_shape()

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
            wire_width = input('\n'+"Input Wire Width [cm]: ")
            if float(wire_width) > 0:
                self.wire_width = float(wire_width)
                break
            else:
                print('\n' + "!!!!Input Error!!!!" + '\n')

        while True:
            outer_d = input('\n'+"Input Outer Length of Coil [cm]: ")
            if float(outer_d) > 0:
                self.outer_d = float(outer_d)
                break
            else:
                print('\n' + "!!!!Input Error!!!!" + '\n')

        while True:
            wire_distance = input('\n'+"Input Wire Distance [cm]: ")
            if float(wire_width) > 0:
                self.wire_distance = float(wire_distance) 
                break
            else:
                print('\n' + "!!!!Input Error!!!!")

        while True:
            height = input('\n'+"Input Height [cm]: ")
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

    def generate_shape(self):
        cond_arr_Xpdir = []
        cond_arr_Xmdir = []
        cond_arr_Ypdir = []
        cond_arr_Ymdir = []
        for n in range(self.turn):
            # Straight Cond I flows in x+ direction
            if n == 0 or n == 1:
                l_xp = self.outer_d - (n+1)*self.wire_width - n*self.wire_distance 
            else:
                l_xp = self.outer_d - (2*n)*self.wire_width - (2*n-1)*self.wire_distance
            cond_temp_xp = StraightCoil(w=self.wire_width, h=self.height ,l=l_xp)
            # Straight Cond I flows in y- direction
            l_ym = self.outer_d - (2*n+1)*self.wire_width - (2*n)*self.wire_distance
            cond_temp_ym = StraightCoil(w=self.wire_width, h=self.height ,l=l_ym)
            # Straight Cond I flows in x- direction
            l_xm = self.outer_d - (2*n+1)*self.wire_width - (2*n)*self.wire_distance
            cond_temp_xm = StraightCoil(w=self.wire_width, h=self.height ,l=l_xm)
            # Straight Cond I flows in y+ direction
            l_yp = self.outer_d - (2*n+2)*self.wire_width - (2*n+1)*self.wire_distance
            cond_temp_yp = StraightCoil(w=self.wire_width, h=self.height ,l=l_yp)
            
            cond_arr_Xpdir.append(cond_temp_xp)
            cond_arr_Xmdir.append(cond_temp_xm)
            cond_arr_Ypdir.append(cond_temp_ym)
            cond_arr_Ymdir.append(cond_temp_yp)

    def mutual_inductance(self, cond1, cond2):
        
        pass 

    def calc_inductance(self):
        print('\n\n' + "="*20)
        print("Inducatnce calculation")
        print("="*20 + '\n\n')


if __name__ == "__main__":
    # Execute only if run as a script
    ex_planar = Planarcoil()
    #cond1 = StraightCoil(1,2,3,4)
    #cond2 = StraightCoil(5,6,7,8)
    #ex_planar.mutual_inductance(cond1, cond2)