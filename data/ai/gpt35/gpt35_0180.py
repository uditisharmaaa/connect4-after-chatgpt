import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows=ROWS, columns=COLUMNS):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(columns)]
    print('  ' + '   '.join(labels))
    row_sep = '+' + ('---+' * columns)
    for row in board:
        print(row_sep)
        line = '|'
        for cell in row:
            line += f' {cell} |'
        print(line)
    print(row_sep)

def get_valid_column_input(board, player):
    columns = len(board[0])
    valid_cols = [chr(ord('A') + i) for i in range(columns)]
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(move) != 1:
            print("Invalid input. Enter a single uppercase letter corresponding to a column.")
            continue
        if move not in valid_cols:
            print("Invalid column letter. Please enter a letter within the board range.")
            continue
        col_idx = ord(move) - ord('A')
        if board[0][col_idx] != ' ':
            # If top cell is not empty, column is full
            print("Column is full. You lose your turn.")
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker at lowest available row in the column
    for row_idx in range(len(board)-1, -1, -1):
        if board[row_idx][col_idx] == ' ':
            board[row_idx][col_idx] = checker
            return row_idx, col_idx
    # Column full
    return None

def check_win(board, checker, last_row, last_col):
    rows = len(board)
    cols = len(board[0])

    def count_in_direction(r, c, dr, dc):
        count = 0
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        return count

    # Check all directions from last placed checker:
    # Horizontal (0,1), Vertical (1,0), Diag1 (1,1), Diag2 (1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1  # Count self
        count += count_in_direction(last_row, last_col, dr, dc)
        count += count_in_direction(last_row, last_col, -dr, -dc)
        if count >= WIN_LENGTH:
            return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Randomly selected Player {players[current_player_idx]} to start.")

    while True:
        checker = players[current_player_idx]
        col_idx = get_valid_column_input(board, checker)
        if col_idx is None:
            # player loses turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        res = place_checker(board, col_idx, checker)
        if res is None:
            # Should not happen as column full is checked before
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            print_board(board)
            continue

        row_idx, col_idx = res

        print_board(board)

        if check_win(board, checker, row_idx, col_idx):
            print(f"Player {checker} won!")
            break

        if board_full(board):
            print("Game is a draw.")
            break

        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
