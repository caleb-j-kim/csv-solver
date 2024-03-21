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


def check_consistency(value1, value2, constraint):
    op = constraint[1]
    if op == "=":
        return value1 == value2
    elif op == "!":
        return value1 != value2
    elif op == ">":
        return value1 > value2
    elif op == "<":
        return value1 < value2
    else:
        raise ValueError(f"Unsupported constraint operator: {op}")


def validate(v, value, assignment, constraints): #v = variable(s), validates if values fit constraints
    for constraint in constraints:
        v1, op, v2 = constraint
        if v1 == v and v2 in assignment:
            if not check_consistency(value, assignment[v2], op):
                return False
        elif v2 == v and v1 in assignment:
            if not check_consistency(assignment[v1], value, op):
                return False
    return True


def mrv(variables, constraints): #minimum remaining value function, for solver to choose a variable
    degrees = {v: 0 for v in variables.keys()} #finds degree / total amount of constraints of each variable
    for constraint in constraints:
        for v in constraints[:2]:
            if v in degrees:
                degrees[v] += 1

    sorted_v = sorted(variables.keys(), key = lambda vars: (len(variables[vars]), -degrees[vars], vars)) #sorts variables by mrv, degree, then alphabetically
    if sorted_v:
        return sorted_v[0] #returns most constrained variable with highest degree after breaking ties alphabetically
    else:
        return None


def lcv(v, variables, constraints): #least constraining value heuristic function, for solver to choose a value
    constraining_values = {}
    for value in variables[v]:
        constraining_values[value] = 0
        for constraint in constraints:
            if v in constraint:
                if v == constraint[2]:
                    v2 = constraint[0]
                else:
                    v2 = constraint[2]
                if v2 != v:
                    for value2 in variables[v2]:
                        if not check_consistency(value, value2, constraint): #determine if there are any constraining values inside of v and v2
                            constraining_values[value] += 1
    ordered_values = sorted(constraining_values, key = lambda vars: (constraining_values[vars], vars))
    return ordered_values


def forward_check(var, value, assignment, domains, constraints):
    new_domains = {v: domains[v][:] for v in domains}  # Copy domains
    for constraint in constraints:
        if var in constraint[:2]:
            op = constraint[1]
            other_var = constraint[0] if constraint[2] == var else constraint[2]
            if other_var not in assignment:  # Skip if already assigned
                new_domain = []
                for other_value in new_domains[other_var]:
                    if check_consistency(value, other_value, op):
                        new_domain.append(other_value)
                if not new_domain:  # No valid values left for other_var
                    return None  # Indicate failure
                new_domains[other_var] = new_domain
    return new_domains


def backtrack(assignment, variables, domains, constraints, use_forward_checking, path=[], attempt=1):
    if len(assignment) == len(variables):
        print(f"{attempt}. ", ", ".join(path), "solution")
        return assignment  #Solution is found and returned

    var = mrv(variables, constraints)
    for value in lcv(var, variables, constraints):
        path_copy = path + [f"{var}={value}"]
        if validate(var, value, assignment, constraints):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if use_forward_checking:
                new_domains = forward_check(var, value, new_assignment, domains, constraints)
                if new_domains is None:  #Forward checking indicated a failure
                    print(f"{attempt}. ", ", ".join(path_copy), "failure")
                    continue
            else:
                new_domains = domains

            result = backtrack(new_assignment, variables, new_domains, constraints, use_forward_checking, path_copy, attempt + 1)
            if result:
                return result

    if not path:  #If no solution was found
        print("Failed to find a solution.")
    return None


def solve_csp(variables, constraints, tracking):
    domains = {v: variables[v] for v in variables}
    assignment = {}
    backtrack(assignment, variables, domains, constraints, tracking)


if __name__ == "__main__":
    variables = read_var_file("ex1.var1")
    constraints = read_con_file("ex1.con")
    t = get_tracking()
    result = solve_csp(variables, constraints, t)
    print(result)
