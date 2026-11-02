import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create and return an empty game board"""
    board = []
    for _ in range(ROWS):
        board.append([' '] * COLS)
    return board

def print_board(board):
    """Print the current state of the board"""
    # Clear screen
    os.system('clear')
    
    # Print column letters
    print('  ', end='')
    for col in range(COLS):
        print(f' {chr(65 + col)}  ', end='')
    print()
    
    # Print board rows
    for row in range(ROWS):
        # Print top border
        print(' +' + '---+' * COLS)
        
        # Print row content
        print(' |', end='')
        for col in range(COLS):
            print(f' {board[row][col]} |', end='')
        print()
    
    # Print bottom border
    print(' +' + '---+' * COLS)

def is_valid_move(board, col):
    """Check if a move is valid"""
    return 0 <= col < COLS and board[0][col] == ' '

def make_move(board, col, checker):
    """Place checker in the specified column"""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won"""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col + 1] == checker and 
                board[row][col + 2] == checker and 
                board[row][col + 3] == checker):
                return True
    
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row + 1][col] == checker and 
                board[row + 2][col] == checker and 
                board[row + 3][col] == checker):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row + 1][col + 1] == checker and 
                board[row + 2][col + 2] == checker and 
                board[row + 3][col + 3] == checker):
                return True
    
    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row - 1][col + 1] == checker and 
                board[row - 2][col + 2] == checker and 
                board[row - 3][col + 3] == checker):
                return True
    
    return False

def is_board_full(board):
    """Check if the board is full (draw)"""
    for col in range(COLS):
        if board[0][col] == ' ':
            return False
    return True

def get_player_move(player, checker):
    """Get and validate player input"""
    while True:
        move = input(f"Player {checker}, please enter a column: ").upper()
        if len(move) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(move) - ord('A')
        if 0 <= col < COLS:
            return col
        else:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")

def play_game():
    """Main game loop"""
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)
    checkers = CHECKERS[:PLAYERS]
    
    print_board(board)
    
    while True:
        checker = checkers[current_player]
        col = get_player_move(current_player + 1, checker)
        
        if not is_valid_move(board, col):
            print("Column is full. Please try another column.")
            continue
            
        make_move(board, col, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            break
            
        if is_board_full(board):
            print("Game ended in a draw!")
            break
            
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
