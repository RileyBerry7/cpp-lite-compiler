
class DecNode:
    def __init__(self):

        # Abstract Node Details
        self.name = None
        self.children = []

        # Semantic Details (for LLVM IR)
        self.decorations = {}