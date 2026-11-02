import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_PIECES = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print(' ' + ' '.join(COL_LABELS))
    for row in board:
        print(' ' + ' '.join(row))

def get_valid_column(board, player):
    while True:
        col_input = input(f"Player {player} - Choose column (A-G): ").upper()
        if col_input not in COL_LABELS:
            print("Invalid column. Choose letter A-G.")
            continue
        col = COL_LABELS.index(col_input)
        if board[0][col] != '.':
            print("Column is full. Choose another one.")
            continue
        return col

def drop_piece(board, col, piece):
    for row in reversed(range(ROWS)):
        if board[row][col] == '.':
            board[row][col] = piece
            return row, col

def check_direction(board, start_row, start_col, delta_row, delta_col, piece):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == piece:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, piece):
    # Check all 4 directions: horizontal, vertical, and two diagonals
    directions = [
        ((0, 1), (0, -1)),   # horizontal
        ((1, 0), (-1, 0)),   # vertical
        ((1, 1), (-1, -1)),  # diagonal /
        ((1, -1), (-1, 1))   # diagonal \
    ]
    for (d1, d2) in directions:
        count = 1  # count the piece just placed
        count += check_direction(board, row + d1[0], col + d1[1], d1[0], d1[1], piece)
        count += check_direction(board, row + d2[0], col + d2[1], d2[0], d2[1], piece)
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(board[0][col] != '.' for col in range(COLS))

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            num_players = int(input(f"Enter number of players (2-5): "))
            if 2 <= num_players <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("That is not a valid number.")

    players = PLAYER_PIECES[:num_players]
    current_player_index = random.randint(0, num_players - 1)

    board = create_board()

    while True:
        clear_screen()
        print_board(board)
        player = players[current_player_index]
        col = get_valid_column(board, player)
        row, col = drop_piece(board, col, player)

        if check_win(board, row, col, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        current_player_index = (current_player_index + 1) % num_players

if __name__ == "__main__":
    main()
