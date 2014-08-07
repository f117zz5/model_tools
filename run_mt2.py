

import model_tools2 as mt

# reimport the module to thest the new changes
#mt = reload(mt)
# at the moment it se

a1 = mt.ang()

a1.eq_add('delta__L1', 'x_1-L_1')
a1.eq_add('delta__L2', 'x_2-L_2')

a1.ode_eq_add('x_1', 'y_1')
a1.ode_eq_add('y_1', '(-b_1 * y_1 - k_1 * delta__L1 + k_2 * (delta__L2 - x_1)) / m_1')
a1.ode_eq_add('x_2', 'y_2')
a1.ode_eq_add('y_2', '(-b_2 * y_2 - k_2 * (delta__L2 - x_1)) / m_2')

#for current_key in a1.eq['ode'].keys():
#	a1.substitute_concept2(current_key, a1.eq['algebraic'])

# the gen_ode_subs method makes exactly the two lines above
a1.gen_ode_subs()

#a1.substitute_concept2('y_1', a1.eq['algebraic'])
#a1.substitute_concept2('y_2', a1.eq['algebraic'])

#a1.eq_all_params(Zone = 'ode_subs')
