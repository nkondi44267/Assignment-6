"""Run a short demonstration of every required implementation."""
import random

from .selection import deterministic_select, randomized_quickselect
from .structures import ArrayQueue, ArrayStack, DynamicArray, Matrix, SinglyLinkedList


def main() -> None:
    values = [8, 2, 5, 2, 9, 4]
    rank = 3
    print(f"Input: {values}; {rank}rd smallest:")
    print("  deterministic:", deterministic_select(values, rank))
    print("  randomized:   ", randomized_quickselect(values, rank, random.Random(42)))

    array = DynamicArray([10, 20, 30])
    array.insert(1, 15)
    array.delete(2)
    print("Dynamic array:  ", array.to_list())

    matrix = Matrix[int](2, 2, 0)
    matrix.set(0, 1, 7)
    matrix.insert_column(2, [5, 6])
    print("Matrix:         ", matrix.to_lists())

    stack = ArrayStack[int]()
    stack.push(3); stack.push(5)
    print("Stack pop:      ", stack.pop())

    queue = ArrayQueue[int]()
    queue.enqueue(3); queue.enqueue(5)
    print("Queue dequeue:  ", queue.dequeue())

    linked = SinglyLinkedList([2, 4, 6])
    linked.insert(1, 3)
    linked.delete(4)
    print("Linked list:    ", linked.to_list())


if __name__ == "__main__":
    main()
