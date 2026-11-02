import os
import random
import string

# === CONSTANTS ===
ROWS = 6
COLUMNS = 7           # Can be up to 26
MAX_PLAYERS = 5
NUM_PLAYERS = 2       # Set number of players: 2-5
PLAYER_TOKENS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# === FUNCTIONS ===

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the board in required format."""
    clear_screen()
    col_labels = "  " + "   ".join(string.ascii_uppercase[:len(board[0])])
    print(col_labels)
    print("+" + "---+" * len(board[0]))
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * len(board[0]))

def get_valid_input(board):
    """Ask current player for valid input and return the column index."""
    columns = len(board[0])
    valid_letters = string.ascii_uppercase[:columns]
    while True:
        move = input().strip().upper()
        if len(move) != 1 or move not in valid_letters:
            print(f"Invalid input. Please enter a column letter ({valid_letters[0]}-{valid_letters[-1]}):")
            continue
        col = ord(move) - ord('A')
        # Check if the column is not full
        if board[0][col] != " ":
            print(f"Column {move} is full. You lose your turn!")
            return None
        return col

def drop_checker(board, col, checker):
    """Place the checker in the lowest available spot in the chosen column."""
    for row in reversed(board):
        if row[col] == " ":
            row[col] = checker
            return board.index(row), col  # row number, col number
    return None  # Should not reach here if input checking is correct

def is_winning_move(board, row, col, checker):
    """Check if putting checker at (row, col) creates a win."""
    directions = [
        (0, 1),   # horizontal right
        (1, 0),   # vertical down
        (1, 1),   # diagonal down-right
        (1, -1),  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        for step in [1, -1]:
            rr, cc = row, col
            while True:
                rr += dr * step
                cc += dc * step
                if (0 <= rr < len(board) and 0 <= cc < len(board[0]) and
                    board[rr][cc] == checker):
                    count += 1
                    if count == 4:
                        return True
                else:
                    break
    return False

def is_draw(board):
    """Check if the board is full (no spaces in first row)."""
    return all(cell != " " for cell in board[0])

def main():
    # Set up initial state
    board = create_board(ROWS, COLUMNS)
    player_tokens = PLAYER_TOKENS
    player_names = [f"Player {tok}" for tok in player_tokens]
    current_player = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"{player_names[current_player]}, you start.")

    while True:
        player_token = player_tokens[current_player]
        print_board(board)
        print(f"{player_names[current_player]}, please enter a column:")

        col = get_valid_input(board)
        if col is None:
            # Column was full; lose turn
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        row, col = drop_checker(board, col, player_token)

        if is_winning_move(board, row, col, player_token):
            print_board(board)
            print(f"{player_names[current_player]} won!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Next player's turn
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
