import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O']  # Adjust this list for more players if needed

def clear_screen():
    """Clears the terminal screen."""
    os.system('clear')

def create_board():
    """Creates and returns an empty Connect 4 board."""
    return [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the current state of the board."""
    clear_screen()
    # Print column labels
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))
    print("+---" * COLUMNS + "+")
    
    # Print the contents of the board
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_valid_input(player):
    """Gets a valid column input from the player."""
    while True:
        column = input(f"Player {player}, please enter a column (A-G): ").strip().upper()
        if len(column) == 1 and column >= 'A' and column <= chr(65 + COLUMNS - 1):
            return ord(column) - 65  # Convert to index
        print("Invalid input. Please enter a valid column (A-G).")

def place_checker(board, column, player):
    """Places a checker for the current player in the specified column."""
    for row in reversed(board):  # Start from the bottom of the column
        if row[column] == ' ':
            row[column] = player
            return True  # Successfully placed the checker
    return False  # Column is full

def check_winner(board, player):
    """Checks if the specified player has won the game."""
    # Check horizontal, vertical, and diagonal positions
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c] == player:
                # Check horizontal
                if c + 3 < COLUMNS and all(board[r][c + i] == player for i in range(4)):
                    return True
                # Check vertical
                if r + 3 < ROWS and all(board[r + i][c] == player for i in range(4)):
                    return True
                # Check diagonal (down-right)
                if r + 3 < ROWS and c + 3 < COLUMNS and all(board[r + i][c + i] == player for i in range(4)):
                    return True
                # Check diagonal (down-left)
                if r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == player for i in range(4)):
                    return True
    return False

def check_draw(board):
    """Checks if the board is full and there is no winner."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = create_board()
    random_player = random.choice(PLAYERS)  # Randomly choose the first player
    current_player_index = PLAYERS.index(random_player)
    
    print_board(board)

    while True:
        current_player = PLAYERS[current_player_index]
        column = get_valid_input(current_player)
        
        if place_checker(board, column, current_player):
            print_board(board)
            
            if check_winner(board, current_player):
                print(f"Player {current_player} won!")
                break
            elif check_draw(board):
                print("The game is a draw!")
                break
            
            current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch to the next player
        else:
            print("Column is full, try again!")

if __name__ == "__main__":
    main()
