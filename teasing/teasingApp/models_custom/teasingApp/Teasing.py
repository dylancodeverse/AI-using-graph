import random
import copy

class Teasing:
    def __init__(self, sizeX, sizeY):
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.matrix = [[0 for _ in range(sizeX)] for _ in range(sizeY)]

    def __str__(self):
        rows = []
        for row in self.matrix:
            row_str = " ".join(str(cell) for cell in row)
            rows.append(row_str)
        return "\n".join(rows)

    def move_empty(self, direction):
        empty_pos = self.find_empty()
        if direction == "up":
            if empty_pos[0] > 0:
                # echange simultanee
                self.matrix[empty_pos[0]][empty_pos[1]], self.matrix[empty_pos[0]-1][empty_pos[1]] = self.matrix[empty_pos[0]-1][empty_pos[1]], self.matrix[empty_pos[0]][empty_pos[1]]
        elif direction == "down":
            if empty_pos[0] < self.sizeY - 1:
                self.matrix[empty_pos[0]][empty_pos[1]], self.matrix[empty_pos[0]+1][empty_pos[1]] = self.matrix[empty_pos[0]+1][empty_pos[1]], self.matrix[empty_pos[0]][empty_pos[1]]
        elif direction == "left":
            if empty_pos[1] > 0:
                self.matrix[empty_pos[0]][empty_pos[1]], self.matrix[empty_pos[0]][empty_pos[1]-1] = self.matrix[empty_pos[0]][empty_pos[1]-1], self.matrix[empty_pos[0]][empty_pos[1]]
        elif direction == "right":
            if empty_pos[1] < self.sizeX - 1:
                self.matrix[empty_pos[0]][empty_pos[1]], self.matrix[empty_pos[0]][empty_pos[1]+1] = self.matrix[empty_pos[0]][empty_pos[1]+1], self.matrix[empty_pos[0]][empty_pos[1]]
        else:
            raise ValueError("Invalid direction")

    def find_empty(self):
        for i in range(self.sizeY):
            for j in range(self.sizeX):
                if self.matrix[i][j] == 0:
                    return (i, j)
        raise ValueError("Empty cell not found")

    def get_available_moves(self):
        empty_pos = self.find_empty()
        available_moves = []

        if empty_pos[0] > 0:
            available_moves.append("up")
        if empty_pos[0] < self.sizeY - 1:
            available_moves.append("down")
        if empty_pos[1] > 0:
            available_moves.append("left")
        if empty_pos[1] < self.sizeX - 1:
            available_moves.append("right")

        return available_moves

    def get_tuples_derivate(self):
        moves = self.get_available_moves()
        tuples =[]
        for move in moves :
            taquin_copy =Teasing(self.sizeX, self.sizeY)
            taquin_copy.matrix = [row[:] for row in self.matrix]  
            taquin_copy.move_empty(move)
            tuples.append((taquin_copy,move))
        return tuples
    

    def shuffle(self ,shuffle_number: int):
        for i in range (shuffle_number): 
            available_moves = self.get_available_moves()
            random.shuffle(available_moves)
            self.move_empty(available_moves[0])

    def get_list_of_result_move(self, move_list: list[str]):
        ls: list[Teasing] = []
        ls.append(self)
        for move in move_list:
            x = copy.deepcopy(ls[-1])  
            x.move_empty(move)
            ls.append(x)
        return ls

        
