import os
import random

# Constants for dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Symbols for checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    column_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    print("  " + "   ".join(column_labels[:len(board[0])]))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_move(board, column_index):
    return board[0][column_index] == ' '

def get_move(board):
    while True:
        column = input("Please enter a column: ").upper()
        if column in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:len(board[0])]:
            column_index = ord(column) - ord('A')
            if is_valid_move(board, column_index):
                return column_index
            else:
                print("Column is full. Try another column.")
        else:
            print("Invalid input. Try again.")

def place_checker(board, column_index, checker):
    for row in reversed(board):
        if row[column_index] == ' ':
            row[column_index] = checker
            break

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal for a win
    for row in range(len(board)):
        for col in range(len(board[0])):
            if col <= len(board[0]) - 4 and all(board[row][col + i] == checker for i in range(4)):
                return True
            if row <= len(board) - 4 and all(board[row + i][col] == checker for i in range(4)):
                return True
            if col <= len(board[0]) - 4 and row <= len(board) - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if col >= 3 and row <= len(board) - 4 and all(board[row + i][col - i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    # Randomly select the starting player
    current_player = random.randint(0, PLAYERS - 1)
    board = create_board(ROWS, COLUMNS)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        column_index = get_move(board)
        place_checker(board, column_index, CHECKERS[current_player])
        print_board(board)

        if check_winner(board, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch players
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
