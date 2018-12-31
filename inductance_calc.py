# -*- coding: utf-8 -*- 
import math

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

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
        self.cond_arr_XPdir = []
        self.cond_arr_XMdir = []
        self.cond_arr_YMdir = []
        self.cond_arr_YPdir = []
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
            if isNumber(turn) and int(turn) > 0:
                self.turn = int(turn)
                break
            else:
                print('\n' + "!!!!Input Error!!!!" + '\n')

        while True:
            wire_width = input('\n'+"Input Wire Width [cm]: ")
            if isNumber(wire_width) is True:
                if float(wire_width) > 0:
                    self.wire_width = float(wire_width)
                    break
                else:
                    print('\n' + "!!!!Input Error!!!! - MINUS VALUE" + '\n')
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
        for n in range(self.turn+1):
            if n != self.turn:
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
                
                self.cond_arr_XPdir.append(cond_temp_xp)
                self.cond_arr_XMdir.append(cond_temp_xm)
                self.cond_arr_YMdir.append(cond_temp_ym)
                self.cond_arr_YPdir.append(cond_temp_yp)
            else:
                #Add the last turn of the rest conductor
                if self.num_coil % 4 == 1:
                    # phase 0
                    self.cond_arr_XPdir.append(cond_temp_xp)
                elif self.num_coil % 4 == 2:
                    # phase 270
                    self.cond_arr_XPdir.append(cond_temp_xp)
                    self.cond_arr_YMdir.append(cond_temp_ym)
                elif self.num_coil % 4 == 3:
                    # phase 180
                    self.cond_arr_XPdir.append(cond_temp_xp)
                    self.cond_arr_XMdir.append(cond_temp_xm)
                    self.cond_arr_YMdir.append(cond_temp_ym)

    def mutual_L(self, l_wire, d):
        # l_wire for length and d for distance btw the track centers
        # GMD for Geometric Mean Distance
        GMD = d #/(math.exp(1/12*math.pow(d/self.wire_width,2)))
        Q = math.log((l_wire/GMD) + math.pow((1+(math.pow(l_wire/GMD,2))),0.5)) - \
            math.pow((1+(math.pow(GMD/l_wire,2))),0.5) + GMD/l_wire
        result = 2*l_wire*Q
        return result

    def self_inductance_total(self):
        result = 0
        for i in self.cond_arr_XPdir:
            result = result + i.L_self
        for i in self.cond_arr_XMdir:
            result = result + i.L_self
        for i in self.cond_arr_YPdir:
            result = result + i.L_self
        for i in self.cond_arr_YMdir:
            result = result + i.L_self
        print("\n"+"="*40)
        print("Total Self Inductance : %f" %(result))
        print("="*40 +"\n")
        return result

    def mutual_inductance_totalP(self, arr_cond):
        mutual_totL = 0
        for i in range(len(arr_cond) - 1):
            for j in range(i+1, len(arr_cond)):
                # mutual inductance between conductors
                len_p = arr_cond[j].l + 2*(self.wire_width+self.wire_distance)
                len_m = 2*(j-i)*(self.wire_width+self.wire_distance)
                dist_btw = self.wire_width + (j-i)*self.wire_distance
                mutual_temp = (self.mutual_L(l_wire=len_p,d=dist_btw)-self.mutual_L(l_wire=len_m,d=dist_btw))
                # Unit Fix nH to uH
                mutual_totL = mutual_totL + 0.001*mutual_temp
                #print("Mutual Temp[%d, %d] : %f" %(i,j, mutual_temp))
        mutual_totL = 2 * mutual_totL 
        print("\n"+"="*40)
        print("Total Plus Mutual Inductance : %f" %(mutual_totL))
        print("="*40 +"\n")
        return mutual_totL

    def mutual_inductance_totalM(self, arr_cond1, arr_cond2):
        mutual_totL = 0
        for i in range(len(arr_cond1)):
            for j in range(len(arr_cond2)):
                # mutual inductance between opposite I dir. conductors
                short_l = arr_cond2[j].l
                if arr_cond1[i].l < arr_cond2[j].l:
                    short_l = arr_cond1[i].l 
                len_l = abs(i-j)*(self.wire_width+self.wire_distance)+self.wire_width
                len_r = abs(abs(i-j)-1)*(self.wire_width+self.wire_distance)+self.wire_distance
                dist_btw = self.outer_d - (i+j-2)*(self.wire_width+self.wire_distance) - self.wire_width
                mutual_temp = 0.5*(self.mutual_L(l_wire=(len_l+short_l),d=dist_btw)
                    +self.mutual_L(l_wire=(len_r+short_l),d=dist_btw)
                    -self.mutual_L(l_wire=len_l,d=dist_btw)
                    -self.mutual_L(l_wire=len_r,d=dist_btw))
                # Unit Fix nH to uH
                mutual_totL = mutual_totL + 0.001*mutual_temp
                #print("Mutual Temp[%d, %d] : %f" %(i,j, mutual_temp))
        mutual_totL = 2 * mutual_totL
        print("\n"+"="*40)
        print("Total Minus Mutual Inductance : %f" %(mutual_totL))
        print("="*40 +"\n")
        return mutual_totL

    def calc_inductance(self):
        print('\n\n' + "="*40)
        print("\tInducatnce calculation")
        print("="*40 + '\n\n')
        L_tot = 0
        L_tot = L_tot + self.self_inductance_total()
        print("\nPLUS Mutual Inductance of X+direction")
        L_tot = L_tot + self.mutual_inductance_totalP(self.cond_arr_XPdir)
        print("\nPLUS Mutual Inductance of X-direction")
        L_tot = L_tot + self.mutual_inductance_totalP(self.cond_arr_XMdir)
        print("\nPLUS Mutual Inductance of Y+direction")
        L_tot = L_tot + self.mutual_inductance_totalP(self.cond_arr_YPdir)
        print("\nPLUS Mutual Inductance of Y-direction")
        L_tot = L_tot + self.mutual_inductance_totalP(self.cond_arr_YMdir)
        print("\nMINUS Mutual Inductance of X direction")
        L_tot = L_tot - self.mutual_inductance_totalM(self.cond_arr_XPdir, self.cond_arr_XMdir)
        print("\nMINUS Mutual Inductance of Y direction")
        L_tot = L_tot - self.mutual_inductance_totalM(self.cond_arr_YPdir, self.cond_arr_YMdir)
        return L_tot


if __name__ == "__main__":
    # Execute only if run as a script
    ex_planar = Planarcoil()
    print("%f [uH]" %(ex_planar.calc_inductance()))