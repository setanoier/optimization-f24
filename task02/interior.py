import numpy as np
from numpy.linalg import norm

def interior_point(sample):
    A = sample['A']  # Constraint coefficients
    b = sample['b']  # Right-hand side values
    C = sample['C']  # Objective function coefficients
    is_max = sample["is_max"]  # Maximization or minimization flag
    alpha = 0.5 
    accuracy = 0.0001

    A = np.array(A, float)
    b = np.array(b, float)
    C = np.array(C, float)

    N = A.shape[0]
    M = A.shape[1]

    # Initial feasible solution
    x = np.hstack((np.ones(M), b - np.sum(A, axis=1)))
    A = np.hstack((A, np.eye(N)))
    c = np.hstack((C, np.zeros(N))) * (1 if is_max else -1)

    i = 1
    i = 1
    while True:
        v = x
        D = np.diag(x)
        AA = np.dot(A, D)
        cc = np.dot(D, c)
        I = np.eye(x.size)
        F = np.dot(AA, np.transpose(AA))

        # Check for unboundedness by examining if F is non-invertible.
        try:
            if np.linalg.cond(F) > 1 / accuracy:
                pass
        except:
            print("The problem does not have solution!")
            return

        FI = np.linalg.inv(F)
        H = np.dot(np.transpose(AA), FI)
        P = np.subtract(I, np.dot(H, AA))
        cp = np.dot(P, cc)

        # Check for infeasibility.
        if np.all(cp >= 0) and is_max or np.all(cp <= 0) and not is_max:
            print("The problem does not have solution!")
            return

        nu = np.absolute(np.min(cp))
        x_tilde = np.add(np.ones(x.size, float), (alpha / nu) * cp)
        x = np.dot(D, x_tilde)

        # Print the first few iterations for tracking
        if i <= 4:
            print(f"In iteration {i} we have:\nx= [{ ' '.join([str(i) for i in x]) }]")
            i += 1

        # Check for convergence
        if norm(np.subtract(x, v), ord=2) < accuracy:
            break

    print(f"In the last iteration {i} we have x:\n{ ' '.join([str(i) for i in x]) }")

    z_new = np.dot(c, x)
    if not is_max:
        z_new = -z_new

    x = x[:M]
    filtered = [(i, sol) for (i, sol) in list(enumerate(x)) if abs(sol) > accuracy]
    return filtered, z_new
