import os
import random

# Constants
ROWS = 6
COLS =7PLAYERS = ['X', 'O']
CHECKER_WIN_COUNT = 4

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(65 + col) for col in range(COLS)) + ' ')
    print('+' + ('---+' * COLS))
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + ('---+' * COLS))

def get_player_input(player):
    while True:
        column = input(f"Player {player}, please enter a column: ").strip().upper()
        if len(column) == 1 and 'A' <= column <= chr(64 + COLS) and board[0][ord(column) - 65] == ' ':
            return ord(column) - 65
        print("Invalid input. Please try again.")

def place_checker(board, column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == ' ':
            board[row][column] = player
            return row, column

def check_win(board, row, col, player):
    # Check horizontal
    for c in range(max(0, col - CHECKER_WIN_COUNT +1), min(col + 1, COLS - CHECKER_WIN_COUNT + 1)):
        if all(board[row][c + i] == player for i in range(CHECKER_WIN_COUNT)):
            return True
    
    # Check vertical
    for r in range(max(0, row - CHECKER_WIN_COUNT +1), min(row + 1, ROWS - CHECKER_WIN_COUNT + 1)):
        if all(board[r + i][col] == player for i in range(CHECKER_WIN_COUNT)):
            return True
    
    # Check diagonal /
    for r, c in zip(range(row - CHECKER_WIN_COUNT + 1, row + 1), range(col + CHECKER_WIN_COUNT -1, col - 1, -1)):
        if 0 <= r < ROWS and 0 <= c < COLS and all(board[r + i][c - i] == player for i in range(CHECKER_WIN_COUNT)):
            return True
    
    # Check diagonal \
    for r, c in zip(range(row - CHECKER_WIN_COUNT + 1, row + 1), range(col - CHECKER_WIN_COUNT + 1, col + 1)):
        if 0 <= r < ROWS and 0 <= c < COLS and all(board[r + i][c + i] == player for i in range(CHECKER_WIN_COUNT)):
            return True
    
    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    
    while True:
        print_board(board)
        column = get_player_input(PLAYERS[current_player_index])
        row, col = place_checker(board, column, PLAYERS[current_player_index])
        
        if check_win(board, row, col, PLAYERS[current_player_index]):
            print_board(board)
            print(f"Player {PLAYERS[current_player_index]} won!")
            break
        
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
