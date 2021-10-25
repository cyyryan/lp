Yuyang Chen
V00935234

# Overview

The code solves Lineaer Programming by Simplex Method.

1. Initialize the use of Dual Simplex Method
2. Use the largest coefficient rule, falling back on Bland’s rule in specific cases where cycling is possible


## running guide
1. Run the following command:
    python3 lp.py < filename.txt

or

2. python3 lp.py
     1 2
     3 4
     5 6 
     .......
ctrl + D once you complete the value input process

## how it works

1. Read the parameters from standard input
2. Initialize the dictionary representation, which is `Simplex._coeff_matrix`
3. Use Dual Simplex Method, to make Feasible Original Dictionary
4. Use the largest coefficient rule and bland's rule to solve
5. print the output

## dictionary representation

`Simplex._coeff_matrix` format

```
0      c_1      c_2      ...    c_n
b_1    a_1,1    a_1,2    ...    a_1,n
b_2    a_2,1    a_2,2    ...    a_2,n
.
.
.
b_m    a_m,1    a_m,2    ...    a_m,n
```

## cycling

### condition 1

Check visiting the same solution more than once.

The code specified a variable objective_coeff_set to hold existed solution signatures.

```
objective_coeff_set = {','.join([str(x) for x in self._coeff_matrix[0][1:]])}
```

Cycling is set if the same solution signautre occurd.

### condition 2

Check max iteration count. (n+m)!/n!m!.

`Simplex._max_iterate_count`

## pivot loop

1. Find pivot col(leaving variable index) in first row of `Simplex._coeff_matrix` with specified rule.
2. If the pivot col is less or equal 0, break loop. Optimal is found.
3. Find pivot row(entering variable index) with specified rule.
4. Replace leaving variables and entering variables.
5. Update current variable assignment(Simplex._values). eg `(x1, x2, x3,w1,w2,w3) = (0, 0, 0, 3, 4, 1)`
6. Go step 1.
