import timeit
import matplotlib.pyplot as plt
from collections import deque
from typing import Callable, Dict, Any


def build_tree_recursive(
    root: int,
    height: int,
    left_branch: Callable[[int], int] = lambda r: r ** 2,
    right_branch: Callable[[int], int] = lambda r: 2 + r ** 2,
) -> Dict[int, Dict[str, Any]]:
    if height == 0:
        return {root: {"left": None, "right": None}}

    left = left_branch(root)
    right = right_branch(root)

    tree = {root: {"left": left, "right": right}}
    tree.update(build_tree_recursive(left, height - 1, left_branch, right_branch))
    tree.update(build_tree_recursive(right, height - 1, left_branch, right_branch))
    return tree


def build_tree_iterative(
    root: int,
    height: int,
    left_branch: Callable[[int], int] = lambda r: r ** 2,
    right_branch: Callable[[int], int] = lambda r: 2 + r ** 2,
) -> Dict[int, Dict[str, Any]]:
    tree: Dict[int, Dict[str, Any]] = {}
    queue = deque([(root, 1)])

    while queue:
        node, level = queue.popleft()
        if level < height:
            left = left_branch(node)
            right = right_branch(node)
            tree[node] = {"left": left, "right": right}
            queue.append((left, level + 1))
            queue.append((right, level + 1))
        else:
            tree[node] = {"left": None, "right": None}

    return tree



def measure_time():
    heights = list(range(2, 10))
    recursive_times = []
    iterative_times = []

    for h in heights:
        t_recursive = timeit.timeit(
            lambda: build_tree_recursive(11, h),
            number=10,
        )
        t_iterative = timeit.timeit(
            lambda: build_tree_iterative(11, h),
            number=10,
        )

        recursive_times.append(t_recursive)
        iterative_times.append(t_iterative)


    plt.figure(figsize=(8, 5))
    plt.plot(heights, recursive_times, marker="o", label="Рекурсивная реализация")
    plt.plot(heights, iterative_times, marker="s", label="Нерекурсивная реализация")
    plt.xlabel("Высота дерева (h)")
    plt.ylabel("Время построения (сек)")
    plt.title("Сравнение рекурсивного и нерекурсивного построения бинарного дерева")
    plt.legend()
    plt.grid(True)
    plt.show()


    print()
    for h, tr, ti in zip(heights, recursive_times, iterative_times):
        print(f"{h:7} | {tr:.6f}     | {ti:.6f}")


if __name__ == "__main__":
    measure_time()