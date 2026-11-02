import random
import os

# Constants for the game
NUM_ROWS = 6
NUM_COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def initialize_board():
    return [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

def print_board(board):
    os.system('clear')  # Clear screen
    print(' '.join(COLUMN_LABELS))
    for row in board:
        print(' '.join(row))
    print()

def get_next_player(current_player, total_players):
    return (current_player + 1) % total_players

def validate_input(choice):
    return choice.upper() in COLUMN_LABELS

def make_move(board, column, player_symbol):
    col_index = COLUMN_LABELS.index(column.upper())
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = player_symbol
            return True
    return False

def check_winner(board, player_symbol):
    # Check horizontal
    for row in board:
        for col in range(NUM_COLUMNS - 3):
            if all(row[col + i] == player_symbol for i in range(4)):
                return True

    # Check vertical
    for col in range(NUM_COLUMNS):
        for row in range(NUM_ROWS - 3):
            if all(board[row + i][col] == player_symbol for i in range(4)):
                return True

    # Check diagonal (/)
    for row in range(NUM_ROWS - 3):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row + i][col + i] == player_symbol for i in range(4)):
                return True

    # Check diagonal (\)
    for row in range(3, NUM_ROWS):
        for col in range(NUM_COLUMNS - 3):
            if all(board[row - i][col + i] == player_symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    board = initialize_board()
    total_players = int(input("How many players? (2 to 5): "))
    if total_players < 2 or total_players > 5:
        print("Invalid number of players. Please select between 2 to 5 players.")
        return
    
    current_player = random.randint(0, total_players - 1)
    game_over = False

    while not game_over:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        print(f"Player {current_player + 1}'s turn ({player_symbol})")

        choice = input("Choose a column (A-G): ")
        if not validate_input(choice):
            print("Invalid input. Please choose a valid column label (A-G).")
            continue

        if not make_move(board, choice, player_symbol):
            print("Column is full. Choose another column.")
            continue

        if check_winner(board, player_symbol):
            print_board(board)
            print(f"Player {current_player + 1} ({player_symbol}) wins!")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            current_player = get_next_player(current_player, total_players)

if __name__ == "__main__":
    play_game()
