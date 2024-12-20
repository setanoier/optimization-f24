import numpy as np
import random


class TransportationTable:
    def __init__(self, sources_number: int = 3, destinations_number: int = 4):
        self.destinations_number: int = destinations_number
        self.sources_number: int = sources_number
        self.supplies = np.array([random.randint(1, 50)
                                 for _ in range(sources_number)])
        self.demands = self.generate_demands()
        self.costs = self.generate_costs()

    def generate_demands(self):
        supplies_sum: int = sum(self.supplies)

        demands = np.zeros(self.destinations_number, dtype=int)

        demands[0] = random.randint(1, supplies_sum // 2)
        demands[1]: int = random.randint(
            1 if sum(demands) != supplies_sum else 0, supplies_sum - sum(demands))
        demands[2]: int = random.randint(
            1 if sum(demands) != supplies_sum else 0, supplies_sum - sum(demands))
        demands[3]: int = supplies_sum - sum(demands)

        return demands

    def generate_costs(self):
        costs = np.random.randint(1, 600, size=(
            self.sources_number, self.destinations_number))

        return costs

    def print_table(self):
        for i in range(self.sources_number):
            for j in range(self.destinations_number):
                print(f'{self.costs[i][j]: 4}', end=" ")
            print(f'{self.supplies[i]: 4}')

        for i in range(self.destinations_number):
            print(f'{self.demands[i]: 4}', end=" ")


def set_zeros_horizontally(row: int, table: TransportationTable):
    for j in range(table.destinations_number):
        table.costs[row][j] = 0


def set_zeros_vertically(column: int, table: TransportationTable):
    for i in range(table.sources_number):
        table.costs[i][column] = 0


def is_balanced(table: TransportationTable) -> bool:
    return sum(table.supplies) == sum(table.demands)


def north_west_corner_method(table: TransportationTable) -> int:
    if not is_balanced(table):
        print("The method is not applicable!")
        return None

    answer: int = 0

    for i in range(table.sources_number):
        for j in range(table.destinations_number):
            if table.costs[i][j] > 0:
                if table.supplies[i] > table.demands[j]:
                    answer += table.costs[i][j] * table.demands[j]
                    table.supplies[i] -= table.demands[j]
                    table.demands[j] = 0
                    set_zeros_vertically(j, table)
                elif table.supplies[i] < table.demands[j]:
                    answer += table.costs[i][j] * table.supplies[i]
                    table.demands[j] -= table.supplies[i]
                    table.supplies[i] = 0
                    set_zeros_horizontally(i, table)
                else:
                    answer += table.costs[i][j] * table.demands[j]
                    table.supplies[i] = 0
                    table.demands[j] = 0
                    set_zeros_horizontally(i, table)
                    set_zeros_vertically(j, table)

    return answer


def vogel_approximation_method(table: TransportationTable) -> int:
    if not is_balanced(table):
        print("The method is not applicable!")
        return None

    answer: int = 0

    while np.any(table.supplies > 0) and np.any(table.demands > 0):
        rows_values = []
        for i in range(table.sources_number):
            valid_costs = table.costs[i, table.demands > 0]
            valid_costs = valid_costs[valid_costs != 1e9]
            if len(valid_costs) > 1:
                sorted_costs = np.sort(valid_costs)
                penalty = sorted_costs[1] - sorted_costs[0]
            else:
                penalty = 0
            rows_values.append(penalty)

        column_values = []
        for j in range(table.destinations_number):
            valid_costs = table.costs[table.supplies > 0, j]
            valid_costs = valid_costs[valid_costs != 1e9]
            if len(valid_costs) > 1:
                sorted_costs = np.sort(valid_costs)
                penalty = sorted_costs[1] - sorted_costs[0]
            else:
                penalty = 0
            column_values.append(penalty)

        max_row_value, max_column_value = max(rows_values), max(column_values)

        if max_row_value >= max_column_value:
            row = rows_values.index(max_row_value)
            valid_columns = np.where(table.demands > 0)[0]
            column = valid_columns[np.argmin(table.costs[row, valid_columns])]
        else:
            column = column_values.index(max_column_value)
            valid_rows = np.where(table.supplies > 0)[0]
            row = valid_rows[np.argmin(table.costs[valid_rows, column])]

        replacement = min(table.supplies[row], table.demands[column])
        answer += replacement * table.costs[row, column]
        table.supplies[row] -= replacement
        table.demands[column] -= replacement

        if table.supplies[row] == 0:
            table.costs[row, :] = 1e9
        if table.demands[column] == 0:
            table.costs[:, column] = 1e9

        if len(np.where(table.supplies > 0)[0]) == 1 and len(np.where(table.demands > 0)[0]) == 1:
            supply_index = np.where(table.supplies > 0)[0][0]
            demand_index = np.where(table.demands > 0)[0][0]
            if table.supplies[supply_index] == table.demands[demand_index]:
                answer += table.supplies[supply_index] * \
                    table.costs[supply_index, demand_index]
                break

    return answer


def russel_approximation_method(table: TransportationTable) -> int:
    if not is_balanced(table):
        print("The method is not applicable!")
        return None

    answer = 0

    temp_table = np.copy(table.costs)

    while np.any(table.demands > 0) and np.any(table.supplies > 0):
        valid_row_indexes = np.where(table.supplies > 0)[0]
        valid_column_indexes = np.where(table.demands > 0)[0]

        for i in valid_row_indexes:
            for j in valid_column_indexes:
                if table.costs[i][j] != 1e9:
                    max_column_value = np.max(
                        table.costs[table.costs[:, j] != 1e9, j])
                    max_row_value = np.max(
                        table.costs[i, table.costs[i, :] != 1e9])
                    temp_table[i][j] = table.costs[i, j] - \
                        max_column_value - max_row_value

        max_negative_value = 1e9
        for i in valid_row_indexes:
            for j in valid_column_indexes:
                if table.costs[i][j] != 1e9:
                    max_negative_value = min(
                        max_negative_value, temp_table[i, j])

        min_negative_indexes = []
        for i in valid_row_indexes:
            for j in valid_column_indexes:
                if table.costs[i][j] != 1e9 and max_negative_value == temp_table[i][j]:
                    min_negative_indexes.append((i, j))

        for pair in min_negative_indexes:
            row, column = pair
            replacement = min(table.supplies[row], table.demands[column])
            answer += replacement * table.costs[row, column]

            table.supplies[row] -= replacement
            table.demands[column] -= replacement

            if table.supplies[row] == 0:
                table.costs[row, :] = 1e9
                temp_table[row, :] = 1e9

            if table.demands[column] == 0:
                table.costs[:, column] = 1e9
                temp_table[:, column] = 1e9

        if len(np.where(table.supplies > 0)[0]) == 1 and len(np.where(table.demands > 0)[0]) == 1:
            supply_index = np.where(table.supplies > 0)[0][0]
            demand_index = np.where(table.demands > 0)[0][0]
            if table.supplies[supply_index] == table.demands[demand_index]:
                answer += table.supplies[supply_index] * \
                    table.costs[supply_index, demand_index]
                break

    return answer


def main():
    # First table
    first_table = TransportationTable(3, 4)
    first_table.supplies = np.array([160, 140, 170])
    first_table.demands = np.array([120, 50, 190, 110])

    first_table.costs = np.array([[7, 8, 1, 2],
                                  [4, 5, 9, 8],
                                  [9, 2, 3, 6]])

    print("First table")
    print("-------------------------")
    first_table.print_table()
    print("\n-------------------------")
    print("Northwest Corner Method:", north_west_corner_method(first_table))

    # Second table
    second_table = TransportationTable(3, 4)
    second_table.supplies = np.array([160, 140, 170])
    second_table.demands = np.array([120, 50, 190, 110])

    second_table.costs = np.array([[7, 8, 1, 2],
                                   [4, 5, 9, 8],
                                   [9, 2, 3, 6]])

    print("\nSecond table")
    print("-------------------------")
    second_table.print_table()
    print("\n-------------------------")
    print("Vogel's Approximation Method:",
          vogel_approximation_method(second_table))

    # Third table
    third_table = TransportationTable(3, 4)
    third_table.supplies = np.array([160, 140, 170])
    third_table.demands = np.array([120, 50, 190, 110])

    third_table.costs = np.array([[7, 8, 1, 2],
                                  [4, 5, 9, 8],
                                  [9, 2, 3, 6]])

    print("\nThird table")
    print("-------------------------")
    third_table.print_table()
    print("\n-------------------------")
    print("Russell's Approximation Method:",
          russel_approximation_method(third_table))

    # Unbalanced case
    unbalanced_table = TransportationTable(3, 4)
    unbalanced_table.supplies = np.array([160, 140, 170])
    unbalanced_table.demands = np.array([120, 50, 190, 150])  # Sum doesn't match supplies

    print("\nUnbalanced table")
    print("-------------------------")
    unbalanced_table.print_table()
    print("\n-------------------------")
    if not north_west_corner_method(unbalanced_table) and \
        not vogel_approximation_method(unbalanced_table) and \
        not russel_approximation_method(unbalanced_table): print("Problem is not balanced!")

    fourth_table = TransportationTable(3, 4)
    fourth_table.supplies = np.array([120, 100, 130])  # Balanced total supply
    fourth_table.demands = np.array([90, 60, 110, 90])  # Balanced total demand

    fourth_table.costs = np.array([[3, 7, 9, 4],
                                   [8, 5, 6, 2],
                                   [4, 3, 5, 7]])

    print("\nFourth table")
    print("-------------------------")
    fourth_table.print_table()
    print("\n-------------------------")
    print("Northwest Corner Method:", north_west_corner_method(fourth_table))
    fourth_table.supplies = np.array([120, 100, 130])  # Balanced total supply
    fourth_table.demands = np.array([90, 60, 110, 90])  # Balanced total demand

    fourth_table.costs = np.array([[3, 7, 9, 4],
                                   [8, 5, 6, 2],
                                   [4, 3, 5, 7]])
    print("Vogel's Approximation Method:", vogel_approximation_method(fourth_table))
    third_table.supplies = np.array([120, 100, 130])  # Balanced total supply
    third_table.demands = np.array([90, 60, 110, 90])  # Balanced total demand

    fourth_table.costs = np.array([[3, 7, 9, 4],
                                   [8, 5, 6, 2],
                                   [4, 3, 5, 7]])
    print("Russell's Approximation Method:", russel_approximation_method(fourth_table))

if __name__ == '__main__':
    main()
