#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>

const int N = 9; // Size of the Sudoku grid

void printBoard(const std::vector<std::vector<int>>& board) {
    for (const auto& row : board) {
        for (int num : row) {
            std::cout << num << " ";
        }
        std::cout << std::endl;
    }
}

// Function to load the relationships from a CSV file
void loadRelationships(const std::string& filename, std::vector<std::vector<std::string>>& relationships) {
    std::ifstream file(filename);
    std::string line;
    for (int i = 0; i < N && std::getline(file, line); ++i) {
        std::stringstream ss(line);
        for (int j = 0; j < N; ++j) {
            std::string item;
            std::getline(ss, item, ',');
            relationships[i][j] = item; 
        }
    }
}

// Function to check if a number obeys the regular sudoku rules
bool isSafe(const std::vector<std::vector<int>>& board, int row, int col, int num, const std::vector<std::vector<std::string>>& relationships) {

    for (int x = 0; x < N; x++) {
        if (board[row][x] == num || board[x][col] == num) {
            return false;
        }
    }

    // Check 3x3 subgrid
    int startRow = row - row % 3, startCol = col - col % 3;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i + startRow][j + startCol] == num) {
                return false;
            }
        }
    }

    // Check Greater Than relationships
    // Top cell
    if (row > 0 && relationships[row][col][0] == 'g' && board[row - 1][col] != 0 && num <= board[row - 1][col]) {
        return false;
    }
    if (row > 0 && relationships[row][col][0] == 'l' && board[row - 1][col] != 0 && num >= board[row - 1][col]) {
        return false;
    }

    // Right cell
    if (col < N - 1 && relationships[row][col][1] == 'g' && board[row][col + 1] != 0 && num <= board[row][col + 1]) {
        return false;
    }
    if (col < N - 1 && relationships[row][col][1] == 'l' && board[row][col + 1] != 0 && num >= board[row][col + 1]) {
        return false;
    }

    // Bottom cell
    if (row < N - 1 && relationships[row][col][2] == 'g' && board[row + 1][col] != 0 && num <= board[row + 1][col]) {
        return false;
    }
    if (row < N - 1 && relationships[row][col][2] == 'l' && board[row + 1][col] != 0 && num >= board[row + 1][col]) {
        return false;
    }

    // Left cell
    if (col > 0 && relationships[row][col][3] == 'g' && board[row][col - 1] != 0 && num <= board[row][col - 1]) {
        return false;
    }
    if (col > 0 && relationships[row][col][3] == 'l' && board[row][col - 1] != 0 && num >= board[row][col - 1]) {
        return false;
    }

    return true;
}


// Backtracking function to solve the Greater Than Sudoku
bool solveGreaterThanSudoku(std::vector<std::vector<int>>& board, const std::vector<std::vector<std::string>>& relationships) {
    for (int row = 0; row < N; row++) {
        for (int col = 0; col < N; col++) {

            // Find an empty cell (use 0)
            if (board[row][col] == 0) {

                for (int num = 1; num <= 9; num++) {
                    if (isSafe(board, row, col, num, relationships)) {
                        board[row][col] = num; 
                        std::cout << " " << num ;

                        // Recursively try to solve
                        if (solveGreaterThanSudoku(board, relationships)) {
                            return true;
                        }

                        // If not correct, backtrack
                        board[row][col] = 0;
                    }
                }
                return false; // Trigger backtracking when no num is valid
            }
        }
    }
    return true; // Sudoku is solved
}

int main() {
    // 9x9 Sudoku board initialized to 0 (empty cells)
    std::vector<std::vector<int>> board(N, std::vector<int>(N, 0));

    // Load the relationships from the CSV file
    std::vector<std::vector<std::string>> relationships(N, std::vector<std::string>(N, std::string(4, 'n'))); // 4 characters per cell for top,right,bottom,left
    loadRelationships("sudoku_greater_matrix.csv", relationships); // Comes from the python scrapping side

    std::cout << "Initial Board:\n";
    printBoard(board);

    // Solve the Greater Than Sudoku
    if (solveGreaterThanSudoku(board, relationships)) {
        std::cout << "Sudoku solved successfully:\n";
        printBoard(board);
    } else {
        std::cout << "No solution exists.\n";
    }

    return 0;
}




























// #include "utils.hpp"

// //Functions to read CSV files
// void loadCsv(const std::string& filename, std::vector<std::vector<int>>& matrix) {
//     std::ifstream file(filename);
//     std::string line;
//     while (std::getline(file, line)) {
//         std::stringstream ss(line);
//         std::string item;
//         std::vector<int> row;
//         while (std::getline(ss, item, ',')) {
//             row.push_back(std::stoi(item));
//         }
//         matrix.push_back(row);
//     }
// }

// void loadStringCsv(const std::string& filename, std::vector<std::string>& matrix) {
//     std::ifstream file(filename);
//     std::string line;
//     while (std::getline(file, line)) {
//         matrix.push_back(line);
//     }
// }


// int main(int argc, char* argv[]) {

//     std::vector<std::vector<int>> intMatrix;
//     std::vector<std::string> stringMatrix;

//     // Load integer CSV
//     loadCsv("sudoku_digit_matrix.csv", intMatrix);

//     // Load string CSV
//     loadStringCsv("sudoku_greater_matrix.csv", stringMatrix);

//     // Display integer matrix
//     std::cout << "Integer Matrix:\n";
//     for (const auto& row : intMatrix) {
//         for (const auto& item : row) {
//             std::cout << item << " ";
//         }
//         std::cout << "\n";
//     }

//     // Display string matrix
//     std::cout << "\nString Matrix:\n";
//     for (const auto& line : stringMatrix) {
//         std::cout << line << "\n";
//     }

//     return 0;
// }
