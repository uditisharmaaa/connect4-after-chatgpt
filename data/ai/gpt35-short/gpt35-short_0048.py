import os
import random

# Constants
ROWS = 6
COLS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def clear_screen():
    os.system('clear')  # For Linux/Mac; for Windows use 'cls'

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print(" Connect 4\n")
    # Print column labels
    print('  ' + '   '.join(COL_LABELS))
    print(' +' + '---+' * COLS)
    # Print rows
    for row in board:
        print(' | ' + ' | '.join(row) + ' |')
        print(' +' + '---+' * COLS)

def get_valid_columns(board):
    """Return list of column indices that are not full"""
    valid_cols = []
    for c in range(COLS):
        if board[0][c] == ' ':
            valid_cols.append(c)
    return valid_cols

def get_player_move(board, player_symbol):
    valid_cols = get_valid_columns(board)
    valid_col_labels = [COL_LABELS[c] for c in valid_cols]

    while True:
        move = input(f"Player {player_symbol}, choose a column ({', '.join(valid_col_labels)}): ").upper().strip()
        if move in valid_col_labels:
            col_index = COL_LABELS.index(move)
            if col_index in valid_cols:
                return col_index
            else:
                print("That column is full. Choose another one.")
        else:
            print("Invalid input. Please enter a valid column label.")

def make_move(board, col, player_symbol):
    """Put player_symbol in the lowest empty row in given col"""
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = player_symbol
            return row, col  # Return position where the disc landed

def check_win(board, row, col, player_symbol):
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player_symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    return False

def is_draw(board):
    # If top row is full (no space), it's a draw
    return all(cell != ' ' for cell in board[0])

def select_num_players():
    while True:
        try:
            n = int(input("Enter number of players (2-5): "))
            if 2 <= n <= 5:
                return n
            else:
                print("Please enter a number between 2 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    num_players = select_num_players()
    players = PLAYER_SYMBOLS[:num_players]
    current_idx = random.randint(0, num_players-1)
    board = create_board()

    while True:
        print_board(board)
        player = players[current_idx]
        col = get_player_move(board, player)
        row, col = make_move(board, col, player)

        # Check win
        if check_win(board, row, col, player):
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break

        # Check draw
        if is_draw(board):
            print_board(board)
            print("The game is a draw! No more moves possible.")
            break

        # Next player's turn
        current_idx = (current_idx + 1) % num_players

if __name__ == "__main__":
    main()
