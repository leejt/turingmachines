from random import choice
from collections import Counter
from itertools import product

class Cell:
	def __init__(self, prev, next):
		self.data = 0
		self._prev = prev
		self._next = next

	def next(self):
		if self._next is not None:
			return self._next
		self._next = Cell(self, None)
		return self._next

	def prev(self):
		if self._prev is not None:
			return self._prev
		self._prev = Cell(None, self)
		return self._prev

	def write(self, data):
		self.data = data

class TuringMachine:
	def __init__(self, machine, tape=None):
		self.machine = machine
		if tape is None:
			self.tape = Cell(None, None)
		else:
			self.tape = tape

	def show_tape(self, location):
		pointer = self.tape
		while pointer._prev is not None:
			pointer = pointer._prev
		s = ""
		while pointer is not None:
			if pointer == location:
				s += "'%s'"%pointer.data
			else:
				s += "%s"%pointer.data
			pointer = pointer._next
		return s

	def run(self, until):
		state = 0
		pointer = self.tape
		count = 0
		while True:
			count += 1
			write, move, newstate = self.machine[state][pointer.data]
			pointer.write(write)
			if move == 'R':
				pointer = pointer.next()
			else:
				pointer = pointer.prev()
			state = newstate
			if state == 'H' or count >= until:
				break
		return count

def random_cell(states, symbols):
	return (choice(range(symbols)), choice('LR'), choice(['H'] + range(states)))

def random_machine(states, symbols):
	return tuple(tuple(random_cell(states, symbols) for i in range(symbols)) for j in range(states))

def test_all(states, symbols, until):
	c = Counter()
	qs = product(range(symbols), 'LR', ['H'] + range(states))
	machines = product(product(qs, repeat=symbols), repeat=states)
	for i, machine in enumerate(machines):
		if machine[0][0][1] == 'L':
			continue
		tm = TuringMachine(machine)
		c[tm.run(until)] += 1
	return c

test_all(states=3, symbols=2, until=108)