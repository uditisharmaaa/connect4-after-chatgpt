import random
import os

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M']  # Checker symbols for up to 5 players

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(COLS))
    print(header)
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(column, board):
    return 0 <= column < COLS and board[0][column] == ' '

def apply_move(column, player, board):
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = CHECKERS[player]
            return

def check_winner(board, player):
    checker = CHECKERS[player]

    for row in range(ROWS):
        for col in range(COLS):
            # Horizontal check
            if col <= COLS - 4 and all(board[row][col + i] == checker for i in range(4)):
                return True
            # Vertical check
            if row <= ROWS - 4 and all(board[row + i][col] == checker for i in range(4)):
                return True
            # Diagonal / check
            if row <= ROWS - 4 and col <= COLS - 4 and all(board[row + i][col + i] == checker for i in range(4)):
                return True
            # Diagonal \ check
            if row >= 3 and col <= COLS - 4 and all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLS)
    current_player = random.randint(0, MAX_PLAYERS - 1)

    print_board(board)
    
    while True:
        print(f"Player {CHECKERS[current_player]}, please enter a column:")
        move = input().strip().upper()

        if len(move) != 1 or not ('A' <= move <= chr(ord('A') + COLS - 1)):
            print("Invalid input, try again.")
            continue

        column = ord(move) - ord('A')

        if not is_valid_move(column, board):
            print("Column full or invalid, try again.")
            continue

        apply_move(column, current_player, board)

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        current_player = (current_player + 1) % MAX_PLAYERS

if __name__ == "__main__":
    main()
