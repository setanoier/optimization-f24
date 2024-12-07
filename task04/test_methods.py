import optimization_methods as om
import math


def test_bisection():
    # Test: f(x) = x^3 - 6x^2 + 11x - 6, interval [1, 2]
    def f(x): return x - 2
    a, b = 1, 3
    epsilon = 1e-6
    root = om.bisection(f, a, b, epsilon)
    print(
        f"Test - Root: {root}")

def test_golden_section():
    # Test: f(x) = (x - 2)^2 + 3, interval [0, 5]
    def f(x): return (x - 2)**2 + 3
    a, b = 0, 5
    epsilon = 1e-6
    x_min, f_min = om.golden_section(f, a, b, epsilon)
    print(
        f"Test - x_min: {x_min}, f_min: {f_min}")

def test_gradient_ascent():
    # Test: f(x) = -x^2 + 4x + 1, df(x) = -2x + 4, x0=0, alpha=0.1, N=100
    def f(x): return -x**2 + 4*x + 1
    def df(x): return -2*x + 4
    x0 = 0
    alpha = 0.1
    N = 100
    x_max, f_max = om.gradient_ascent(f, df, x0, alpha, N)
    print(
        f"Test - x_max: {x_max}, f_max: {f_max}")

def main():
    print("Running Bisection Method Tests:")
    test_bisection()
    print("\nRunning Golden Section Method Tests:")
    test_golden_section()
    print("\nRunning Gradient Ascent Method Tests:")
    test_gradient_ascent()


if __name__ == "__main__":
    main()
