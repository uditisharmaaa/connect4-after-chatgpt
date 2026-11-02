import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def valid_input(col):
    return col.isalpha() and len(col) == 1 and ord(col.upper()) - ord('A') < COLS

def place_checker(board, col, player):
    for row in reversed(board):
        if row[ord(col.upper()) - ord('A')] == ' ':
            row[ord(col.upper()) - ord('A')] = player
            return True
    return False

def check_win(board, player):
    def check_direction(r, c, dr, dc):
        count = 0
        for _ in range(4):
            if (0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player):
                count += 1
            else:
                break
            r += dr
            c += dc
        return count == 4

    for r in range(ROWS):
        for c in range(COLS):
            if (check_direction(r, c, 1, 0) or   # Vertical
                check_direction(r, c, 0, 1) or   # Horizontal
                check_direction(r, c, 1, 1) or   # Diagonal \
                check_direction(r, c, 1, -1)):    # Diagonal /
                return True
    return False

def check_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def connect4():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not valid_input(col):
            print("Invalid input. Please enter a valid column.")
            continue
        
        if not place_checker(board, col, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    connect4()
