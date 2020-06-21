from graphviz import Digraph

# Using an finite-state automaton that checks if a binary number is divisible by three as an example,
# FSAs will be represented as follows:
divisible = {
    'S0': {0: 'S0', 1: 'S1', 'start': True , 'accept': True },
    'S1': {0: 'S2', 1: 'S0', 'start': False, 'accept': False},
    'S2': {0: 'S1', 1: 'S2', 'start': False, 'accept': False}
}
# Each key represents a different state, and each value contains a dictionary
# with the following information: the new state upon reception of a particular input,
# whether a state is the starting state, and whether a state is an accepting state.

# Additionally, the matrix representation of the directed graph corresponding to
# the aforementioned FSA is as follows:
div_matrix = [
    [ 0,  1, ()],
    [ 1, (),  0],
    [(),  0,  1]
]
# The ij-th entry indicates which symbols cause a transition from the i-th state to the j-th state.
# If an entry is the empty tuple, nothing causes a transition between the two.
# Notation adapted from:
# 'Generalized transition matrix of a sequential machine and its applications' - T.Kameda


class StateMach:
    def __init__(self, fsa):
        self.fsa    = fsa
        self.state  = [k for k in fsa if fsa[k]['start']][0]
        self.accept = self.fsa[self.state]['accept']
        self.is_min = False
        self.norm()

    def __call__(self, *arg):
        if isinstance(arg[0], list):
            arg = arg[0]
        for k in arg:
            self.state = self.fsa[self.state][k]
        self.accept = self.fsa[self.state]['accept']
        return self

    def __str__(self):
        dct = '\n'.join(f'{k}: {v}' for k,v in self.fsa.items())
        dct = dct.replace('True', 'True ').replace('\'', '').replace(', ', ',\t')
        return dct.replace('{', '| ').replace('}', ' |')

    # Creates a StateMach object of an FSA that checks if a number is divisible by num in a particular base.
    @staticmethod
    def div_by(base, num):
        f = lambda k: {n: f'S{(base * k + n) % num}' for n in range(base)}
        fsa = {f'S{k}': f(k) for k in range(num)}
        for k in fsa:
            fsa[k].update({'start': False, 'accept': False})
        fsa['S0']['start'] = fsa['S0']['accept'] = True
        return StateMach(fsa)

    # Normalizes an FSA by renaming states.
    def norm(self):
        keys     = sorted([k for k in self.fsa], key=lambda x: int(x[1:]))
        key_dict = {k:f'S{keys.index(k)}' for k in keys}
        key_dict.update({True:True, False:False})
        temp = {}
        for k,v in self.fsa.items():
            temp[key_dict[k]] = v
            for m in v:
                temp[key_dict[k]][m] = key_dict[v[m]]
        self.fsa = temp
        return self

    # Minimizes the FSA using the table-filling algorithm.
    def fsa_min(self):
        if self.is_min:
            return self
        # Removes unreachable states.
        reach = True
        while reach:
            reach = False
            values = set()
            for v in self.fsa.values():
                values |= set(v.values())
            for k in self.fsa:
                if k not in values:
                    del self.fsa[k]
                    reach = True
                    break
        self.norm()
        # Divides states into accepting and non-accepting.
        copy, size = 0, len(self.fsa)
        accept     = [int(k[1:]) for k in self.fsa if self.fsa[k]['accept']]
        diff       = lambda i,j: ((i in accept) + (j in accept)) % 2
        table      = [[diff(i,j) for i in range(size)] for j in range(size)]
        # Fills the table.
        while copy != table:
            copy = [k[:] for k in table]
            for i in range(size):
                for j in range(size):
                    if not table[i][j] and i != j:
                        for k,v in self.fsa[f'S{i}'].items():
                            if not isinstance(v, bool):
                                x = self.fsa[f'S{i}'][k]
                                y = self.fsa[f'S{j}'][k]
                                if table[int(x[1:])][int(y[1:])]:
                                    table[i][j] = table[j][i] = 1
        # Creates set of tuples of similar states.
        sim = set()
        for i in range(size):
            for j in range(i):
                if not table[i][j]:
                    sim.add((j, i))
        sim = list(map(set, sim))
        # Joins sets together until all sets are pairwise disjoint.
        unmerged = True
        while unmerged:
            unmerged = False
            results = []
            while sim:
                common, rest = sim[0], sim[1:]
                sim = []
                for k in rest:
                    if k.isdisjoint(common):
                        sim.append(k)
                    else:
                        unmerged = True
                        common |= k
                results.append(common)
            sim = results
        # Replaces redundant states.
        redundant = {}
        for i in [sorted(k) for k in sim]:
            for j in i[1:]:
                redundant.update({f'S{j}':f'S{i[0]}'})
                del self.fsa[f'S{j}']
        for key in self.fsa:
            for sec_key in self.fsa[key]:
                if self.fsa[key][sec_key] in redundant:
                    self.fsa[key][sec_key] = redundant[self.fsa[key][sec_key]]
        self.norm()
        self.is_min = True
        return self

    # Creates a named function code object which mimics the FSA.
    def function(self, name, output=False):
        if not name.replace('_', '').isalnum():
            return 'Not a valid name.'
        start    = [k for k in self.fsa if self.fsa[k]['start']][0]
        define   = f'def {name}(arg, state="{start}"):\n'
        stop     = f'\tif arg == "stop": return "accept" if state == "{start}" else "reject" \n'
        cond     = lambda st: f'\tif state == "{st}":\n'
        resp     = lambda a, n, st: f'\t\tif str(arg) == "{a}": return lambda a: {n}(a, "{st}")\n'
        instruct = lambda d: {k: d[k] for k in d if not isinstance(d[k], bool)}
        func     = define + '\tprint(state)\n' * output + stop
        for j in self.fsa:
            func += cond(j)
            for k, v in instruct(self.fsa[j]).items():
                func += resp(k, name, v)
        code = compile(func, 'fsa', 'exec')
        return code

    # Converts the FSA to a matrix.
    def matrix(self):
        size  = len(self.fsa)
        trans = lambda mach, old, new: tuple(i for i in mach[old] if mach[old][i] == new)
        entry = lambda e: e[0] if len(e) == 1 else e
        res   = [[] for _ in range(size)]
        for k in range(size):
            for j in range(size):
                res[k].append(entry(trans(self.fsa, f'S{k}', f'S{j}')))
        return res

    # Creates a visual representation of the FSA using Graphviz.
    def graph(self, space=False):
        # Groups similar state transitions. Not necessary for small alphabets or large FSAs (many states).
        temp = {}
        for k in self.fsa:
            values    = set(v for v in self.fsa[k].values() if not isinstance(v, bool))
            sort_func = lambda x: x if isinstance(x, int) else ord(x)
            new       = {}
            for v in values:
                i_sort = sorted([j for j in self.fsa[k] if self.fsa[k][j] == v], key=sort_func)
                inputs = (',' + ' '*space).join(str(i) for i in i_sort) if len(i_sort) > 1 else i_sort[0]
                new.update({inputs:v})
            new.update({'start':self.fsa[k]['start'], 'accept':self.fsa[k]['accept']})
            temp[k] = new
        # Creates the actual graph.
        state = Digraph()
        state.attr(rankdir='LR', size='8,5')
        state.node('', shape='none', height='0', width='0')
        for key in temp:
            if temp[key]['accept']:
                state.node(key, shape='doublecircle')
            else:
                state.node(key, shape='circle')
            if temp[key]['start']:
                state.edge('', key, arrowsize='0.75')
            for k,v in temp[key].items():
                if not isinstance(v, bool):
                    state.edge(key, v, label=str(k), arrowsize='0.75')
        return state
