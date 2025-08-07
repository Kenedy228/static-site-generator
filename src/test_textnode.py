import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    nodes = [
        TextNode("This is a text node", TextType.BOLD, None),
        TextNode("This is a text node", TextType.BOLD, None),
        TextNode(None, None, None),
        TextNode("foo", TextType.CODE, None),
        TextNode(None, TextType.LINK, "DAWDAD"),
        TextNode(None, TextType.IMAGE, "DAWDAD"),
    ]

    def test_eq(self):
        self.assertEqual(self.nodes[0], self.nodes[1])

    def test_not_eq(self):
        self.assertNotEqual(self.nodes[2], self.nodes[3])
        self.assertNotEqual(self.nodes[4], self.nodes[5])


if __name__ == "__main__":
    unittest.main()
