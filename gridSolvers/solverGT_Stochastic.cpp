#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <random>
#include <algorithm>
#include <chrono>


const int N = 9; // Size of the Sudoku grid

void printBoard(const std::vector<std::vector<int>>& board) {
    for (const auto& row : board) {
        for (int num : row) {
            std::cout << num << " ";
        }
        std::cout << std::endl;
    }
}

void loadRelationships(const std::string& filename, std::vector<std::vector<std::string>>& relationships) {
    std::ifstream file(filename);
    std::string line;
    for (int i = 0; i < N && std::getline(file, line); ++i) {
        std::stringstream ss(line);
        for (int j = 0; j < N; ++j) {
            std::string item;
            std::getline(ss, item, ',');
            relationships[i][j] = item; // Load the cell relationship
        }
    }
}

// Function to check the number of valid relationships
int countValidRelationships(const std::vector<std::vector<int>>& board, int row, int col, int num, const std::vector<std::vector<std::string>>& relationships) {
    int count = 0;

    // Check top cell
    if (row > 0 && relationships[row][col][0] != 'n' && board[row - 1][col] != 0) {
        if ((relationships[row][col][0] == 'g' && num > board[row - 1][col]) ||
            (relationships[row][col][0] == 'l' && num < board[row - 1][col])) {
            count++;
        }
    }

    // Check right cell
    if (col < N - 1 && relationships[row][col][1] != 'n' && board[row][col + 1] != 0) {
        if ((relationships[row][col][1] == 'g' && num > board[row][col + 1]) ||
            (relationships[row][col][1] == 'l' && num < board[row][col + 1])) {
            count++;
        }
    }

    // Check bottom cell
    if (row < N - 1 && relationships[row][col][2] != 'n' && board[row + 1][col] != 0) {
        if ((relationships[row][col][2] == 'g' && num > board[row + 1][col]) ||
            (relationships[row][col][2] == 'l' && num < board[row + 1][col])) {
            count++;
        }
    }

    // Check left cell
    if (col > 0 && relationships[row][col][3] != 'n' && board[row][col - 1] != 0) {
        if ((relationships[row][col][3] == 'g' && num > board[row][col - 1]) ||
            (relationships[row][col][3] == 'l' && num < board[row][col - 1])) {
            count++;
        }
    }

    return count;
}

// Stochastic approach to solve Greater Than Sudoku
void stochasticSudokuSolver(std::vector<std::vector<int>>& board, const std::vector<std::vector<std::string>>& relationships) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(1, 9);

    bool filled = false;

    while (!filled) {
        // Fill board with random values
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                // Assign a random value to the cell
                int num = distrib(gen);
                board[i][j] = num;

                // Validate relationships
                int validCount = countValidRelationships(board, i, j, num, relationships);
                if (validCount < 2) {
                    // If less than 2 valid relationships, reset the cell
                    board[i][j] = 0;  // Reset for reevaluation
                }
            }
        }

        // Check if the board is filled with valid numbers
        filled = std::all_of(board.begin(), board.end(), [](const std::vector<int>& row) {
            return std::all_of(row.begin(), row.end(), [](int num) { return num != 0; });
        });
    }
}

int main() {
    // Define a 9x9 Sudoku board initialized to 0 (empty cells)
    std::vector<std::vector<int>> board(N, std::vector<int>(N, 0));

    // Load the relationships from the CSV file
    std::vector<std::vector<std::string>> relationships(N, std::vector<std::string>(N, std::string(4, 'n'))); // 4 characters per cell
    loadRelationships("sudoku_greater_matrix.csv", relationships); // Adjust the filename as needed

    // Display the initial board
    std::cout << "Initial Board:\n";
    printBoard(board);

    
    auto start = std::chrono::high_resolution_clock::now();

    // Solve the Greater Than Sudoku using stochastic approach
    stochasticSudokuSolver(board, relationships);

    // Display the final board
    std::cout << "Final Board after Stochastic Solver:\n";
    printBoard(board);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Time elapsed: " << elapsed.count() << " seconds" << std::endl;


    return 0;
}
