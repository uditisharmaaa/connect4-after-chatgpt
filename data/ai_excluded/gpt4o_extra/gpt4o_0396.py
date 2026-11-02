import os
import random

# Game constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2

def clear_screen():
    os.system('clear')  # For Linux/Unix

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    for row in board:
        print("+---" * COLUMNS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLUMNS + "+")

def get_player_input():
    while True:
        column = input("Please enter a column: ").strip().upper()
        if len(column) != 1 or not 'A' <= column <= 'G':
            print("Invalid input. Please enter a column letter between A and G.")
        else:
            return ord(column) - 65

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = PLAYER_SYMBOLS[player]
            return

def check_for_winner(board, player):
    symbol = PLAYER_SYMBOLS[player]

    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == symbol for i in range(4)):
                return True

    return False

def check_for_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = create_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {PLAYER_SYMBOLS[current_player]}'s turn.")
        
        col = get_player_input()

        if not is_valid_move(board, col):
            print("Column is full. You lose your turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        make_move(board, col, current_player)

        if check_for_winner(board, current_player):
            print_board(board)
            print(f"Player {PLAYER_SYMBOLS[current_player]} won!")
            break

        if check_for_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
