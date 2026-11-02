import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Initialize the game board with empty spaces."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    # Print column headers
    print('  ' + '   '.join([chr(65 + i) for i in range(BOARD_COLS)]))
    
    # Print each row with borders
    for row in board:
        print('+' + '---+' * BOARD_COLS)
        print('|' + '|'.join([f' {cell} ' for cell in row]) + '|')
    
    # Print bottom border
    print('+' + '---+' * BOARD_COLS)

def get_valid_column(board):
    """Get a valid column input from the player."""
    while True:
        column = input(f"Player {current_player}, please enter a column: ").upper()
        if len(column) != 1 or column < 'A' or column > chr(65 + BOARD_COLS - 1):
            print(f"Invalid column. Please enter a letter from A to {chr(65 + BOARD_COLS - 1)}.")
            continue
        
        col_index = ord(column) - ord('A')
        if board[0][col_index] != ' ':
            print("Column is full. Please choose another column.")
            continue
        
        return col_index

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False

def check_win(board, player):
    """Check if the player has won."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == player:
                for dr, dc in directions:
                    count = 1
                    for step in range(1, 4):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == player:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_draw(board):
    """Check if the game is a draw (board is full)."""
    return all(cell != ' ' for cell in board[0])

def main():
    global current_player
    board = initialize_board()
    current_player = random.choice(PLAYERS[:NUM_PLAYERS])
    print_board(board)
    
    while True:
        col = get_valid_column(board)
        place_checker(board, col, current_player)
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("Game ended in a draw.")
            break
        
        # Switch to next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
