import os
import random

# Constants for game dimensions and players
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print('  ' + '   '.join(chr(i) for i in range(65, 65 + COLS)))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(row) + '|')
        print('+' + '---+' * COLS)

def drop_checker(board, col, checker):
    for row in reversed(board):
        if row[col] == ' ':
            row[col] = checker
            return True
    return False
    
def is_winner(board, checker):
    for row in range(ROWS):
        for col in range(COLS):
            if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                return True
            if col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)):
                return True
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            if row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == checker for i in range(4)):
                return True
    return False

def is_draw(board):
    return all(cell != ' ' for row in board for cell in row)

def main():
    board = create_board()
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)
    
    while True:
        current_player = PLAYERS[current_player_index]
        col_input = input(f"Player {current_player}, please enter a column (A-G): ").upper()
        
        if col_input < 'A' or col_input >= chr(65 + COLS):
            print("Invalid column. Please try again.")
            continue

        col = ord(col_input) - 65
        
        if not drop_checker(board, col, current_player):
            print("Column is full. Please choose another column.")
            continue
        
        print_board(board)

        if is_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if is_draw(board):
            print("The game is a draw!")
            break
        
        current_player_index = (current_player_index + 1) % len(PLAYERS)

if __name__ == "__main__":
    main()
