import os
import random

# Constants for pre-defined board dimensions and player count
ROWS = 6
COLUMNS = 7
PLAYERS = 2  # You can change this to between 2 and 5 as needed

# Checkers for players
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def drop_checker(board, column, checker):
    for row in reversed(board):
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def is_winning_move(board, checker):
    # Check all possible win conditions: horizontal, vertical, diagonal down, diagonal up
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == checker:
                if c + 3 < COLUMNS and all(board[r][c+i] == checker for i in range(4)):
                    return True
                if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                    return True
                if c + 3 < COLUMNS and r + 3 < ROWS and all(board[r+i][c+i] == checker for i in range(4)):
                    return True
                if c - 3 >= 0 and r + 3 < ROWS and all(board[r+i][c-i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize game board
    board = create_board()
    current_player = random.choice(range(PLAYERS))
    print_board(board)

    while True:
        player_checker = CHECKERS[current_player]
        column_input = input(f"Player {player_checker}, please enter a column: ")

        # Validate input
        if len(column_input) == 1 and column_input.isalpha():
            col_index = ord(column_input.upper()) - 65
            if 0 <= col_index < COLUMNS:
                if not drop_checker(board, col_index, player_checker):
                    print("Column is full! You lose your turn.")
                else:
                    print_board(board)
                    if is_winning_move(board, player_checker):
                        print(f"Player {player_checker} won!")
                        break
                    if is_draw(board):
                        print("The game is a draw!")
                        break
                    current_player = (current_player + 1) % PLAYERS
            else:
                print("Invalid column! Please choose a valid column.")
        else:
            print("Invalid input! Please enter a valid column letter.")

if __name__ == "__main__":
    main()
