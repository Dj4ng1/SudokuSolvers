//This function as a test to solve regular sudoku
#include "utils.hpp"


void printBoard(const std::vector<std::vector<int>>& board) {
    for (const auto& row : board) {
        for (int num : row) {
            std::cout << num << " ";
        }
        std::cout << std::endl;
    }
}

bool isSafe(const std::vector<std::vector<int>>& board, int row, int col, int num) {
    // Check row
    for (int x = 0; x < N; x++) {
        if (board[row][x] == num) return false;
    }

    // Check column
    for (int x = 0; x < N; x++) {
        if (board[x][col] == num) return false;
    }

    // Check 3x3 subgrid
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i + startRow][j + startCol] == num) return false;
        }
    }

    return true;
}

// Backtracking function to solve the Sudoku
bool solveSudoku(std::vector<std::vector<int>>& board) {
    for (int row = 0; row < N; row++) {
        for (int col = 0; col < N; col++) {
            // Find an empty cell
            if (board[row][col] == 0) {
                // Try digits from 1 to 9
                for (int num = 1; num <= 9; num++) {
                    if (isSafe(board, row, col, num)) {
                        board[row][col] = num; // Assign num to the cell

                        // Recursively try to solve
                        if (solveSudoku(board)) {
                            return true;
                        }

                        // If not correct, backtrack
                        board[row][col] = 0;
                    }
                }
                return false; // Trigger backtracking
            }
        }
    }
    return true; // Sudoku is solved
}

int main() {
    // Example Sudoku board (0 represents empty cells)
    std::vector<std::vector<int>> board = {
        {5, 3, 0, 0, 7, 0, 0, 0, 0},
        {6, 0, 0, 1, 9, 5, 0, 0, 0},
        {0, 9, 8, 0, 0, 0, 0, 6, 0},
        {8, 0, 0, 0, 6, 0, 0, 0, 3},
        {4, 0, 0, 8, 0, 3, 0, 0, 1},
        {7, 0, 0, 0, 2, 0, 0, 0, 6},
        {0, 6, 0, 0, 0, 0, 2, 8, 0},
        {0, 0, 0, 4, 1, 9, 0, 0, 5},
        {0, 0, 0, 0, 8, 0, 0, 7, 9}
    };

    if (solveSudoku(board)) {
        std::cout << "Sudoku solved successfully:\n";
        printBoard(board);
    } else {
        std::cout << "No solution exists.\n";
    }

    return 0;
}
