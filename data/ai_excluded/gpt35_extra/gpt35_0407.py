import os
import random
import string

# Constants for the game settings
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']
REQUIRED_TO_WIN = 4

def clear_screen():
    os.system('clear')

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    columns = len(board[0])
    rows = len(board)
    # Print column headers
    headers = '  ' + '   '.join(string.ascii_uppercase[:columns])
    print(headers)
    # Print the board rows with separators
    line = '+' + '---+' * columns
    for r in range(rows):
        print(line)
        row_cells = '| ' + ' | '.join(board[r]) + ' |'
        print(row_cells)
    print(line)

def is_valid_column_choice(choice, columns):
    if len(choice) != 1:
        return False
    if choice not in string.ascii_uppercase[:columns]:
        return False
    return True

def get_column_index(letter):
    return ord(letter) - ord('A')

def place_checker(board, column, checker):
    # Places the checker at the lowest empty row in the column
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = checker
            return row, column
    # Column full, return None
    return None

def board_full(board):
    # Returns True if no empty space in any row of any column
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def check_win(board, last_row, last_col, checker):
    # Check all directions from last placed checker for 4 continuous checkers
    directions = [
        (0, 1),   # Horizontal right
        (1, 0),   # Vertical down
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    rows = len(board)
    cols = len(board[0])

    for dr, dc in directions:
        count = 1  # Count includes last placed checker

        # Check forward direction
        r, c = last_row + dr, last_col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check backward direction
        r, c = last_row - dr, last_col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc

        if count >= REQUIRED_TO_WIN:
            return True

    return False

def main():
    board = create_board(ROWS, COLUMNS)
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randrange(PLAYERS)

    print_board(board)

    while True:
        player = players[current_player_idx]
        prompt = f"Player {player}, please enter a column: "
        col_choice = input(prompt).strip().upper()

        # Validate input - must be a letter in range and not empty
        while not is_valid_column_choice(col_choice, COLUMNS):
            print(f"Invalid column input. Please enter a letter between A and {chr(ord('A') + COLUMNS - 1)}.")
            col_choice = input(prompt).strip().upper()

        col_index = get_column_index(col_choice)

        # Try to place checker in chosen column
        position = place_checker(board, col_index, player)
        if position is None:
            # Column full, player loses turn
            current_player_idx = (current_player_idx + 1) % PLAYERS
            print_board(board)
            continue

        last_row, last_col = position
        
        print_board(board)

        # Check win
        if check_win(board, last_row, last_col, player):
            print(f"Player {player} won!")
            break

        # Check draw
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player's turn
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    main()
