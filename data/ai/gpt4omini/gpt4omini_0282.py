import random
import os

# Constants for the board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # supporting up to 5 players

def create_board():
    # Create a board initialized with empty spaces
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    # Clear the screen (Linux/Unix)
    os.system('clear')  # You may need to change this for Windows users to 'cls'
    
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    
    # Print the board rows
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column, board):
    # Check if the input is a valid column
    if column < 0 or column >= COLS or board[0][column] != " ":
        return False
    return True

def drop_checker(board, column, checker):
    # Place the checker in the selected column
    for row in reversed(range(ROWS)):
        if board[row][column] == " ":
            board[row][column] = checker
            return True
    return False

def check_winner(board, checker):
    # Check horizontal, vertical and diagonal for a win condition
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    # Check if the board is completely filled
    return all(board[0][col] != " " for col in range(COLS))

def main():
    board = create_board()
    current_player_index = random.randint(0, 1)  # Randomly select a starting player
    game_active = True
    
    print_board(board)
    
    while game_active:
        current_checker = PLAYERS[current_player_index]
        valid_move = False
        
        while not valid_move:
            # Prompt current player for input
            try:
                column_input = input(f"Player {current_checker}, please enter a column (A-G): ").strip().upper()
                column = ord(column_input) - 65  # Convert letter to index
                if is_valid_input(column, board):
                    drop_checker(board, column, current_checker)
                    valid_move = True
                else:
                    print("Invalid input. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a letter between A and G.")
        
        print_board(board)
        
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
