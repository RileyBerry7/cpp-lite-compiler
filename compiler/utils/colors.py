# colors.py
# Simple color + style helper using ANSI escape sequences

class AnsiColor:
    def __init__(self, r, g, b, styles=None):
        self.r = r
        self.g = g
        self.b = b
        self.styles = styles or []

    def __call__(self, text: str) -> str:
        """Apply color + styles to text"""
        style_seq = "".join(self.styles)
        return f"\033[38;2;{self.r};{self.g};{self.b}m{style_seq}{text}\033[0m"

    def _with_style(self, code: str):
        return AnsiColor(self.r, self.g, self.b, self.styles + [code])

    @property
    def bold(self):
        return self._with_style("\033[1m")

    @property
    def underline(self):
        return self._with_style("\033[4m")

    @property
    def italic(self):
        return self._with_style("\033[3m")

    @property
    def dim(self):
        return self._with_style("\033[2m")

    @property
    def blink(self):
        return self._with_style("\033[5m")


class Colors:
    """Named color palette — extend as needed."""

    red     = AnsiColor(255, 0, 0)
    green   = AnsiColor(0, 255, 0)
    blue    = AnsiColor(0, 128, 255)
    yellow  = AnsiColor(255, 255, 0)
    orange  = AnsiColor(255, 165, 0)
    purple  = AnsiColor(160, 32, 240)
    pink    = AnsiColor(255, 105, 180)
    teal    = AnsiColor(0, 191, 165)
    cyan    = AnsiColor(0, 255, 255)
    white   = AnsiColor(255, 255, 255)
    grey    = AnsiColor(128, 128, 128)
    black   = AnsiColor(0, 0, 0)
    gold = AnsiColor(255, 215, 95)  # Golden yellow / amber (#FFD75F)


# Singleton instance for easy importing
colors = Colors()
