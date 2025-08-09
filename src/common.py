import re

from textnode import TextType, TextNode
from leafnode import LeafNode
from blocktype import BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode

REGEXP_IMAGE = r"!\[.*?\]\(.*?\)"
REGEXP_LINK = r"\[.*?\]\(.*?\)"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise ValueError("error: unknown text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        indent = len(delimiter)
        delimiter_start_index = text.find(delimiter)

        if delimiter_start_index == -1:
            new_nodes.append(node)
            continue

        if delimiter_start_index != 0:
            new_nodes.append(
                TextNode(text[0:delimiter_start_index], TextType.TEXT))

        while True:
            delimiter_end_index = text.find(
                delimiter, delimiter_start_index + indent)

            if delimiter_end_index == -1:
                break

            new_nodes.append(
                TextNode(text[delimiter_start_index + indent: delimiter_end_index], text_type))
            delimiter_start_index = text.find(
                delimiter, delimiter_end_index + indent)

            if delimiter_start_index == -1:
                break

            new_nodes.append(
                TextNode(text[delimiter_end_index +
                              indent: delimiter_start_index], TextType.TEXT))

        if delimiter_start_index == -1:
            new_nodes.append(
                TextNode(text[delimiter_end_index + indent:], TextType.TEXT))

        if delimiter_end_index == -1 and delimiter_start_index != -1:
            raise ValueError("error: not found close delimiter")

    return new_nodes


def extract_markdown_images(text):
    result = []
    matches = re.findall(REGEXP_IMAGE, text)
    for match in matches:
        splitted = match.split("](")
        result.append((splitted[0][2:], splitted[1][:len(splitted[1]) - 1]))
    return result


def extract_markdown_links(text):
    result = []
    matches = re.findall(REGEXP_LINK, text)
    for match in matches:
        splitted = match.split("](")
        result.append((splitted[0][1:], splitted[1][:len(splitted[1]) - 1]))
    return result


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        images = extract_markdown_images(text)
        matches = re.findall(REGEXP_IMAGE, text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        match_start_index = 0

        for i in range(0, len(matches)):
            match_start_index = text.find(matches[i])

            if match_start_index != 0:
                new_nodes.append(
                    TextNode(text[:match_start_index], TextType.TEXT))

            new_nodes.append(
                TextNode(images[i][0], TextType.IMAGE, images[i][1]))

            text = text[match_start_index + len(matches[i]):]

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        links = extract_markdown_links(text)
        matches = re.findall(REGEXP_LINK, text)

        if len(matches) == 0:
            new_nodes.append(node)
            continue

        match_start_index = 0

        for i in range(0, len(matches)):
            match_start_index = text.find(matches[i])

            if match_start_index != 0:
                new_nodes.append(
                    TextNode(text[:match_start_index], TextType.TEXT))

            new_nodes.append(
                TextNode(links[i][0], TextType.LINK, links[i][1]))
            text = text[match_start_index + len(matches[i]):]

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


# use decorator here
def text_to_textnodes(text):
    text = text.strip(" ")
    nodes = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = []
    splitted = markdown.split("\n\n")
    for s in splitted:
        block = s.strip(" ")
        block = block.strip("\n")
        if len(block) > 0:
            blocks.append(block)
    return blocks


def block_to_block_type(block):
    if block_to_header_block(block):
        return BlockType.HEADING

    if block_to_code_block(block):
        return BlockType.CODE

    if block_to_qoute_block(block):
        return BlockType.QUOTE

    if block_to_unordered_list(block):
        return BlockType.UNORDERED_LIST

    if block_to_ordered_list(block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def block_to_header_block(block):
    prefix = "#"
    count = 0

    for i in range(0, len(block)):
        if block[i] == prefix:
            count += 1
        else:
            if count > 0 and count <= 6 and block[i] == " ":
                return True
            return False
    return False


def block_to_code_block(block):
    prefix = "```"
    suffix = "```"

    if len(block) < 6:
        return False

    if block[0:3] == prefix and block[len(block) - 3: len(block)] == suffix:
        return True
    return False


def block_to_qoute_block(block):
    prefix = ">"
    lines = block.split("\n")

    for line in lines:
        if line[0] != prefix:
            return False

    return True


def block_to_unordered_list(block):
    prefix = "-"
    lines = block.split("\n")

    for line in lines:
        if line[0] != prefix or line[1] != " ":
            return False

    return True


def block_to_ordered_list(block):
    lines = block.split("\n")
    prev = 0

    for line in lines:
        if line[0] == 0:
            return False

        splitted = line.split(" ")
        seq = None

        try:
            seq = int(splitted[0][0: len(splitted[0]) - 1])
        except ValueError:
            return False

        if seq - 1 != prev:
            return False

        prev = seq
    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            nodes.append(block_to_header_tag(block))
        elif block_type == BlockType.CODE:
            nodes.append(block_to_code_tag(block))
        elif block_type == BlockType.ORDERED_LIST:
            nodes.append(block_to_ol_tag(block))
        elif block_type == BlockType.UNORDERED_LIST:
            nodes.append(block_to_ul_tag(block))
        elif block_type == BlockType.QUOTE:
            nodes.append(block_to_quote_tag(block))
        elif block_type == BlockType.PARAGRAPH:
            nodes.append(block_to_paragraph_tag(block))

    result_node = ParentNode(tag="div", children=nodes)
    return result_node


def block_to_header_tag(block):
    splitted = block.split(" ")
    tag_holder = splitted[0].strip()
    tag = f"h{len(tag_holder)}"

    text = " ".join(splitted[1:]).strip()
    nodes = text_to_textnodes(text)

    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))

    header_node = ParentNode(tag=tag, children=children)
    result_node = ParentNode(tag="div", children=[header_node])

    return result_node


def block_to_paragraph_tag(block):
    lines = block.split("\n")
    text = " ".join(lines).strip()

    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))

    paragraph_node = ParentNode(tag="p", children=children)
    result_node = ParentNode(tag="div", children=[paragraph_node])

    return result_node


def block_to_quote_tag(block):
    block = block.replace(">", "")
    text = " ".join(block.split("\n")).strip()

    nodes = text_to_textnodes(text)
    children = []

    for node in nodes:
        children.append(text_node_to_html_node(node))

    quote = ParentNode(tag="blockquote", children=children)

    result_node = ParentNode(tag="div", children=[quote])
    return result_node


def block_to_code_tag(block):
    block = block.strip()
    lines = block[3:len(block) - 3].strip().split("\n")
    text = " ".join(lines).strip()

    nodes = text_to_textnodes(text)
    children = []

    for node in nodes:
        children.append(text_node_to_html_node(node))

    code_tag = ParentNode(tag="code", children=children)
    pre_tag = ParentNode(tag="pre", children=[code_tag])
    result_tag = ParentNode(tag="div", children=[pre_tag])

    return result_tag


def block_to_ul_tag(block):
    block = block.strip()
    lines = block.split("\n")
    list_items = []

    for line in lines:
        text = line[2:].strip()

        nodes = text_to_textnodes(text)
        children = []

        for node in nodes:
            children.append(text_node_to_html_node(node))

        list_items.append(ParentNode("li", children=children))

    ul_tag = ParentNode("ul", children=list_items)
    result_tag = ParentNode("div", children=[ul_tag])

    return result_tag


def block_to_ol_tag(block):
    block = block.strip()
    lines = block.split("\n")
    list_items = []

    for line in lines:
        splitted = line.split(" ")
        text = " ".join(splitted[1:]).strip()

        nodes = text_to_textnodes(text)
        children = []

        for node in nodes:
            children.append(text_node_to_html_node(node))

        list_items.append(ParentNode("li", children=children))

    ol_tag = ParentNode("ol", children=list_items)
    result_tag = ParentNode("div", children=[ol_tag])

    return result_tag


def extract_title(markdown):
    blocks = markdown.strip().split("\n\n")
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception("not found title")
