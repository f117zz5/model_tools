

import model_tools2 as mt

# reimport the module to thest the new changes
#mt = reload(mt)



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


