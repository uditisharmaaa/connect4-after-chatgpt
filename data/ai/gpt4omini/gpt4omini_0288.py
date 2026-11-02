import os
import random

# Constants for game dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clear the console for every new board print
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Print column letters
    print("+" + "---+" * COLS)  # Print top border
    for row in board:
        print("| " + " | ".join(row) + " |")  # Print each row
        print("+" + "---+" * COLS)  # Print row border

def drop_checker(board, column, checker):
    for row in reversed(board):  # Start from the bottom row
        if row[column] == " ":
            row[column] = checker
            return True
    return False

def is_winner(board, checker):
    # Check horizontal, vertical and diagonal wins
    for row in range(ROWS):
        for col in range(COLS):
            if (col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)) or
                row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)) or
                row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4)) or
                row <= ROWS - 4 and col >= 3 and all(board[row + i][col - i] == checker for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(board[0][col] != " " for col in range(COLS))

def get_valid_column(player):
    while True:
        column_input = input(f"Player {player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(column_input) == 1 and 'A' <= column_input <= chr(65 + COLS - 1):
            column = ord(column_input) - 65  # Convert letter to column index
            return column
        print("Invalid input. Please try again.")

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    game_over = False

    print_board(board)

    while not game_over:
        current_player = PLAYERS[current_player_index]
        column = get_valid_column(current_player)

        if drop_checker(board, column, current_player):
            print_board(board)
            if is_winner(board, current_player):
                print(f"Player {current_player} won!")
                game_over = True
            elif is_draw(board):
                print("The game is a draw!")
                game_over = True
            else:
                current_player_index = (current_player_index + 1) % len(PLAYERS)
        else:
            print("Column is full! Try a different column.")

if __name__ == "__main__":
    main()
