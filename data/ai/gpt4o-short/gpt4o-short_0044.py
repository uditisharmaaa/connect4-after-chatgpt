import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("\n")

def get_player_count():
    while True:
        try:
            count = int(input("Enter number of players (2-5): "))
            if 2 <= count <= 5:
                return count
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def check_win(board, symbol):
    # Check horizontal lines
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col] == symbol and all(row[col + i] == symbol for i in range(4)):
                return True

    # Check vertical lines
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if board[row][col] == symbol and all(board[row + i][col] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom left to top right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and all(board[row + i][col + i] == symbol for i in range(4)):
                return True

    # Check diagonal (top left to bottom right)
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if board[row][col] == symbol and all(board[row - i][col + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def drop_disc(board, column, symbol):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = symbol
            return True
    return False

def get_player_move(player_symbol):
    while True:
        move = input(f"Player {player_symbol}, pick a column ({COLUMN_LABELS}): ").upper()
        if len(move) == 1 and move in COLUMN_LABELS:
            return COLUMN_LABELS.index(move)
        else:
            print("Invalid move. Try again.")

def play_game():
    player_count = get_player_count()
    current_player = random.choice(range(player_count))
    board = create_board(ROWS, COLUMNS)
    while True:
        print_board(board)
        player_symbol = PLAYER_SYMBOLS[current_player]
        column_choice = get_player_move(player_symbol)
        
        if drop_disc(board, column_choice, player_symbol):
            if check_win(board, player_symbol):
                print_board(board)
                print(f"Player {player_symbol} wins!")
                break
            elif check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
            else:
                current_player = (current_player + 1) % player_count
        else:
            print("Column is full. Try a different column.")

if __name__ == "__main__":
    play_game()
