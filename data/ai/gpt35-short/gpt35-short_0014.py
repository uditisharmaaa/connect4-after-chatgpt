import os
import random

ROWS = 6
COLS = 7
COLUMNS_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# You can change these to have 2 to 5 players
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Use first N for the game

NUM_PLAYERS = 3  # set number of players here between 2 to 5
PLAYERS = PLAYERS[:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    print('  ' + ' '.join(COLUMNS_LABELS))
    for row in board:
        print('|'+ '|'.join(row) + '|')
    print('+' + '--'*COLS + '+')

def get_column_index(player):
    while True:
        col = input(f"Player {player}, choose a column (A-G): ").upper()
        if col in COLUMNS_LABELS:
            col_idx = COLUMNS_LABELS.index(col)
            return col_idx
        else:
            print("Invalid column. Please enter a letter from A to G.")

def is_valid_move(board, col):
    return board[0][col] == ' '

def make_move(board, col, player):
    # Drop token to the lowest empty space in the column
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row, col

def check_direction(board, start_row, start_col, delta_row, delta_col, player):
    count = 0
    row, col = start_row, start_col
    while 0 <= row < ROWS and 0 <= col < COLS and board[row][col] == player:
        count += 1
        row += delta_row
        col += delta_col
    return count

def check_win(board, row, col, player):
    # Check all 4 directions for a connect 4
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1  # start with 1 for the placed token
        count += check_direction(board, row - dr, col - dc, -dr, -dc, player)
        count += check_direction(board, row + dr, col + dc, dr, dc, player)
        if count >= 4:
            return True
    return False

def check_draw(board):
    # Draw if top row is all filled (no space)
    for c in range(COLS):
        if board[0][c] == ' ':
            return False
    return True

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        print(f"Players: {PLAYERS}")
        print(f"Current player: {current_player}")

        col = get_column_index(current_player)
        if not is_valid_move(board, col):
            print("Column full. Try again.")
            input("Press Enter to continue...")
            continue

        row, col = make_move(board, col, current_player)

        if check_win(board, row, col, current_player):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        # Next player's turn
        idx = PLAYERS.index(current_player)
        current_player = PLAYERS[(idx + 1) % len(PLAYERS)]

if __name__ == '__main__':
    main()
