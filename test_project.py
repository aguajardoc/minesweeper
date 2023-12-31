from project import get_cell, get_size, win_condition


def test_get_cell():
    assert get_cell(567, 124) == 19
    assert get_cell(892, 335) == 176
    assert get_cell(721, 942) == -12
    assert get_cell(10, 9999) == 0
    assert get_cell(0, 0) == -1


def test_get_size():
    assert get_size() == (39.55555555555556, 39.55555555555556)


def test_win_condition():
    assert win_condition([[4, 3], [2, 8], [7, 3], [6, 2], [5, 1], [5, 2], [4, 1], [3, 0], [2, 0], [1, 0], [0, 0],
                          [0, 1], [0, 2], [1, 1], [1, 2], [2, 1], [2, 2], [3, 1], [3, 2], [4, 0], [5, 0], [4, 2],
                          [5, 3], [4, 4], [5, 4], [4, 5], [5, 5], [6, 3], [6, 4], [6, 5], [5, 6], [6, 6], [5, 7],
                          [6, 7], [5, 8], [4, 7], [4, 8], [6, 8], [7, 7], [7, 6], [7, 5], [7, 4], [8, 3], [7, 2],
                          [6, 1], [7, 1], [8, 1], [7, 0], [8, 0], [8, 2], [8, 4], [8, 5], [8, 6], [8, 7], [7, 8],
                          [8, 8], [3, 4], [2, 3], [2, 4], [2, 5], [3, 5], [0, 3], [0, 4], [1, 6], [2, 6], [3, 6],
                          [2, 7], [3, 7], [1, 7], [0, 8], [0, 6]]
                         ) == True
    assert win_condition([1, 2, 3, 4, 5, 6, 7, 8]) == False
    assert win_condition([71]) == False