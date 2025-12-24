from collections import deque
import unittest
from typing import Callable, Dict, Any


def gen_bin_tree(
    height: int = 3,
    root: int = 11,
    left_branch: Callable[[int], int] = lambda r: r ** 2,
    right_branch: Callable[[int], int] = lambda r: 2 + r ** 2
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


def print_tree(tree: Dict[int, Dict[str, Any]]) -> None:

    print("")
    for node, children in tree.items():
        print(f"{node} → {children}")


if __name__ == "__main__":
    tree = gen_bin_tree()
    print_tree(tree)

    print("")
    unittest.main(exit=False)



class TestBinaryTree(unittest.TestCase):
    def test_tree_structure(self):
        tree = gen_bin_tree(height=3, root=11)
        self.assertIsInstance(tree, dict)
        self.assertIn(11, tree)
        self.assertIn("left", tree[11])
        self.assertIn("right", tree[11])

    def test_leaf_calculation(self):
        tree = gen_bin_tree(height=2, root=11)
        self.assertEqual(tree[11]["left"], 11 ** 2)
        self.assertEqual(tree[11]["right"], 2 + 11 ** 2)

    def test_height(self):
        tree = gen_bin_tree(height=3, root=11)
        self.assertTrue(len(tree) > 0)
        self.assertIn(11, tree)