from htmlnode import HTMLNode


def main():
    child_node_1 = HTMLNode(tag="li", value="foo", props={"prop1": "val1"})
    child_node_2 = HTMLNode(tag="li", value="bar", props={"prop2": "val2"})

    node = HTMLNode(tag="ul", children=[child_node_1, child_node_2],
                    props={"color": "red"})

    print(node)
main()
