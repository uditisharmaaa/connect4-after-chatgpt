import os
import random

# Constants (modify if you want to change board size or number of players)
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # Change between 2 and 5 for more players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    cols = len(board[0])
    col_labels = "  ".join([chr(ord('A') + i) for i in range(cols)])
    print('  ' + col_labels)
    print('+' + '---+' * cols)
    for row in board:
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
        print('+' + '---+' * cols)

def get_column_index(col_letter, cols):
    if len(col_letter) == 1 and 'A' <= col_letter <= chr(ord('A') + cols - 1):
        return ord(col_letter) - ord('A')
    return -1

def is_column_full(board, col_idx):
    return board[0][col_idx] != ' '

def place_checker(board, col_idx, player_symbol):
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = player_symbol
            return board.index(row)
    return -1  # Column is full

def valid_input(user_input, cols):
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_letter = user_input.upper()
    return 'A' <= col_letter < chr(ord('A') + cols)

def check_win(board, row_idx, col_idx, player_symbol):
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (1, 1),   # down-diagonal right
        (-1, 1)   # up-diagonal right
    ]
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row_idx + dr, col_idx + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        # Check opposite direction
        r, c = row_idx - dr, col_idx - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        # Check if four in a row
        if count >= 4:
            return True
    return False

def check_draw(board):
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def main():
    board = create_board(ROWS, COLUMNS)
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    # Randomly pick first player
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current_player_idx]}, you go first!")

    game_over = False
    while not game_over:
        player_symbol = players[current_player_idx]
        print_board(board)
        print(f"Player {player_symbol}, please enter a column:")

        col_input = input().strip().upper()
        while not valid_input(col_input, COLUMNS):
            print("Invalid input. Please enter a valid column letter:")
            col_input = input().strip().upper()

        col_idx = get_column_index(col_input, COLUMNS)
        if col_idx == -1:
            print("Invalid column! Try again.")
            continue
        if is_column_full(board, col_idx):
            print("That column is full! You lose your turn!")
            # Move to next player
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            continue

        row_idx = place_checker(board, col_idx, player_symbol)

        if check_win(board, row_idx, col_idx, player_symbol):
            print_board(board)
            print(f"Player {player_symbol} won!")
            game_over = True
            break

        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            game_over = True
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
