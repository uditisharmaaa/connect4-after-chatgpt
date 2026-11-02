import random
import os

# Constants
ROWS = 6
COLS = 7
PLAYERS = ["X", "O", "V", "H", "M"]

def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def drop_checker(board, col, player):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = player
            return True
    return False

def is_winner(board, player):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if all(row[col + i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Check diagonal (down-right)
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Check diagonal (down-left)
    for col in range(3, COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col - i] == player for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(all(cell != " " for cell in row) for row in board)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    total_players = len(PLAYERS)

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column:")
        while True:
            col_input = input().upper()
            if len(col_input) == 1 and col_input.isalpha() and 65 <= ord(col_input) < 65 + COLS:
                col = ord(col_input) - 65
                if drop_checker(board, col, current_player):
                    break
                else:
                    print("Column is full. Try again.")
            else:
                print("Invalid input. Please enter a valid column letter (A-G).")

        print_board(board)

        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
            
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % total_players]

if __name__ == "__main__":
    main()
