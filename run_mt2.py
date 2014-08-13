

import model_tools2 as mt

# reimport the module to thest the new changes
mt = reload(mt)



a1 = mt.ang()

a1.eq_add('delta_L1', 'x_1-L_1')
a1.eq_add('delta_L2', 'x_2-L_2')

a1.ode_eq_add('dot_x_1', 'y_1')
a1.ode_eq_add('dot_y_1', '(-b_1 * y_1 - k_1 * delta_L1 + k_2 * (delta_L2 - x_1)) / m_1')
a1.ode_eq_add('dot_x_2', 'y_2')
a1.ode_eq_add('dot_y_2', '(-b_2 * y_2 - k_2 * (delta_L2 - x_1)) / m_2')

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
par_vec = [a1.all_params_ode_subs['m_1'], a1.all_params_ode_subs['m_2']]


sens_sys_list = a1.sys_dict_to_list(a1.eq['ode_subs'])

sens_sys = a1.sens_ext_sys(sens_sys_list, x_vec, par_vec)
print sens_sys


sens_sys_list = a1.sys_dict_to_list(sens_sys)
from sympy import cse, numbered_symbols
a4=cse(sens_sys_list, symbols=numbered_symbols(prefix='t', start=0))

print '#----------'
print 'def ODE_sys(w, t):'
prtStr='  ('
for ii in range(len(sens_sys_list)):
    if ii< len(sens_sys_list)-1:
        prtStr='%sx%d, ' % (prtStr, ii+1)
    else:
        prtStr='%sx%d' % (prtStr, ii+1)
prtStr='%s)=w ' % (prtStr)
print prtStr
for t_ii in a4[0]:
  t_ii_Lhs, t_ii_rhs = t_ii
  print '  %s=%s' % (t_ii_Lhs, t_ii_rhs)
for ii, current_eq in enumerate(a4[1]):
  if ii==0:
    print '  dot_x=[%s,' % current_eq
  elif ii>0 and ii!=len(a4[1])-1:
    print '  %s,' % current_eq
  else:
    print '  %s]' % current_eq
print '  '
print '  return dot_x'