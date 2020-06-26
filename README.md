# Python State Machine
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f7f5afb6b8414c74b4ea46cf3d49cb34)](https://app.codacy.com/manual/bangyen99/python-fsa?utm_source=github.com&utm_medium=referral&utm_content=bangyen/python-fsa&utm_campaign=Badge_Grade_Dashboard)
[![CodeFactor](https://www.codefactor.io/repository/github/bangyen/python-fsa/badge)](https://www.codefactor.io/repository/github/bangyen/python-fsa)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\
A Python class implementation of deterministic finite-state machines.

## Format
Using an finite-state automaton that checks if a binary number is divisible by three as an example, DFAs will be represented as follows:
```python
divisible = {
    'S0': {0: 'S0', 1: 'S1', 'start': True , 'accept': True },
    'S1': {0: 'S2', 1: 'S0', 'start': False, 'accept': False},
    'S2': {0: 'S1', 1: 'S2', 'start': False, 'accept': False}
}
```
Each key represents a different state, and each value contains a dictionary with the following information: the new state upon reception of a particular input, whether a state is the starting state, and whether a state is an accepting state. For NFAs, if an input has multiple new states, the new states will be represented as a list. ε-moves will be represented as a new key.

Additionally, the matrix representation of the directed graph corresponding to the aforementioned FSA is as follows:
```python
div_matrix = [
    [0, 1, ()],
    [1, (), 0],
    [(), 0, 1]
]
```
The ij-th entry indicates which symbols cause a transition from the i-th state to the j-th state. If an entry is the empty tuple, nothing causes a transition between the two. Notation adapted from: 'Generalized transition matrix of a sequential machine and its applications' - T.Kameda

## Coverage
<div id="header">

<div class="content">

# Coverage for **automaton.py** : <span class="pc_cov">97%</span>

![Show keyboard shortcuts](keybd_closed.png)

## 152 statements   <span class="run shortkey_r button_toggle_run">148 run</span> <span class="mis show_mis shortkey_m button_toggle_mis">4 missing</span> <span class="exc show_exc shortkey_x button_toggle_exc">0 excluded</span>

</div>

</div>

<div class="help_panel">![Hide keyboard shortcuts](keybd_open.png)

Hot-keys on this page

<div>

<span class="key">r</span> <span class="key">m</span> <span class="key">x</span> <span class="key">p</span>   toggle line displays

<span class="key">j</span> <span class="key">k</span>   next/prev highlighted chunk

<span class="key">0</span>   (zero) top of page

<span class="key">1</span>   (one) first highlighted chunk

</div>

</div>

<div id="source">

<span class="n">[1](#t1)</span><span class="t"><span class="key">import</span> <span class="nam">os</span> </span><span class="r"></span>

<span class="n">[2](#t2)</span><span class="t"><span class="key">from</span> <span class="nam">graphviz</span> <span class="key">import</span> <span class="nam">Digraph</span> </span><span class="r"></span>

<span class="n">[3](#t3)</span><span class="t"> </span><span class="r"></span>

<span class="n">[4](#t4)</span><span class="t"><span class="nam">os</span><span class="op">.</span><span class="nam">environ</span><span class="op">[</span><span class="str">"PATH"</span><span class="op">]</span> <span class="op">+=</span> <span class="op">(</span> </span><span class="r"></span>

<span class="n">[5](#t5)</span> <span class="t"><span class="nam">os</span><span class="op">.</span><span class="nam">pathsep</span> <span class="op">+</span> <span class="str">r"C:/.../graphviz/bin"</span></span><span class="r"></span>

<span class="n">[6](#t6)</span><span class="t"><span class="op">)</span> </span><span class="r"></span>

<span class="n">[7](#t7)</span><span class="t"> </span><span class="r"></span>

<span class="n">[8](#t8)</span><span class="t"> </span><span class="r"></span>

<span class="n">[9](#t9)</span><span class="t"><span class="key">class</span> <span class="nam">StateMach</span><span class="op">:</span> </span><span class="r"></span>

<span class="n">[10](#t10)</span> <span class="t"><span class="key">def</span> <span class="nam">__init__</span><span class="op">(</span><span class="nam">self</span><span class="op">,</span> <span class="nam">fsa</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[11](#t11)</span> <span class="t"><span class="str">"""</span></span><span class="r"></span>

<span class="n">[12](#t12)</span><span class="t"> <span class="str">Initializes the StateMach object with its FSA,</span> </span><span class="r"></span>

<span class="n">[13](#t13)</span><span class="t"> <span class="str">converts NFAs to DFAs, sets the initial state,</span> </span><span class="r"></span>

<span class="n">[14](#t14)</span><span class="t"> <span class="str">sets the initial acceptance value, then normalizes it.</span> </span><span class="r"></span>

<span class="n">[15](#t15)</span><span class="t"> <span class="str">:param fsa: The dictionary representation of the FSA.</span> </span><span class="r"></span>

<span class="n">[16](#t16)</span><span class="t"> <span class="str">"""</span> </span><span class="r"></span>

<span class="n">[17](#t17)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span> <span class="op">=</span> <span class="nam">fsa</span></span><span class="r"></span>

<span class="n">[18](#t18)</span><span class="t"> </span><span class="r"></span>

<span class="n">[19](#t19)</span> <span class="t"><span class="com"># start_num = sum(self.fsa[key]["start"] for key in self.fsa)</span></span><span class="r"></span>

<span class="n">[20](#t20)</span> <span class="t"><span class="com"># trans_num = sum(</span></span><span class="r"></span>

<span class="n">[21](#t21)</span> <span class="t"><span class="com"># any(isinstance(val, list) for val in self.fsa[key].values())</span></span><span class="r"></span>

<span class="n">[22](#t22)</span> <span class="t"><span class="com"># for key in self.fsa</span></span><span class="r"></span>

<span class="n">[23](#t23)</span> <span class="t"><span class="com"># )</span></span><span class="r"></span>

<span class="n">[24](#t24)</span><span class="t"> </span><span class="r"></span>

<span class="n">[25](#t25)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">state</span> <span class="op">=</span> <span class="op">[</span><span class="nam">key</span> <span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">fsa</span> <span class="key">if</span> <span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="str">"start"</span><span class="op">]</span><span class="op">]</span><span class="op">[</span><span class="num">0</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[26](#t26)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">accept</span> <span class="op">=</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">self</span><span class="op">.</span><span class="nam">state</span><span class="op">]</span><span class="op">[</span><span class="str">"accept"</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[27](#t27)</span><span class="t"> </span><span class="r"></span>

<span class="n">[28](#t28)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">is_min</span> <span class="op">=</span> <span class="key">False</span></span><span class="r"></span>

<span class="n">[29](#t29)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">norm</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[30](#t30)</span><span class="t"> </span><span class="r"></span>

<span class="n">[31](#t31)</span> <span class="t"><span class="key">def</span> <span class="nam">__call__</span><span class="op">(</span><span class="nam">self</span><span class="op">,</span> <span class="op">*</span><span class="nam">arg</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[32](#t32)</span> <span class="t"><span class="str">"""</span></span><span class="r"></span>

<span class="n">[33](#t33)</span><span class="t"> <span class="str">Accepts an input which is passed through the FSA,</span> </span><span class="r"></span>

<span class="n">[34](#t34)</span><span class="t"> <span class="str">changing the current state and whether the word is accepted.</span> </span><span class="r"></span>

<span class="n">[35](#t35)</span><span class="t"> <span class="str">:param arg: Either an int, multiple ints, or a list of ints.</span> </span><span class="r"></span>

<span class="n">[36](#t36)</span><span class="t"> <span class="str">:return: Returns self so as to allow multiple calls.</span> </span><span class="r"></span>

<span class="n">[37](#t37)</span><span class="t"> <span class="str">"""</span> </span><span class="r"></span>

<span class="n">[38](#t38)</span> <span class="t"><span class="key">if</span> <span class="nam">isinstance</span><span class="op">(</span><span class="nam">arg</span><span class="op">[</span><span class="num">0</span><span class="op">]</span><span class="op">,</span> <span class="nam">list</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[39](#t39)</span> <span class="t"><span class="nam">arg</span> <span class="op">=</span> <span class="nam">arg</span><span class="op">[</span><span class="num">0</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[40](#t40)</span> <span class="t"><span class="key">for</span> <span class="nam">num</span> <span class="key">in</span> <span class="nam">arg</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[41](#t41)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">state</span> <span class="op">=</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">self</span><span class="op">.</span><span class="nam">state</span><span class="op">]</span><span class="op">[</span><span class="nam">num</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[42](#t42)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">accept</span> <span class="op">=</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">self</span><span class="op">.</span><span class="nam">state</span><span class="op">]</span><span class="op">[</span><span class="str">"accept"</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[43](#t43)</span> <span class="t"><span class="key">return</span> <span class="nam">self</span></span><span class="r"></span>

<span class="n">[44](#t44)</span><span class="t"> </span><span class="r"></span>

<span class="n">[45](#t45)</span> <span class="t"><span class="key">def</span> <span class="nam">__str__</span><span class="op">(</span><span class="nam">self</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[46](#t46)</span> <span class="t"><span class="str">"""</span></span><span class="r"></span>

<span class="n">[47](#t47)</span><span class="t"> <span class="str">Creates a table, where the left-hand side is the current state</span> </span><span class="r"></span>

<span class="n">[48](#t48)</span><span class="t"> <span class="str">and the right hand side is the associated information.</span> </span><span class="r"></span>

<span class="n">[49](#t49)</span><span class="t"> <span class="str">:return: Returns a more readable version of the FSA.</span> </span><span class="r"></span>

<span class="n">[50](#t50)</span><span class="t"> <span class="str">"""</span> </span><span class="r"></span>

<span class="n">[51](#t51)</span> <span class="t"><span class="nam">dct</span> <span class="op">=</span> <span class="str">"\n"</span><span class="op">.</span><span class="nam">join</span><span class="op">(</span><span class="str">f"{key}: {val}"</span> <span class="key">for</span> <span class="nam">key</span><span class="op">,</span> <span class="nam">val</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">.</span><span class="nam">items</span><span class="op">(</span><span class="op">)</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[52](#t52)</span> <span class="t"><span class="nam">dct</span> <span class="op">=</span> <span class="nam">dct</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">"True"</span><span class="op">,</span> <span class="str">"True "</span><span class="op">)</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">"'"</span><span class="op">,</span> <span class="str">""</span><span class="op">)</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">", "</span><span class="op">,</span> <span class="str">",\t"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[53](#t53)</span> <span class="t"><span class="key">return</span> <span class="nam">dct</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">"{"</span><span class="op">,</span> <span class="str">"| "</span><span class="op">)</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">"}"</span><span class="op">,</span> <span class="str">" |"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[54](#t54)</span><span class="t"> </span><span class="r"></span>

<span class="n">[55](#t55)</span> <span class="t"><span class="com"># Creates a StateMach object of an FSA that checks if a number is divisible by num in a particular base.</span></span><span class="r"></span>

<span class="n">[56](#t56)</span> <span class="t"><span class="op">@</span><span class="nam">staticmethod</span></span><span class="r"></span>

<span class="n">[57](#t57)</span> <span class="t"><span class="key">def</span> <span class="nam">div_by</span><span class="op">(</span><span class="nam">base</span><span class="op">,</span> <span class="nam">num</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[58](#t58)</span> <span class="t"><span class="key">def</span> <span class="nam">trans</span><span class="op">(</span><span class="nam">state</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[59](#t59)</span> <span class="t"><span class="key">return</span> <span class="op">{</span><span class="nam">sym</span><span class="op">:</span> <span class="str">f"S{(base * state + sym) % num}"</span> <span class="key">for</span> <span class="nam">sym</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">base</span><span class="op">)</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[60](#t60)</span><span class="t"> </span><span class="r"></span>

<span class="n">[61](#t61)</span> <span class="t"><span class="nam">fsa</span> <span class="op">=</span> <span class="op">{</span><span class="str">f"S{state}"</span><span class="op">:</span> <span class="nam">trans</span><span class="op">(</span><span class="nam">state</span><span class="op">)</span> <span class="key">for</span> <span class="nam">state</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">num</span><span class="op">)</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[62](#t62)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">fsa</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[63](#t63)</span> <span class="t"><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">.</span><span class="nam">update</span><span class="op">(</span><span class="op">{</span><span class="str">"start"</span><span class="op">:</span> <span class="key">False</span><span class="op">,</span> <span class="str">"accept"</span><span class="op">:</span> <span class="key">False</span><span class="op">}</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[64](#t64)</span> <span class="t"><span class="nam">fsa</span><span class="op">[</span><span class="str">"S0"</span><span class="op">]</span><span class="op">[</span><span class="str">"start"</span><span class="op">]</span> <span class="op">=</span> <span class="nam">fsa</span><span class="op">[</span><span class="str">"S0"</span><span class="op">]</span><span class="op">[</span><span class="str">"accept"</span><span class="op">]</span> <span class="op">=</span> <span class="key">True</span></span><span class="r"></span>

<span class="n">[65](#t65)</span> <span class="t"><span class="key">return</span> <span class="nam">StateMach</span><span class="op">(</span><span class="nam">fsa</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[66](#t66)</span><span class="t"> </span><span class="r"></span>

<span class="n">[67](#t67)</span> <span class="t"><span class="com"># Combines states of an NFA.</span></span><span class="r"></span>

<span class="n">[68](#t68)</span> <span class="t"><span class="key">def</span> <span class="nam">combine</span><span class="op">(</span><span class="nam">self</span><span class="op">,</span> <span class="op">*</span><span class="nam">keys</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[69](#t69)</span> <span class="t"><span class="nam">new_key</span> <span class="op">=</span> <span class="str">"{%s}"</span> <span class="op">%</span> <span class="str">","</span><span class="op">.</span><span class="nam">join</span><span class="op">(</span><span class="nam">sorted</span><span class="op">(</span><span class="nam">keys</span><span class="op">)</span><span class="op">)</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">"{"</span><span class="op">,</span> <span class="str">""</span><span class="op">)</span><span class="op">.</span><span class="nam">replace</span><span class="op">(</span><span class="str">"}"</span><span class="op">,</span> <span class="str">""</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[70](#t70)</span> <span class="t"><span class="nam">new_val</span> <span class="op">=</span> <span class="op">{</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[71](#t71)</span> <span class="t"><span class="key">for</span> <span class="nam">sec_key</span> <span class="key">in</span> <span class="nam">set</span><span class="op">(</span><span class="op">)</span><span class="op">.</span><span class="nam">union</span><span class="op">(</span><span class="op">*</span><span class="op">[</span><span class="nam">set</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">)</span> <span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">keys</span><span class="op">]</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[72](#t72)</span> <span class="t"><span class="nam">states</span> <span class="op">=</span> <span class="nam">set</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[73](#t73)</span> <span class="t"><span class="key">if</span> <span class="nam">sec_key</span> <span class="key">not</span> <span class="key">in</span> <span class="op">[</span><span class="str">"start"</span><span class="op">,</span> <span class="str">"accept"</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[74](#t74)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">keys</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[75](#t75)</span> <span class="t"><span class="nam">states</span><span class="op">.</span><span class="nam">add</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[76](#t76)</span> <span class="t"><span class="nam">states</span> <span class="op">=</span> <span class="nam">sorted</span><span class="op">(</span><span class="nam">states</span><span class="op">)</span><span class="op">[</span><span class="num">0</span><span class="op">]</span> <span class="key">if</span> <span class="nam">len</span><span class="op">(</span><span class="nam">states</span><span class="op">)</span> <span class="op">==</span> <span class="num">1</span> <span class="key">else</span> <span class="nam">sorted</span><span class="op">(</span><span class="nam">states</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[77](#t77)</span> <span class="t"><span class="key">else</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[78](#t78)</span> <span class="t"><span class="nam">states</span> <span class="op">=</span> <span class="nam">any</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span> <span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">keys</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[79](#t79)</span> <span class="t"><span class="nam">new_val</span><span class="op">.</span><span class="nam">update</span><span class="op">(</span><span class="op">{</span><span class="nam">sec_key</span><span class="op">:</span> <span class="nam">states</span><span class="op">}</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[80](#t80)</span> <span class="t"><span class="key">return</span> <span class="op">{</span><span class="nam">new_key</span><span class="op">:</span> <span class="nam">new_val</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[81](#t81)</span><span class="t"> </span><span class="r"></span>

<span class="n">[82](#t82)</span> <span class="t"><span class="com"># Normalizes an FSA by renaming states.</span></span><span class="r"></span>

<span class="n">[83](#t83)</span> <span class="t"><span class="key">def</span> <span class="nam">norm</span><span class="op">(</span><span class="nam">self</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[84](#t84)</span> <span class="t"><span class="nam">key_list</span> <span class="op">=</span> <span class="nam">sorted</span><span class="op">(</span><span class="op">[</span><span class="nam">key</span> <span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">]</span><span class="op">,</span> <span class="nam">key</span><span class="op">=</span><span class="key">lambda</span> <span class="nam">key</span><span class="op">:</span> <span class="nam">int</span><span class="op">(</span><span class="nam">key</span><span class="op">[</span><span class="num">1</span><span class="op">:</span><span class="op">]</span><span class="op">)</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[85](#t85)</span> <span class="t"><span class="nam">trans_dict</span> <span class="op">=</span> <span class="op">{</span><span class="nam">key</span><span class="op">:</span> <span class="str">f"S{key_list.index(key)}"</span> <span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">key_list</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[86](#t86)</span> <span class="t"><span class="nam">trans_dict</span><span class="op">.</span><span class="nam">update</span><span class="op">(</span><span class="op">{</span><span class="key">True</span><span class="op">:</span> <span class="key">True</span><span class="op">,</span> <span class="key">False</span><span class="op">:</span> <span class="key">False</span><span class="op">}</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[87](#t87)</span> <span class="t"><span class="nam">temp</span> <span class="op">=</span> <span class="op">{</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[88](#t88)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span><span class="op">,</span> <span class="nam">val</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">.</span><span class="nam">items</span><span class="op">(</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[89](#t89)</span> <span class="t"><span class="nam">temp</span><span class="op">[</span><span class="nam">trans_dict</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">]</span> <span class="op">=</span> <span class="nam">val</span></span><span class="r"></span>

<span class="n">[90](#t90)</span> <span class="t"><span class="key">for</span> <span class="nam">sec_key</span> <span class="key">in</span> <span class="nam">val</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[91](#t91)</span> <span class="t"><span class="nam">temp</span><span class="op">[</span><span class="nam">trans_dict</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">]</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span> <span class="op">=</span> <span class="nam">trans_dict</span><span class="op">[</span><span class="nam">val</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[92](#t92)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span> <span class="op">=</span> <span class="nam">temp</span></span><span class="r"></span>

<span class="n">[93](#t93)</span> <span class="t"><span class="key">return</span> <span class="nam">self</span></span><span class="r"></span>

<span class="n">[94](#t94)</span><span class="t"> </span><span class="r"></span>

<span class="n">[95](#t95)</span> <span class="t"><span class="com"># Groups similar state transitions. Not necessary for small alphabets or large FSAs (many states).</span></span><span class="r"></span>

<span class="n">[96](#t96)</span> <span class="t"><span class="key">def</span> <span class="nam">arrow_min</span><span class="op">(</span><span class="nam">self</span><span class="op">,</span> <span class="nam">space</span><span class="op">=</span><span class="key">False</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[97](#t97)</span> <span class="t"><span class="nam">temp</span> <span class="op">=</span> <span class="op">{</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[98](#t98)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[99](#t99)</span> <span class="t"><span class="nam">trans</span> <span class="op">=</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[100](#t100)</span> <span class="t"><span class="nam">values</span> <span class="op">=</span> <span class="nam">set</span><span class="op">(</span><span class="nam">trans</span><span class="op">.</span><span class="nam">values</span><span class="op">(</span><span class="op">)</span><span class="op">)</span> <span class="op">-</span> <span class="op">{</span><span class="key">True</span><span class="op">,</span> <span class="key">False</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[101](#t101)</span><span class="t"> </span><span class="r"></span>

<span class="n">[102](#t102)</span> <span class="t"><span class="key">def</span> <span class="nam">sort_func</span><span class="op">(</span><span class="nam">value</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[103](#t103)</span> <span class="t"><span class="key">return</span> <span class="nam">value</span> <span class="key">if</span> <span class="nam">isinstance</span><span class="op">(</span><span class="nam">value</span><span class="op">,</span> <span class="nam">int</span><span class="op">)</span> <span class="key">else</span> <span class="nam">ord</span><span class="op">(</span><span class="nam">value</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[104](#t104)</span><span class="t"> </span><span class="r"></span>

<span class="n">[105](#t105)</span> <span class="t"><span class="nam">new</span> <span class="op">=</span> <span class="op">{</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[106](#t106)</span> <span class="t"><span class="key">for</span> <span class="nam">val</span> <span class="key">in</span> <span class="nam">values</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[107](#t107)</span> <span class="t"><span class="nam">sec_list</span> <span class="op">=</span> <span class="op">[</span><span class="nam">sec_key</span> <span class="key">for</span> <span class="nam">sec_key</span> <span class="key">in</span> <span class="nam">trans</span> <span class="key">if</span> <span class="nam">trans</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span> <span class="op">==</span> <span class="nam">val</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[108](#t108)</span> <span class="t"><span class="nam">key_sort</span> <span class="op">=</span> <span class="nam">sorted</span><span class="op">(</span><span class="nam">sec_list</span><span class="op">,</span> <span class="nam">key</span><span class="op">=</span><span class="nam">sort_func</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[109](#t109)</span> <span class="t"><span class="nam">inputs</span> <span class="op">=</span> <span class="op">(</span></span><span class="r"></span>

<span class="n">[110](#t110)</span> <span class="t"><span class="op">(</span><span class="str">","</span> <span class="op">+</span> <span class="str">" "</span> <span class="op">*</span> <span class="nam">space</span><span class="op">)</span><span class="op">.</span><span class="nam">join</span><span class="op">(</span><span class="nam">str</span><span class="op">(</span><span class="nam">sec_key</span><span class="op">)</span> <span class="key">for</span> <span class="nam">sec_key</span> <span class="key">in</span> <span class="nam">key_sort</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[111](#t111)</span> <span class="t"><span class="key">if</span> <span class="nam">len</span><span class="op">(</span><span class="nam">key_sort</span><span class="op">)</span> <span class="op">></span> <span class="num">1</span></span><span class="r"></span>

<span class="n">[112](#t112)</span> <span class="t"><span class="key">else</span> <span class="nam">key_sort</span><span class="op">[</span><span class="num">0</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[113](#t113)</span> <span class="t"><span class="op">)</span></span><span class="r"></span>

<span class="n">[114](#t114)</span> <span class="t"><span class="nam">new</span><span class="op">.</span><span class="nam">update</span><span class="op">(</span><span class="op">{</span><span class="nam">inputs</span><span class="op">:</span> <span class="nam">val</span><span class="op">}</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[115](#t115)</span> <span class="t"><span class="nam">new</span><span class="op">.</span><span class="nam">update</span><span class="op">(</span><span class="op">{</span><span class="str">"start"</span><span class="op">:</span> <span class="nam">trans</span><span class="op">[</span><span class="str">"start"</span><span class="op">]</span><span class="op">,</span> <span class="str">"accept"</span><span class="op">:</span> <span class="nam">trans</span><span class="op">[</span><span class="str">"accept"</span><span class="op">]</span><span class="op">}</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[116](#t116)</span> <span class="t"><span class="nam">temp</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span> <span class="op">=</span> <span class="nam">new</span></span><span class="r"></span>

<span class="n">[117](#t117)</span> <span class="t"><span class="key">return</span> <span class="nam">temp</span></span><span class="r"></span>

<span class="n">[118](#t118)</span><span class="t"> </span><span class="r"></span>

<span class="n">[119](#t119)</span> <span class="t"><span class="com"># Removes unreachable states.</span></span><span class="r"></span>

<span class="n">[120](#t120)</span> <span class="t"><span class="key">def</span> <span class="nam">remove</span><span class="op">(</span><span class="nam">self</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[121](#t121)</span> <span class="t"><span class="nam">reach</span> <span class="op">=</span> <span class="key">True</span></span><span class="r"></span>

<span class="n">[122](#t122)</span> <span class="t"><span class="key">while</span> <span class="nam">reach</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[123](#t123)</span> <span class="t"><span class="nam">reach</span> <span class="op">=</span> <span class="key">False</span></span><span class="r"></span>

<span class="n">[124](#t124)</span> <span class="t"><span class="nam">values</span> <span class="op">=</span> <span class="nam">set</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[125](#t125)</span> <span class="t"><span class="key">for</span> <span class="nam">val</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">.</span><span class="nam">values</span><span class="op">(</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[126](#t126)</span> <span class="t"><span class="nam">values</span> <span class="op">|=</span> <span class="nam">set</span><span class="op">(</span><span class="nam">val</span><span class="op">.</span><span class="nam">values</span><span class="op">(</span><span class="op">)</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[127](#t127)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[128](#t128)</span> <span class="t"><span class="key">if</span> <span class="nam">key</span> <span class="key">not</span> <span class="key">in</span> <span class="nam">values</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[129](#t129)</span> <span class="t"><span class="key">del</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[130](#t130)</span> <span class="t"><span class="nam">reach</span> <span class="op">=</span> <span class="key">True</span></span><span class="r"></span>

<span class="n">[131](#t131)</span> <span class="t"><span class="key">break</span></span><span class="r"></span>

<span class="n">[132](#t132)</span> <span class="t"><span class="key">return</span> <span class="nam">self</span></span><span class="r"></span>

<span class="n">[133](#t133)</span><span class="t"> </span><span class="r"></span>

<span class="n">[134](#t134)</span> <span class="t"><span class="com"># Minimizes the FSA using the table-filling algorithm.</span></span><span class="r"></span>

<span class="n">[135](#t135)</span> <span class="t"><span class="key">def</span> <span class="nam">fsa_min</span><span class="op">(</span><span class="nam">self</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[136](#t136)</span> <span class="t"><span class="key">if</span> <span class="nam">self</span><span class="op">.</span><span class="nam">is_min</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[137](#t137)</span> <span class="t"><span class="key">return</span> <span class="nam">self</span></span><span class="r"></span>

<span class="n">[138](#t138)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">remove</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[139](#t139)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">norm</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[140](#t140)</span> <span class="t"><span class="com"># Divides states into accepting and non-accepting.</span></span><span class="r"></span>

<span class="n">[141](#t141)</span> <span class="t"><span class="nam">copy</span><span class="op">,</span> <span class="nam">size</span> <span class="op">=</span> <span class="num">0</span><span class="op">,</span> <span class="nam">len</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[142](#t142)</span> <span class="t"><span class="nam">accept</span> <span class="op">=</span> <span class="op">[</span><span class="nam">int</span><span class="op">(</span><span class="nam">key</span><span class="op">[</span><span class="num">1</span><span class="op">:</span><span class="op">]</span><span class="op">)</span> <span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span> <span class="key">if</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="str">"accept"</span><span class="op">]</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[143](#t143)</span><span class="t"> </span><span class="r"></span>

<span class="n">[144](#t144)</span> <span class="t"><span class="key">def</span> <span class="nam">diff</span><span class="op">(</span><span class="nam">row</span><span class="op">,</span> <span class="nam">col</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[145](#t145)</span> <span class="t"><span class="key">return</span> <span class="op">(</span><span class="op">(</span><span class="nam">row</span> <span class="key">in</span> <span class="nam">accept</span><span class="op">)</span> <span class="op">+</span> <span class="op">(</span><span class="nam">col</span> <span class="key">in</span> <span class="nam">accept</span><span class="op">)</span><span class="op">)</span> <span class="op">%</span> <span class="num">2</span></span><span class="r"></span>

<span class="n">[146](#t146)</span><span class="t"> </span><span class="r"></span>

<span class="n">[147](#t147)</span> <span class="t"><span class="nam">table</span> <span class="op">=</span> <span class="op">[</span><span class="op">[</span><span class="nam">diff</span><span class="op">(</span><span class="nam">row</span><span class="op">,</span> <span class="nam">col</span><span class="op">)</span> <span class="key">for</span> <span class="nam">row</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">size</span><span class="op">)</span><span class="op">]</span> <span class="key">for</span> <span class="nam">col</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">size</span><span class="op">)</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[148](#t148)</span> <span class="t"><span class="com"># Fills the table.</span></span><span class="r"></span>

<span class="n">[149](#t149)</span> <span class="t"><span class="key">while</span> <span class="nam">copy</span> <span class="op">!=</span> <span class="nam">table</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[150](#t150)</span> <span class="t"><span class="nam">copy</span> <span class="op">=</span> <span class="op">[</span><span class="nam">row</span><span class="op">[</span><span class="op">:</span><span class="op">]</span> <span class="key">for</span> <span class="nam">row</span> <span class="key">in</span> <span class="nam">table</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[151](#t151)</span> <span class="t"><span class="key">for</span> <span class="nam">row</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">size</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[152](#t152)</span> <span class="t"><span class="key">for</span> <span class="nam">col</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">size</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[153](#t153)</span> <span class="t"><span class="key">if</span> <span class="key">not</span> <span class="nam">table</span><span class="op">[</span><span class="nam">row</span><span class="op">]</span><span class="op">[</span><span class="nam">col</span><span class="op">]</span> <span class="key">and</span> <span class="nam">row</span> <span class="op">!=</span> <span class="nam">col</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[154](#t154)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span><span class="op">,</span> <span class="nam">val</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="str">f"S{row}"</span><span class="op">]</span><span class="op">.</span><span class="nam">items</span><span class="op">(</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[155](#t155)</span> <span class="t"><span class="key">if</span> <span class="key">not</span> <span class="nam">isinstance</span><span class="op">(</span><span class="nam">val</span><span class="op">,</span> <span class="nam">bool</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[156](#t156)</span> <span class="t"><span class="nam">state_one</span> <span class="op">=</span> <span class="nam">int</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="str">f"S{row}"</span><span class="op">]</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="num">1</span><span class="op">:</span><span class="op">]</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[157](#t157)</span> <span class="t"><span class="nam">state_two</span> <span class="op">=</span> <span class="nam">int</span><span class="op">(</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="str">f"S{col}"</span><span class="op">]</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="num">1</span><span class="op">:</span><span class="op">]</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[158](#t158)</span> <span class="t"><span class="key">if</span> <span class="nam">table</span><span class="op">[</span><span class="nam">state_one</span><span class="op">]</span><span class="op">[</span><span class="nam">state_two</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[159](#t159)</span> <span class="t"><span class="nam">table</span><span class="op">[</span><span class="nam">row</span><span class="op">]</span><span class="op">[</span><span class="nam">col</span><span class="op">]</span> <span class="op">=</span> <span class="nam">table</span><span class="op">[</span><span class="nam">col</span><span class="op">]</span><span class="op">[</span><span class="nam">row</span><span class="op">]</span> <span class="op">=</span> <span class="num">1</span></span><span class="r"></span>

<span class="n">[160](#t160)</span> <span class="t"><span class="com"># Creates a set of tuples of similar states.</span></span><span class="r"></span>

<span class="n">[161](#t161)</span> <span class="t"><span class="nam">sim</span> <span class="op">=</span> <span class="nam">set</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[162](#t162)</span> <span class="t"><span class="key">for</span> <span class="nam">row</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">size</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[163](#t163)</span> <span class="t"><span class="key">for</span> <span class="nam">col</span> <span class="key">in</span> <span class="nam">range</span><span class="op">(</span><span class="nam">row</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[164](#t164)</span> <span class="t"><span class="key">if</span> <span class="key">not</span> <span class="nam">table</span><span class="op">[</span><span class="nam">row</span><span class="op">]</span><span class="op">[</span><span class="nam">col</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[165](#t165)</span> <span class="t"><span class="nam">sim</span><span class="op">.</span><span class="nam">add</span><span class="op">(</span><span class="op">(</span><span class="nam">col</span><span class="op">,</span> <span class="nam">row</span><span class="op">)</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[166](#t166)</span> <span class="t"><span class="nam">sim</span> <span class="op">=</span> <span class="nam">list</span><span class="op">(</span><span class="nam">map</span><span class="op">(</span><span class="nam">set</span><span class="op">,</span> <span class="nam">sim</span><span class="op">)</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[167](#t167)</span> <span class="t"><span class="com"># Joins sets together until all sets are pairwise disjoint.</span></span><span class="r"></span>

<span class="n">[168](#t168)</span> <span class="t"><span class="nam">unmerged</span> <span class="op">=</span> <span class="key">True</span></span><span class="r"></span>

<span class="n">[169](#t169)</span> <span class="t"><span class="key">while</span> <span class="nam">unmerged</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[170](#t170)</span> <span class="t"><span class="nam">unmerged</span> <span class="op">=</span> <span class="key">False</span></span><span class="r"></span>

<span class="n">[171](#t171)</span> <span class="t"><span class="nam">results</span> <span class="op">=</span> <span class="op">[</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[172](#t172)</span> <span class="t"><span class="key">while</span> <span class="nam">sim</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[173](#t173)</span> <span class="t"><span class="nam">common</span><span class="op">,</span> <span class="nam">rest</span> <span class="op">=</span> <span class="nam">sim</span><span class="op">[</span><span class="num">0</span><span class="op">]</span><span class="op">,</span> <span class="nam">sim</span><span class="op">[</span><span class="num">1</span><span class="op">:</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[174](#t174)</span> <span class="t"><span class="nam">sim</span> <span class="op">=</span> <span class="op">[</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[175](#t175)</span> <span class="t"><span class="key">for</span> <span class="nam">group</span> <span class="key">in</span> <span class="nam">rest</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[176](#t176)</span> <span class="t"><span class="key">if</span> <span class="nam">group</span><span class="op">.</span><span class="nam">isdisjoint</span><span class="op">(</span><span class="nam">common</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[177](#t177)</span> <span class="t"><span class="nam">sim</span><span class="op">.</span><span class="nam">append</span><span class="op">(</span><span class="nam">group</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[178](#t178)</span> <span class="t"><span class="key">else</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[179](#t179)</span> <span class="t"><span class="nam">unmerged</span> <span class="op">=</span> <span class="key">True</span></span><span class="r"></span>

<span class="n">[180](#t180)</span> <span class="t"><span class="nam">common</span> <span class="op">|=</span> <span class="nam">group</span></span><span class="r"></span>

<span class="n">[181](#t181)</span> <span class="t"><span class="nam">results</span><span class="op">.</span><span class="nam">append</span><span class="op">(</span><span class="nam">common</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[182](#t182)</span> <span class="t"><span class="nam">sim</span> <span class="op">=</span> <span class="nam">results</span></span><span class="r"></span>

<span class="n">[183](#t183)</span> <span class="t"><span class="com"># Replaces redundant states.</span></span><span class="r"></span>

<span class="n">[184](#t184)</span> <span class="t"><span class="nam">redundant</span> <span class="op">=</span> <span class="op">{</span><span class="op">}</span></span><span class="r"></span>

<span class="n">[185](#t185)</span> <span class="t"><span class="key">for</span> <span class="nam">states</span> <span class="key">in</span> <span class="op">[</span><span class="nam">sorted</span><span class="op">(</span><span class="nam">sets</span><span class="op">)</span> <span class="key">for</span> <span class="nam">sets</span> <span class="key">in</span> <span class="nam">sim</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[186](#t186)</span> <span class="t"><span class="key">for</span> <span class="nam">state</span> <span class="key">in</span> <span class="nam">states</span><span class="op">[</span><span class="num">1</span><span class="op">:</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[187](#t187)</span> <span class="t"><span class="nam">redundant</span><span class="op">.</span><span class="nam">update</span><span class="op">(</span><span class="op">{</span><span class="str">f"S{state}"</span><span class="op">:</span> <span class="str">f"S{states[0]}"</span><span class="op">}</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[188](#t188)</span> <span class="t"><span class="key">del</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="str">f"S{state}"</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[189](#t189)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[190](#t190)</span> <span class="t"><span class="key">for</span> <span class="nam">sec_key</span> <span class="key">in</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[191](#t191)</span> <span class="t"><span class="key">if</span> <span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span> <span class="key">in</span> <span class="nam">redundant</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[192](#t192)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span> <span class="op">=</span> <span class="nam">redundant</span><span class="op">[</span><span class="nam">self</span><span class="op">.</span><span class="nam">fsa</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="nam">sec_key</span><span class="op">]</span><span class="op">]</span></span><span class="r"></span>

<span class="n">[193](#t193)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">norm</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[194](#t194)</span> <span class="t"><span class="nam">self</span><span class="op">.</span><span class="nam">is_min</span> <span class="op">=</span> <span class="key">True</span></span><span class="r"></span>

<span class="n">[195](#t195)</span> <span class="t"><span class="key">return</span> <span class="nam">self</span></span><span class="r"></span>

<span class="n">[196](#t196)</span><span class="t"> </span><span class="r"></span>

<span class="n">[197](#t197)</span> <span class="t"><span class="com"># Creates a visual representation of the FSA using Graphviz.</span></span><span class="r"></span>

<span class="n">[198](#t198)</span> <span class="t"><span class="key">def</span> <span class="nam">graph</span><span class="op">(</span><span class="nam">self</span><span class="op">,</span> <span class="nam">space</span><span class="op">=</span><span class="key">False</span><span class="op">,</span> <span class="nam">circle</span><span class="op">=</span><span class="key">False</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[199](#t199)</span> <span class="t"><span class="nam">temp</span> <span class="op">=</span> <span class="nam">self</span><span class="op">.</span><span class="nam">arrow_min</span><span class="op">(</span><span class="nam">space</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[200](#t200)</span> <span class="t"><span class="com"># Creates the actual graph.</span></span><span class="r"></span>

<span class="n">[201](#t201)</span> <span class="t"><span class="nam">state</span> <span class="op">=</span> <span class="nam">Digraph</span><span class="op">(</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[202](#t202)</span> <span class="t"><span class="key">if</span> <span class="nam">circle</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[203](#t203)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">attr</span><span class="op">(</span><span class="nam">rankdir</span><span class="op">=</span><span class="str">"LR"</span><span class="op">,</span> <span class="nam">size</span><span class="op">=</span><span class="str">"8,5"</span><span class="op">,</span> <span class="nam">layout</span><span class="op">=</span><span class="str">"circo"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[204](#t204)</span> <span class="t"><span class="key">else</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[205](#t205)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">attr</span><span class="op">(</span><span class="nam">rankdir</span><span class="op">=</span><span class="str">"LR"</span><span class="op">,</span> <span class="nam">size</span><span class="op">=</span><span class="str">"8,5"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[206](#t206)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">node</span><span class="op">(</span><span class="str">""</span><span class="op">,</span> <span class="nam">shape</span><span class="op">=</span><span class="str">"none"</span><span class="op">,</span> <span class="nam">height</span><span class="op">=</span><span class="str">"0"</span><span class="op">,</span> <span class="nam">width</span><span class="op">=</span><span class="str">"0"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[207](#t207)</span> <span class="t"><span class="key">for</span> <span class="nam">key</span> <span class="key">in</span> <span class="nam">temp</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[208](#t208)</span> <span class="t"><span class="key">if</span> <span class="nam">temp</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="str">"accept"</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[209](#t209)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">node</span><span class="op">(</span><span class="nam">key</span><span class="op">,</span> <span class="nam">shape</span><span class="op">=</span><span class="str">"doublecircle"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[210](#t210)</span> <span class="t"><span class="key">else</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[211](#t211)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">node</span><span class="op">(</span><span class="nam">key</span><span class="op">,</span> <span class="nam">shape</span><span class="op">=</span><span class="str">"circle"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[212](#t212)</span> <span class="t"><span class="key">if</span> <span class="nam">temp</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">[</span><span class="str">"start"</span><span class="op">]</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[213](#t213)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">edge</span><span class="op">(</span><span class="str">""</span><span class="op">,</span> <span class="nam">key</span><span class="op">,</span> <span class="nam">arrowsize</span><span class="op">=</span><span class="str">"0.75"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[214](#t214)</span> <span class="t"><span class="key">for</span> <span class="nam">sec_key</span><span class="op">,</span> <span class="nam">val</span> <span class="key">in</span> <span class="nam">temp</span><span class="op">[</span><span class="nam">key</span><span class="op">]</span><span class="op">.</span><span class="nam">items</span><span class="op">(</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[215](#t215)</span> <span class="t"><span class="key">if</span> <span class="key">not</span> <span class="nam">isinstance</span><span class="op">(</span><span class="nam">val</span><span class="op">,</span> <span class="nam">bool</span><span class="op">)</span><span class="op">:</span></span><span class="r"></span>

<span class="n">[216](#t216)</span> <span class="t"><span class="nam">state</span><span class="op">.</span><span class="nam">edge</span><span class="op">(</span><span class="nam">key</span><span class="op">,</span> <span class="nam">val</span><span class="op">,</span> <span class="nam">label</span><span class="op">=</span><span class="nam">str</span><span class="op">(</span><span class="nam">sec_key</span><span class="op">)</span><span class="op">,</span> <span class="nam">arrowsize</span><span class="op">=</span><span class="str">"0.75"</span><span class="op">)</span></span><span class="r"></span>

<span class="n">[217](#t217)</span> <span class="t"><span class="key">return</span> <span class="nam">state</span></span><span class="r"></span>

</div>

<div id="footer">

<div class="content">

[« index](index.html)     [coverage.py v5.1](https://coverage.readthedocs.io), created at 2020-06-25 23:37

</div>

</div>
