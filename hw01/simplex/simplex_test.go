package simplex_test

import (
	"math"
	"reflect"
	"testing"

	smp "github.com/setanoier/optimization-f24/simplex"
)

func TestMaximizationFirst(t *testing.T) {
	C := []float64{
		2.0, 3.0, 0.0, -1.0, 0.0, 0.0,
	}
	A := [][]float64{
		{2.0, -1.0, 0.0, -2.0, 1.0, 0.0},
		{3.0, 2.0, 1.0, -3.0, 0.0, 0.0},
		{-1.0, 3.0, 0.0, 4.0, 0.0, 1.0},
	}
	b := []float64{
		16.0, 18.0, 24.0,
	}
	eps, isMax := 0.01, true

	actualState, actualSolution, actualObjectiveValue := smp.Simplex(C, A, b, eps, isMax)
	expectedState, expectedSolution, expectedObjectiveValue := "solved", []float64{0.55, 8.18, 0.0, 0.0, 23.09, 0.0}, 25.64

	if actualState != expectedState {
		t.Errorf("expected state %v, got %v", expectedState,
			actualState)
	}

	if !reflect.DeepEqual(actualSolution, expectedSolution) {
		t.Errorf("expected solution %v, got %v", expectedSolution,
			actualSolution)
	}

	if actualObjectiveValue != expectedObjectiveValue {
		t.Errorf("expected objective value %v, got %v",
			expectedObjectiveValue, actualObjectiveValue)
	}
}

func TestMinimizationFirst(t *testing.T) {
	C := []float64{
		-2.0, 2.0, -6.0,
	}
	A := [][]float64{
		{2.0, 1.0, -2.0},
		{1.0, 2.0, 4.0},
		{1.0, -1.0, 2.0},
	}
	b := []float64{
		24.0, 23.0, 10.0,
	}

	eps, isMax := 0.01, false

	actualState, actualSolution, actualObjectiveValue := smp.Simplex(C, A, b, eps, isMax)
	expectedState, expectedSolution, expectedObjectiveValue := "solved", []float64{0.0, 0.75, 5.38}, -30.75

	if actualState != expectedState {
		t.Errorf("expected state %v, got %v", expectedState,
			actualState)
	}

	if !reflect.DeepEqual(actualSolution, expectedSolution) {
		t.Errorf("expected solution %v, got %v", expectedSolution,
			actualSolution)
	}

	if actualObjectiveValue != expectedObjectiveValue {
		t.Errorf("expected objective value %v, got %v",
			expectedObjectiveValue, actualObjectiveValue)
	}
}

func TestMaximazationSecond(t *testing.T) {
	C := []float64{
		9.0, 10.0, 16.0,
	}
	A := [][]float64{
		{18.0, 15.0, 12.0},
		{6.0, 4.0, 8.0},
		{5.0, 3.0, 3.0},
	}
	b := []float64{
		360.0, 192.0, 180.0,
	}

	eps, isMax := 0.01, true

	actualState, actualSolution, actualObjectiveValue := smp.Simplex(C, A, b, eps, isMax)
	expectedState, expectedSolution, expectedObjectiveValue := "solved", []float64{0.0, 8.0, 20.0}, 400.0

	if actualState != expectedState {
		t.Errorf("expected state %v, got %v", expectedState,
			actualState)
	}

	if !reflect.DeepEqual(actualSolution, expectedSolution) {
		t.Errorf("expected solution %v, got %v", expectedSolution,
			actualSolution)
	}

	if actualObjectiveValue != expectedObjectiveValue {
		t.Errorf("expected objective value %v, got %v",
			expectedObjectiveValue, actualObjectiveValue)
	}
}

func TestUnboundedFirst(t *testing.T) {
	C := []float64{
		5.0, 4.0,
	}
	A := [][]float64{
		{1.0, 0.0},
		{1.0, -1.0},
	}
	b := []float64{
		7.0, 8.0,
	}

	eps, isMax := 0.01, true

	actualState, _, _ := smp.Simplex(C, A, b, eps, isMax)
	expectedState := "the method is not applicable"

	if actualState != expectedState {
		t.Errorf("expected state %v, got %v", expectedState, actualState)
	}
}

func TestSimplex_Minimization_Custom(t *testing.T) {
	C := []float64{-3, 4, -5}
	A := [][]float64{
		{4, 3, 1},
		{2, 5, -2},
		{1, -1, 3},
	}
	b := []float64{15, 20, 10}
	eps := 0.01
	isMax := false

	result, x, objValue := smp.Simplex(C, A, b, eps, isMax)

	expectedResult := "solved"
	expectedX := []float64{3.18, 0, 2.27}
	expectedObjValue := -20.91

	if result != expectedResult {
		t.Errorf("Expected result %s, but got %s", expectedResult, result)
	}

	for i := range expectedX {
		if math.Abs(x[i]-expectedX[i]) > eps {
			t.Errorf("Expected x[%d] to be %.2f, but got %.2f", i, expectedX[i], x[i])
		}
	}

	if math.Abs(objValue-expectedObjValue) > eps {
		t.Errorf("Expected objective value %.2f, but got %.2f", expectedObjValue, objValue)
	}
}
