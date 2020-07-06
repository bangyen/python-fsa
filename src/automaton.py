from graphviz import Digraph


class StateMach:
    def __init__(self, fsa):
        """
        Initializes the object with its FSA, sets initial values, then normalizes it.

        :param fsa: The dictionary representation of the FSA.
        """
        self.fsa = fsa

        # start_num = sum(self.fsa[key]["start"] for key in self.fsa)
        # trans_num = sum(
        #     any(isinstance(val, list) for val in self.fsa[key].values())
        #     for key in self.fsa
        # )

        self.state = [key for key in fsa if fsa[key]["start"]][0]
        self.accept = self.fsa[self.state]["accept"]

        self.is_min = False
        self.norm()

    def __call__(self, *arg):
        """
        Accepts an input which is passed through the FSA,
        changing the current state and whether the word is accepted.

        :param arg: Either an int, multiple ints, or a list of ints.
        :return: Returns self so as to allow multiple calls.
        """
        if isinstance(arg[0], list):
            arg = arg[0]
        for num in arg:
            self.state = self.fsa[self.state][num]
        self.accept = self.fsa[self.state]["accept"]
        return self

    def __str__(self):
        """
        Creates a table, where the left-hand side is the current state
        and the right hand side is the associated information.

        :return: Returns a more readable version of the FSA.
        """
        dct = "\n".join(f"{key}: {val}" for key, val in self.fsa.items())
        dct = dct.replace("True", "True ").replace("'", "").replace(", ", ",\t")
        return dct.replace("{", "| ").replace("}", " |")

    # Creates a StateMach object of an FSA that checks if a number is divisible by num in a particular base.
    @staticmethod
    def div_by(base, num):
        def trans(state):
            return {sym: f"S{(base * state + sym) % num}" for sym in range(base)}

        fsa = {f"S{state}": trans(state) for state in range(num)}
        for key in fsa:
            fsa[key].update({"start": False, "accept": False})
        fsa["S0"]["start"] = fsa["S0"]["accept"] = True
        return StateMach(fsa)

    # Combines states of an NFA.
    def combine(self, *keys):
        new_key = "{%s}" % ",".join(sorted(keys)).replace("{", "").replace("}", "")
        new_val = {}
        for sec_key in set().union(*[set(self.fsa[key]) for key in keys]):
            states = set()
            if sec_key not in ["start", "accept"]:
                for key in keys:
                    states.add(self.fsa[key][sec_key])
                states = sorted(states)[0] if len(states) == 1 else sorted(states)
            else:
                states = any(self.fsa[key][sec_key] for key in keys)
            new_val.update({sec_key: states})
        return {new_key: new_val}

    # Normalizes an FSA by renaming states.
    def norm(self):
        key_list = sorted([key for key in self.fsa], key=lambda key: int(key[1:]))
        trans_dict = {key: f"S{key_list.index(key)}" for key in key_list}
        trans_dict.update({True: True, False: False})
        temp = {}
        for key, val in self.fsa.items():
            temp[trans_dict[key]] = val
            for sec_key in val:
                temp[trans_dict[key]][sec_key] = trans_dict[val[sec_key]]
        self.fsa = temp
        return self

    # Groups similar state transitions. Not necessary for small alphabets or large FSAs (many states).
    def arrow_min(self, space=False):
        temp = {}
        for key in self.fsa:
            trans = self.fsa[key]
            values = set(trans.values()) - {True, False}

            def sort_func(value):
                return value if isinstance(value, int) else ord(value)

            new = {}
            for val in values:
                sec_list = [sec_key for sec_key in trans if trans[sec_key] == val]
                key_sort = sorted(sec_list, key=sort_func)
                inputs = (
                    ("," + " " * space).join(str(sec_key) for sec_key in key_sort)
                    if len(key_sort) > 1
                    else key_sort[0]
                )
                new.update({inputs: val})
            new.update({"start": trans["start"], "accept": trans["accept"]})
            temp[key] = new
        return temp

    # Removes unreachable states.
    def remove(self):
        reach = True
        while reach:
            reach = False
            values = set()
            for val in self.fsa.values():
                values |= set(val.values())
            for key in self.fsa:
                if key not in values:
                    del self.fsa[key]
                    reach = True
                    break
        return self
    
    # Minimizes the FSA using the table-filling algorithm.
    def fsa_min(self):
        if self.is_min:
            return self
        self.remove()
        self.norm()
        # Divides states into accepting and non-accepting.
        copy, size = 0, len(self.fsa)
        accept = [int(key[1:]) for key in self.fsa if self.fsa[key]["accept"]]

        def diff(row, col):
            return ((row in accept) + (col in accept)) % 2

        table = [[diff(row, col) for row in range(size)] for col in range(size)]
        # Fills the table.
        while copy != table:
            copy = [row[:] for row in table]
            for row in range(size):
                for col in range(size):
                    if not table[row][col] and row != col:
                        for key, val in self.fsa[f"S{row}"].items():
                            if not isinstance(val, bool):
                                state_one = int(self.fsa[f"S{row}"][key][1:])
                                state_two = int(self.fsa[f"S{col}"][key][1:])
                                if table[state_one][state_two]:
                                    table[row][col] = table[col][row] = 1
        # Creates a set of tuples of similar states.
        sim = set()
        for row in range(size):
            for col in range(row):
                if not table[row][col]:
                    sim.add((col, row))
        sim = list(map(set, sim))
        # Joins sets together until all sets are pairwise disjoint.
        unmerged = True
        while unmerged:
            unmerged = False
            results = []
            while sim:
                common, rest = sim[0], sim[1:]
                sim = []
                for group in rest:
                    if group.isdisjoint(common):
                        sim.append(group)
                    else:
                        unmerged = True
                        common |= group
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

    # Creates a visual representation of the FSA using Graphviz.
    def graph(self, space=False, circle=False):
        temp = self.arrow_min(space)
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
            for sec_key, val in temp[key].items():
                if not isinstance(val, bool):
                    state.edge(key, val, label=str(sec_key), arrowsize="0.75")
        return state
