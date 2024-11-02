import numpy as np

from interior import interior_point
from simplex import simplex
import samples

def main():
    print("First Sample:\n")

    solution, z_new = interior_point(samples.first_sample)
    print(solution, z_new, '\n\n')

    solution, z_new = simplex(samples.first_sample)
    print(solution, z_new, '\n\n')

    print("Second Sample:\n")

    _ = interior_point(samples.second_sample)
    print('\n')

    _ = simplex(samples.second_sample)
    print('\n')

    print("Third Sample:\n")

    _ = interior_point(samples.third_sample)
    print('\n')

    _ = simplex(samples.third_sample)
    print('\n')

    print("Fourth Sample:\n")

    solution, z_new = interior_point(samples.fourth_sample)
    print(solution, z_new, '\n\n')

    solution, z_new = simplex(samples.fourth_sample)
    print(solution, z_new, '\n\n')

    print("Fifth Sample:\n")

    solution, z_new = interior_point(samples.fifth_sample)
    print(solution, z_new, '\n\n')

    solution, z_new = simplex(samples.fifth_sample)
    print(solution, z_new, '\n\n')

if __name__ == "__main__":
    main()
