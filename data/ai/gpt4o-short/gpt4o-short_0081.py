import os
import random

# Constants
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Used for 2-5 players
NUM_PLAYERS = 3  # Change this constant to set how many players will participate (between 2 and 5)

# Board dimensions
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def display_board(board):
    os.system('clear')
    print('  ' + ' '.join(COLUMN_LABELS))
    for row in board:
        print('|' + '|'.join(row) + '|')
    print()

def is_valid_move(board, column):
    return board[0][column] == ' '

def make_move(board, column, player_symbol):
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player_symbol
            break

def check_winner(board, player_symbol):
    # Check horizontal, vertical, and diagonal directions
    def check_line(line):
        return any(player_symbol*4 in ''.join(line[i:i+4]) for i in range(len(line)-3))

    for row in board:
        if check_line(row):
            return True

    for col in range(COLUMNS):
        if check_line([board[row][col] for row in range(ROWS)]):
            return True

    # Check diagonals
    for row in range(ROWS-3):
        for col in range(COLUMNS-3):
            if player_symbol == board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return True
            if player_symbol == board[row][col+3] == board[row+1][col+2] == board[row+2][col+1] == board[row+3][col]:
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def main():
    board = create_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    player_symbols = PLAYER_SYMBOLS[:NUM_PLAYERS]

    while True:
        display_board(board)
        print(f"Player {player_symbols[current_player_index]}'s turn.")

        move = input("Choose a column (A-G): ").upper()
        if move not in COLUMN_LABELS:
            print("Invalid input! Please choose a column between A and G.")
            continue
        
        column = COLUMN_LABELS.index(move)
        if not is_valid_move(board, column):
            print("Column is full! Try another one.")
            continue

        make_move(board, column, player_symbols[current_player_index])

        if check_winner(board, player_symbols[current_player_index]):
            display_board(board)
            print(f"Player {player_symbols[current_player_index]} wins!")
            break

        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
