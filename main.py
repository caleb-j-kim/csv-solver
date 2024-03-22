# Caleb Kim
# 3/14/24
# CS 4365
# Programming Assignment #2
# #

import sys


def read_var_file(filename): #delimits var file to seperate variables and their values
    variables = {}
    with open(filename) as file:
        for line in file:
            var, *values = line.strip().split(': ')
            variables[var] = list(map(int, values[0].split()))

    return variables


def read_con_file(filename): #delimts con file to seperate variables and operands
    constraints = []
    with open(filename) as file:
        for line in file:
            constraint = tuple(line.strip().split())
            constraints.append(constraint)

    return constraints


def get_tracking(): #update function after adding fc and bc
    while True:
        user_input = input("\nThis CSP solver uses backtracking by default when traversing through its search tree.\nIf you would like to use forward checking, please input 'fc'.\nOtherwise, please input 'none'.")

        if user_input in ('fc', 'none'):
            if (user_input == 'fc'):
                return True
            elif (user_input == 'none'):
                return False


def check_consistency(value1, value2, constraint, assignment):
    op = constraint[0]
    isValid = True
    for constraint in constraints:
        if op == "=" and value1 != value2:
            isValid = False
        elif op == "!" and value1 == value2:
            isValid = False
        elif op == ">" and value1 <= value2:
            isValid = False
        elif op == "<" and value1 >= value2:
            isValid = False
        if not isValid:
            print("Failure")
            print(assignment)
    return isValid


def validate(v, value, assignment, constraints): #v = variable(s), validates if values fit constraints
    for constraint in constraints:
        v1, op, v2 = constraint
        if v1 == v and v2 in assignment:
            if not check_consistency(value, assignment[v2], op, assignment):
                return False
        elif v2 == v and v1 in assignment:
            if not check_consistency(assignment[v1], value, op, assignment):
                return False
    return True


def count_constraining_effect(value, v, domains, constraints):
    count = 0
    for constraint in constraints:
        if v in constraint:
            other_var = constraint[0] if constraint[2] == v else constraint[2]
            if other_var != v:
                # Safely access domain of other_var
                other_domain = domains.get(other_var, [])
                for other_value in other_domain:
                    if not validate(v, value, {v: value, other_var: other_value}, constraints):
                        count += 1
    return count


def mrv(variables, domains): #minimum remaining value function, for solver to choose a variable
    unassigned_variables = {var: len(domains[var]) for var in domains}
    if unassigned_variables:
        return sorted(unassigned_variables, key=lambda x: (unassigned_variables[x], x))[0] 
    else:
        None

    sorted_v = sorted(variables.keys(), key = lambda vars: (len(variables[vars]), -degrees[vars], vars)) #sorts variables by mrv, degree, then alphabetically
    if sorted_v:
        return sorted_v[0] #returns most constrained variable with highest degree after breaking ties alphabetically
    else:
        return None


def lcv(v, domains, constraints, assignment): #least constraining value heuristic function, for solver to choose a value
    if v not in domains:
        return []

    values_sorted_by_lcv = sorted(domains[v], key=lambda x: count_constraining_effect(x, v, domains, constraints))
    return values_sorted_by_lcv


def forward_check(var, value, assignment, domains, constraints):
    new_domains = {v: domains[v][:] for v in domains}  # Copy domains
    for constraint in constraints:
        if var in constraint[:2]:
            op = constraint[1]
            other_var = constraint[0] if constraint[2] == var else constraint[2]
            if other_var not in assignment:  # Skip if already assigned
                new_domain = []
                for other_value in new_domains[other_var]:
                    if check_consistency(value, other_value, constraints, assignment):
                        new_domain.append(other_value)
                if not new_domain:  # No valid values left for other_var
                    return None  # Indicate failure
                new_domains[other_var] = new_domain
    return new_domains


def backtrack(assignment, variables, domains, constraints, tracking, path=[], attempt=1):
    if len(assignment) == len(variables):
        # Print solution
        print_solution(path, True)
        return True

    v = mrv(variables, domains)
    for value in lcv(v, domains, constraints, assignment):
        if check_consistency(v, value, constraints, assignment):
            assignment[v] = value
            new_path = path[:] + [f"{v}={value}"]
            new_domains = domains.copy()
            if v in new_domains: del new_domains[v]  # Remove assigned var from domains

            if tracking and not forward_check(v, value, assignment, new_domains, constraints):
                # Forward checking failed, try next value
                print_solution(new_path, False)
                attempt += 1
                continue
            
            if backtrack(assignment.copy(), variables, new_domains, constraints, tracking, new_path, attempt):
                return True  # Successful completion
            else:
                # Backtracking, this path failed
                print_solution(new_path, False)
                attempt += 1
    
    return False  # Failed to find a solution


def print_solution(path, found):
    if found:
        print("Solution found.")
    else:
        print("Failure.")
    
    for assignment in path:
        print(assignment)
        

def solve_csp(variables, constraints, tracking):
    domains = {v: variables[v] for v in variables}
    assignment = {}
    backtrack(assignment, variables, domains, constraints, tracking)


if __name__ == "__main__":
    variables = read_var_file("ex1.var1")
    constraints = read_con_file("ex1.con")
    print(constraints)
    t = get_tracking()
    result = solve_csp(variables, constraints, t)
