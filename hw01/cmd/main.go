package main

import (
	"fmt"

	inou "github.com/setanoier/optimization-f24/io"
	smp "github.com/setanoier/optimization-f24/simplex"
)

func main() {
	var n, m int
	fmt.Print("Enter the number of decision variables (n): ")
	fmt.Scan(&n)
	fmt.Print("Enter the number of constraints (m): ")
	fmt.Scan(&m)

	C := make([]float64, n)
	A := make([][]float64, m)
	b := make([]float64, m)
	eps := 1e-6
	var isMax bool

	inou.ObjectiveCoefficientsInput(n, &C)
	inou.ConstraitMatrixInput(n, m, &A)
	inou.ValuesVectorInput(m, &b)
	inou.AccuracyInput(&eps)
	inou.IsMaximizationInput(&isMax)

	inou.RenderProblem(isMax, n, C, A, b)

	state, x, z := smp.Simplex(C, A, b, eps, isMax)
	inou.RenderSolver(state, x, z)
}
