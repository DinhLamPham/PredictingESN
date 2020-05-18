import numpy as np

my1Darray = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                      'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                      'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
print(len(my1Darray))
print(my1Darray.shape)

my2Darray = np.array([
    ['a', 'b'],
    ['c', 'd'],
    ['e', 'f'],
    ['g', 'h'],
    ['i', 'j'],
    ['k', 'l'],
    ['m', 'n'],
    ['o', 'p'],
    ['q', 'r'],
    ['s', 't'],
    ['u', 'v'],
    ['w', 'x'],
    ['y', 'z'],
    ['1', '2'],
    ['3', '4'],
    ['5', '6'],
    ['7', '8'],
    ['9', '10']
])
print(my2Darray.shape)
print(len(my2Darray))


my3Darray = np.array([
    [['a', 'b'], ['c', 'd'], ['e', 'f']],
    [['g', 'h'], ['i', 'j'], ['k', 'l']],
    [['m', 'n'], ['o', 'p'], ['q', 'r']],
    [['s', 't'], ['u', 'v'], ['w', 'x']],
    [['y', 'z'], ['1', '2'], ['3', '4']],
    [['5', '6'], ['7', '8'], ['9', '10']]
])
print(my3Darray.shape)
print(len(my3Darray))

newarray = my3Darray.reshape(my3Darray.shape[0] * my3Darray.shape[1], -1)
print(newarray, newarray.shape)