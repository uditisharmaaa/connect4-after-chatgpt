import os
import random

# Constants for players
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players
NUM_PLAYERS = 3  # Change this to between 2 and 5

# Board dimensions
ROWS = 6
COLUMNS = 7

def create_board():
    """Create an empty Connect 4 board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    print("  A B C D E F G")
    for row in board:
        print('|' + '|'.join(row) + '|')

def is_valid_column(column, board):
    """Check if the selected column is valid for a move."""
    return 0 <= column < COLUMNS and board[0][column] == ' '

def get_next_open_row(column, board):
    """Find the next open row in the selected column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][column] == ' ':
            return row
    return None

def make_move(column, player, board):
    """Place the player's token in the selected column."""
    row = get_next_open_row(column, board)
    if row is not None:
        board[row][column] = player

def check_winner(player, board):
    """Check if the given player has won in the current board."""
    # Check horizontal locations for win
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    # Check vertical locations for win
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check positively sloped diagonals
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check negatively sloped diagonals
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the board is full and the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLUMNS))

def clear_console():
    """Clear the system console."""
    os.system('clear')

def get_player_input(player, board):
    """Get a valid column input from the player."""
    while True:
        try:
            column = input(f"Player {player}'s turn. Choose a column (A-G): ").strip().upper()
            if column in "ABCDEFG":
                col_index = ord(column) - ord('A')
                if is_valid_column(col_index, board):
                    return col_index
            print("Invalid input. Please try again.")
        except Exception as e:
            print(f"Error occurred: {e}. Please try again.")

def main():
    board = create_board()
    # Randomize players' turn order
    players = PLAYERS[:NUM_PLAYERS]
    random.shuffle(players)
    
    clear_console()
    current_winner = None
    turn = 0
    
    while not current_winner and not is_draw(board):
        current_player = players[turn % NUM_PLAYERS]
        print_board(board)
        column = get_player_input(current_player, board)
        make_move(column, current_player, board)
        
        if check_winner(current_player, board):
            current_winner = current_player
        
        turn += 1

    clear_console()
    print_board(board)
    if current_winner:
        print(f"Player {current_winner} wins!")
    else:
        print("The game is a draw!")

if __name__ == "__main__":
    main()
