import os
import random
import string

# --- Constants ---
ROWS = 6            # Number of rows
COLUMNS = 7         # Number of columns
NUMBER_OF_PLAYERS = 2    # Number of players (2-5)
CHECKERS = ['X', 'O', 'V', 'H', 'M']

# --- Board Creation and Print ---

def create_board(rows, cols):
    """
    Create a board with the specified dimensions, filled with spaces.
    """
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    """
    Clear the terminal screen using the 'clear' command (Unix/Linux).
    """
    os.system('clear')

def print_board(board):
    """
    Print the Connect 4 board with column headers.
    """
    cols = len(board[0])
    header = '  ' + '   '.join(string.ascii_uppercase[:cols])
    separator = '+' + ('---+' * cols)
    print(header)
    print(separator)
    for row in board:
        row_str = '| ' + ' | '.join(row) + ' |'
        print(row_str)
        print(separator)

# --- Game Logic ---

def get_valid_input(board, num_columns, player_checker):
    """
    Prompt the user until a valid column letter is entered.
    """
    valid_letters = string.ascii_uppercase[:num_columns]
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip()
        if len(user_input) != 1 or user_input.upper() not in valid_letters:
            print(f"Invalid input. Please enter a column letter ({valid_letters}).")
            continue
        col_index = valid_letters.index(user_input.upper())
        # Check if column is full
        if board[0][col_index] != ' ':
            print("Column is full! You lose your turn.")
            return None  # Lose the turn
        return col_index

def place_checker(board, col, checker):
    """
    Place a checker in the specified column for the player.
    Returns the row where the checker was placed.
    """
    for i in reversed(range(len(board))):
        if board[i][col] == ' ':
            board[i][col] = checker
            return i
    return None  # Should not happen due to validation

def check_winner(board, row, col, checker_to_check, win_length=4):
    """
    Check if placing a checker at (row, col) caused a win.

    Returns True if the player has won; False otherwise.
    """
    directions = [
        (0, 1),   # Horizontal (right)
        (1, 0),   # Vertical (down)
        (1, 1),   # Diagonal down-right
        (1, -1),  # Diagonal down-left
    ]
    for dr, dc in directions:
        count = 1  # Current cell
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker_to_check:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker_to_check:
            count += 1
            r -= dr
            c -= dc
        if count >= win_length:
            return True
    return False

def is_draw(board):
    """
    Check if the board is full (game is a draw).
    """
    return all(cell != ' ' for cell in board[0])

def main():
    # Use global constants; But they can be changed at the top for other board sizes/players
    rows = ROWS
    cols = COLUMNS
    num_players = NUMBER_OF_PLAYERS
    player_checkers = CHECKERS[:num_players]

    # --- Game Setup ---
    board = create_board(rows, cols)
    current_player = random.randint(0, num_players - 1)

    # --- Game Loop ---
    while True:
        clear_screen()
        print_board(board)
        player_checker = player_checkers[current_player]

        col = get_valid_input(board, cols, player_checker)
        if col is None:
            # Column full -> player loses turn
            current_player = (current_player + 1) % num_players
            continue

        row = place_checker(board, col, player_checker)
        clear_screen()
        print_board(board)
        
        if check_winner(board, row, col, player_checker):
            print(f"Player {player_checker} won!")
            break
        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % num_players

if __name__ == "__main__":
    main()
