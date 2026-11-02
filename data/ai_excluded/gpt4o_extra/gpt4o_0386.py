import os
import random

# Constants for board dimensions and number of players
ROWS = 6
COLUMNS = 7
PLAYERS = 2

# Symbols for players' checkers
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def print_board(board):
    os.system('clear')  # Clear the screen
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def valid_input(input_char):
    return input_char.isalpha() and ord(input_char.upper()) - ord('A') < COLUMNS

def place_checker(board, col, checker):
    # Place the checker in the lowest available row in the column
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board, checker):
    # Check horizontally, vertically, and diagonally for a win
    # Horizontal check
    for row in board:
        for c in range(COLUMNS - 3):
            if all(symbol == checker for symbol in row[c:c+4]):
                return True

    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Diagonal check (positive slope)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Diagonal check (negative slope)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def play_game():
    board = create_board()
    print_board(board)
    
    current_player_index = random.randint(0, PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    while True:
        print(f"Player {current_checker}, please enter a column:")
        user_input = input().strip().upper()

        if not valid_input(user_input):
            print("Invalid input. Please enter a valid column.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if place_checker(board, col, current_checker):
            print_board(board)
            if check_win(board, current_checker):
                print(f"Player {current_checker} won!")
                break
            if check_draw(board):
                print("The game is a draw!")
                break
            # Switch to the next player
            current_player_index = (current_player_index + 1) % PLAYERS
            current_checker = CHECKERS[current_player_index]
        else:
            print("Column is full, turn is lost!")

if __name__ == "__main__":
    play_game()
