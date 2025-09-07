# Subset C++ Compiler

A near-fully-featured **C++ subset compiler** with a practical, learning-oriented design. The front end uses **Lark** for lexing and parsing. After validation, the AST is lowered into **LLVM IR**, and **llvmlite** handles optimization and code generation. The grammar follows **ISO C++ (N3092)** closely, with only minor adjustments to reduce ambiguity. All grammar modifications are **documented**.



**Languages:** Python, C++  
**Libraries:** Lark, llvmlite (LLVM)

**Demo:** (WIP)  

---

## Compiler Pipeline

- **Parsing/Lexing:** Started with a custom grammar inspired by Clang/GCC, then retrofitted to a faithful ISO-based grammar to improve coverage and correctness. Lark runs **LALR** by default for speed, with a switchable **Earley** mode for grammar debugging and ambiguity analysis.
- **Abstraction:** `Transformer` sub-class flattens the deep ISO-style CST into a clean **AST**—same meaning, much easier to reason about.
- **Semantic Analysis:** A series of “decorator” passes populate the **compiler context** (symbol table, scope stack, diagnostics) and handle essentials like symbol declaration/binding, constant-expression evaluation, type resolution/checking, and parameter validation.
- **IR Generation:** A dedicated module lowers the validated AST to **LLVM IR** (modules, functions, basic blocks). LLVM then takes over for optimization and code generation.

This structure keeps the codebase highly extensible with high-fideltiy to formal C++.

---

## Lessons Learned

- Official ISO language documentation is great for **specification**, not always for **implementation**, you need a lot of pragmatic tweaks to keep real parsers workable.
- Separating concerns (lexing -> parsing -> transforming -> decorating -> IR generating) makes a compiler **maintainable**, but it is often not that **practical** in real compilers.
- C++ is terrifying: deeply **ambiguous**, and endlessly **complex**. But at the same time implementing a compiler for it really makes you appreciate the how and why it is such a **powerful language**.
- This project has greatly deepened my fundamental understanding of C++.
Using **Lark** and **LLVM** bridges compiler theory with practical implementation.

---

## Screenshots
(WIP)

---

## Backlog

- Abstract Declarator: left & right recursive ambiguity
- Declarator Suffix binding precedence
- Class Constructor: expacts class_name in declarator_id 

---

## Acknowledgements
ISO C++ Website: [https://isocpp.org/std/the-standard](https://isocpp.org/std/the-standard)
