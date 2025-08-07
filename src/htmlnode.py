class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props = []
        for key, value in self.props.items():
            props.append(f"{key}=\"{value}\"")
        return " ".join(props)

    def __repr__(self, indent=0):
        indent_str = " " * indent

        tag = f"{indent_str}Tag: {self.tag}\n"
        value = f"{indent_str}Value: {self.value}\n"

        children = ""
        if self.children is not None:
            children += f"{indent_str}Children:\n"
            children_details = []
            for i in range(0, len(self.children)):
                children_details.append(f"{indent_str}Child {
                                        i + 1}:\n{self.children[i].__repr__(4)}")
            children += "\n".join(children_details)
        else:
            children = f"{indent_str}Children: None\n"

        props = ""
        if self.props is not None:
            props += f"{indent_str}Properties:\n"
            props_details = []
            for k, v in self.props.items():
                props_details.append(f"{indent_str}{k}: {v}")
            props += "\n".join(props_details)
        else:
            props = f"{indent_str}Properties: None"

        return f"{tag}{value}{children}{props}"
