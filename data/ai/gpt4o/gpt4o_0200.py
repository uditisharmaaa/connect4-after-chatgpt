import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_COLUMNS = 26
PLAYER_COUNT = 2
PLAYER_MARKERS = ['X', 'O', 'V', 'H', 'M'][:PLAYER_COUNT]

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def create_board():
    """Create a game board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Display the game board."""
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def check_column_valid(column, board):
    """Check if the column is valid and has space."""
    if column < 0 or column >= COLUMNS:
        return False
    return board[0][column] == ' '

def get_available_row(column, board):
    """Find the first available row in the specified column."""
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == ' ':
            return r
    return None

def make_move(column, player, board):
    """Place the player's marker in the board."""
    available_row = get_available_row(column, board)
    if available_row is not None:
        board[available_row][column] = PLAYER_MARKERS[player]
        return True
    return False

def check_win(player, board):
    """Check the board for a win condition."""
    marker = PLAYER_MARKERS[player]

    # Check horizontal win
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == marker for i in range(4)):
                return True

    # Check vertical win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == marker for i in range(4)):
                return True

    # Check diagonal win (/ direction)
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if all(board[r-i][c+i] == marker for i in range(4)):
                return True

    # Check diagonal win (\ direction)
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if all(board[r+i][c+i] == marker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != ' ' for c in range(COLUMNS))

def main():
    board = create_board()
    random_player = random.randint(0, PLAYER_COUNT - 1)
    current_player = random_player
    
    while True:
        print_board(board)
        print(f"Player {PLAYER_MARKERS[current_player]}, please enter a column:")
        
        valid_move = False
        while not valid_move:
            try:
                move = input().strip().upper()
                if len(move) != 1 or move < 'A' or move >= chr(ord('A') + COLUMNS):
                    raise ValueError("Invalid column.")
                
                column = ord(move) - ord('A')
                if not check_column_valid(column, board):
                    raise ValueError("Column full or invalid.")
                
                valid_move = make_move(column, current_player, board)
            except ValueError as e:
                print(e)
                continue
        
        if check_win(current_player, board):
            print_board(board)
            print(f"Player {PLAYER_MARKERS[current_player]} won!")
            break
        
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % PLAYER_COUNT

if __name__ == "__main__":
    main()
