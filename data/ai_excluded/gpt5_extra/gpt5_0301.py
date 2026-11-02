import os, random, string, sys

# Constants (you may change these for testing, final submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # between 2 and 5
TOKENS = ["X", "O", "V", "H", "M"]

# Derived
PLAYERS = TOKENS[:NUM_PLAYERS]
LETTERS = list(string.ascii_uppercase[:COLS])

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear()
    # Header
    header = "  " + "   ".join(LETTERS)
    print(header)
    print("+---" * COLS + "+")
    for r in range(ROWS):
        row = "| " + " | ".join(board[r]) + " |"
        print(row)
        print("+---" * COLS + "+")
        
def valid_input(s):
    return len(s) == 1 and s.isalpha() and s.upper() in LETTERS

def drop_checker(board, col_idx, token):
    # place from bottom up
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == " ":
            board[r][col_idx] = token
            return r, col_idx
    return None  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_winner(board, r, c):
    token = board[r][c]
    if token == " ":
        return False
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            nr, nc = r, c
            while True:
                nr += dr * step
                nc += dc * step
                if in_bounds(nr, nc) and board[nr][nc] == token:
                    count += 1
                    if count >= 4:
                        return True
                else:
                    break
    return False

def is_draw(board):
    # draw if top row is full
    return all(board[0][c] != " " for c in range(COLS))

def main():
    if COLS > 26 or COLS < 1 or ROWS < 1 or not (2 <= NUM_PLAYERS <= 5):
        print("Invalid configuration.")
        sys.exit(1)

    board = create_board(ROWS, COLS)
    current_idx = random.randrange(NUM_PLAYERS)
    print_board(board)

    while True:
        player = PLAYERS[current_idx]
        # Input loop for validation only (invalid inputs do not lose turn)
        while True:
            print(f"Player {player}, please enter a column:")
            user_in = input().strip()
            if not valid_input(user_in):
                print_board(board)
                print("Invalid input. Please enter a valid column letter.")
                continue
            col = user_in.upper()
            col_idx = LETTERS.index(col)
            placed = drop_checker(board, col_idx, player)
            print_board(board)
            if placed is None:
                print(f"Column {col} is full. You lose this turn.")
                break  # lose turn
            r, c = placed
            if check_winner(board, r, c):
                print(f"Player {player} won!")
                return
            if is_draw(board):
                print("It's a draw!")
                return
            # successful move; next player's turn
            current_idx = (current_idx + 1) % NUM_PLAYERS
            break
        else:
            # not used
            pass
        # If column was full, still advance to next player
        if placed is None:
            current_idx = (current_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
