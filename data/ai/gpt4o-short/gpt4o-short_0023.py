import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUMBER_OF_PLAYERS = 3  # Set the number of players (2 to 5)

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  '.join(COLUMN_LABELS))
    for row in board:
        print(' | '.join(row))
        print('-' * (COLUMNS * 4 - 1))

def make_move(board, column, player_symbol):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player_symbol
            return True
    return False

def is_valid_move(board, column):
    return board[0][column] == ' '

def check_winner(board, player_symbol):
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player_symbol for i in range(4)):
                return True
    # Vertical check
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True
    # Diagonal (positive slope) check
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True
    # Diagonal (negative slope) check
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def choose_first_player():
    return random.choice(range(NUMBER_OF_PLAYERS))

def play_game():
    board = create_board()
    players = PLAYER_SYMBOLS[:NUMBER_OF_PLAYERS]
    current_player_idx = choose_first_player()

    while True:
        print_board(board)
        current_player = players[current_player_idx]
        move_valid = False

        while not move_valid:
            move_input = input(f"Player {current_player} ({COLUMN_LABELS[0]}-{COLUMN_LABELS[-1]}): ").strip().upper()
            if move_input in COLUMN_LABELS:
                column = COLUMN_LABELS.index(move_input)
                if is_valid_move(board, column):
                    make_move(board, column, current_player)
                    move_valid = True
                else:
                    print("Column is full, try another column.")
            else:
                print(f"Invalid input, please enter a letter between {COLUMN_LABELS[0]} and {COLUMN_LABELS[-1]}.")

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to next player
        current_player_idx = (current_player_idx + 1) % NUMBER_OF_PLAYERS

if __name__ == "__main__":
    play_game()
