import os
import random
import string

# Constants
BOARD_WIDTH = 7
BOARD_HEIGHT = 6
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board(width, height):
    """Create a 2D list filled with spaces to represent the game board."""
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_board(board):
    """Print the current state of the game board."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers
    print('  A', end='')
    for i in range(1, BOARD_WIDTH):
        print(f' {string.ascii_uppercase[i]}', end='')
    print()
    
    # Print rows
    for row in board:
        print('+---' * BOARD_WIDTH + '+')
        print('|', end='')
        for cell in row:
            print(f' {cell} |', end='')
        print()
    print('+---' * BOARD_WIDTH + '+')

def get_player_move(player):
    """Get the player's column choice and validate it."""
    while True:
        move = input(f"Player {player}, please enter a column: ")
        if move.upper() in string.ascii_uppercase[:BOARD_WIDTH]:
            return string.ascii_uppercase.index(move.upper())
        else:
            print("Invalid input. Please try again.")

def place_checker(board, player, column):
    """Place the player's checker in the chosen column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = player
            break
    else:
        print("Column is full. You lose your turn.")
        return False
    return True

def check_win(board, player):
    """Check if the player has won the game."""
    # Check horizontal wins
    for row in board:
        for i in range(BOARD_WIDTH - 3):
            if row[i] == player and row[i + 1] == player and row[i + 2] == player and row[i + 3] == player:
                return True
    
    # Check vertical wins
    for col in range(BOARD_WIDTH):
        for i in range(BOARD_HEIGHT - 3):
            if board[i][col] == player and board[i + 1][col] == player and board[i + 2][col] == player and board[i + 3][col] == player:
                return True
    
    # Check diagonal wins (top-left to bottom-right)
    for row in range(BOARD_HEIGHT - 3):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and board[row + 3][col + 3] == player:
                return True
    
    # Check diagonal wins (bottom-left to top-right)
    for row in range(3, BOARD_HEIGHT):
        for col in range(BOARD_WIDTH - 3):
            if board[row][col] == player and board[row - 1][col + 1] == player and board[row - 2][col + 2] == player and board[row - 3][col + 3] == player:
                return True
    
    return False

def check_draw(board):
    """Check if the game is a draw."""
    return all(cell!= ' ' for row in board for cell in row)

def main():
    # Create the game board
    board = create_board(BOARD_WIDTH, BOARD_HEIGHT)
    
    # Randomly select the first player
    players = CHECKERS[:NUM_PLAYERS]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Main game loop
    while True:
        # Print the current state of the board
        print_board(board)
        
        # Get the current player's move
        current_player = players[current_player_index]
        column = get_player_move(current_player)
        
        # Place the player's checker
        if place_checker(board, current_player, column):
            # Check for a win
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            
            # Check for a draw
            if check_draw(board):
                print_board(board)
                print("It's a draw!")
                break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
