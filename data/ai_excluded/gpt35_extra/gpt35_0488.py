import os
import random

# Constants for board dimensions and players
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    # Print the board with separators
    sep = "+" + "---+" * len(board[0])
    for row in board:
        print(sep)
        print("| " + " | ".join(row) + " |")
    print(sep)

def input_column(player_checker, board):
    columns_letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    while True:
        inp = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        # Input validation: must be one letter in the board columns
        if len(inp) != 1 or inp not in columns_letters:
            continue  # invalid input (invalid char or length), ask again
        col = ord(inp) - ord('A')
        # Check if column is full
        if board[0][col] != " ":
            # According to instructions: If full, turn is lost. Return None to indicate lost turn
            return None
        return col

def place_checker(board, col, checker):
    # Place checker to the lowest empty space in the column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Column full, should not come here if logic is correct
    return None

def check_win(board, row, col, checker):
    directions = [
        (0, 1),  # Horizontal right
        (1, 0),  # Vertical down
        (1, 1),  # Diagonal down-right
        (1, -1), # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in directions:
        count = 1
        # Check one direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check the opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def check_draw(board):
    # If no empty space in top row -> draw
    return all(cell != " " for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:NUM_PLAYERS]
    # Random first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        player_checker = players[current_player_index]

        col = input_column(player_checker, board)
        if col is None:
            # Turn lost due to full column
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        pos = place_checker(board, col, player_checker)
        print_board(board)

        if pos is None:
            # Should never happen as we check full column before
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue

        row, col_placed = pos
        if check_win(board, row, col_placed, player_checker):
            print(f"Player {player_checker} won!")
            break

        if check_draw(board):
            print("The game is a draw!")
            break

        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
