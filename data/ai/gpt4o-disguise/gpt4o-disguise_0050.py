import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join([chr(c) for c in range(65, 65 + COLS)]))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

def valid_input(input_str):
    return input_str.isalpha() and len(input_str) == 1 and 65 <= ord(input_str) < 65 + COLS

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False  # Column full

def check_winner(board, checker):
    # Check horizontal win
    for row in board:
        for c in range(COLS - 3):
            if row[c] == checker and all(row[c + i] == checker for i in range(1, 4)):
                return True

    # Check vertical win
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == checker and all(board[r + i][c] == checker for i in range(1, 4)):
                return True

    # Check diagonal win (/)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == checker and all(board[r + i][c + i] == checker for i in range(1, 4)):
                return True

    # Check diagonal win (\)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == checker and all(board[r - i][c + i] == checker for i in range(1, 4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        user_input = input().strip()
        
        if valid_input(user_input):
            col = ord(user_input.upper()) - 65
            if drop_checker(board, col, CHECKERS[current_player]):
                print_board(board)

                if check_winner(board, CHECKERS[current_player]):
                    print(f"Player {CHECKERS[current_player]} won!")
                    break

                if check_draw(board):
                    print("The game is a draw!")
                    break

                current_player = (current_player + 1) % PLAYERS
            else:
                print("Column full! You lose the turn.")
        else:
            print("Invalid input! Please enter a valid column letter.")

if __name__ == "__main__":
    main()
