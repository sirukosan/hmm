def initialize_matrix(dim1, dim2, value=0):
    F = []
    for i in range(0, dim1):
        F.append([])
        for j in range(0, dim2):
            F[i].append(value)
    return F


def print_matrix(matrix, axis1, axis2):
    w = '{:<10}'
    print(w.format('') + w.format('0') + ''.join([w.format(char) for char in axis2]) + w.format('0'))
    for i, row in enumerate(matrix):
        print(w.format(axis1[i]) + ''.join(['{:<10.2e}'.format(item) for item in row]))


def print_matrix_p(matrix, axis1, axis2):
    w = '{:<10}'
    print(w.format('') + w.format('0') + ''.join([w.format(char) for char in axis2]) + w.format('0'))
    for i, row in enumerate(matrix):
        print(w.format(axis1[i]) + ''.join(['{:<10s}'.format(item) for item in row]))


def get_max_val_ind(values):
    max_val = values[0]
    max_ind = 0
    for ind, val in enumerate(values):
        if val > max_val:
            max_val = val
            max_ind = ind
    return max_val, max_ind


def traceback(states, FP):
    path = ['e']  # the last element of the path is the end state
    current = FP[-1][-1]  # the current state is the one written in the last cell of the matrix
    for i in range(len(FP[0]) - 2, 0, -1):  # loops on the symbols
        path = [current] + path  # appends the current state to the path
        current = FP[states.index(current)][
            i]  # finds the index of the current state in the list of states and moves to the corresponing row of FP
    path = ['b'] + path  # the first element of the path is the begin state
    return ' '.join(path)  # transforms the list into a string where elements are separated by spaces


def forward(states, transitions, emissions, sequence):
    F = initialize_matrix(len(states), len(sequence) + 2)
    F[0][0] = 1
    for i in range(1, len(states) - 1):
        F[i][1] = transitions[(states[0], states[i])] * emissions[states[i]][sequence[0]]
    for j in range(2, len(sequence) + 1):
        for i in range(1, len(states) - 1):
            p_sum = 0
            for k in range(1, len(states) - 1):
                p_sum += F[k][j - 1] * transitions[(states[k], states[i])] * emissions[states[i]][sequence[j - 1]]
            F[i][j] = p_sum
    p_sum = 0
    for k in range(1, len(states) - 1):
        p_sum += F[k][len(sequence)] * transitions[(states[k], states[-1])]
    F[-1][-1] = p_sum
    return F


def viterbi(states, transitions, emissions, sequence):
    F = initialize_matrix(len(states), len(sequence) + 2)
    FP = initialize_matrix(len(states), len(sequence) + 2, states[0])
    F[0][0] = 1
    for i in range(1, len(states) - 1):
        F[i][1] = transitions[(states[0], states[i])] * emissions[states[i]][sequence[0]]
    for j in range(2, len(sequence) + 1):
        for i in range(1, len(states) - 1):
            values = []
            for k in range(1, len(states) - 1):
                values.append(F[k][j - 1] * transitions[(states[k], states[i])] * emissions[states[i]][sequence[j - 1]])
            max_val, max_ind = get_max_val_ind(values)
            F[i][j] = max_val
            FP[i][j] = states[max_ind + 1]
    values = []
    for k in range(1, len(states) - 1):
        values.append(F[k][len(sequence)] * transitions[(states[k], states[-1])])
    max_val, max_ind = get_max_val_ind(values)
    F[-1][-1] = max_val
    FP[-1][-1] = states[max_ind + 1]
    return F, FP


def backward(states, transitions, emissions, sequence):
    F = initialize_matrix(len(states), len(sequence) + 2)
    F[-1][-1] = 1
    for i in range(1, len(states) - 1):
        F[i][-2] = transitions[(states[i], states[-1])] * emissions[states[i]][sequence[-1]]
    for j in range(len(sequence) - 1, 0, -1):
        for i in range(1, len(states) - 1):
            p_sum = 0
            for k in range(1, len(states)):
                p_sum += F[k][j + 1] * transitions[(states[i], states[k])] * emissions[states[i]][sequence[j - 1]]
            F[i][j] = p_sum
    p_sum = 0
    for k in range(1, len(states) - 1):
        p_sum += F[k][1] * transitions[(states[0], states[k])]
    F[0][0] = p_sum
    return F
