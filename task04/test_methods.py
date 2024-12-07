import optimization_methods as om
import math


def test_bisection():
    # Test 1: f(x) = x - 2, interval [1, 3], expected root 2
    def f(x): return x - 2
    a, b = 1, 3
    epsilon = 1e-6
    root = om.bisection(f, a, b, epsilon)
    print(
        f"Test 1 - Root: {root}, Expected: 2.0, Difference: {abs(root - 2.0)}")

    # Test 2: f(x) = x^3 - 6x^2 + 11x - 6, interval [1.5, 2.5], expected root 2
    def f(x): return x**3 - 6*x**2 + 11*x - 6
    a, b = 1.5, 2.5
    epsilon = 1e-6
    root = om.bisection(f, a, b, epsilon)
    print(
        f"Test 2 - Root: {root}, Expected: 2.0, Difference: {abs(root - 2.0)}")

    # Test 3: f(x) = sin(x), interval [0, 2*pi], expected root pi
    def f(x): return math.sin(x)
    a, b = 0, 2*math.pi
    epsilon = 1e-6
    root = om.bisection(f, a, b, epsilon)
    print(
        f"Test 3 - Root: {root}, Expected: pi, Difference: {abs(root - math.pi)}")

    # Test 4: f(x) = x^2 + 1, interval [-2, 2], no root
    def f(x): return x**2 + 1
    a, b = -2, 2
    epsilon = 1e-6
    root = om.bisection(f, a, b, epsilon)
    if root is None:
        print("Test 4 - No root found, as expected.")
    else:
        print(f"Test 4 - Unexpected root found: {root}")


def test_golden_section():
    # Test 1: f(x) = (x - 2)^2 + 3, interval [0, 5], expected min x=2, f(x)=3
    def f(x): return (x - 2)**2 + 3
    a, b = 0, 5
    epsilon = 1e-6
    x_min, f_min = om.golden_section(f, a, b, epsilon)
    print(
        f"Test 1 - x_min: {x_min}, f_min: {f_min}, Expected x: 2.0, f(x): 3.0")

    # Test 2: f(x) = x^2 - 4x + 5, interval [1, 4], expected min x=2, f(x)=1
    def f(x): return x**2 - 4*x + 5
    a, b = 1, 4
    epsilon = 1e-6
    x_min, f_min = om.golden_section(f, a, b, epsilon)
    print(
        f"Test 2 - x_min: {x_min}, f_min: {f_min}, Expected x: 2.0, f(x): 1.0")

    # Test 3: f(x) = e^x + x, interval [-2, 2], expected min around x ~ -1
    def f(x): return math.exp(x) + x
    a, b = -2, 2
    epsilon = 1e-6
    x_min, f_min = om.golden_section(f, a, b, epsilon)
    expected_x = -1  # approximate
    expected_f = math.exp(-1) - 1
    print(
        f"Test 3 - x_min: {x_min}, f_min: {f_min}, Expected x: ~{-1}, f(x): {expected_f}")

    # Test 4: f(x) = x^3 - 3x + 1, interval [-2, 2], not unimodal
    def f(x): return x**3 - 3*x + 1
    a, b = -2, 2
    epsilon = 1e-6
    x_min, f_min = om.golden_section(f, a, b, epsilon)
    print(
        f"Test 4 - x_min: {x_min}, f_min: {f_min}, Expected: Not guaranteed, function not unimodal")


def test_gradient_ascent():
    # Test 1: f(x) = -x^2 + 4x + 1, df(x) = -2x + 4, x0=0, alpha=0.1, N=100, expected x=2, f(x)=5
    def f(x): return -x**2 + 4*x + 1
    def df(x): return -2*x + 4
    x0 = 0
    alpha = 0.1
    N = 100
    x_max, f_max = om.gradient_ascent(f, df, x0, alpha, N)
    print(
        f"Test 1 - x_max: {x_max}, f_max: {f_max}, Expected x: 2.0, f(x): 5.0")

    # Test 2: f(x) = -x^2 + 4x + 1, df(x) = -2x + 4, x0=0, alpha=0.5, N=100
    def f(x): return -x**2 + 4*x + 1
    def df(x): return -2*x + 4
    x0 = 0
    alpha = 0.5
    N = 100
    x_max, f_max = om.gradient_ascent(f, df, x0, alpha, N)
    print(
        f"Test 2 - x_max: {x_max}, f_max: {f_max}, Expected x: 2.0, f(x): 5.0")

    # Test 3: f(x) = -x^4 + 2x^2 + 1, df(x) = -4x^3 + 4x, x0=1, alpha=0.1, N=100
    def f(x): return -x**4 + 2*x**2 + 1
    def df(x): return -4*x**3 + 4*x
    x0 = 1
    alpha = 0.1
    N = 100
    x_max, f_max = om.gradient_ascent(f, df, x0, alpha, N)
    print(
        f"Test 3 - x_max: {x_max}, f_max: {f_max}, Expected x: 1.0 or -1.0, f(x): 2.0")

    # Test 4: f(x) = sin(x), df(x) = cos(x), x0=0, alpha=0.1, N=100
    def f(x): return math.sin(x)
    def df(x): return math.cos(x)
    x0 = 0
    alpha = 0.1
    N = 100
    x_max, f_max = om.gradient_ascent(f, df, x0, alpha, N)
    expected_x = math.pi/2
    expected_f = 1.0
    print(
        f"Test 4 - x_max: {x_max}, f_max: {f_max}, Expected x: {expected_x}, f(x): {expected_f}")


def main():
    print("Running Bisection Method Tests:")
    test_bisection()
    print("\nRunning Golden Section Method Tests:")
    test_golden_section()
    print("\nRunning Gradient Ascent Method Tests:")
    test_gradient_ascent()


if __name__ == "__main__":
    main()
