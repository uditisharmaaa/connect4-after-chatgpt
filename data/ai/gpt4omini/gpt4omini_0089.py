import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # For 2 players

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels A to G
    print("+---" + "+---" * (COLUMNS - 1) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" + "+---" * (COLUMNS - 1) + "+")

def is_valid_input(column_input, board):
    if len(column_input) != 1 or not column_input.isalpha():
        return False
    col_index = ord(column_input.upper()) - 65
    return 0 <= col_index < COLUMNS and board[0][col_index] == ' '

def place_checker(board, col_index, checker):
    for row in reversed(board):  # Start from the last row
        if row[col_index] == ' ':
            row[col_index] = checker
            break

def check_win(board, checker):
    # Check horizontal, vertical, and diagonal win conditions
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == checker:
                # Horizontal check
                if c + 3 < COLUMNS and all(board[r][c+i] == checker for i in range(4)):
                    return True
                # Vertical check
                if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                    return True
                # Diagonal right check
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r+i][c+i] == checker for i in range(4)):
                    return True
                # Diagonal left check
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)  # Random player at the start
    game_over = False

    while not game_over:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        column_input = input().strip()

        if is_valid_input(column_input, board):
            col_index = ord(column_input.upper()) - 65
            place_checker(board, col_index, current_player)

            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                game_over = True
            elif is_draw(board):
                print_board(board)
                print("The game is a draw!")
                game_over = True
            else:
                current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]
        else:
            print("Invalid input. Please try again.")
    
if __name__ == "__main__":
    main()
