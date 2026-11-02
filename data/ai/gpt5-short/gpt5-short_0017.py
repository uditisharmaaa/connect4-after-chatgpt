import random
import os

# Constants (change NUM_PLAYERS from 2 to 5 as needed)
ROWS = 6
COLS = 7
COL_LABELS = "ABCDEFG"
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']
NUM_PLAYERS = 2  # set between 2 and 5

def clear_screen():
    # As requested, use clear
    os.system('clear')

def make_board():
    return [['.' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board, active_players):
    print("  " + " ".join(COL_LABELS))
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(board[r][c])
        print(str(ROWS - r) + " " + " ".join(row))
    print("\nPlayers this game: " + " ".join(active_players))

def get_col_index(choice):
    choice = choice.strip().upper()
    if len(choice) != 1:
        return -1
    if choice in COL_LABELS:
        return COL_LABELS.index(choice)
    return -1

def drop_piece(board, col, symbol):
    # Drop from bottom up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '.':
            board[r][col] = symbol
            return r, col
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win_from(board, r, c, sym):
    # Check 4 directions: horiz, vert, diag down-right, diag up-right
    directions = [(0,1), (1,0), (1,1), (-1,1)]
    for dr, dc in directions:
        count = 1
        # one way
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc) and board[rr][cc] == sym:
            count += 1
            rr += dr
            cc += dc
        # other way
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc) and board[rr][cc] == sym:
            count += 1
            rr -= dr
            cc -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == '.':
                return False
    return True

def main():
    # Validate NUM_PLAYERS
    n = NUM_PLAYERS
    if n < 2:
        n = 2
    if n > 5:
        n = 5
    active_players = PLAYER_SYMBOLS[:n]

    board = make_board()

    # Pick random starting player
    current_index = random.randrange(len(active_players))

    winner = None

    while True:
        clear_screen()
        print_board(board, active_players)
        current_player = active_players[current_index]
        # Ask for input
        while True:
            choice = input(f"Player {current_player}, choose column (A-G): ")
            col = get_col_index(choice)
            if col == -1:
                print("Invalid input. Enter a letter A-G.")
                continue
            # Try to drop
            result = drop_piece(board, col, current_player)
            if result is None:
                print("Column is full. Pick another column.")
                continue
            else:
                last_r, last_c = result
                break

        # Check win
        if check_win_from(board, last_r, last_c, current_player):
            winner = current_player
            clear_screen()
            print_board(board, active_players)
            print(f"Player {winner} wins!")
            break

        # Check draw
        if is_draw(board):
            clear_screen()
            print_board(board, active_players)
            print("It's a draw!")
            break

        # Next player's turn
        current_index = (current_index + 1) % len(active_players)

    print("Game over.")

if __name__ == "__main__":
    main()
