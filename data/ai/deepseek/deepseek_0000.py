import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board."""
    # Print column headers
    headers = [chr(ord('A') + i) for i in range(BOARD_COLS)]
    print('  ' + '   '.join(headers))
    
    # Print board rows
    for row in board:
        print('+' + '---+' * BOARD_COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    print('+' + '---+' * BOARD_COLS)

def is_valid_move(board, col):
    """Check if a move is valid."""
    if col < 0 or col >= BOARD_COLS:
        return False
    return board[0][col] == ' '

def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if the current move results in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= 4:
            return True
    return False

def is_board_full(board):
    """Check if the board is full."""
    return all(cell != ' ' for cell in board[0])

def get_column_input(player):
    """Get and validate column input from the player."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").strip().upper()
            if not col_input or ord(col_input) < ord('A') or ord(col_input) > ord('A') + BOARD_COLS - 1:
                print(f"Invalid column. Please enter a letter from A to {chr(ord('A') + BOARD_COLS - 1)}.")
                continue
            return ord(col_input) - ord('A')
        except EOFError:
            print("Invalid input. Please try again.")
        except:
            print("Invalid input. Please try again.")

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear')

def main():
    """Main game loop."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    clear_screen()
    print_board(board)
    
    while True:
        col = get_column_input(current_player)
        
        if not is_valid_move(board, col):
            print("Column is full or invalid. Try another column.")
            continue
        
        row = place_checker(board, col, current_player)
        clear_screen()
        print_board(board)
        
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_board_full(board):
            print("Game over. It's a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
