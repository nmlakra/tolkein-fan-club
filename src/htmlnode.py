
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

