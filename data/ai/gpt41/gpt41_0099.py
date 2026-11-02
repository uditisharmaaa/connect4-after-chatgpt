import os
import random
import string

# ----- CONSTANT GLOBAL VARIABLES -----
BOARD_ROWS = 6             # Number of rows
BOARD_COLS = 7             # Number of columns (max 26)
NUM_PLAYERS = 2            # Number of players (2 to 5)

CHECkERS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players

COLUMN_LABELS = list(string.ascii_uppercase)[:BOARD_COLS]
EMPTY = " "

def clear_screen():
    os.system('clear')  # For Linux/Unix
    # os.system('cls')  # For Windows

def create_board(rows, cols):
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    # Print column headers
    print("  " + "   ".join(COLUMN_LABELS))
    print("+" + "---+" * BOARD_COLS)
    for row in board:
        # Print row content
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * BOARD_COLS)

def get_valid_input(board, col_labels):
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1 or user_input not in col_labels:
            print(f"Invalid input. Please enter a column letter from {col_labels[0]} to {col_labels[-1]}: ")
            continue
        col_idx = col_labels.index(user_input)
        # Check for full column
        if board[0][col_idx] != EMPTY:
            print(f"Column {user_input} is full! You lose your turn.")
            return None  # signify lost turn due to full column
        return col_idx

def place_checker(board, col_idx, checker):
    # Place checker in the lowest available row of the column
    for row_idx in reversed(range(BOARD_ROWS)):
        if board[row_idx][col_idx] == EMPTY:
            board[row_idx][col_idx] = checker
            return row_idx, col_idx  # Return the row and column where placed
    return None  # Shouldn't get here if validity is checked

def is_winner(board, last_row, last_col, checker):
    # Check all directions from (last_row, last_col)
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal (down-right)
        (1, -1),  # Diagonal (down-left)
    ]
    for dr, dc in directions:
        count = 1  # Start with current checker
        # Check in the positive direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_draw(board):
    # If the top row has no empty space, it's a draw
    return all(cell != EMPTY for cell in board[0])

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    # Pick player order and checkers
    players = CHECkERS[:NUM_PLAYERS]
    player_names = [f"Player {players[i]}" for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS-1)
    clear_screen()
    print_board(board)
    print(f"{player_names[current_player_idx]}, you start!\n")

    while True:
        player_char = players[current_player_idx]
        print(f"{player_names[current_player_idx]}, please enter a column:")
        col_idx = get_valid_input(board, COLUMN_LABELS)
        if col_idx is None:
            # Invalid due to full column: skip turn
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS
            clear_screen()
            print_board(board)
            continue
        # Place checker and update board
        last_row, last_col = place_checker(board, col_idx, player_char)
        clear_screen()
        print_board(board)
        # Check for win
        if is_winner(board, last_row, last_col, player_char):
            print(f"{player_names[current_player_idx]} won!")
            break
        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break
        # Next player's turn
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
