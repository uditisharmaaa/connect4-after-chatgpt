import os
import random

# Constants: player symbols and board dimensions
PLAYERS = ['X', 'O', 'V', 'H', 'M']
ROWS, COLS = 6, 7
COL_LABELS = 'ABCDEFG'

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    os.system('clear')
    print(' '.join(COL_LABELS))
    for row in board:
        print(' '.join(row))

def check_winner(board, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Vertical, Horizontal, Diagonal /
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == player:
                for dr, dc in directions:
                    if all((0 <= r + dr*i < ROWS) and (0 <= c + dc*i < COLS) and (board[r + dr*i][c + dc*i] == player) for i in range(4)):
                        return True
    return False

def is_draw(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def get_valid_move():
    while True:
        move = input(f"Choose a column ({COL_LABELS}): ").strip().upper()
        if len(move) == 1 and move in COL_LABELS:
            return COL_LABELS.index(move)
        print("Invalid input. Please choose a valid column.")

def main():
    num_players = min(max(int(input("Enter number of players (2-5): ")), 2), 5)
    players = PLAYERS[:num_players]
    board = create_board()
    current_player = random.choice(players)

    while True:
        print_board(board)
        print(f"{current_player}'s turn")

        col = get_valid_move()
        for row in reversed(board):
            if row[col] == ' ':
                row[col] = current_player
                break
        else:
            print("Column is full. Choose another.")
            continue

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
