from sympy import  *
#import model_tools as mt

class ang(object):
    def __init__(self):
        # there are two types pf containers: eq and params. 
        # The first one, eq, contains the equations. The second one, params, 
        # contains the parameters.
        #
        # For each eq and params there are three areas: 
        # - algebraic - list of algebraic equations
        # - ode - list of differential equations
        # - ode_subs - list of differential equations where the algebraic ones are substituted in
        self.eq = dict()
        self.params = dict()
        self.all_params = dict()
        # dict for all the equations defined
        self.eq['algebraic'] = dict()
        self.params['algebraic'] = dict()
        self.all_params['algebraic'] = list()
        # dict for the ODE system described by eqns_list
        self.eq['ode'] = dict()
        self.params['ode'] = dict()
        self.all_params['ode'] = list()
        # the substituted diff_eqns_list
        self.eq['ode_subs'] = dict()
        self.params['ode_subs'] = dict()
        self.all_params['ode_subs'] = list()
        self.all_params_ode_subs = dict()

    # def find_param_to_subs(self, params_to_search, equation):
    #     #eqns = set(eqns_list.keys())
    #     b1 = list(equation.free_symbols)
    #     curr_list = list()
    #     for curr_el in b1:
    #         curr_list.append(curr_el.name)

    #     return params_to_search.intersection(set(curr_list))

    def convert_func(self, string):
        """
        This function converts a string containing a math expression to a sympy 
        function.
        """
        expr = sympify(string)
        my_vars = expr.free_symbols
        my_vars_list = list(my_vars)
        #my_vars_list.sort()
        subs_dict = dict()
        for current_var in my_vars_list:
            subs_dict[current_var.name] = Symbol(current_var.name, real=True)
        expr_real = expr.subs(subs_dict)
        #return {'eq': expr_real, 'Subs_Dict': subs_dict}
        return expr_real


    def substitute_concept2(self, eq_key, eqns_list):
        """
        Takes a single equation and substitutes all the variables that are
        found in eqns_list. The equation is addressed by the key from the ode
        dictionary.
        
        eq_key - key from the ode dictionary.
        eqns_list - dictionary with equations to be substituted.
        
        eqation - dictionary
        eqns_list - dictionary
        """
        eqns = set(eqns_list.keys())
        curr_eq = self.eq['ode'][eq_key]
        something_found=True
        while something_found:
            a1 = list(curr_eq.free_symbols)
            a1_list = list()
            a1_dict = dict()
            for curr_el in a1:
                a1_list.append(curr_el.name)
                a1_dict[curr_el.name] =curr_el

            to_subs = list(eqns.intersection(set(a1_list)))
            if not to_subs:
                something_found = False
            else:
                for curr_el in to_subs:
                    curr_eq = curr_eq.subs(a1_dict[curr_el], eqns_list[curr_el])

        self.eq['ode_subs'][eq_key] = curr_eq
        self.params['ode_subs'][eq_key] = curr_eq.free_symbols


    def replace_singe_var(self, equation, old_var, new_var):
        # This method replaces a single variable in one equation by a new one.
        # In other words: it renames a single variable...
        # curr_eq = eqns_list['G_eff']['eq']
        curr_eq = equation
        a1 = list(curr_eq.free_symbols)
        a1_list = list()
        a1_dict = dict()
        for curr_el in a1:
            a1_list.append(curr_el.name)
            a1_dict[curr_el.name] =curr_el
        return curr_eq.subs(a1_dict[old_var], Symbol(new_var, real=True))
    def ode_eq_add(self, Name, Equation):
        self.eq_add(Name, Equation, Zone = 'ode')
        
    def eq_add(self, Name, Equation, Zone = 'algebraic'):
        if self.eq[Zone].has_key(Name):
            # equation already defined
            print "Warning: equation for '%s' already defined!" % Name
        else:
            self.eq[Zone][Name] = self.convert_func(Equation)
            self.params[Zone][Name] = self.eq[Zone][Name].free_symbols

    def ode_eq_get(self, Name, Equation):
        self.eq_get(Name, Equation, Zone = 'ode')
        
    def eq_get(self, Name, Zone = 'algebraic'):
        """
        Returns an equation by its key from the dictionary.
        Default zone is algebraic.
        """
        
        if self.eq[Zone].has_key(Name):
            return self.eq[Zone][Name]
        else:
            # TODO: probably generate an error here?
            return None

    def ode_eq_remove(self, Name):
        self.eq_remove(Name, Zone = 'ode')
        
    def eq_remove(self, Name, Zone = 'algebraic'):
        if self.eq[Zone].has_key(Name):
            self.eq[Zone].pop(Name, None)
            self.params[Zone].pop(Name, None)
            
    def eq_all_params(self, Zone = 'algebraic'):
        # This function gets all the params from all the equations

        # TODO: 
        #   - if Zone = 'ode_subs' or Zone = 'ode', remove the states. Get them from
        #   keys
        #   - loop over algebraic, ode & ode_subs. Whats the point of having three
        #   zones and only one all_params

        # make sure the list is empty before starting
        self.all_params[Zone] = []

        all_params = set()
        for current_key in self.eq[Zone].keys():
            all_params = all_params.union(self.params[Zone][current_key])

        # convert the set to list
        all_params_list = list(all_params)

        # call the name method for each sympy variable and append them to list
        for current_el in all_params_list:
            self.all_params[Zone].append(current_el.name)
            self.all_params_ode_subs[current_el.name] = current_el

        # sort the list of variables names
        self.all_params[Zone].sort()

    # It seems the method remove_states has not been finished and right now
    # after months not working on this project I have no idea what it should do...
    # def remove_states(self, Zone = 'algebraic'):

    #     # finish me!
    #     d1 = set(self.all_params)
    #     d2 = list(d1.difference(set(self.eq[Zone].keys())))
    #     d2.sort()
    #     return d2

    def gen_ode_subs(self):

        for current_key in self.eq['ode'].keys():
            self.substitute_concept2(current_key, self.eq['algebraic'])
            
    def sys_dict_to_list(self, sys_dict):
        # This method gets a system of ODEs definded as a dictionary and converts
        # it to list container to be used later in sens_ext_sys() for example
        sys_list = []
        keys = sys_dict.keys()
        keys.sort()
        for key in keys:
            sys_list.append(sys_dict[key])
        return sys_list

    def sens_ext_sys(self, eq_sys, x_vec, par_vec):
        """
        Calculation of the sensitivity equations of a ode system eq_sys. 
        The eq_sys has states x_vec and parameters par_vec.
        
        The sentitivities are 
        \frac{\partial x}{\partial \theta}
        
        The algorithm comes from 
        Hassan K. Khalil, Nonlinear Systems, Prentice Hall, 2001, 0130673897
        """

        n_x=len(x_vec)
        n_par=len(par_vec)

        A_Matrix=Matrix(n_x,n_x,n_x*n_x*[0.0])
        B_Matrix=Matrix(n_x,n_par,n_x*n_par*[0.0])


        S_Matrix=Matrix(n_x,n_par,lambda i_n_x,i_n_par: 'x%d' % (n_x+1+n_x*i_n_par+i_n_x))

        for ii in range(n_x):
            for jj in range(n_x):
                A_Matrix[ii,jj]=eq_sys[ii].diff(x_vec[jj])

        for ii in range(n_x):
            for jj in range(n_par):
                B_Matrix[ii,jj]=eq_sys[ii].diff(par_vec[jj])

        
        dot_S=A_Matrix.multiply(S_Matrix).add(B_Matrix)

        eq=dict()



        for ii in range(n_x):
            keyString= 'dot_y%03d' % (ii+1)
            eq[keyString] = eq_sys[ii]
            for jj in range(n_par):
                keyString= 'dot_y%03d' % (n_x+1+n_x*jj+ii)
                eq[keyString] = dot_S[ii, jj]

        return eq


def main():
    pass

if __name__ == '__main__':
    main()
    a1 = ang()
    
    a1.eq_add('delta__L1', 'x_1-L_1')
    a1.eq_add('delta__L2', 'x_2-L_2')
    
    a1.ode_eq_add('x_1', 'y_1')
    a1.ode_eq_add('y_1', '(-b_1 * y_1 - k_1 * delta__L1 + k_2 * (delta__L2 - x_1)) / m_1')
    a1.ode_eq_add('x_2', 'y_2')
    a1.ode_eq_add('y_2', '(-b_2 * y_2 - k_2 * (delta__L2 - x_1)) / m_2')

    a1.substitute_concept2(a1.eq['ode']['y_1'], a1.eq['algebraic'])
    a1.substitute_concept2(a1.eq['ode']['y_2'], a1.eq['algebraic'])
    #a1.eq_all_params()
    #print a1.all_params
    #print a1.remove_states()
    #a1.eq
    #a1.params
    #a1.ode_eq_remove('y_1')
    #a1.eq
    #a1.params    
    print 'Hello!'