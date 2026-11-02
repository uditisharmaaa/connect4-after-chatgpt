import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_CONDITION = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Print column headers (A, B, C, ...)
    headers = "  " + "   ".join(chr(ord('A') + i) for i in range(len(board[0])))
    print(headers)
    # Print the board rows with separator lines
    for r in range(len(board)):
        line = "+"
        for _ in range(len(board[0])):
            line += "---+"
        # Print row content
        print(line)
        row_content = "|"
        for c in range(len(board[0])):
            row_content += " " + board[r][c] + " |"
        print(row_content)
    # Print bottom line of the board
    line = "+"
    for _ in range(len(board[0])):
        line += "---+"
    print(line)

def is_valid_column(input_str, board):
    # Check if input_str is a single uppercase letter in board columns
    if len(input_str) != 1:
        return False
    c = ord(input_str)
    start = ord('A')
    end = start + len(board[0]) - 1
    if c < start or c > end:
        return False
    # Check if column is not full
    col_index = c - start
    if board[0][col_index] != " ":
        # Top cell is occupied means column is full
        return False
    return True

def place_checker(board, col_letter, checker):
    col = ord(col_letter) - ord('A')
    # Place checker from bottom row upward
    for row in reversed(range(len(board))):
        if board[row][col] == " ":
            board[row][col] = checker
            return row, col
    # Full column, should not happen if checked before
    return None

def check_win(board, checker, row, col):
    # Check directions: horizontal, vertical, diagonal /
    # and diagonal \
    directions = [
        (0, 1),  # horizontal right
        (1, 0),  # vertical down
        (1, 1),  # diagonal down-right
        (1, -1)  # diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # count the placed checker itself
        # check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_CONDITION:
            return True
    return False

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        checker = players[current_player_index]
        prompt = f"Player {checker}, please enter a column: "
        
        while True:
            move = input(prompt).strip().upper()
            if not is_valid_column(move, board):
                # Check if input is a valid uppercase letter even if column full
                if len(move) == 1 and 'A' <= move <= chr(ord('A') + COLS - 1):
                    # Valid column but full → lose turn
                    print(f"Column {move} is full. Turn lost.")
                    move = None
                    break
                else:
                    print("Invalid input. Try again.")
                continue
            else:
                break
        
        if move is None:
            # Turn lost, advance to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            print_board(board)
            continue
        
        # Place checker
        row, col = place_checker(board, move, checker)
        
        print_board(board)
        
        # Check win
        if check_win(board, checker, row, col):
            print(f"Player {checker} won!")
            break
        
        # Check draw
        if board_full(board):
            print("Game is a draw!")
            break
        
        # Next player's turn
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
