import os
import random

# Constants
ROWS = 6
COLUMNS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYERS_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # max 5 players

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print(" " + " ".join(COLUMN_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print("-" * (COLUMNS * 2 + 1))

def is_valid_column(col_char):
    return col_char in COLUMN_LABELS

def get_column_index(col_char):
    return COLUMN_LABELS.index(col_char)

def is_column_not_full(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, symbol):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row, col

def check_win(board, row, col, symbol):
    # Directions: horizontal, vertical, diag1(/), diag2(\)
    directions = [
        [(0,1), (0,-1)],     # horizontal
        [(1,0), (-1,0)],     # vertical
        [(1,1), (-1,-1)],    # diagonal \
        [(1,-1), (-1,1)]     # diagonal /
    ]

    for direction in directions:
        count = 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def get_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Number must be between 2 and 5.")
        except:
            print("Invalid input. Please enter a number.")

def get_player_input(player_symbol, board):
    while True:
        col_char = input(f"Player {player_symbol}, choose column A-G: ").upper()
        if not is_valid_column(col_char):
            print("Invalid column. Please enter a letter A-G.")
            continue
        col = get_column_index(col_char)
        if not is_column_not_full(board, col):
            print("That column is full. Pick another one.")
            continue
        return col

def main():
    num_players = get_num_players()
    players = PLAYERS_SYMBOLS[:num_players]
    current_player_idx = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player_symbol = players[current_player_idx]
        col = get_player_input(player_symbol, board)
        row, col = drop_piece(board, col, player_symbol)

        if check_win(board, row, col, player_symbol):
            clear_screen()
            print_board(board)
            print(f"Player {player_symbol} wins! Congratulations!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
