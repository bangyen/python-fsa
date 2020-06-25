from graphviz import Digraph


class StateMach:
    def __init__(self, fsa):
        self.fsa = fsa

        start_num = sum(self.fsa[k]["start"] for k in self.fsa)
        trans_num = sum(
            any(isinstance(v, list) for v in self.fsa[k].values()) for k in self.fsa
        )

        if start_num != 1 or trans_num > 0:
            self.to_dfa()
        else:
            self.state = [k for k in fsa if fsa[k]["start"]][0]
            self.accept = self.fsa[self.state]["accept"]

        self.is_min = False
        self.norm()

    def __call__(self, *arg):
        if isinstance(arg[0], list):
            arg = arg[0]
        for k in arg:
            self.state = self.fsa[self.state][k]
        self.accept = self.fsa[self.state]["accept"]
        return self

    def __str__(self):
        dct = "\n".join(f"{k}: {v}" for k, v in self.fsa.items())
        dct = dct.replace("True", "True ").replace("'", "").replace(", ", ",\t")
        return dct.replace("{", "| ").replace("}", " |")

    # Creates a StateMach object of an FSA that checks if a number is divisible by num in a particular base.
    @staticmethod
    def div_by(base, num):
        def trans(k):
            return {n: f"S{(base * k + n) % num}" for n in range(base)}

        fsa = {f"S{k}": trans(k) for k in range(num)}
        for k in fsa:
            fsa[k].update({"start": False, "accept": False})
        fsa["S0"]["start"] = fsa["S0"]["accept"] = True
        return StateMach(fsa)

    # Normalizes an FSA by renaming states.
    def norm(self):
        keys = sorted([k for k in self.fsa], key=lambda x: int(x[1:]))
        key_dict = {k: f"S{keys.index(k)}" for k in keys}
        key_dict.update({True: True, False: False})
        temp = {}
        for k, v in self.fsa.items():
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
        accept = [int(k[1:]) for k in self.fsa if self.fsa[k]["accept"]]

        def diff(i, j):
            return ((i in accept) + (j in accept)) % 2

        table = [[diff(i, j) for i in range(size)] for j in range(size)]
        # Fills the table.
        while copy != table:
            copy = [k[:] for k in table]
            for i in range(size):
                for j in range(size):
                    if not table[i][j] and i != j:
                        for k, v in self.fsa[f"S{i}"].items():
                            if not isinstance(v, bool):
                                x = self.fsa[f"S{i}"][k]
                                y = self.fsa[f"S{j}"][k]
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
        for states in [sorted(sets) for sets in sim]:
            for state in states[1:]:
                redundant.update({f"S{state}": f"S{states[0]}"})
                del self.fsa[f"S{state}"]
        for key in self.fsa:
            for sec_key in self.fsa[key]:
                if self.fsa[key][sec_key] in redundant:
                    self.fsa[key][sec_key] = redundant[self.fsa[key][sec_key]]
        self.norm()
        self.is_min = True
        return self

    def to_dfa(self):
        ...

    # Creates a visual representation of the FSA using Graphviz.
    def graph(self, space=False, circle=False):
        # Groups similar state transitions. Not necessary for small alphabets or large FSAs (many states).
        temp = {}
        for k in self.fsa:
            values = set(val for val in self.fsa[k].values() if type(val) is not bool)

            def sort_func(x):
                return x if isinstance(x, int) else ord(x)

            new = {}
            for v in values:
                i_sort = sorted(
                    [j for j in self.fsa[k] if self.fsa[k][j] == v], key=sort_func
                )
                inputs = (
                    ("," + " " * space).join(str(i) for i in i_sort)
                    if len(i_sort) > 1
                    else i_sort[0]
                )
                new.update({inputs: v})
            new.update({"start": self.fsa[k]["start"], "accept": self.fsa[k]["accept"]})
            temp[k] = new
        # Creates the actual graph.
        state = Digraph()
        if circle:
            state.attr(rankdir="LR", size="8,5", layout="circo")
        else:
            state.attr(rankdir="LR", size="8,5")
        state.node("", shape="none", height="0", width="0")
        for key in temp:
            if temp[key]["accept"]:
                state.node(key, shape="doublecircle")
            else:
                state.node(key, shape="circle")
            if temp[key]["start"]:
                state.edge("", key, arrowsize="0.75")
            for k, v in temp[key].items():
                if not isinstance(v, bool):
                    state.edge(key, v, label=str(k), arrowsize="0.75")
        return state
