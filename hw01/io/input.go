package io

import (
	"fmt"
)

func ObjectiveCoefficientsInput(n int, C *[]float64) {
	fmt.Println("Enter the coefficients of the objective function (C):")
	for i := range n {
		fmt.Printf("x%d = ", i+1)
		fmt.Scan(&(*C)[i])
	}
}

func ConstraintMatrixInput(n, m int, A *[][]float64) {
	fmt.Println("Enter the constraint matrix (A) row by row:")
	for i := range m {
		(*A)[i] = make([]float64, n)
		for j := range n {
			fmt.Printf("x%d = ", j+1)
			fmt.Scan(&(*A)[i][j])
		}
		fmt.Println("-------------------")
	}
}

func ValuesVectorInput(m int, b *[]float64) {
	fmt.Println("Enter the right-hand side values (b):")
	for i := range m {
		fmt.Printf("b[%d] = ", i)
		fmt.Scan(&(*b)[i])
	}
}

func AccuracyInput(eps *float64) {
	fmt.Print("[Optional] Enter the approximation accuracy (eps): ")
	fmt.Scanln(&(*eps))
}

func IsMaximizationInput(isMax *bool) {
	var isMaximization string
	fmt.Print("Is this a maximazation problem? (yes/no): ")
	fmt.Scan(&isMaximization)
	*isMax = isMaximization == "yes"
}
