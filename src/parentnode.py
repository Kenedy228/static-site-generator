from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("error: tag is None")
        if self.children is None:
            raise ValueError("error: children is None")
        children = ""
        for child in self.children:
            children += child.to_html()

        return f"<{self.tag}>{children}</{self.tag}>"
