import os
import random

ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# Player symbols in order for 2 to 5 players
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COL_LABELS))
    for row in board:
        print('|'+ '|'.join(row) + '|')
    print('-' * (COLS * 2 + 1))

def get_valid_column(board, player_symbol):
    while True:
        col_input = input(f"Player {player_symbol}, choose a column (A-G): ").upper()
        if col_input not in COL_LABELS:
            print("Invalid column. Please choose between A and G.")
            continue
        col_idx = COL_LABELS.index(col_input)
        if board[0][col_idx] != ' ':
            print("Column full. Pick another one.")
            continue
        return col_idx

def drop_piece(board, col, player_symbol):
    # Drop piece into col, from bottom row going up
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row, col

def check_win(board, row, col, player_symbol):
    # Directions to check: horizontal, vertical, diag1 (/), diag2 (\)
    directions = [
        [(0,1), (0,-1)],
        [(1,0), (-1,0)],
        [(1,1), (-1,-1)],
        [(1,-1), (-1,1)]
    ]
    for direction in directions:
        count = 1
        for dr, dc in direction:
            r, c = row, col
            while True:
                r += dr
                c += dc
                if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
                    count += 1
                else:
                    break
        if count >= 4:
            return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    clear_screen()
    print("Welcome to Connect 4!")
    while True:
        try:
            player_count = int(input("Enter number of players (2-5): "))
            if 2 <= player_count <= 5:
                break
            else:
                print("Please enter a number between 2 and 5.")
        except:
            print("Invalid input. Please enter a number.")

    players = PLAYER_SYMBOLS[:player_count]

    board = create_board()
    current_player_idx = random.randint(0, player_count -1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_idx]

        col = get_valid_column(board, current_player)
        row, col = drop_piece(board, col, current_player)

        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins! Congratulations!")
            break
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw! The board is full.")
            break

        current_player_idx = (current_player_idx + 1) % player_count

    print("Thanks for playing!")

if __name__ == "__main__":
    main()
