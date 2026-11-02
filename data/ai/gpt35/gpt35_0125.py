import os, random

ROWS, COLS = 6, 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear(): os.system('clear')

def create_board():
    return [[" "]*COLS for _ in range(ROWS)]

def print_board(board):
    clear()
    print("  " + "   ".join(chr(ord("A")+i) for i in range(COLS)))
    for r in range(ROWS):
        print("+" + "---+"*COLS)
        print("|" + "|".join(f" {board[r][c]} " for c in range(COLS)) + "|")
    print("+" + "---+"*COLS)

def valid_column(col):
    return len(col) == 1 and "A" <= col <= chr(ord("A")+COLS-1)

def place_checker(board, col, checker):
    c = ord(col) - ord("A")
    for r in range(ROWS-1, -1, -1):
        if board[r][c] == " ":
            board[r][c] = checker
            return r, c
    return -1, -1

def check_direction(board, r, c, dr, dc, checker):
    count = 0
    for i in range(4):
        rr, cc = r + dr*i, c + dc*i
        if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr][cc] == checker:
            count +=1
        else:
            break
    return count == 4

def check_win(board, r, c, checker):
    return any(check_direction(board, r, c, dr, dc, checker) for dr, dc
               in [(0,1),(1,0),(1,1),(1,-1)])

def board_full(board):
    return all(board[0][c] != " " for c in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS-1)
    print_board(board)
    while True:
        checker = players[current]
        print(f"Player {checker}, please enter a column:")
        col = input().strip().upper()
        if not valid_column(col):
            print("Invalid input. Please enter a valid column letter.")
            continue
        r, c = place_checker(board, col, checker)
        if r == -1:
            print("Column is full. You lose your turn.")
        else:
            print_board(board)
            if check_win(board, r, c, checker):
                print(f"Player {checker} won!")
                break
            if board_full(board):
                print("Game is a draw!")
                break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
