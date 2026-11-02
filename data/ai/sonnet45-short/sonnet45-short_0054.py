import random
import os

# Constants
ROWS = 6
COLS = 7
COLUMN_LABELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
NUM_PLAYERS = 2  # Change this to 2, 3, 4, or 5
PLAYER_SYMBOLS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create an empty game board"""
    board = []
    for row in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Display the game board"""
    os.system('clear')
    print('\n  Connect 4\n')
    
    # Print column labels
    print('  ', end='')
    for label in COLUMN_LABELS:
        print(label + ' ', end='')
    print()
    
    # Print top border
    print(' +' + '-' * (COLS * 2 + 1) + '+')
    
    # Print rows
    for row in board:
        print(' | ', end='')
        for cell in row:
            print(cell + ' ', end='')
        print('|')
    
    # Print bottom border
    print(' +' + '-' * (COLS * 2 + 1) + '+')
    print()

def get_column_input(player):
    """Get and validate column input from player"""
    while True:
        choice = input(f"Player {player}, enter column (A-G): ").upper()
        
        if len(choice) != 1:
            print("Please enter a single letter.")
            continue
            
        if choice not in COLUMN_LABELS:
            print("Invalid column. Choose A-G.")
            continue
            
        return COLUMN_LABELS.index(choice)

def drop_piece(board, col, player):
    """Drop a piece in the specified column, return row number or -1 if full"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return row
    return -1

def check_win(board, row, col, player):
    """Check if the last move resulted in a win"""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r = start_row
    c = start_col
    while r < ROWS and c < COLS:
        if board[r][c] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r = start_row
    c = start_col
    while r >= 0 and c < COLS:
        if board[r][c] == player:
            count += 1
            if count >= 4:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full"""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def play_game():
    """Main game loop"""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print(f"\nStarting with Player {players[current_player_index]}!\n")
    input("Press Enter to start...")
    
    while True:
        current_player = players[current_player_index]
        print_board(board)
        
        # Get valid column
        while True:
            col = get_column_input(current_player)
            row = drop_piece(board, col, current_player)
            
            if row == -1:
                print("That column is full! Choose another.")
            else:
                break
        
        # Check for win
        if check_win(board, row, col, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins! 🎉\n")
            break
        
        # Check for draw
        if is_board_full(board):
            print_board(board)
            print("It's a draw! The board is full.\n")
            break
        
        # Next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

# Start the game
if __name__ == "__main__":
    print("=" * 30)
    print("  WELCOME TO CONNECT 4!")
    print("=" * 30)
    print(f"\nNumber of players: {NUM_PLAYERS}")
    print("Players: ", end='')
    for i in range(NUM_PLAYERS):
        print(PLAYER_SYMBOLS[i], end=' ')
    print("\n\nGet 4 in a row to win!")
    print("(horizontal, vertical, or diagonal)\n")
    
    play_game()
    
    # Play again option
    while True:
        again = input("Play again? (y/n): ").lower()
        if again == 'y':
            play_game()
        elif again == 'n':
            print("\nThanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'")
