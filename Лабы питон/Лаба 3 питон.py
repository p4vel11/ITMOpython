from typing import Union, Dict, Any, Optional
from collections import namedtuple, defaultdict
import unittest


def gen_bin_tree(height: int = 3, root: Union[int, float] = 11) -> Optional[Dict[str, Any]]:
    if height <= 0:
        return None

    if height == 1:
        return {"value": root, "left": None, "right": None}

    left_value = root ** 2
    right_value = 2 + root ** 2

    left_subtree = gen_bin_tree(height - 1, left_value)
    right_subtree = gen_bin_tree(height - 1, right_value)

    return {"value": root, "left": left_subtree, "right": right_subtree}

Node = namedtuple("Node", ["value", "left", "right"])


def gen_bin_tree_namedtuple(height: int = 3, root: Union[int, float] = 11) -> Optional[Node]:
    if height <= 0:
        return None

    if height == 1:
        return Node(value=root, left=None, right=None)

    left_value = root ** 2
    right_value = 2 + root ** 2

    left_subtree = gen_bin_tree_namedtuple(height - 1, left_value)
    right_subtree = gen_bin_tree_namedtuple(height - 1, right_value)

    return Node(value=root, left=left_subtree, right=right_subtree)


def gen_bin_tree_defaultdict(height: int = 3, root: Union[int, float] = 11) -> Optional[defaultdict]:
    if height <= 0:
        return None

    def make_node(val):
        return defaultdict(lambda: None, {"valuе": val})

    if height == 1:
        return make_node(root)

    left_value = root ** 2
    right_value = 2 + root ** 2

    node = make_node(root)
    node["left"] = gen_bin_tree_defaultdict(height - 1, left_value)
    node["right"] = gen_bin_tree_defaultdict(height - 1, right_value)

    return node

class TestGenBinTree(unittest.TestCase):

    def test_height_1(self):
        tree = gen_bin_tree(height=1, root=11)
        expected = {"value": 11, "left": None, "right": None}
        self.assertEqual(tree, expected)

    def test_height_2(self):
        tree = gen_bin_tree(height=2, root=11)
        expected = {
            "value": 11,
            "left": {"value": 121, "left": None, "right": None},
            "right": {"value": 123, "left": None, "right": None},
        }
        self.assertEqual(tree, expected)

    def test_recursive_depth(self):
        tree = gen_bin_tree(height=3, root=11)
        self.assertIsInstance(tree["left"]["left"], dict)
        self.assertIsInstance(tree["right"]["right"], dict)

    def test_namedtuple_version(self):
        tree = gen_bin_tree_namedtuple(2, 11)
        self.assertEqual(tree.value, 11)
        self.assertEqual(tree.left.value, 121)
        self.assertEqual(tree.right.value, 123)

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)