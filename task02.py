import random
import time
from functools import lru_cache
import matplotlib.pyplot as plt

# Реалізація Splay Tree для кешування
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root
        else:
            if root.right is None:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
            return

        new_node = Node(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

# Реалізація чисел Фібоначчі з LRU-кешем
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Реалізація чисел Фібоначчі з Splay Tree
def fibonacci_splay(n, tree):
    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value

    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)

    tree.insert(n, result)
    return result

# Тестування та порівняння
if __name__ == "__main__":
    ns = list(range(0, 951, 50))
    lru_times = []
    splay_times = []

    for n in ns:
        # Вимірювання для LRU-кешу
        start = time.time()
        fibonacci_lru(n)
        lru_times.append(time.time() - start)

        # Вимірювання для Splay Tree
        tree = SplayTree()
        start = time.time()
        fibonacci_splay(n, tree)
        splay_times.append(time.time() - start)

    # Побудова графіка
    plt.figure(figsize=(12, 8))
    plt.plot(ns, lru_times, label="LRU Cache", marker="o", linestyle="-", color="blue")
    plt.plot(ns, splay_times, label="Splay Tree", marker="s", linestyle="--", color="green")
    plt.xlabel("n (номер числа Фібоначчі)", fontsize=12)
    plt.ylabel("Час виконання (с)", fontsize=12)
    plt.title("Порівняння продуктивності LRU Cache та Splay Tree", fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.show()

    # Виведення таблиці результатів
    print(f"{'n':<10}{'LRU Cache Time (s)':<20}{'Splay Tree Time (s)':<20}")
    print("-" * 50)
    for n, lru_time, splay_time in zip(ns, lru_times, splay_times):
        print(f"{n:<10}{lru_time:<20.8f}{splay_time:<20.8f}")
