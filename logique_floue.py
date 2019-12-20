import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

error = ctrl.Antecedent(np.arange(-4, 4, 0.5), 'error')
error_dot = ctrl.Antecedent(np.arange(-10, 10, 0.5), 'error_dot')
output = ctrl.Consequent(np.arange(-100, 100, 1), 'Percent_Output')

error['too_hot'] = fuzz.trapmf(error.universe, [-4, -4, -2, 0])
error['just_right'] = fuzz.trimf(error.universe, [-2, 0, 2])
error['too_cold'] = fuzz.trapmf(error.universe, [0, 2, 4, 4])

error_dot['getting_hotter'] = fuzz.trapmf(error_dot.universe, [-10, -10, -5, 0])
error_dot['no_change'] = fuzz.trimf(error_dot.universe, [-5, 0, 5])
error_dot['getting_colder'] = fuzz.trapmf(error_dot.universe, [0, 5, 10, 10])

output['cool'] = fuzz.trapmf(output.universe, [-100, -100, -50, 0])
output['do_nothing'] = fuzz.trimf(output.universe, [-50, 0, 50])
output['heat'] = fuzz.trapmf(output.universe, [0, 50, 100, 100])


rule_heat1 = ctrl.Rule(error['too_cold'] | error_dot['getting_colder'], output['heat'])
rule_heat2 = ctrl.Rule(error['too_cold'] | error_dot['no_change'], output['heat'])
rule_heat3 = ctrl.Rule(error['too_cold'] | error_dot['getting_hotter'], output['heat'])
rule_heat4 = ctrl.Rule(error['just_right'] | error_dot['getting_colder'], output['heat'])
rule_do_nothing = ctrl.Rule(error['just_right'] | error_dot['no_change'], output['do_nothing'])
rule_cool1 = ctrl.Rule(error['too_hot'] | error_dot['getting_colder'], output['cool'])
rule_cool2 = ctrl.Rule(error['too_hot'] | error_dot['no_change'], output['cool'])
rule_cool3 = ctrl.Rule(error['too_hot'] | error_dot['getting_hotter'], output['cool'])
rule_cool4 = ctrl.Rule(error['just_right'] | error_dot['getting_hotter'], output['cool'])


output_ctrl = ctrl.ControlSystem([rule_cool1, rule_cool2, rule_cool3, rule_cool4, rule_do_nothing,
                                 rule_heat1, rule_heat2, rule_heat3, rule_heat4])
output_check = ctrl.ControlSystemSimulation(output_ctrl)

error_list = [-1.5, -1.5, 0.5, 0.5]
error_dot_list = [-4, -1, 1, 4]

for i in range(0, 4):
    output_check.input['error'] = error_list[i]
    output_check.input['error_dot'] = error_dot_list[i]

    output_check.compute()
    print(output_check.output['Percent_Output'])
