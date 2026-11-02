import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O"]  # Can be extended up to 5 players with "X", "O", "V", "H", "M"

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

def is_winner(board, player):
    # Check horizontal, vertical and diagonal
    for row in range(ROWS):
        for col in range(COLS):
            if (col + 3 < COLS and all(board[row][col + i] == player for i in range(4))) or \
               (row + 3 < ROWS and all(board[row + i][col] == player for i in range(4))) or \
               (row + 3 < ROWS and col + 3 < COLS and all(board[row + i][col + i] == player for i in range(4))) or \
               (row + 3 < ROWS and col - 3 >= 0 and all(board[row + i][col - i] == player for i in range(4))):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    game_over = False

    print_board(board)
    
    while not game_over:
        col_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        
        if col_input not in {chr(65 + i) for i in range(COLS)}:
            print("Invalid input. Please enter a valid column letter.")
            continue

        col = ord(col_input) - 65
        
        if not drop_checker(board, col, current_player):
            print("Column is full! Try a different column.")
            continue

        print_board(board)

        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            game_over = True
            break

        if is_draw(board):
            print("The game is a draw!")
            game_over = True
            break

        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
