# About
While a regular data structure supports only updates and queries to its latest
version, with a *retroactive* data structure it is possible to added or remove
operations at any point in a timeline.
The differ from *persistent* data structures in the sense that changes to the
past are propagated to the present (like in Back to the Future) instead of
creating a fork in the timeline.

This repository implements a *partially* retroactive priority queue: It supports
adding and removing priority queue updates (`insert` and `delete_min`) at any
point in the timeline but can perform queries only at the end of the timeline.
All operations are implemented in *logarithmic* time with respect to the length
of the timeline by using the data structure proposed in the [Retroactive Data
Structures][retro-ds] paper by Demaine, Iacono, and Langerman.

# Usage
```
>>> from rpq import RetroactivePriorityQueue
>>> q = RetroactivePriorityQueue()

>>> # Add insertions
>>> q.add_insert(10, 3)          # Timeline:
>>> q.add_insert(0, 2)           #   0         10        20
>>> q.add_insert(20, 1)          # --+---------+---------+-------
>>> q.get_min()                  #  i(2)      i(3)      i(1)
1
>>> list(q)
[1, 2, 3]

>>> # Add deletions
>>> q.add_delete_min(5)          # --+----+----+---------+-------
>>> list(q)                      #  i(2)  dm  i(3)      i(1)
[1, 3]
>>> q.add_delete_min(25)         # --+----+----+---------+----+--
>>> list(q)                      #  i(2)  dm  i(3)      i(1)  dm
[3]

>>> # Remove insert
>>> q.remove(20)                 # --+----+----+--------------+--
>>> list(q)                      #  i(2)  dm  i(3)            dm
[]

>>> # Invalid operations
>>> q.remove(7)                  # No operation at t=7
KeyError
>>> q.add_delete_min(15)         # delete_min on an empty queue at t=25
ValueError

>>> # Remove delete_min
>>> q.remove(5)                  # --+---------+--------------+--
>>> list(q)                      #  i(2)      i(3)            dm
[3]
```

For a full documentation of the API, check out the [docstrings][rpq-docstring]
in the source code.

## Testing
To run the tests, execute at the repository root:
```
python -m unittest
```

[retro-ds]: http://erikdemaine.org/papers/Retroactive_TALG/
[rpq-docstring]: rpq/rpq.py
