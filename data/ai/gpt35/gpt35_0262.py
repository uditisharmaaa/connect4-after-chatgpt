import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
WINNING_COUNT = 4
COLUMN_LABELS = [chr(ord('A') + i) for i in range(COLUMNS)]

def clear_screen():
    os.system('clear')

def create_board():
    # Create a ROWS x COLUMNS board filled with spaces
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    # Print column labels
    print('  ' + '   '.join(COLUMN_LABELS))
    # Print the board
    for row in board:
        print('+' + '---+' * COLUMNS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * COLUMNS)

def get_valid_column_input(current_player):
    while True:
        inp = input(f"Player {CHECKERS[current_player]}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            print("Invalid input. Please enter a single letter corresponding to a column.")
            continue
        if inp not in COLUMN_LABELS:
            print(f"Invalid column. Please enter a letter between A and {COLUMN_LABELS[-1]}.")
            continue
        col = COLUMN_LABELS.index(inp)
        return col

def place_checker(board, col, checker):
    # Place the checker into the lowest available spot in the column
    for row_idx in range(ROWS-1, -1, -1):
        if board[row_idx][col] == ' ':
            board[row_idx][col] = checker
            return row_idx, col
    # Column full
    return None

def check_winner(board, row, col, checker):
    # Directions to check: horiz, vert, diag /
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1
        # Check forward direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check backward direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WINNING_COUNT:
            return True
    return False

def board_full(board):
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        # Get column from player
        col = get_valid_column_input(current_player)
        placed = place_checker(board, col, CHECKERS[current_player])
        if placed is None:
            # Column full, turn lost
            print(f"Column {COLUMN_LABELS[col]} is full. Player {CHECKERS[current_player]} loses the turn.")
            input("Press Enter to continue...")
        else:
            row, col = placed
            print_board(board)
            # Check if current player won
            if check_winner(board, row, col, CHECKERS[current_player]):
                print(f"Player {CHECKERS[current_player]} won!")
                break
            # Check for draw
            if board_full(board):
                print("The game is a draw!")
                break
        # Next player's turn
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
