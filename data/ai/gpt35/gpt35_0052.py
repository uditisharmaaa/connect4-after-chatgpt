import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Support up to 5 players

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    clear_screen()
    # Print column labels
    labels = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(labels))
    # Print board rows with separators
    for row in board:
        print("+" + "---+" * cols)
        print("| " + " | ".join(row) + " |")
    print("+" + "---+" * cols)

def get_valid_column(board, player_checker):
    cols = len(board[0])
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            # Input length invalid
            continue
        col_idx = ord(inp) - ord('A')
        if not (0 <= col_idx < cols):
            # Out of board columns
            continue
        # Check if column is full
        if board[0][col_idx] != " ":
            # Column full, player loses turn for this input
            return None
        return col_idx

def place_checker(board, col_idx, checker):
    rows = len(board)
    # From bottom to top find first empty space in col_idx
    for r in reversed(range(rows)):
        if board[r][col_idx] == " ":
            board[r][col_idx] = checker
            return r, col_idx
    # Column full (should be handled before calling this)
    return None

def check_win(board, last_r, last_c, checker):
    rows = len(board)
    cols = len(board[0])
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = last_r + dr, last_c + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_r - dr, last_c - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def board_full(board):
    return all(board[0][c] != " " for c in range(len(board[0])))

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_idx]
        col_idx = get_valid_column(board, checker)
        if col_idx is None:
            # Column full, turn lost as per specification
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue
        pos = place_checker(board, col_idx, checker)
        print_board(board)
        if pos is None:
            # Should not happen, since we checked column full earlier
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue
        r, c = pos
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if board_full(board):
            print("The game is a draw!")
            break
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
