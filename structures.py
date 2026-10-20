"""Educational implementations of arrays, matrices, stacks, queues, and lists.

Python lists are used only as raw fixed-capacity backing storage, not as an
implementation of Python's built-in queue, stack, or linked-list operations.
"""

from __future__ import annotations
from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class DynamicArray(Generic[T]):
    """Resizable indexed array with doubling capacity and amortized O(1) append."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._capacity = 4
        self._size = 0
        self._storage: list[T | None] = [None] * self._capacity
        for item in values:
            self.append(item)

    def __len__(self) -> int:
        return self._size

    def _check_index(self, index: int) -> None:
        if not isinstance(index, int) or not 0 <= index < self._size:
            raise IndexError("array index out of range")

    def _resize(self, capacity: int) -> None:
        next_storage: list[T | None] = [None] * capacity
        for i in range(self._size):
            next_storage[i] = self._storage[i]
        self._storage, self._capacity = next_storage, capacity

    def append(self, value: T) -> None:
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._storage[self._size] = value
        self._size += 1

    def insert(self, index: int, value: T) -> None:
        if not isinstance(index, int) or not 0 <= index <= self._size:
            raise IndexError("insert index out of range")
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        for i in range(self._size, index, -1):
            self._storage[i] = self._storage[i - 1]
        self._storage[index] = value
        self._size += 1

    def pop(self, index: int = -1) -> T:
        if index == -1:
            index = self._size - 1
        self._check_index(index)
        value = self._storage[index]
        for i in range(index, self._size - 1):
            self._storage[i] = self._storage[i + 1]
        self._size -= 1
        self._storage[self._size] = None
        if self._capacity > 4 and self._size <= self._capacity // 4:
            self._resize(max(4, self._capacity // 2))
        return value  # type: ignore[return-value]

    def delete(self, index: int) -> T:
        """Remove and return element at index."""
        return self.pop(index)

    def __getitem__(self, index: int) -> T:
        self._check_index(index)
        return self._storage[index]  # type: ignore[return-value]

    def __setitem__(self, index: int, value: T) -> None:
        self._check_index(index)
        self._storage[index] = value

    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self[i]

    def to_list(self) -> list[T]:
        return list(self)


class Matrix(Generic[T]):
    """Rectangular 2D array with row/column insertion, deletion, and access."""

    def __init__(self, rows: int, cols: int, fill: T | None = None) -> None:
        if rows < 0 or cols < 0:
            raise ValueError("rows and cols must be nonnegative")
        self._cols = cols
        self._rows: DynamicArray[DynamicArray[T | None]] = DynamicArray()
        for _ in range(rows):
            self._rows.append(DynamicArray([fill] * cols))

    @property
    def shape(self) -> tuple[int, int]:
        return len(self._rows), self._cols

    def _check_cell(self, row: int, col: int) -> None:
        if not 0 <= row < len(self._rows) or not 0 <= col < self._cols:
            raise IndexError("matrix coordinates out of range")

    def get(self, row: int, col: int) -> T | None:
        self._check_cell(row, col)
        return self._rows[row][col]

    def set(self, row: int, col: int, value: T | None) -> None:
        self._check_cell(row, col)
        self._rows[row][col] = value

    def insert_row(self, index: int, values: Iterable[T | None]) -> None:
        row = list(values)
        if len(row) != self._cols:
            raise ValueError("row width must equal existing column count")
        self._rows.insert(index, DynamicArray(row))

    def delete_row(self, index: int) -> list[T | None]:
        return self._rows.delete(index).to_list()

    def insert_column(self, index: int, values: Iterable[T | None]) -> None:
        if not 0 <= index <= self._cols:
            raise IndexError("column index out of range")
        entries = list(values)
        if len(entries) != len(self._rows):
            raise ValueError("new column height must equal row count")
        for row_index, value in enumerate(entries):
            self._rows[row_index].insert(index, value)
        self._cols += 1

    def delete_column(self, index: int) -> list[T | None]:
        if not 0 <= index < self._cols:
            raise IndexError("column index out of range")
        removed = [row.delete(index) for row in self._rows]
        self._cols -= 1
        return removed

    def to_lists(self) -> list[list[T | None]]:
        return [row.to_list() for row in self._rows]


class ArrayStack(Generic[T]):
    """LIFO container backed by a dynamic array."""

    def __init__(self) -> None:
        self._items: DynamicArray[T] = DynamicArray()

    def __len__(self) -> int:
        return len(self._items)

    def push(self, value: T) -> None:
        self._items.append(value)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[len(self._items) - 1]


class ArrayQueue(Generic[T]):
    """FIFO circular array; amortized O(1) enqueue and O(1) dequeue."""

    def __init__(self) -> None:
        self._capacity = 4
        self._storage: list[T | None] = [None] * self._capacity
        self._head = 0
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _resize(self, capacity: int) -> None:
        storage: list[T | None] = [None] * capacity
        for index in range(self._size):
            storage[index] = self._storage[(self._head + index) % self._capacity]
        self._storage = storage
        self._head = 0
        self._capacity = capacity

    def enqueue(self, item: T) -> None:
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        tail = (self._head + self._size) % self._capacity
        self._storage[tail] = item
        self._size += 1

    def dequeue(self) -> T:
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        item = self._storage[self._head]
        self._storage[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        if self._capacity > 4 and self._size <= self._capacity // 4:
            self._resize(max(4, self._capacity // 2))
        return item  # type: ignore[return-value]

    def peek(self) -> T:
        if self._size == 0:
            raise IndexError("peek from empty queue")
        return self._storage[self._head]  # type: ignore[return-value]


class _Node(Generic[T]):
    def __init__(self, data: T, next_node: _Node[T] | None = None):
        self.data = data
        self.next = next_node


class SinglyLinkedList(Generic[T]):
    """Singly linked list with head and tail pointers for O(1) append."""

    def __init__(self, values: Iterable[T] = ()) -> None:
        self.head: _Node[T] | None = None
        self.tail: _Node[T] | None = None
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self) -> int:
        return self._size

    def prepend(self, item: T) -> None:
        node = _Node(item, self.head)
        self.head = node
        if self._size == 0:
            self.tail = node
        self._size += 1

    def append(self, item: T) -> None:
        node = _Node(item)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1

    def _node_at(self, index: int) -> _Node[T]:
        if not 0 <= index < self._size:
            raise IndexError("linked-list index out of range")
        current = self.head
        for _ in range(index):
            assert current is not None
            current = current.next
        assert current is not None
        return current

    def get(self, index: int) -> T:
        return self._node_at(index).data

    def insert(self, index: int, item: T) -> None:
        if not 0 <= index <= self._size:
            raise IndexError("linked-list insert index out of range")
        if index == 0:
            self.prepend(item)
        elif index == self._size:
            self.append(item)
        else:
            prior = self._node_at(index - 1)
            prior.next = _Node(item, prior.next)
            self._size += 1

    def remove_at(self, index: int) -> T:
        if not 0 <= index < self._size:
            raise IndexError("linked-list index out of range")
        if index == 0:
            assert self.head is not None
            value = self.head.data
            self.head = self.head.next
            self._size -= 1
            if self._size == 0:
                self.tail = None
            return value
        prior = self._node_at(index - 1)
        assert prior.next is not None
        target = prior.next
        prior.next = target.next
        self._size -= 1
        if prior.next is None:
            self.tail = prior
        return target.data

    def delete(self, value: T) -> bool:
        """Remove first matching node; return False if value was absent."""
        previous: _Node[T] | None = None
        current = self.head
        while current is not None:
            if current.data == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                self._size -= 1
                return True
            previous, current = current, current.next
        return False

    def __iter__(self) -> Iterator[T]:
        node = self.head
        while node is not None:
            yield node.data
            node = node.next

    def to_list(self) -> list[T]:
        return list(self)
