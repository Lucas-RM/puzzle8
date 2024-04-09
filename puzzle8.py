import heapq

class Puzzle8State:
    def __init__(self, puzzle, parent=None, move=0):
        self.puzzle = puzzle
        self.parent = parent
        self.move = move
        self.cost = self.calculate_cost()

    def __lt__(self, other):
        return self.cost < other.cost

    def calculate_cost(self):
        # Heuristic: soma da distância de Manhattan e contagem de inversões
        manhattan_distance = 0
        inversion_count = 0
        flatten_puzzle = [item for row in self.puzzle for item in row if item != 0]

        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] != 0:
                    x_goal = (self.puzzle[i][j] - 1) // 3
                    y_goal = (self.puzzle[i][j] - 1) % 3
                    manhattan_distance += abs(i - x_goal) + abs(j - y_goal)

        for i in range(len(flatten_puzzle)):
            for j in range(i + 1, len(flatten_puzzle)):
                if flatten_puzzle[i] > flatten_puzzle[j]:
                    inversion_count += 1

        return manhattan_distance + inversion_count + self.move

    def is_goal(self):
        return self.puzzle == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def get_neighbors(self):
        neighbors = []
        x, y = self.find_blank()
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_puzzle = [row[:] for row in self.puzzle]
                new_puzzle[x][y], new_puzzle[new_x][new_y] = new_puzzle[new_x][new_y], new_puzzle[x][y]
                neighbors.append(Puzzle8State(new_puzzle, self, self.move + 1))
        return neighbors

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle[i][j] == 0:
                    return i, j

    def get_path(self):
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return reversed(path)


def astar(initial_state):
    open_set = [initial_state]
    closed_set = set()
    comparisons = 0

    while open_set:
        current_state = heapq.heappop(open_set)
        comparisons += 1
        if current_state.is_goal():
            return current_state.get_path(), comparisons

        closed_set.add(tuple(map(tuple, current_state.puzzle)))

        for neighbor in current_state.get_neighbors():
            if tuple(map(tuple, neighbor.puzzle)) not in closed_set:
                heapq.heappush(open_set, neighbor)
                comparisons += 1
    return None, comparisons


def print_puzzle(state):
    for row in state.puzzle:
        print(row)
    print()


def solution_puzzle(initial_puzzle):
    initial_state = Puzzle8State(initial_puzzle)
    solution, comparisons = astar(initial_state)

    if solution:
        print("Solução encontrada:")
        for state in solution:
            print_puzzle(state)
    else:
        print("Não foi encontrada uma solução.\n")

    print(f"Número de comparações realizadas: {comparisons}\n")

def main():
    # Teste 1: Melhor Caso
    best_case_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    print("Teste 1 - Melhor Caso:")
    solution_puzzle(best_case_puzzle)

    # Teste 2: Caso Intermediário
    intermediate_case_puzzle = [[1, 2, 3], [8, 0, 5], [7, 6, 4]]
    print("Teste 2 - Caso Intermediário:")
    solution_puzzle(intermediate_case_puzzle)

    # Teste 3: Pior Caso
    worst_case_puzzle = [[8, 6, 7], [2, 5, 4], [3, 0, 1]]
    print("Teste 3 - Pior Caso:")
    solution_puzzle(worst_case_puzzle)

    # Teste 4: Heurística de distância de Manhattan
    manhattan_puzzle = [[2, 0, 3], [1, 8, 4], [7, 6, 5]]
    print("Teste 4 - Heurística de distância de Manhattan:")
    solution_puzzle(manhattan_puzzle)

    # Teste 5: Heurística de contagem de inversões
    inversion_puzzle = [[1, 8, 2], [0, 4, 3], [7, 6, 5]]
    print("Teste 5 - Heurística de contagem de inversões:")
    solution_puzzle(inversion_puzzle)

    # Teste 6: Heurística combinada
    combined_puzzle = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    print("Teste 6 - Heurística combinada:")
    solution_puzzle(combined_puzzle)


if __name__ == "__main__":
    main()
