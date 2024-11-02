import numpy as np

# Set error handling for division by zero
np.seterr(divide='ignore')

def simplex(sample):
    A = sample['A']  # Constraint coefficients
    b = sample['b']  # Right-hand side values
    C = sample['C']  # Objective function coefficients
    is_max = sample['is_max']  # Maximization or minimization flag
    
    eps = 0.0001
    num_constr = len(A)
    num_vars = len(C)
    

    A = np.array(A, float)
    b = np.array(b, float)
    C = np.array(C, float)
    
    # Initialize tableau
    tableau = np.zeros((num_constr + 1, num_constr + num_vars + 1))

    # Fill the objective function row
    tableau[0, :num_vars] = -C if is_max else C

    # Fill constraint rows
    tableau[1:, :num_vars] = A
    tableau[1:, -1] = b

    # Add identity matrix for slack variables
    tableau[1:, num_vars:num_vars + num_constr] = np.identity(num_constr)

    # Perform the simplex algorithm
    while non_zero_presence(tableau[0, :-1], eps):
        # Identify pivot column
        pivot_col = np.argmin(tableau[0, :-1])

        # Calculate ratios to find pivot row
        ratios = tableau[1:, -1] / tableau[1:, pivot_col]
        ratios[ratios < eps] = np.inf  # Ignore non-positive values

        # Check for boundedness
        if check_boundedness(ratios, eps):
            return

        # Check for degeneracy
        if check_degenerate(ratios):
            print("Degenerate solution!")
            break

        # Select pivot row
        pivot_row = np.argmin(ratios) + 1
        pivot = tableau[pivot_row, pivot_col]

        # Normalize the pivot row
        tableau[pivot_row] /= pivot
        for i in range(num_constr + 1):
            if i != pivot_row:
                tableau[i] -= tableau[i, pivot_col] * tableau[pivot_row]

    # Solution extraction
    solution = np.zeros(num_vars)
    for i in range(num_vars):
        col = tableau[1:, i]
        if np.count_nonzero(col) == 1 and np.isclose(np.max(col), 1):
            basic_row = np.where(col == 1)[0][0] + 1
            solution[i] = tableau[basic_row, -1]

    # Calculate objective value
    objective_value = tableau[0, -1]
    filtered = [(i, sol) for (i, sol) in list(enumerate(solution)) if abs(sol) > eps]
    return filtered, objective_value

# Utility functions
def non_zero_presence(row, eps):
    return np.any(row < -eps)

def check_boundedness(ratios, eps):
    if np.all(np.isinf(ratios)):
        print("The method is not applicable.")
        return True
    return False

def check_degenerate(ratios):
    for i, x in enumerate(ratios):
        for j, y in enumerate(ratios):
            if i != j and x == y and x == np.min(ratios):
                return True
    return False
    