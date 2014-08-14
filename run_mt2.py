

import model_tools2 as mt

# reimport the module to thest the new changes
mt = reload(mt)



a1 = mt.ang()

a1.eq_add('delta_L1', 'x1-L1')
a1.eq_add('delta_L2', 'x2-L2')

a1.ode_eq_add('dot_x1', 'y1')
a1.ode_eq_add('dot_y1', '(-b1 * y1 - k1 * delta_L1 + k2 * (delta_L2 - x1)) / m1')
a1.ode_eq_add('dot_x2', 'y2')
a1.ode_eq_add('dot_y2', '(-b2 * y2 - k2 * (delta_L2 - x1)) / m2')

# substitute the algabrain equations in the ode system to generate the complete ode_subs
a1.gen_ode_subs()


# finding all the parameters
a1.eq_all_params(Zone = 'algebraic')
a1.eq_all_params(Zone = 'ode')
a1.eq_all_params(Zone = 'ode_subs')

# eample how to use the method replace_singe_var()
# a1.eq['algebraic']['delta_L1'] = a1.replace_singe_var(a1.eq['algebraic']['delta_L1'], 'x_1', 'x_11')


x_vec = a1.eq['ode_subs'].keys()
# fixme: the code below is not working as 'm_1' and 'm_2' are strings, but they should be sympy objects
# todo: change eq_all_params() to store and the sympy objects
par_vec = [a1.all_params_ode_subs['m1'], a1.all_params_ode_subs['m2']]


sens_sys_list = a1.sys_dict_to_list(a1.eq['ode_subs'])

sens_sys = a1.sens_ext_sys(sens_sys_list, x_vec, par_vec)
print sens_sys


sens_sys_list = a1.sys_dict_to_list(sens_sys)
from sympy import cse, numbered_symbols
a4=cse(sens_sys_list, symbols=numbered_symbols(prefix='t', start=0))

a1.print_Sys_optim(a4, func_name = 'r1')
