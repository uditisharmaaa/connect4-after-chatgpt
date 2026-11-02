import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(ord('A') + i) for i in range(COLS)))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def check_win(board, row, col, checker):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in range(1, 4):
            r, c = row + dr * step, col + dc * step
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
            else:
                break
        for step in range(1, 4):
            r, c = row - dr * step, col - dc * step
            if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == checker:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

def is_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def play_game():
    board = create_board()
    current_player_idx = random.randint(0, PLAYERS - 1)
    print_board(board)
    
    while True:
        player_checker = CHECKERS[current_player_idx]
        column_choice = input(f"Player {player_checker}, please enter a column: ").upper()
        
        if column_choice not in [chr(ord('A') + i) for i in range(COLS)]:
            print("Invalid input! Choose a valid column.")
            continue
        
        column = ord(column_choice) - ord('A')
        
        # Check if column is full
        if board[0][column] != ' ':
            print("Column is full! You lose a turn.")
            current_player_idx = (current_player_idx + 1) % PLAYERS
            continue
        
        # Place the checker in the correct row
        for row in reversed(range(ROWS)):
            if board[row][column] == ' ':
                board[row][column] = player_checker
                break
        
        print_board(board)
        
        # Check for win or draw
        if check_win(board, row, column, player_checker):
            print(f"Player {player_checker} won!")
            break
        elif is_draw(board):
            print("The game is a draw!")
            break
        
        # Change to next player
        current_player_idx = (current_player_idx + 1) % PLAYERS

if __name__ == "__main__":
    play_game()
