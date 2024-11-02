package simplex

import (
	"math"
)

func Simplex(C []float64, A [][]float64, b []float64, eps float64, isMax bool) (string, []float64, float64) {
	n, m := len(C), len(b)
	tableau := make([][]float64, m+1)
	basicMapping := make([]int, m) // Maps basic variables (slack vars and initial ones)

	// Step 1: Objective function row (C) in the tableau
	tableau[0] = make([]float64, n+m+1)
	for j := 0; j < n; j++ {
		if isMax {
			tableau[0][j] = -C[j]
		} else {
			tableau[0][j] = C[j]
		}
	}

	// Step 2: Form the initial tableau by introducing slack variables for inequalities
	for i := range m {
		tableau[i+1] = make([]float64, n+m+1)
		copy(tableau[i+1], A[i])
		if slackVarNeed(i, &basicMapping, A, C) {
			tableau[i+1][n+i] = 1
			basicMapping[i] = n + i
		}
		tableau[i+1][n+m] = b[i]
	}

	for {
		// Step 3.1: Identify the entering variable (most negative coefficient in the objective row)
		pivotCol := -1
		minVal := 0.0
		for j := 0; j < n+m; j++ {
			if tableau[0][j] < minVal {
				minVal = tableau[0][j]
				pivotCol = j
			}
		}

		// If no negative values are found, we have reached the optimal solution
		if pivotCol == -1 {
			break
		}

		// Step 3.2: Compute the ratio of RHS to pivot column
		rhsRatios := make([]float64, m)
		for i := 0; i < m; i++ {
			if tableau[i+1][pivotCol] > eps {
				rhsRatios[i] = tableau[i+1][n+m] / tableau[i+1][pivotCol]
			} else {
				rhsRatios[i] = math.Inf(1) // Exclude non-positive pivot elements
			}
		}

		// Step 3.3: Identify the smallest positive ratio of RHS to pivot column
		pivotRow := -1
		minRatio := math.MaxFloat64
		for i, ratio := range rhsRatios {
			if ratio < minRatio {
				minRatio = ratio
				pivotRow = i + 1 // +1 because tableau has one extra row for the objective function
			}
		}

		if pivotRow == -1 {
			return "the method is not applicable", nil, 0
		}

		// Step 3.4: Perform the pivot operation
		pivotValue := tableau[pivotRow][pivotCol]
		for j := 0; j < n+m+1; j++ {
			tableau[pivotRow][j] /= pivotValue
		}

		for i := 0; i < m+1; i++ {
			if i != pivotRow {
				factor := tableau[i][pivotCol]
				for j := 0; j < n+m+1; j++ {
					tableau[i][j] -= factor * tableau[pivotRow][j]
				}
			}
		}

		// Update basic variable mapping
		basicMapping[pivotRow-1] = pivotCol
	}

	// Extract the solution
	x := make([]float64, n)
	for i, pos := range basicMapping {
		if pos < n { // Only assign if it's a decision variable, not a slack variable
			x[pos] = roundFloat(tableau[i+1][n+m], 2)
		}
	}

	// Handle minimization case
	objValue := tableau[0][n+m]
	if !isMax {
		objValue = -objValue
	}

	objValue = roundFloat(objValue, 2)

	return "solved", x, objValue
}

func slackVarNeed(row int, basicMapping *[]int, A [][]float64, C []float64) bool {
	for i, val := range A[row] {
		if val == 1 && C[i] == 0 {
			(*basicMapping)[row] = i
			return false
		}
	}
	return true
}

func roundFloat(val float64, precision uint) float64 {
	ratio := math.Pow(10, float64(precision))
	return math.Round(val*ratio) / ratio
}
