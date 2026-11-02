import os
import random

# --------- Constants (can be changed for larger boards, more players) -------------
NUM_ROWS = 6           # Board height
NUM_COLS = 7           # Board width (max 26)
NUM_PLAYERS = 2        # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]   # Checker symbols per player, in order
TO_WIN = 4             # Number of checkers in a row needed to win

# ---------- Functions ------------

def clear_screen():
    # Clear the terminal screen (compatible with Linux/Mac)
    os.system('clear')

def create_board(rows, cols):
    # Creates a board as a 2D list with spaces
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Prints column letters
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(len(board[0]))])
    print(header)
    # Prints horizontal separator
    print("+" + "---+" * len(board[0]))
    # Prints each row of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(row))

def valid_columns(board):
    # Returns a list of column indices where at least space is empty (not filled)
    return [col for col in range(len(board[0])) if board[0][col] == ' ']

def get_player_input(board, player_checker):
    # Continuously prompt user until valid, return valid column index
    available_cols = valid_columns(board)
    col_letters = [chr(ord('A') + idx) for idx in available_cols]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if len(user_input) != 1 or user_input < 'A' or user_input > chr(ord('A') + len(board[0])-1):
            print("Invalid input: Please enter a valid column letter.")
            continue
        col = ord(user_input) - ord('A')
        if col not in available_cols:
            # Column full or not available
            print("Column is full or not available. You lose your turn.")
            return None
        return col

def drop_checker(board, col, checker):
    # Attempt to place the checker in the first available space from bottom up
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col # Return where checker went
    # Should not reach here, but just in case, return None
    return None

def check_win(board, checker):
    # Check horizontal, vertical, and both diagonals for a winning streak for this checker
    rows = len(board)
    cols = len(board[0])

    # Directions: (delta_row, delta_col)
    directions = [
        (0, 1),    # Horizontal right
        (1, 0),    # Vertical down
        (1, 1),    # Diagonal down-right
        (1, -1),   # Diagonal down-left
    ]

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != checker:
                continue
            # At each position, check all directions
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while (0 <= rr < rows and 0 <= cc < cols and
                       board[rr][cc] == checker):
                    count += 1
                    if count == TO_WIN:
                        return True
                    rr += dr
                    cc += dc

    return False

def is_draw(board):
    # If there's no empty space in the board, it's a draw
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def random_first_player(player_count):
    # Returns an integer index between 0 and player_count-1
    return random.randint(0, player_count - 1)

# ------------- Main game logic ------------

def main():
    # Set checkers for number of players
    player_checkers = CHECKERS[:NUM_PLAYERS]
    board = create_board(NUM_ROWS, NUM_COLS)

    # Pick random player
    current_player = random_first_player(NUM_PLAYERS)

    while True:
        clear_screen()
        print_board(board)
        checker = player_checkers[current_player]

        # Turn prompt & input validation
        col = get_player_input(board, checker)
        if col is None:
            # Invalid/filled column: player's turn is lost, move to next player
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Place checker in selected column
        row_col = drop_checker(board, col, checker)
        if row_col is None:
            # Should not occur since we already validated
            print("Unexpected error: Could not place checker.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue

        # Win check
        if check_win(board, checker):
            clear_screen()
            print_board(board)
            print(f"Player {checker} won!")
            break

        # Draw check
        if is_draw(board):
            clear_screen()
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
