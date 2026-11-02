import random
import os

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O']

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    for row in board:
        print("+---" * len(row) + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * len(board[0]) + "+")

def place_checker(board, col, player):
    for i in range(ROWS - 1, -1, -1):
        if board[i][col] == ' ':
            board[i][col] = player
            return True
    return False

def check_win(board, player):
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board(ROWS, COLS)
    print_board(board)
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, please enter a column:")
        while True:
            user_input = input().strip().upper()
            if user_input.isalpha() and len(user_input) == 1:
                col = ord(user_input) - 65
                if 0 <= col < COLS:
                    if place_checker(board, col, current_player):
                        break
                    else:
                        print("Column full. Choose another.")
                else:
                    print("Invalid column. Choose between A and G.")
            else:
                print("Invalid input. Enter a letter.")
        
        print_board(board)
        
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("It's a draw!")
            break
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
