import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M'][:PLAYERS]

def initialize_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with column labels."""
    # Print column headers
    header = '  ' + '   '.join([chr(65 + i) for i in range(COLS)]) + '  '
    print(header)
    
    # Print the board rows
    for row in board:
        line = '+---' * COLS + '+'
        print(line)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print the bottom border
    print('+---' * COLS + '+')

def get_valid_column_input(player, board):
    """Ask the player for a column input until it's valid."""
    while True:
        try:
            col_input = input(f"Player {player}, please enter a column: ").upper()
            if len(col_input) != 1 or not col_input.isalpha():
                print("Invalid input. Please enter a single letter (A-" + chr(65 + COLS - 1) + ").")
                continue
            col = ord(col_input) - 65
            if col < 0 or col >= COLS:
                print(f"Column must be between A and {chr(65 + COLS - 1)}.")
                continue
            if board[0][col] != ' ':
                print("This column is full. Please choose another column.")
                continue
            return col
        except EOFError:
            print("\nExiting the game.")
            exit()
        except Exception as e:
            print(f"Invalid input. Error: {e}")

def place_checker(board, col, symbol):
    """Place the checker in the specified column at the lowest available row."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [
        (0, 1),  # horizontal
        (1, 0),   # vertical
        (1, 1),   # diagonal down
        (1, -1)   # diagonal up
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        # If count >= 4, win
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)
    game_over = False
    
    while not game_over:
        os.system('clear')
        print_board(board)
        symbol = PLAYER_SYMBOLS[current_player]
        col = get_valid_column_input(symbol, board)
        row = place_checker(board, col, symbol)
        
        if check_win(board, row, col, symbol):
            os.system('clear')
            print_board(board)
            print(f"Player {symbol} won!")
            game_over = True
        elif is_draw(board):
            os.system('clear')
            print_board(board)
            print("The game is a draw!")
            game_over = True
        else:
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
