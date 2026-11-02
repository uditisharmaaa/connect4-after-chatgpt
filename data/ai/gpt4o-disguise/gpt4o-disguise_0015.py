import random
import os

def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---+---+---+---+---+---+---+")

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def check_winner(board, player, rows, cols):
    # Check horizontal
    for row in range(rows):
        for col in range(cols - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == player:
                return True
    # Check vertical
    for col in range(cols):
        for row in range(rows - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == player:
                return True
    # Check diagonal /
    for row in range(3, rows):
        for col in range(cols - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] == player:
                return True
    # Check diagonal \
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] == player:
                return True
    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    rows, cols = 6, 7
    board = create_board(rows, cols)
    players = ["X", "O"]
    current_player = random.choice(players)
    print_board(board)
    
    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()
        if len(column) != 1 or not ("A" <= column <= "G"):
            print("Invalid input. Please enter a valid column between A to G.")
            continue
        
        col_index = ord(column) - ord('A')
        
        if board[0][col_index] != " ":
            print("Column is full. Turn is lost.")
            current_player = players[1] if current_player == players[0] else players[0]
            continue
        
        for row in range(rows-1, -1, -1):
            if board[row][col_index] == " ":
                board[row][col_index] = current_player
                break
        
        print_board(board)
        
        if check_winner(board, current_player, rows, cols):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        current_player = players[1] if current_player == players[0] else players[0]

play_game()
