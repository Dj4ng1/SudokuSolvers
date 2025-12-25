#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>

const int N = 9; // Size of the Sudoku grid

//Load Sudoku Grid
void loadCsv(const std::string& filename, std::vector<std::vector<int>>& matrix);

//Load Greater grid
void loadStringCsv(const std::string& filename, std::vector<std::string>& matrix);


// Function to print the Sudoku board
void printBoard(const std::vector<std::vector<int>>& board);

// Function to check if a number is valid in the given cell
bool isSafe(const std::vector<std::vector<int>>& board, int row, int col, int num);

// Backtracking function to solve the Sudoku
bool solveSudoku(std::vector<std::vector<int>>& board);


