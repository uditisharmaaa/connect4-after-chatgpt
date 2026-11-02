import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def initialize_board():
    """Create and return an empty board with ROWS x COLS dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    # Clear the screen
    os.system('clear')
    
    # Print column letters
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLS]
    print('  ' + '   '.join(letters))
    
    # Print each row with borders
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---+' * COLS)

def get_player_input(player):
    """Get and validate player input for column choice."""
    while True:
        try:
            col = input(f"Player {player}, please enter a column: ").upper()
            if len(col) != 1 or col not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:COLS]:
                print(f"Please enter a letter from A to {'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[COLS-1]}")
                continue
            return ord(col) - ord('A')  # Convert letter to column index
        except EOFError:
            exit()
        except:
            print("Invalid input!")

def place_checker(board, col, player):
    """Place the player's checker in the specified column."""
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return True
    return False  # Column is full

def check_win(board, player):
    """Check if the player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row+i][col] == player for i in range(4)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if all(board[row+i][col-i] == player for i in range(4)):
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    """Main game loop."""
    board = initialize_board()
    players = PLAYERS[:NUM_PLAYERS]
    current_player = random.choice(players)
    
    while True:
        print_board(board)
        col = get_player_input(current_player)
        
        if not place_checker(board, col, current_player):
            print("Column is full! Player loses turn.")
            input("Press Enter to continue...")
        
        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = players[(players.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    play_game()
