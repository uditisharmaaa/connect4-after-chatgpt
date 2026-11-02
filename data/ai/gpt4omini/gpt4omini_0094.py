import os
import random

# Constants for board dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]  # Up to 5 players

# Initialize the board with empty spaces
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column Labels A-G
    print("+" + "---+" * COLS)  # Top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Row content
        print("+" + "---+" * COLS)  # Row border

# Check for a win condition
def check_win(board, player):
    # Check horizontal, vertical, and diagonal
    # Horizontal check
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True
            
    # Vertical check
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Diagonal check (bottom-left to top-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Diagonal check (top-left to bottom-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

# Find the lowest empty row in a column
def find_lowest_empty_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

# Main game loop
def main():
    board = create_board()
    current_player_index = random.randint(0, 1)  # Randomly select starting player
    game_over = False

    while not game_over:
        print_board(board)
        player = PLAYERS[current_player_index]
        col_input = input(f"Player {player}, please enter a column (A-G): ").upper()

        if col_input in [chr(65 + i) for i in range(COLS)]:  # Check valid column input
            col = ord(col_input) - 65
            row = find_lowest_empty_row(board, col)

            if row != -1:
                board[row][col] = player  # Place checker
                if check_win(board, player):
                    print_board(board)
                    print(f"Player {player} won!")
                    game_over = True
                elif check_draw(board):
                    print_board(board)
                    print("The game is a draw!")
                    game_over = True
                else:
                    current_player_index = (current_player_index + 1) % len(PLAYERS)  # Switch turns
            else:
                print("Column is full. Choose another column.")
        else:
            print("Invalid input. Please enter a letter from A to G.")

if __name__ == "__main__":
    main()
