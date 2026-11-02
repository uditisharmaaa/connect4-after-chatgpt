import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
PLAYERS = 2

# Checkers for players
CHECKERS = ["X", "O", "V", "H", "M"]

# Initialize the board
def create_board():
    board = []
    for _ in range(BOARD_ROWS):
        row = []
        for _ in range(BOARD_COLS):
            row.append(" ")
        board.append(row)
    return board

# Print the board
def print_board(board):
    os.system('clear')
    print("  A   B   C   D   E   F   G")
    print("+---+---+---+---+---+---+---+")
    for row in board:
        print("|", end="   ")
        for cell in row:
            print(cell, end="   |")
        print("\n+---+---+---+---+---+---+---+")
    print()

# Validate user input
def validate_input(column):
    if column < 0 or column >= BOARD_COLS:
        return False
    if not 'A' <= column + 65 <= 'Z':
        return False
    return True

# Check for a win
def check_win(board, player):
    # Check horizontal locations for win
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Check vertical locations for win
    for c in range(BOARD_COLS):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Check positively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(BOARD_ROWS-3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Check negatively sloped diagonals
    for c in range(BOARD_COLS-3):
        for r in range(3, BOARD_ROWS):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

# Check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Main game loop
def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current_player = random.choice(players)
    players.remove(current_player)
    players.insert(0, current_player)
    while True:
        print_board(board)
        print("Player", current_player, ", please enter a column (A-G):")
        column = ord(input().upper()) - 65
        if not validate_input(column):
            print("Invalid input. Please try again.")
            continue
        for row in reversed(board):
            if row[column] == " ":
                row[column] = current_player
                break
        else:
            print("Column is full. Please try again.")
            continue
        if check_win(board, current_player):
            print_board(board)
            print("Player", current_player, "won!")
            break
        if check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        current_player = players[1]
        players.insert(0, players.pop())

if __name__ == "__main__":
    main()
