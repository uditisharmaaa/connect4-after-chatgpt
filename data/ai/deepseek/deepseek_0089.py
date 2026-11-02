import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with the specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen before printing the board
    os.system('clear')
    
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join(chr(ord('A') + i) for i in range(BOARD_COLS)))
    
    # Print each row with borders
    border = '+' + ('---+' * BOARD_COLS)
    for row in board:
        print(border)
        print('| ' + ' | '.join(cell for cell in row) + ' |')
    print(border)

def is_valid_column(col):
    """Check if the column input is valid (uppercase A-G)."""
    return len(col) == 1 and 'A' <= col <= chr(ord('A') + BOARD_COLS - 1)

def get_player_move(player):
    """Ask the player for a valid move."""
    while True:
        col = input(f"Player {player}, please enter a column: ").upper()
        if is_valid_column(col):
            return ord(col) - ord('A')
        print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + BOARD_COLS - 1)}")

def place_checker(board, col, player):
    """Place the player's checker in the lowest available row of the column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the player has won by getting 4 in a row horizontally, vertically or diagonally."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, vertical, diagonal down-right, diagonal down-left
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + dr * i, col + dc * i
                        if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    print(f"Player {current_player} starts the game.")
    print_board(board)
    
    while True:
        col = get_player_move(current_player)
        if not place_checker(board, col, current_player):
            print(f"Column {chr(ord('A') + col)} is full. Lost turn.")
            continue
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
