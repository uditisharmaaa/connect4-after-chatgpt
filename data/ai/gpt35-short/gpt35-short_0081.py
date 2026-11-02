import os
import random

ROWS = 6
COLUMNS = 7
COL_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

# You can change number of players here (between 2 and 5)
NUM_PLAYERS = 3  
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLUMNS board filled with spaces
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    print("  " + " ".join(COL_LABELS))
    for row in board:
        print("|" + "|".join(row) + "|")
    print()

def get_column_index(col):
    col = col.upper()
    if col in COL_LABELS:
        return COL_LABELS.index(col)
    return -1

def is_valid_move(board, col_idx):
    return board[0][col_idx] == ' '

def make_move(board, col_idx, player):
    # Drop the piece to the lowest empty spot in the column
    for row in reversed(range(ROWS)):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = player
            return row, col_idx

def check_direction(board, start_row, start_col, delta_row, delta_col, player):
    count = 0
    r, c = start_row, start_col
    while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
        count += 1
        r += delta_row
        c += delta_col
    return count

def check_win(board, row, col, player):
    # Check all directions from the placed piece
    # Horizontal (left + right)
    total = (check_direction(board, row, col, 0, -1, player) -1) + (check_direction(board, row, col, 0, 1, player))
    if total >= 4:
        return True
    # Vertical (up + down)
    total = (check_direction(board, row, col, -1, 0, player) -1) + (check_direction(board, row, col, 1, 0, player))
    if total >= 4:
        return True
    # Diagonal /
    total = (check_direction(board, row, col, -1, 1, player) -1) + (check_direction(board, row, col, 1, -1, player))
    if total >= 4:
        return True
    # Diagonal \
    total = (check_direction(board, row, col, -1, -1, player) -1) + (check_direction(board, row, col, 1, 1, player))
    if total >= 4:
        return True
    return False

def is_draw(board):
    # If top row has no empty spaces, it's a draw
    return all(space != ' ' for space in board[0])

def main():
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS -1)

    while True:
        clear_screen()
        print_board(board)
        player = PLAYERS[current_player_idx]
        move = input(f"Player {player}, choose a column (A-G): ").strip()
        col_idx = get_column_index(move)
        if col_idx == -1:
            print("Invalid column. Please choose A-G.")
            input("Press Enter to continue...")
            continue
        if not is_valid_move(board, col_idx):
            print("That column is full. Try another one.")
            input("Press Enter to continue...")
            continue

        row, col = make_move(board, col_idx, player)

        if check_win(board, row, col, player):
            clear_screen()
            print_board(board)
            print(f"Player {player} wins! Congratulations!")
            break
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("It's a draw!")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
