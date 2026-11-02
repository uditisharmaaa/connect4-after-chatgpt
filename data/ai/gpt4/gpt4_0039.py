import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')  # For Linux/Unix
    # os.system('cls')  # For Windows, uncomment if testing on Windows

def initialize_board(rows, columns):
    return [[" "] * columns for _ in range(rows)]

def print_board(board):
    columns_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:len(board[0])]
    print("  " + "   ".join(columns_labels))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, columns_labels):
    return column.upper() in columns_labels

def is_column_full(board, column_index):
    return board[0][column_index] != " "

def get_column_index(column, columns_labels):
    return columns_labels.index(column.upper())

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == " ":
            row[column_index] = checker
            return

def check_for_win(board, checker):
    # Check horizontally
    for row in board:
        for col in range(len(row) - 3):
            if row[col] == checker and all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertically
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            if board[row][col] == checker and all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonally (top-left to bottom-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonally (bottom-left to top-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == checker and all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_board_full(board):
    return all(cell != " " for cell in board[0])

def main():
    # Initialize the game
    board = initialize_board(ROWS, COLUMNS)
    columns_labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:COLUMNS]
    players = CHECKERS[:PLAYERS]
    random.shuffle(players)

    # Choose the starting player
    current_player_index = 0

    while True:
        clear_screen()
        print_board(board)
        print(f"Player {players[current_player_index]}'s turn.")
        
        while True:
            column = input("Please enter a column: ").strip()
            if not is_valid_column(column, columns_labels):
                print("Invalid column! Please choose a valid column.")
                continue

            column_index = get_column_index(column, columns_labels)
            if is_column_full(board, column_index):
                print("Column is full! Please choose another column.")
                continue
            
            break
        
        place_checker(board, column_index, players[current_player_index])

        # Check for a win
        if check_for_win(board, players[current_player_index]):
            clear_screen()
            print_board(board)
            print(f"Player {players[current_player_index]} won!")
            break

        # Check for a draw
        if is_board_full(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
