'''
module for crossword
'''
def crossword(grid, words, count=0):
    '''
    fills crossword
    '''
    if count == len(words):
        return True
    word = words[count]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if can_place_horizontally(word, grid, row, col):
                place_word_horizontally(word, row, col, grid)
                if crossword(grid, words, count + 1):
                    return True
                remove_word_horizontally(word, grid, row, col)

            if can_place_vertically(word, grid, row, col):
                place_word_vertically(word, row, col, grid)
                if crossword(grid, words, count + 1):
                    return True
                remove_word_vertically(word, grid, row, col)
    return False


def can_place_vertically(word, grid, row, col):
    '''
    checks whether can place word vertically
    '''
    if row + len(word) > len(grid):
        return False
    for i in range(len(word)):
        if grid[row+i][col] != '1':
            return False
    return True


def can_place_horizontally(word, grid, row, col):
    '''
    checks whether can place word horizontally
    '''
    if col + len(word) > len(grid[0]):
        return False
    for j in range(len(word)):
        if grid[row][col+j] != '1':
            return False
    return True


def place_word_vertically(word, row, col, grid):
    '''
    places word vertically
    '''
    for i in range(len(word)):
        grid[row+i][col] = word[i]


def place_word_horizontally(word, row, col, grid):
    '''
    places word horizontally
    '''
    for i in range(len(word)):
        grid[row][col+i] = word[i]


def remove_word_vertically(word, row, col, grid):
    '''
    removes word vertically
    '''
    for i in range(len(word)):
        grid[row+i][col] = '1'


def remove_word_horizontally(word, row, col, grid):
    '''
    removes word horizontally
    '''
    for i in range(len(word)):
        grid[row][col+i] = '1'



grid = [
    ['1', '0', '1', '1', '1'],
    ['1', '0', '1', '1', '1'],
    ['1', '0', '0', '0', '1'],
    ['1', '1', '1', '0', '1'],
    ['1', '1', '1', '0', '1']
]
words = ['Hello', 'cat', 'nice']

crossword(grid, words)

print(grid)