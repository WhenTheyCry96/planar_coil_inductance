# -*- coding: utf-8 -*- 
from inductance_calc import *

def flux_calculator(p_coil):
    # temporary
    iter_num = int(p_coil.num_coil/4)
    outer_d = p_coil.outer_d
    coil_w = p_coil.wire_width
    coil_p = p_coil.wire_distance
    field = 0
    flux = 0
    print("%d %f %f %f" %(iter_num, outer_d, coil_w, coil_p))
    while True:
        magnetic_field = input('\n'+"Input B field [T]: ")
        if isNumber(magnetic_field) and float(magnetic_field) > 0:
            field = float(magnetic_field)
            break
        else:
            print('\n' + "!!!!Input Error!!!!" + '\n')
    for i in range(iter_num):
        area = math.pow((outer_d - (coil_w + coil_p)*i),2)
        flux = flux + area * field
    # unit MKS [cm] -> [m]
    flux = flux / 10000
    print("Total Flux : %f [wb]" %(flux))
    return flux

def voltage_calculator(p_coil):
    # temporary
    iter_num = int(p_coil.num_coil/4)
    outer_d = p_coil.outer_d
    coil_w = p_coil.wire_width
    coil_p = p_coil.wire_distance
    field = 0
    voltage = 0
    print("%d %f %f %f" %(iter_num, outer_d, coil_w, coil_p))
    while True:
        magnetic_field = input('\n'+"Input dB/dt field [T/sec]: ")
        if isNumber(magnetic_field) and float(magnetic_field) > 0:
            field = float(magnetic_field)
            break
        else:
            print('\n' + "!!!!Input Error!!!!" + '\n')
    for i in range(iter_num):
        area = math.pow((outer_d - (coil_w + coil_p)*i),2)
        voltage = voltage + area * field
    # unit MKS [cm] -> [m]
    voltage = voltage / 10000
    print("Total voltage induced : %f [V]" %(voltage))
    return voltage

if __name__ == "__main__":
    # Execute only if run as a script
    ex_planar = Planarcoil()
    print("%f [uH]" %(ex_planar.calc_inductance()))
    flux_calculator(ex_planar)
    voltage_calculator(ex_planar)