package io

import "fmt"

func RenderProblem(isMax bool, n int, C []float64, A [][]float64, b []float64) {
	switch isMax {
	case true:
		fmt.Println("\nOptimization problem (maximization)")
		fmt.Print("max z = ")
	case false:
		fmt.Println("\nOptimization problem (minimization)")
		fmt.Print("min z = ")
	}

	for i := range n {
		if i > 0 {
			fmt.Print(" + ")
		}
		fmt.Printf("%.2f * x%d", C[i], i+1)
	}

	fmt.Println("\nsubject to:")

	for i, row := range A {
		for j, val := range row {
			if j > 0 {
				fmt.Print(" + ")
			}
			fmt.Printf("%.2f + x%d", val, j+1)
		}
		fmt.Printf(" <= %.2f\n", b[i])
	}
}

func RenderSolver(state string, x []float64, z float64) {
	if state == "solved" {
		fmt.Println("\nSolver state:", state)
		fmt.Println("Optimal solution (if solved):", x)
		fmt.Println("Optimal value of the objective function:", z)
	} else {
		fmt.Println("The problem is unbounded.")
	}
}
