from compiler.front_end.abstract_nodes.ast_node import ASTNode
from compiler.front_end import abstract_nodes
from compiler.front_end.decorator import Decorator
from lark import Transformer, Token, Tree
from compiler.utils.colors import colors

class Disambiguator(Transformer):

    def __default_token__(self, token: Token):
        if token.type == "IDENTIFIER":
            if token.value in keywords or token.value in operators:
                dead_node = ASTNode("DeadBranch")
                dead_node.ansi_color = colors.red
                return dead_node
        return token

    def __default__(self, data, children, meta):
        # Dead Node Travels Up Branch
        for child in children:
            if isinstance(child, ASTNode):
                return child
        return Tree(data, children)

    def _ambig(self, children):
        healthy = []
        # Cut Dead Branches
        for index, branch in enumerate(children):
            if not isinstance(branch, ASTNode):
                healthy.append(children[index])

        # # Ambiguity Resolved
        # if len(healthy) == 1:
        #     return healthy[0]
        # Ambiguity Remains
        else:
            return Tree("_ambig", healthy)

keywords = {
    # Control-flow
    "if", "else", "switch", "case", "default", "for", "while", "do",
    "break", "continue", "return", "goto", "try", "catch", "throw",

    # Types & specifiers
    "int", "float", "double", "char", "wchar_t", "char16_t", "char32_t",
    "void", "bool", "auto", "signed", "unsigned", "short", "long",
    "const", "constexpr", "consteval", "volatile", "static", "extern",
    "mutable", "register", "restrict", "inline", "virtual", "explicit",
    "noexcept", "final", "override", "thread local", "typename", "new",
    "const_cast", "static_cast", "dynamic_cast", "reinterpret_cast",
    "typeid",

    # Declarations
    "class", "struct", "union", "enum", "namespace", "template", "typedef",
    "using", "friend", "public", "private", "protected", "static_assert",
    "asm", "delete", "operator", "decltype", "this",

    # Punctuation
    "(", ")", "{", "}", "[", "]", ";", ",", ".",

    # Miscellaneous / preprocessing
    "#", "include", "define", "##",
    "<:", ":>", "<%", "%>", "%:", "%:%:"
}

operators = {
    # Operators (string forms only, not tokens like PLUS)
    "+", "-", "*", "/", "%", "=", "...", "+=", "-=", "*=", "/=", "%=",
    "<<=", ">>=", "&=", "|=", "^=",
    "<", ">", "<=", ">=", "==", "!=", "&&", "||", "!", "&", "|", "~", "^",
    "<<", ">>", "++", "--", "->", "->*", ".*", "?", "::", ":", "new[]",
    "delete[]", "()", "[]", "sizeof", "alignof",
}

