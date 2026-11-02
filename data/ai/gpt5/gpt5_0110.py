import os
import random

# Constants (you may change ROWS, COLS, and NUM_PLAYERS for testing; submit with 6x7 and 2 players)
ROWS = 6
COLS = 7  # Maximum supported is 26
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # In order

WIN_LENGTH = 4  # Always 4 to win

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def column_labels(cols):
    labels = []
    for i in range(cols):
        # Limit to 26 columns (A-Z)
        labels.append(chr(ord('A') + i))
    return labels

def print_board(board):
    clear_screen()
    rows = len(board)
    cols = len(board[0])
    labels = column_labels(cols)

    # Header with column labels
    header = "  " + "   ".join(labels)
    print(header)
    # Top border
    print("+" + ("---+" * cols))
    # Rows
    for r in range(rows):
        row_str = "|"
        for c in range(cols):
            row_str += f" {board[r][c]} |"
        print(row_str)
        print("+" + ("---+" * cols))

def get_valid_column_input(valid_labels, current_checker):
    prompt = f"Player {current_checker}, please enter a column: "
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Invalid input. Please enter a column letter.")
            continue
        letter = user_input.upper()
        if len(letter) != 1 or not letter.isalpha():
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if letter not in valid_labels:
            print("Column out of range. Please choose a valid column letter.")
            continue
        return valid_labels.index(letter)

def drop_checker(board, col_index, checker):
    # Place the checker in the lowest available row in the given column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return None  # Column is full

def check_direction(board, start_row, start_col, d_row, d_col, checker):
    count = 0
    r, c = start_row, start_col
    rows = len(board)
    cols = len(board[0])
    while 0 <= r < rows and 0 <= c < cols:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += d_row
        c += d_col
    return False

def check_win(board, checker):
    rows = len(board)
    cols = len(board[0])

    # Horizontal check for each row
    for r in range(rows):
        if check_direction(board, r, 0, 0, 1, checker):
            return True

    # Vertical check for each column
    for c in range(cols):
        if check_direction(board, 0, c, 1, 0, checker):
            return True

    # Diagonal down-right (top-left to bottom-right)
    # Start from first row and each column, and from each row and first column
    for c in range(cols):
        if check_direction(board, 0, c, 1, 1, checker):
            return True
    for r in range(1, rows):
        if check_direction(board, r, 0, 1, 1, checker):
            return True

    # Diagonal up-right (bottom-left to top-right)
    for c in range(cols):
        if check_direction(board, rows - 1, c, -1, 1, checker):
            return True
    for r in range(rows - 2, -1, -1):
        if check_direction(board, r, 0, -1, 1, checker):
            return True

    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def next_player_index(current_index, total_players):
    return (current_index + 1) % total_players

def main():
    # Ensure COLS does not exceed 26
    cols = min(COLS, 26)
    rows = ROWS

    # Prepare players
    players = CHECKERS[:max(2, min(NUM_PLAYERS, 5))]

    # Create game board
    board = create_board(rows, cols)

    # Random starting player
    current_player = random.randint(0, len(players) - 1)

    # Show initial board
    print_board(board)

    labels = column_labels(cols)

    # Game loop
    while True:
        current_checker = players[current_player]

        # Prompt for input
        col_index = get_valid_column_input(labels, current_checker)

        # Try to drop checker
        placed_row = drop_checker(board, col_index, current_checker)
        if placed_row is None:
            # Column full: turn is invalid and lost
            print("That column is full. You lose your turn.")
            input("Press Enter to continue...")
            # Move to next player
            current_player = next_player_index(current_player, len(players))
            print_board(board)
            continue

        # After move, print updated board
        print_board(board)

        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Next player's turn
        current_player = next_player_index(current_player, len(players))

if __name__ == "__main__":
    main()
