import os
import random

COLS = 7
ROWS = 6
PLAYERS = 2

def clear_screen():
    os.system('clear')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def get_player_input(current_checker):
    while True:
        col = input(f"Player {current_checker}, please enter a column: ").upper()
        if len(col) == 1 and 'A' <= col <= chr(ord('A') + COLS - 1):
            return ord(col) - ord('A')
        print("Invalid input. Please choose a valid column between A and G.")

def place_checker(board, col, checker):
    if board[0][col] != ' ':
        print("Column is full. Turn lost.")
        return False
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return True

def check_win(board, checker):
    for r in range(ROWS):
        for c in range(COLS):
            if c + 3 < COLS and all(board[r][c+i] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and all(board[r+i][c] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and c + 3 < COLS and all(board[r+i][c+i] == checker for i in range(4)):
                return True
            if r + 3 < ROWS and c - 3 >= 0 and all(board[r+i][c-i] == checker for i in range(4)):
                return True
    return False

def check_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    checkers = ['X', 'O', 'V', 'H', 'M']
    players_checkers = checkers[:PLAYERS]
    board = create_board()
    current_player = random.randint(0, PLAYERS-1)
    print_board(board)
    
    while True:
        if place_checker(board, get_player_input(players_checkers[current_player]), players_checkers[current_player]):
            print_board(board)
            if check_win(board, players_checkers[current_player]):
                print(f"Player {players_checkers[current_player]} won!")
                break
            if check_draw(board):
                print("Game is a draw!")
                break
            current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
