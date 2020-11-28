from copy import deepcopy
from itertools import permutations


class Permutation:
    def __init__(self, num_list):
        if isinstance(num_list, Permutation):
            self.val = deepcopy(num_list.val)
            return
        if isinstance(num_list, str):
            num_list = list(map(lambda cycle: list(map(int, cycle.split())), num_list[1:-1].split(')(')))
            self.val = sum(map(lambda cycle: len(cycle), num_list)) * [0]
            for cycle in num_list:
                prev = cycle[-1]
                for i in cycle:
                    self[prev] = i
                    prev = i
            return
        self.val = num_list

    def __getitem__(self, item):
        assert 1 <= item <= len(self.val)
        return self.val[item - 1]

    def __setitem__(self, key, value):
        self.val[key - 1] = value

    def __len__(self):
        return len(self.val)

    def __mul__(self, other):
        assert len(self) == len(other)
        n = len(self)
        ans = Permutation([0] * n)
        for i in range(1, n + 1):
            ans[i] = self[other[i]]
        return ans

    def __pow__(self, power, modulo=None):
        if power == -1:
            ans = Permutation([0] * len(self))
            for i in range(1, len(self) + 1):
                ans[self[i]] = i
            return ans
        ans = Permutation(self)
        for i in range(power - 1):
            ans *= self
        return ans

    def __eq__(self, other):
        return tuple(self.val) == tuple(other.val)

    def __str__(self):
        # return ' '.join(map(lambda x: str(x), range(1, len(self) + 1))) + '\n' + ' '.join(map(lambda x: str(x), self.val)) + '\n'
        curr_cycle = [1]
        not_used = set(range(1, len(self) + 1)) - set(curr_cycle)
        cycles = []
        while True:
            next_it = self[curr_cycle[-1]]
            if next_it in not_used:
                curr_cycle.append(next_it)
                not_used.remove(next_it)
            else:
                cycles.append(curr_cycle)
                if not not_used:
                    break
                next_it = min(not_used)
                curr_cycle = [next_it]
                not_used.remove(next_it)
        cycles = list(map(lambda num_list: ' '.join(map(lambda x: str(x), num_list)), cycles))
        return '(' + ')('.join(cycles) + ')\n'


a = Permutation([7, 5, 4, 8, 1, 6, 2, 3])
a = a ** -1
print(a)

b = Permutation([7, 4, 2, 5, 8, 6, 1, 3])
b = b ** 17
print(b)

c = a * b
print(c)

c = c ** 155
print(c)

d = Permutation("(1 2 3)(4 8 7 5 6)")
print(d)

print(Permutation("(1)(2)(3)(4 8 7 5 6)") * c * Permutation("(1 2 3)(4)(8)(7)(5)(6)"))

ans = []
possible = list(map(lambda x: Permutation(x), permutations(range(1, 9))))
for p in possible:
    if p * d * p == c:
        ans.append(p)

print("Solutions: {}".format(len(ans)))
for p in ans:
    print(p)

print('------------------')
print(Permutation("(5 7)(1 4 2 8 3 6)") ** 2)
