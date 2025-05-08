'''
crossword module
'''
import tkinter as tk
from time import sleep

CELL_SIZE = 60
DELAY = 0.025
class Crossword:
    '''
    crossword class
    '''
    def __init__(self, root, grid, words):
        '''
        '''
        self.master = root
        self.grid = grid
        self.words = words
        self.height = len(grid)
        self.width = len(grid[0])
        self.prev_grid = [[[] for _ in range(self.width)] for _ in range(self.height)]
        self.image = tk.Canvas(self.master, width=self.width * CELL_SIZE, height=self.height * CELL_SIZE)
        self.show = [[None] * self.width for _ in range(self.height)]
        self.rects = [[None] * self.width for _ in range(self.height)]
        self.image.pack()
        self.build_grid()
        self.master.after(1000, self.pre_start)


    def build_grid(self):
        '''
        builds grid for visualization
        '''
        for i in range(self.height):
            for j in range(self.width):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                color = "white" if self.grid[i][j] == '1' else "gray"
                self.rects[i][j] = self.image.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                self.show[i][j] = self.image.create_text(
                    x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, text="", font=("Arial", 20))


    def update(self, row, col, element):
        '''
        updates visualization
        '''
        if element == "":
            self.image.itemconfig(self.rects[row][col], fill="red")
        else:
            self.image.itemconfig(self.rects[row][col], fill="green")

        self.image.itemconfig(self.show[row][col], text=element)
        self.master.update()
        sleep(DELAY)

        color = "gray" if self.grid[row][col] == '0' else "white"
        self.image.itemconfig(self.rects[row][col], fill=color)
        self.master.update()


    def pre_start(self):
        '''
        making everything ready for backtracking
        '''
        all_places = self.find_all_places()
        words = sorted(self.words, key = len, reverse=True)
        used_words = set()
        self.crossword_backtrack(words, all_places, used_words, 0)

    def find_all_places(self):
        '''
        finding all places for words
        '''
        horizontal_places = []
        vertical_places = []

        for row in range(self.height):
            col = 0
            while col < self.width:
                start_col = col
                place_length = 0
                while col < self.width and self.grid[row][col] == '1':
                    place_length += 1
                    col += 1
                if place_length > 1:
                    horizontal_places.append((row, start_col, place_length))
                col += 1

        for col in range(self.width):
            row = 0
            while row < self.height:
                start_row = row
                place_length = 0
                while row < self.height and self.grid[row][col] == '1':
                    place_length += 1
                    row += 1
                if place_length > 1:
                    vertical_places.append((start_row, col, place_length))
                row += 1

        all_places = []
        for place in horizontal_places:
            all_places.append(('horizontally', place))
        for place in vertical_places:
            all_places.append(('vertically', place))

        all_places.sort(key=lambda x: x[1][2], reverse=True)

        return all_places

    def crossword_backtrack(self, words, all_places, used_words, count):
        '''
        solves crossword using backtracking
        '''
        if count == len(words):
            return True

        direction, (row, col, place_length) = all_places[count]

        for word in words:
            if word in used_words:
                continue
            if len(word) == place_length:
                if direction == 'horizontally':
                    if self.can_place_horizontally(word, row, col, place_length):
                        self.place_horizontally(word, row, col)
                        used_words.add(word)
                        if self.crossword_backtrack(words, all_places, used_words, count + 1):
                            return True
                        self.remove_horizontally(word, row, col, place_length)
                        used_words.remove(word)
                else:
                    if self.can_place_vertically(word, row, col, place_length):
                        self.place_vertically(word, row, col)
                        used_words.add(word)
                        if self.crossword_backtrack(words, all_places, used_words, count + 1):
                            return True
                        self.remove_vertically(word, row, col, place_length)
                        used_words.remove(word)

        return False

    def can_place_vertically(self, word, row, col, place_length):
        '''
        checks if can place word vertically
        '''
        for i in range(place_length):
            if self.grid[row+i][col] != '1' and self.grid[row+i][col] != word[i]:
                return False
        return True

    def can_place_horizontally(self, word, row, col, place_length):
        '''
        checks if can place word horizontally
        '''
        for j in range(place_length):
            if self.grid[row][col+j] != '1' and self.grid[row][col+j] != word[j]:
                return False
        return True


    def place_vertically(self, word, row, col):
        '''
        checks whether can place word vertically
        '''
        word_len = len(word)
        for i in range(word_len):
            self.prev_grid[row+i][col].append(word)
            self.grid[row+i][col] = word[i]
            self.update(row+i, col, word[i])


    def place_horizontally(self, word, row, col):
        '''
        checks whether can place word horizontally
        '''
        word_len = len(word)
        for j in range(word_len):
            self.prev_grid[row][col+j].append(word)
            self.grid[row][col+j] = word[j]
            self.update(row, col+j, word[j])

    def remove_vertically(self, word, row, col, length):
        '''
        removes word vertically
        '''
        for i in range(length):
            if word in self.prev_grid[row+i][col]:
                self.prev_grid[row+i][col].remove(word)
            if not self.prev_grid[row+i][col]:
                self.grid[row+i][col] = '1'
                self.update(row+i, col, '')
    def remove_horizontally(self, word, row, col, length):
        '''
        removes word horizontally
        '''
        for j in range(length):
            if word in self.prev_grid[row][col+j]:
                self.prev_grid[row][col+j].remove(word)
            if not self.prev_grid[row][col+j]:
                self.grid[row][col+j] = '1'
                self.update(row, col+j, '')




if __name__ == "__main__":
    initial_grid = [
        ['1', '1', '1', '1', '1', '1', '0', '1', '1', '1'],
        ['1', '0', '1', '0', '1', '1', '1', '1', '1', '0'],
        ['1', '1', '1', '1', '1', '1', '0', '1', '1', '1'],
        ['1', '0', '1', '1', '1', '1', '0', '0', '0', '1'],
        ['0', '0', '1', '1', '1', '0', '1', '1', '1', '1'],
        ['1', '1', '1', '1', '0', '1', '1', '1', '0', '0'],
        ['1', '0', '0', '0', '1', '1', '1', '1', '0', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
        ['0', '1', '1', '1', '1', '1', '0', '1', '0', '1'],
        ['1', '1', '1', '0', '1', '1', '1', '1', '1', '1'],
    ]

    words = [
        'LIAR', 'LESION', 'ABATES', 'BUS', 
        'MOLES', 'TEE', 'ENE', 'ISIS',
        'MADE', 'PSALMS', 'TIS', 'RUES',
        'ANNALS', 'RASP', 'TUNES', 'MIEN',
        'ASSAIL', 'TENSE', 'BAT', 'GEN',
        'ATE', 'TEN', 'TUB', 'TREE', 'SPA',
        'RAGE', 'SPARSE', 'TAPE', 'OMEGA', 'NOSE',
        'BET', 'USE'
    ]

    root = tk.Tk()
    app = Crossword(root, initial_grid, words)
    root.mainloop()
