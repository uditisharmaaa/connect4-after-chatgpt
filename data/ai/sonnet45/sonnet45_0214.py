import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board."""
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLS):
            row.append(" ")
        board.append(row)
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print rows with dividers
    for row in range(ROWS):
        # Print top border
        print("+---" * COLS + "+")
        # Print row content
        print("|", end="")
        for col in range(COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    # Print bottom border
    print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if a move is valid (column exists and is not full)."""
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column is empty
    return board[0][col] == " "


def place_checker(board, col, symbol):
    """Place a checker in the specified column."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1


def check_win(board, symbol):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row][col + i] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row + i][col + i] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            count = 0
            for i in range(WIN_LENGTH):
                if board[row - i][col + i] == symbol:
                    count += 1
            if count == WIN_LENGTH:
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_move(board, player_symbol):
    """Get a valid move from the player."""
    while True:
        move = input("Player " + player_symbol + ", please enter a column: ")
        
        # Check if input is a single character
        if len(move) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Convert to uppercase
        move = move.upper()
        
        # Check if input is a letter
        if not move.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(move) - 65
        
        # Check if column is valid and not full
        if col < 0 or col >= COLS:
            print("Invalid column. Please choose a column between A and " + chr(65 + COLS - 1) + ".")
            continue
        
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def main():
    """Main game loop."""
    # Create the board
    board = create_board()
    
    # Get player symbols
    players = []
    for i in range(NUM_PLAYERS):
        players.append(SYMBOLS[i])
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get current player symbol
        current_symbol = players[current_player_index]
        
        # Get player move
        col = get_player_move(board, current_symbol)
        
        # Place checker
        place_checker(board, col, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_symbol):
            print("Player " + current_symbol + " won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
    

if __name__ == "__main__":
    main()
