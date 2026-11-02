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
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False

def check_win(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != ' ':
                if check_direction(board, r, c):
                    return board[r][c]
    return None

def check_direction(board, row, col):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 0
        for i in range(4):
            r, c = row + dr * i, col + dc * i
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == board[row][col]:
                count += 1
            else:
                break
        if count == 4:
            return True
    return False

def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    print_board(board)

    while True:
        col_input = input(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}): ").upper()
        if len(col_input) != 1 or col_input < 'A' or col_input >= chr(65 + COLS):
            continue
        
        col = ord(col_input) - 65
        if not drop_checker(board, col, current_player):
            continue
        
        print_board(board)

        if (winner := check_win(board)):
            print(f"Player {winner} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % len(PLAYERS)]

if __name__ == "__main__":
    main()
