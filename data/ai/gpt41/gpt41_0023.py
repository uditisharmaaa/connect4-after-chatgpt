import os
import random
import string

# ==================== Constants and Configuration ====================

ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26  # as columns are labeled A-Z
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2  # for submission; can be changed to 2 - 5 for other scenarios

# ==================== Helper Functions ====================

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    columns = len(board[0])
    rows = len(board)
    # Print column labels
    col_labels = [string.ascii_uppercase[i] for i in range(columns)]
    print("  " + "   ".join(col_labels))
    print("+" + "---+" * columns)
    # Print each row
    for r in range(rows):
        print("|" + "   |" * columns)
        print("+", end="")
        for c in range(columns):
            print("---+", end="")
        print()
    # Print the board with checkers
    for r in range(rows):
        row_str = "|"
        for c in range(columns):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + "---+" * columns)

def get_current_board_for_print(board):
    columns = len(board[0])
    rows = len(board)
    lines = []
    # Column labels
    col_labels = [string.ascii_uppercase[i] for i in range(columns)]
    lines.append("  " + "   ".join(col_labels))
    lines.append("+" + "---+" * columns)
    # Board rows
    for r in range(rows):
        row_str = "|"
        for c in range(columns):
            row_str += f" {board[r][c]} |"
        lines.append(row_str)
        lines.append("+" + "---+" * columns)
    return "\n".join(lines)

def get_valid_columns(board):
    columns = len(board[0])
    valid_cols = []
    for col in range(columns):
        if board[0][col] == " ":
            valid_cols.append(col)
    return valid_cols

def column_input_to_index(user_input, columns):
    user_input = user_input.strip().upper()
    if len(user_input) != 1 or user_input not in string.ascii_uppercase[:columns]:
        return None
    return ord(user_input) - ord("A")

def place_checker(board, col, symbol):
    """Place the checker for the symbol in the given column. Returns the row index where placed, or None if full."""
    rows = len(board)
    for row in reversed(range(rows)):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return None  # Column full

def check_win(board, last_row, last_col, symbol):
    """Check for win after placing symbol at board[last_row][last_col]."""
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Include the last move itself
        # Check in positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def check_draw(board):
    return all(cell != " " for cell in board[0])

def switch_player(current_player, total_players):
    return (current_player + 1) % total_players

# ==================== Main Game Loop ====================

def main():
    # Game Setup
    rows = ROWS
    columns = COLUMNS
    num_players = NUM_PLAYERS
    symbols = PLAYER_SYMBOLS[:num_players]
    player_names = [f"Player {s}" for s in symbols]

    # Board initialization
    board = create_board(rows, columns)

    # Randomly select starter
    current_player = random.randint(0, num_players - 1)

    # Print initial board
    clear_screen()
    print(get_current_board_for_print(board))

    # Game loop
    while True:
        symbol = symbols[current_player]
        player_name = player_names[current_player]
        valid_columns = get_valid_columns(board)
        print(f"{player_name} ({symbol}), please enter a column:")
        # Input loop
        user_col = None
        while True:
            move = input().strip()
            col_index = column_input_to_index(move, columns)
            # Check for invalid input (not a column label)
            if col_index is None:
                print("Invalid input. Please enter a valid column letter (e.g. A, B, ...).")
                continue
            # Check if column is filled
            if board[0][col_index] != " ":
                print("Column is full! You lose your turn.")
                col_index = None
                break  # Lose turn
            user_col = col_index
            break

        clear_screen()
        # If valid input and not a filled column, place checker and check win/draw
        if user_col is not None:
            row_index = place_checker(board, user_col, symbol)
            print(get_current_board_for_print(board))
            if check_win(board, row_index, user_col, symbol):
                print(f"{player_name} won!")
                return
            if check_draw(board):
                print("Game is a draw!")
                return
        else:
            print(get_current_board_for_print(board))
            # Column was full, do not place and lose turn

        # Next player
        current_player = switch_player(current_player, num_players)

if __name__ == "__main__":
    main()
