# Name: Yuyang Chen
# V00935234
# Programming Project
# 2021.July.19
import sys
from fractions import Fraction


class Simplex:

    def __init__(self):
        self._c = []
        self._a = []
        self._b = []

        self._basic_var_idx = []
        self._coeff_matrix = []
        self._values = []

        self._max_iterate_count = 0

        self._res = 'infeasible'

    def get_result(self):
        if self._res != 'optimal':
            return self._res, None, None
        return self._res, ' '.join([str(self._values[i]) for i in range(len(self._a[0]))]), self._coeff_matrix[0][0]

    def get_float_result(self):
        if self._res != 'optimal':
            return self._res, None, None
        return self._res, ' '.join([str(float(self._values[i])) for i in range(len(self._a[0]))]), float(
            self._coeff_matrix[0][0])

    # def read_file(self, filename):
    #     with open(filename, 'r') as f:
    #         line = None
    #         while not line:
    #             line = next(f).strip()
    #         self._c = [Fraction(x) for x in line.split()]
    #
    #         for line in f:
    #             if line:
    #                 arr = [Fraction(x) for x in line.split()]
    #                 self._a.append(arr[:-1])
    #                 self._b.append(arr[-1])

    def read_stdin(self):
        input_lines = sys.stdin.readlines()
        self._c = [Fraction(x) for x in input_lines[0].split()]
        for i in range(1, len(input_lines)):
            line = input_lines[i].strip()
            if line:
                arr = [Fraction(x) for x in line.split()]
                self._a.append(arr[:-1])
                self._b.append(arr[-1])

    def solve(self):
        self._init_dictionary_coeff()

        if not self._make_feasible():
            self._res = 'infeasible'
            return

        self._iterate_pivot()
    
    # def write_file(self, filename):
    #     with open(filename, 'w') as f:
    #         f.write(self._res + '\n')
    #         if self._res != 'optimal':
    #             return
    #         f.write(' '.join([str(self._values[i]) for i in range(len(self._a[0]))]) + '\n')
    #         f.write(str(self._coeff_matrix[0][0]))

    def _iterate_pivot(self):
        self._res = 'cycling'
        self._pivot_largest_coefficient_rule()
        if self._res == 'cycling':
            self._pivot_bland_rule()

    def _pivot_largest_coefficient_rule(self):
        objective_coeff_set = {','.join([str(x) for x in self._coeff_matrix[0][1:]])}

        pivot_col = self._max_coeff_index()
        pivot_coeff = self._coeff_matrix[0][pivot_col]
        for count in range(self._max_iterate_count):
            if pivot_coeff <= 0:
                self._res = 'optimal'
                break

            pivot_row = self._find_max_ratio_row(pivot_col)
            if pivot_row is None:
                self._res = 'unbounded'
                break

            self._pivot_normalize(pivot_row, pivot_col)
            self._basic_var_idx[pivot_row] = pivot_col
            self._rearrange_dictionary(pivot_row, pivot_col)
            self._update_values()

            cur_obj_coeff = ','.join([str(x) for x in self._coeff_matrix[0][1:]])
            if cur_obj_coeff in objective_coeff_set:
                # same objective coefficients exists, cycling
                break
            else:
                objective_coeff_set.add(cur_obj_coeff)

            pivot_col = self._max_coeff_index()
            pivot_coeff = self._coeff_matrix[0][pivot_col]

    def _pivot_bland_rule(self):
        pivot_col = self._find_bland_col()
        pivot_coeff = self._coeff_matrix[0][pivot_col]

        while pivot_coeff > 0:
            pivot_row = self._find_bland_row(pivot_col)
            if pivot_row is None:
                self._res = 'unbounded'
                break

            self._pivot_normalize(pivot_row, pivot_col)
            self._basic_var_idx[pivot_row] = pivot_col
            self._rearrange_dictionary(pivot_row, pivot_col)
            self._update_values()

            pivot_col = self._find_bland_col()
            pivot_coeff = self._coeff_matrix[0][pivot_col]

        if pivot_coeff <= 0:
            self._res = 'optimal'

    def _find_bland_col(self):
        for i in range(1, len(self._coeff_matrix[0])):
            if self._coeff_matrix[0][i] > 0:
                return i
        return 1

    def _find_bland_row(self, pivot_col):
        min_val = float('inf')
        invalid_num = len(self._coeff_matrix[0])
        lowest_num = invalid_num
        min_idx = -1
        for i in range(1, len(self._coeff_matrix)):
            if self._coeff_matrix[i][pivot_col] < 0:
                val = self._coeff_matrix[i][0] / -self._coeff_matrix[i][pivot_col]
                if val <= min_val:
                    min_val = val
                    if lowest_num > self._basic_var_idx[i]:
                        lowest_num = self._basic_var_idx[i]
                        min_idx = i
        if min_idx < 0:
            return None

        return min_idx

    def _find_max_ratio_row(self, pivot_col):
        min_val = float('inf')
        min_index = -1
        for i in range(1, len(self._coeff_matrix)):
            if self._coeff_matrix[i][pivot_col] < 0:
                val = self._coeff_matrix[i][0] / -self._coeff_matrix[i][pivot_col]
                if val < min_val:
                    min_val = val
                    min_index = i
        if min_val == 0:
            # print('Dengeneracy')
            pass
        if min_index < 0:
            return None

        return min_index

    def _pivot_normalize(self, pivot_row, pivot_col):
        pivot = -self._coeff_matrix[pivot_row][pivot_col]
        self._coeff_matrix[pivot_row][pivot_col] = Fraction('0')

        basic_index = self._basic_var_idx[pivot_row]
        self._coeff_matrix[pivot_row][basic_index] = -1
        for i in range(len(self._coeff_matrix[pivot_row])):
            self._coeff_matrix[pivot_row][i] /= pivot

    def _rearrange_dictionary(self, pivot_row, pivot_col):
        num_columns = len(self._coeff_matrix[0])
        for i in range(len(self._coeff_matrix)):
            if i != pivot_row:
                factor = self._coeff_matrix[i][pivot_col]
                for j in range(num_columns):
                    self._coeff_matrix[i][j] += self._coeff_matrix[pivot_row][j] * factor
                self._coeff_matrix[i][pivot_col] = 0

    def _update_values(self):
        for i in range(len(self._values)):
            self._values[i] = 0
        for i in range(1, len(self._basic_var_idx)):
            idx = self._basic_var_idx[i] - 1
            self._values[idx] = self._coeff_matrix[i][0]

    def _max_coeff_index(self):
        index = 1
        for i in range(1, len(self._coeff_matrix[0])):
            if self._coeff_matrix[0][index] < self._coeff_matrix[0][i]:
                index = i
        return index

    def _make_feasible(self):
        while any(self._coeff_matrix[i][0] < 0 for i in range(1, len(self._coeff_matrix))):
            # apply Dual Simplex Method
            row_idx = self._get_dual_row_idx()
            col_idx = self._get_dual_col_idx(row_idx)
            if col_idx is None:
                return False

            self._pivot_normalize(row_idx, col_idx)
            self._basic_var_idx[row_idx] = col_idx
            self._rearrange_dictionary(row_idx, col_idx)

        return True

    def _get_dual_row_idx(self):
        idx_max = 1
        cur_min = self._coeff_matrix[idx_max][0]
        for i in range(2, len(self._coeff_matrix)):
            if cur_min > self._coeff_matrix[i][0]:
                cur_min = self._coeff_matrix[i][0]
                idx_max = i
        return idx_max

    def _get_dual_col_idx(self, row_idx):
        min_val = float('inf')
        min_index = -1
        for i in range(1, len(self._coeff_matrix[0])):
            if self._coeff_matrix[0][i] < 0:
                if self._coeff_matrix[row_idx][i] > 0:
                    val = -self._coeff_matrix[0][i] / self._coeff_matrix[row_idx][i]
                    if val < min_val:
                        min_val = val
                        min_index = i
            elif self._coeff_matrix[0][i] > 0:
                if self._coeff_matrix[row_idx][i] != 0:
                    val = 0
                    if val < min_val:
                        min_val = val
                        min_index = i
        if min_index < 0:
            return None
        return min_index

    def _init_dictionary_coeff(self):
        num_vars = len(self._a[0])
        num_slack = len(self._a)

        objective_coeff = [Fraction('0')]
        objective_coeff.extend(self._c)
        objective_coeff.extend([Fraction('0')] * num_slack)
        self._coeff_matrix.append(objective_coeff)

        for i in range(num_slack):
            coeff_row = [self._b[i]]
            for x in self._a[i]:
                coeff_row.append(-x)
            coeff_row.extend([Fraction('0')] * num_slack)
            self._coeff_matrix.append(coeff_row)

        self._basic_var_idx = [0]
        self._basic_var_idx.extend([i + 1 + num_vars for i in range(num_slack)])

        self._values = [Fraction('0')] * (num_vars + num_slack)

        self._max_iterate_count = 1
        for i in range(1, num_vars + num_slack + 1):
            self._max_iterate_count *= i
        for i in range(1, num_vars + 1):
            self._max_iterate_count /= i
        for i in range(1, num_slack + 1):
            self._max_iterate_count /= i
        self._max_iterate_count = int(self._max_iterate_count) + 1


# if __name__ == '__main__':
#     simplex = Simplex()
#     simplex.read_file('in.txt')
#
#     simplex.solve()
#     simplex.write_file('out.txt')

if __name__ == '__main__':
    simplex = Simplex()
    simplex.read_stdin()

    simplex.solve()
    res, var, val = simplex.get_float_result()
    print(res)
    if res == 'optimal':
        print(val)
        print(var)
