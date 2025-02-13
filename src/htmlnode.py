
class HTMLNode():

    def __init__(self, tag = None, value = None, children = None , prop = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.prop = prop

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_str = ''

        if self.prop:
            for idx, key in enumerate(self.prop.keys()):
                if idx == 0:
                    html_str += f'{key}="{self.prop[key]}"'
                else:
                    html_str += f' {key}="{self.prop[key]}"'

        return html_str

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.prop})"


class LeafNode(HTMLNode):

    def __init__(self, tag, value, prop=None):
        super().__init__(tag, value, None, prop)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        if self.prop:
            html_str = f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'
            return html_str

        html_str = f'<{self.tag}>{self.value}</{self.tag}>'
        return html_str

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.prop})"


class ParentNode(HTMLNode):

    def __init__(self, tag, children, prop=None):
        super().__init__(tag, None, children, prop)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError

        html_str = f'<{self.tag}>'
        for child in self.children:
            html_str += child.to_html()
        html_str += f'</{self.tag}>'

        return html_str

    def __repr__(self):
        if self.children is None:
            raise ValueError
        return f'''ParentNode(tag=\t{self.tag},
children=\t[{",\n\t\t".join([child.__repr__() for child in self.children])}],
prop=\t\t{self.prop}
)
'''
