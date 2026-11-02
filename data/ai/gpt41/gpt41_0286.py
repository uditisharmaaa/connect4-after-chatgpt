import os
import random

# --- Constants ---
ROWS = 6          # Number of rows (can change for testing, default 6)
COLUMNS = 7       # Number of columns (can change for testing, default 7; max 26)
NUM_PLAYERS = 2   # Number of players (2..5 supported; default 2)
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols per player (up to 5)
WIN_COUNT = 4     # Number in a row to win

# --- Functions ---

def clear_screen():
    # Use 'cls' if on Windows, 'clear' on Unix
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    # Print column headers
    header = '  ' + '   '.join([chr(ord('A') + i) for i in range(cols)])
    sep = '+' + '---+' * cols
    print(header)
    print(sep)
    for row in board:
        print('|' + '|'.join(' {0} '.format(cell) for cell in row) + '|')
        print(sep)

def get_valid_column_input(board, cols):
    valid_inputs = [chr(ord('A') + i) for i in range(cols)]
    while True:
        user_in = input("Please enter a column: ").strip()
        if len(user_in) != 1 or user_in not in valid_inputs:
            print("Invalid input. Please enter a letter between A and {}.".format(valid_inputs[-1]))
            continue
        col = ord(user_in) - ord('A')
        # Check if column is valid
        if board[0][col] != " ":
            print("Column {} is full. Turn is lost.".format(user_in))
            return None     # Lose turn
        return col

def place_checker(board, col, checker):
    for row in reversed(range(len(board))):  # Start bottom up
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    return None, None  # Should not happen with input checking

def check_win(board, checker, win_required):
    rows = len(board)
    cols = len(board[0])
    # Check in all directions
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while (0 <= rr < rows) and (0 <= cc < cols) and board[rr][cc] == checker:
                    count += 1
                    if count == win_required:
                        return True
                    rr += dr
                    cc += dc
    return False

def check_draw(board):
    # If no spaces left at top row, it's a draw
    return all(cell != " " for cell in board[0])

def switch_player(curr, total):
    return (curr + 1) % total

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly choose starting player
    curr_player = random.randint(0, NUM_PLAYERS - 1)
    
    clear_screen()
    print_board(board)
    print("Player {} will start!\n".format(players[curr_player]))
    
    while True:
        # Get column input for current player
        print("Player {}, ".format(players[curr_player]), end="")
        col = get_valid_column_input(board, COLUMNS)
        if col is None:  # Column full, lose turn
            curr_player = switch_player(curr_player, NUM_PLAYERS)
            clear_screen()
            print_board(board)
            continue
        # Place checker
        row, col = place_checker(board, col, players[curr_player])
        clear_screen()
        print_board(board)
        # Check for win
        if check_win(board, players[curr_player], WIN_COUNT):
            print("Player {} won!".format(players[curr_player]))
            break
        # Check draw
        if check_draw(board):
            print("It's a draw!")
            break
        # Switch turn
        curr_player = switch_player(curr_player, NUM_PLAYERS)

if __name__ == "__main__":
    main()
