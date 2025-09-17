from compiler.front_end.abstract_nodes.ast_node import ASTNode
from compiler.front_end.decorator import Decorator
from compiler.utils.colors import colors

class Disambiguator(Decorator):

    def IDENTIFIER(self, node:ASTNode, children: list[ASTNode]):
        if children[0].name in keywords:
            node.name = "DeadBranch"
            node.ansi_color = colors.red
            children.clear()

    def __default__(self, node:ASTNode, children: list[ASTNode]):
        for child in children:
            if child.name == "DeadBranch":
                node.name = "DeadBranch"
                node.ansi_color = colors.red
                children.clear()

    def Ambiguity(self, node:ASTNode, children: list[ASTNode]):
        for index, ambig_branch in enumerate(children):
            if ambig_branch.name == "DeadBranch":
                children.pop(index)
            if len(children) == 1:
                # print("Ambiguous Branch Resolved!!")
                node.name = children[0].name
                children[:] = children[0].children
                node.ansi_color = colors.green.underline

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

    # Operators (string forms only, not tokens like PLUS)
    "+", "-", "*", "/", "%", "=", "...", "+=", "-=", "*=", "/=", "%=",
    "<<=", ">>=", "&=", "|=", "^=",
    "<", ">", "<=", ">=", "==", "!=", "&&", "||", "!", "&", "|", "~", "^",
    "<<", ">>", "++", "--", "->", "->*", ".*", "?", "::", ":", "new[]",
    "delete[]", "()", "[]", "sizeof", "alignof",

    # Punctuation
    "(", ")", "{", "}", "[", "]", ";", ",", ".",

    # Miscellaneous / preprocessing
    "#", "include", "define", "##",
    "<:", ":>", "<%", "%>", "%:", "%:%:"
}