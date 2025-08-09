from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("error: value is None")
        if self.tag is None:
            return self.value
        props = ""

        if self.props is not None:
            props = f" {self.props_to_html()}"

        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
