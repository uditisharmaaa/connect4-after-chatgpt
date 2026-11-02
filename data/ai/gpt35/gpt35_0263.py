import os
import random

# Constants for the game configuration
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
MIN_PLAYERS = 2
MAX_PLAYERS = 5
WIN_COUNT = 4
PLAYERS_CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    # Create a 2D board filled with whitespace characters
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    columns = len(board[0])
    # Print column headers (A, B, C, ...)
    header = "  " + "   ".join([chr(ord('A') + i) for i in range(columns)])
    print(header)
    # Print the board with the borders
    border_line = "+" + "---+" * columns
    for row in range(len(board)):
        print(border_line)
        row_line = "|"
        for col in range(columns):
            row_line += " " + board[row][col] + " |"
        print(row_line)
    print(border_line)

def is_valid_column_input(user_input, columns):
    # Validate the input is a single uppercase letter within board range
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col_idx = ord(user_input) - ord('A')
    if not 0 <= col_idx < columns:
        return False
    return True

def column_is_full(board, col_idx):
    # If the top row in that column is occupied, column is full
    return board[0][col_idx] != " "

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available space in the column
    for row in reversed(range(len(board))):
        if board[row][col_idx] == " ":
            board[row][col_idx] = checker
            return row, col_idx
    # If no space found (should not happen if caller checks full columns)
    return None

def check_win(board, checker, last_pos):
    row, col = last_pos
    rows = len(board)
    columns = len(board[0])
    
    # Directions: horizontal, vertical, and two diagonals
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]

    for dr, dc in directions:
        count = 1
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < columns and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_COUNT:
            return True
    return False

def check_draw(board):
    # Draw if no empty cells in top row
    return all(cell != " " for cell in board[0])

def main():
    # Setup game parameters for 2 players and 6x7 board
    rows = ROWS
    columns = COLUMNS
    num_players = 2
    players = PLAYERS_CHECKERS[:num_players]

    board = create_board(rows, columns)
    current_player_idx = random.randint(0, num_players -1)

    while True:
        clear_screen()
        print_board(board)
        current_player = players[current_player_idx]
        prompt = f"Player {current_player}, please enter a column: "

        while True:
            user_input = input(prompt).upper()
            if not is_valid_column_input(user_input, columns):
                # Invalid input, ask again
                continue
            col_idx = ord(user_input) - ord('A')
            if column_is_full(board, col_idx):
                # According to assignment, player loses turn if the column full
                break
            else:
                # Place checker validly
                placement = place_checker(board, col_idx, current_player)
                break
        
        # If column was full, player loses turn, so no checker placed, just advance turn
        if column_is_full(board, col_idx):
            # Advance turn to next player
            current_player_idx = (current_player_idx + 1) % num_players
            continue

        # Check win condition
        if check_win(board, current_player, placement):
            clear_screen()
            print_board(board)
            print(f"Player {current_player} won!")
            break

        # Check draw condition
        if check_draw(board):
            clear_screen()
            print_board(board)
            print("Game is a draw!")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % num_players

if __name__ == "__main__":
    main()
