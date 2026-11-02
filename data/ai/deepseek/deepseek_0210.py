import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]  # Selected based on NUM_PLAYERS

def initialize_board():
    """
    Initialize an empty game board with dimensions BOARD_ROWS x BOARD_COLS.
    The board is filled with spaces representing empty slots.
    """
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """
    Print the current state of the board with column headers (A, B, C, ...).
    """
    # Print column headers
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(BOARD_COLS)))
    
    # Print each row with borders
    for row in board:
        print('+---+' * BOARD_COLS)
        print('| ' + ' | '.join(row) + ' |')
    print('+---+' * BOARD_COLS)

def is_valid_move(board, col):
    """
    Check if a move in the specified column is valid (i.e., the column is not full).
    """
    return board[0][col] == ' '

def place_checker(board, col, checker):
    """
    Place the checker in the specified column. The checker falls to the lowest available row.
    Returns the row where the checker was placed.
    """
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1  # Should not happen if is_valid_move is checked first

def check_win(board, row, col, checker):
    """
    Check if placing the checker at (row, col) results in a win.
    A win is 4 checkers in a row horizontally, vertically, or diagonally.
    """
    directions = [
        (0, 1),   # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1  # Current checker is already placed
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Win if 4 or more in a row
        if count >= 4:
            return True
    return False

def check_draw(board):
    """
    Check if the game is a draw (i.e., all columns are full).
    """
    for col in range(BOARD_COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(current_player, board):
    """
    Prompt the current player to enter a column and validate the input.
    Repeats until a valid move is entered.
    """
    while True:
        try:
            move = input(f"Player {current_player}, please enter a column: ").strip().upper()
            if len(move) != 1 or not move.isalpha():
                print("Invalid input. Please enter a single letter.")
                continue
            col = ord(move) - ord('A')
            if col < 0 or col >= BOARD_COLS:
                print(f"Column must be between A and {chr(ord('A') + BOARD_COLS - 1)}.")
                continue
            if not is_valid_move(board, col):
                print("That column is full. Please choose another.")
                continue
            return col
        except KeyboardInterrupt:
            print("\nGame exited.")
            exit()
        except:
            print("Invalid input. Please try again.")

def play_game():
    """
    Main game loop. Initializes the board, selects a random starting player,
    and alternates turns until a player wins or the game is a draw.
    """
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        os.system('clear')
        print_board(board)
        print(f"Player {current_player}'s turn.")
        
        col = get_player_move(current_player, board)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        # Switch to next player
        player_index = PLAYERS.index(current_player)
        current_player = PLAYERS[(player_index + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
