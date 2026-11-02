import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')  # Clears the console for a fresh view of the board
    print("  " + "   ".join(chr(65 + i) for i in range(COLUMNS)))  # Column labels (A, B, C, ...)
    print("+" + "---+" * COLUMNS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLUMNS)

def get_player_move(player):
    while True:
        move = input(f"Player {player}, please enter a column: ").upper()
        if len(move) == 1 and move in [chr(65 + i) for i in range(COLUMNS)]:
            return ord(move) - 65  # Convert A-G to 0-6
        else:
            print("Invalid input, please enter a letter from A to G.")

def place_checker(board, column, player):
    for row in reversed(board):  # Check from the bottom row upwards
        if row[column] == " ":
            row[column] = player
            return True
    return False  # The column is full

def check_win(board, player):
    # Check horizontal, vertical, and diagonal for winning condition
    for row in range(ROWS):
        for col in range(COLUMNS):
            if (board[row][col] == player):
                if (col + 3 < COLUMNS and
                        board[row][col + 1] == player and
                        board[row][col + 2] == player and
                        board[row][col + 3] == player):
                    return True
                if (row + 3 < ROWS and
                        board[row + 1][col] == player and
                        board[row + 2][col] == player and
                        board[row + 3][col] == player):
                    return True
                if (row + 3 < ROWS and col + 3 < COLUMNS and
                        board[row + 1][col + 1] == player and
                        board[row + 2][col + 2] == player and
                        board[row + 3][col + 3] == player):
                    return True
                if (row - 3 >= 0 and col + 3 < COLUMNS and
                        board[row - 1][col + 1] == player and
                        board[row - 2][col + 2] == player and
                        board[row - 3][col + 3] == player):
                    return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player_idx = random.randint(0, 1)  # Randomly select the first player
    total_players = len(PLAYERS)

    while True:
        print_board(board)
        current_player = PLAYERS[current_player_idx]
        
        column = get_player_move(current_player)
        if not place_checker(board, column, current_player):
            print("Column is full, try again.")
            continue  # Don't switch player; they get another turn

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player_idx = (current_player_idx + 1) % total_players  # Switch to the next player

if __name__ == "__main__":
    main()
