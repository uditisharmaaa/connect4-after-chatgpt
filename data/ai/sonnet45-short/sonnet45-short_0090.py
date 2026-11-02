import random
import os

# Game constants - modify these to change game settings
NUM_ROWS = 6
NUM_COLS = 7
MIN_PLAYERS = 2
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']  # Symbols for up to 5 players

def create_board():
    """Create and return an empty game board (2D list)"""
    return [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

def print_board(board):
    """Display the game board with column labels"""
    os.system('clear')  # Clear the screen for a clean display
    
    # Print column labels (A-G)
    print('\n  ', end='')
    for i in range(NUM_COLS):
        print(chr(65 + i), end='   ')  # 65 is ASCII for 'A'
    print()
    
    # Print the board rows with row numbers
    for row_num in range(NUM_ROWS):
        print(f'{row_num + 1} ', end='')
        for col in range(NUM_COLS):
            print(f'|{board[row_num][col]}', end='  ')
        print('|')
        
    # Print bottom border
    print('  ' + '----' * NUM_COLS)
    print()

def get_num_players():
    """Get and validate the number of players from user input"""
    while True:
        try:
            num = int(input(f'Enter number of players ({MIN_PLAYERS}-{MAX_PLAYERS}): '))
            if MIN_PLAYERS <= num <= MAX_PLAYERS:
                return num
            else:
                print(f'Please enter a number between {MIN_PLAYERS} and {MAX_PLAYERS}.')
        except ValueError:
            print('Invalid input. Please enter a number.')

def get_column_input():
    """Get and validate column input from user (A-G)"""
    while True:
        col_input = input('Enter column (A-G) or Q to quit: ').upper().strip()
        
        # Check if player wants to quit
        if col_input == 'Q':
            return -1
        
        # Validate input is a single letter
        if len(col_input) != 1:
            print('Please enter a single letter.')
            continue
        
        # Convert letter to column index (A=0, B=1, etc.)
        col_index = ord(col_input) - 65  # 65 is ASCII for 'A'
        
        # Check if column is within valid range
        if 0 <= col_index < NUM_COLS:
            return col_index
        else:
            print(f'Please enter a letter between A and {chr(65 + NUM_COLS - 1)}.')

def drop_piece(board, col, symbol):
    """
    Drop a piece into the specified column.
    Returns the row where piece landed, or -1 if column is full.
    """
    # Start from bottom row and work upward
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = symbol
            return row
    return -1  # Column is full

def check_win(board, row, col, symbol):
    """
    Check if the last move at (row, col) created a winning condition.
    Checks horizontal, vertical, and both diagonals.
    """
    
    # Helper function to count consecutive pieces in a direction
    def count_direction(row_dir, col_dir):
        count = 0
        current_row = row + row_dir
        current_col = col + col_dir
        
        # Keep counting while within bounds and matching symbol
        while (0 <= current_row < NUM_ROWS and 
               0 <= current_col < NUM_COLS and 
               board[current_row][current_col] == symbol):
            count += 1
            current_row += row_dir
            current_col += col_dir
        
        return count
    
    # Check horizontal (left + right + 1 for the placed piece)
    horizontal = count_direction(0, -1) + count_direction(0, 1) + 1
    
    # Check vertical (down + up + 1)
    vertical = count_direction(1, 0) + count_direction(-1, 0) + 1
    
    # Check diagonal (bottom-left to top-right)
    diagonal1 = count_direction(1, -1) + count_direction(-1, 1) + 1
    
    # Check diagonal (top-left to bottom-right)
    diagonal2 = count_direction(-1, -1) + count_direction(1, 1) + 1
    
    # Win condition: 4 or more in a row in any direction
    return max(horizontal, vertical, diagonal1, diagonal2) >= 4

def is_board_full(board):
    """Check if the board is completely full (draw condition)"""
    # Check if top row has any empty spaces
    for col in range(NUM_COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop"""
    # Game setup
    board = create_board()
    num_players = get_num_players()
    
    # Set up player symbols based on number of players
    players = PLAYER_SYMBOLS[:num_players]
    
    # Randomly select starting player
    current_player_index = random.randint(0, num_players - 1)
    
    print(f'\nPlayer symbols: {", ".join(players)}')
    print(f'Player {players[current_player_index]} goes first!')
    input('Press Enter to start...')
    
    # Main game loop
    while True:
        # Display current board state
        print_board(board)
        
        # Get current player's symbol
        current_symbol = players[current_player_index]
        print(f"Player {current_symbol}'s turn")
        
        # Get column choice from player
        col = get_column_input()
        
        # Check if player wants to quit
        if col == -1:
            print('Game ended by player.')
            break
        
        # Try to drop piece in selected column
        row = drop_piece(board, col, current_symbol)
        
        # Check if column was full
        if row == -1:
            print('That column is full! Try another column.')
            input('Press Enter to continue...')
            continue
        
        # Check for win condition
        if check_win(board, row, col, current_symbol):
            print_board(board)
            print(f'🎉 Player {current_symbol} wins! 🎉')
            break
        
        # Check for draw condition
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.")
            break
        
        # Move to next player (cycle through all players)
        current_player_index = (current_player_index + 1) % num_players

def main():
    """Main function to run the game with replay option"""
    print('=' * 40)
    print('Welcome to Connect 4!')
    print('=' * 40)
    print('Get 4 in a row horizontally, vertically,')
    print('or diagonally to win!')
    print()
    
    # Game loop with replay option
    while True:
        play_game()
        
        # Ask if players want to play again
        play_again = input('\nPlay again? (Y/N): ').upper().strip()
        if play_again != 'Y':
            print('Thanks for playing!')
            break

# Run the game when script is executed
if __name__ == '__main__':
    main()
