import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board():
    """Create and return an empty game board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the game board."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column letters
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    
    # Print the board
    for row in board:
        print('+---+' * COLS)
        print('|' + '|'.join(f' {cell} ' for cell in row) + '|')
    
    # Print the bottom border
    print('+---+' * COLS)

def get_valid_move(current_player, board):
    """Get a valid column from the player."""
    while True:
        try:
            col = input(f"Player {current_player}, please enter a column: ").upper()
            if len(col) != 1 or col < 'A' or col >= chr(65 + COLS):
                print(f"Invalid column. Please enter a letter from A to {chr(64 + COLS)}")
                continue
            
            col_idx = ord(col) - ord('A')
            if board[0][col_idx] != ' ':
                print("Column is full. Please choose another column.")
                continue
            
            return col_idx
        except EOFError:
            print("\nExiting game.")
            exit()
        except:
            print(f"Invalid input. Please enter a letter from A to {chr(64 + COLS)}")

def place_checker(board, col_idx, checker):
    """Place the checker in the specified column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return (row, col_idx)
    return None

def check_win(board, row, col):
    """Check if the last move resulted in a win."""
    checker = board[row][col]
    
    # Directions: horizontal, vertical, diagonal down, diagonal up
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    
    for dr, dc in directions:
        count = 1
        
        # Search in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Search in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= 4:
            return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for cell in board[0])

def main():
    """Main game loop."""
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)
    
    while True:
        col_idx = get_valid_move(current_player, board)
        pos = place_checker(board, col_idx, current_player)
        print_board(board)
        
        if check_win(board, pos[0], pos[1]):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    main()
