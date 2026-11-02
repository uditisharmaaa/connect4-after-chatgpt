import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Print column headers
    header = '  ' + '   '.join(chr(65 + i) for i in range(COLS)) + '  '
    print(header)
    
    # Print each row with borders
    for row in board:
        border = '+' + ('---+' * COLS)
        print(border)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print bottom border
    print('+' + ('---+' * COLS))

def is_valid_move(board, col):
    """Check if a column is a valid move (not full)."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == ' '

def get_player_move(player, board):
    """Prompt the player for a move and validate it."""
    while True:
        move = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter (A-G).")
            continue
        
        col = ord(move) - ord('A')
        if is_valid_move(board, col):
            return col
        else:
            print("Column is full or invalid. Please choose another column.")

def place_checker(board, col, checker):
    """Place the checker in the lowest available row of the column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Search in one direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Search in opposite direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # Check if there are 4 in a row
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for cell in board[0])

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    players = CHECKERS[:PLAYERS]
    current_player_idx = random.randint(0, PLAYERS - 1)
    
    while True:
        os.system('clear')
        print_board(board)
        current_player = players[current_player_idx]
        col = get_player_move(current_player, board)
        row = place_checker(board, col, current_player)
        
        if check_win(board, row, col, current_player):
            os.system('clear')
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            break
        
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
