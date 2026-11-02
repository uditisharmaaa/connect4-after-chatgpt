import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYERS = 2  # Can be between 2 and 5
CHECKERS = ["X", "O", "V", "H", "M"]  # Up to 5 players
WIN_STREAK = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    # Print column headers
    header = "  "
    for c in range(columns):
        header += " " + chr(ord('A') + c) + "  "
    print(header)
    # Print the board rows and dividers
    for row in board:
        print("+" + "---+" * columns)
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
    print("+" + "---+" * columns)

def random_first_player(num_players):
    return random.randint(0, num_players - 1)

def validate_input(user_input, columns):
    # Valid if it's a single uppercase character within the board columns
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    uc = user_input.upper()
    if 'A' <= uc < chr(ord('A') + columns):
        return True
    return False

def place_checker(board, column_index, checker):
    # Place checker at lowest empty spot in column
    # Return True if placed, False if column full
    for row in reversed(range(len(board))):
        if board[row][column_index] == " ":
            board[row][column_index] = checker
            return True, row
    return False, -1

def check_winner(board, r, c, checker):
    rows = len(board)
    cols = len(board[0])

    def count_in_direction(dr, dc):
        count = 1  # Count the last placed checker itself
        # Check positive direction
        rr, cc = r + dr, c + dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr += dr
            cc += dc
        # Check negative direction
        rr, cc = r - dr, c - dc
        while 0 <= rr < rows and 0 <= cc < cols and board[rr][cc] == checker:
            count += 1
            rr -= dr
            cc -= dc
        return count

    # Directions: horizontal(0,1), vertical(1,0), diag1(1,1), diag2(1,-1)
    directions = [(0,1), (1,0), (1,1), (1,-1)]
    for dr, dc in directions:
        if count_in_direction(dr, dc) >= WIN_STREAK:
            return True
    return False

def board_full(board):
    # If any top row cell is empty, board not full
    top_row = 0
    for c in range(len(board[0])):
        if board[top_row][c] == " ":
            return False
    return True

def main():
    # Initialize board and players
    if COLUMNS > MAX_COLUMNS:
        raise ValueError(f"Maximum columns allowed is {MAX_COLUMNS}")
    if PLAYERS < 2 or PLAYERS > 5:
        raise ValueError("Number of players must be between 2 and 5")

    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_index = random_first_player(PLAYERS)

    print_board(board)

    while True:
        current_checker = players[current_player_index]
        prompt = f"Player {current_checker}, please enter a column: "
        valid_input = False
        while not valid_input:
            user_input = input(prompt).strip().upper()
            if not validate_input(user_input, COLUMNS):
                # Invalid input, keep asking
                continue
            col_index = ord(user_input) - ord('A')
            # Try to place checker
            placed, placed_row = place_checker(board, col_index, current_checker)
            if not placed:
                # Column full: player loses turn
                break
            valid_input = True

        if valid_input:
            print_board(board)
            # Check win
            if check_winner(board, placed_row, col_index, current_checker):
                print(f"Player {current_checker} won!")
                break
            # Check draw
            if board_full(board):
                print("The game is a draw.")
                break
        else:
            # Turn lost due to full column (no placement)
            print_board(board)

        # Next player
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
