# Lab 5: Static Code Analysis Reflection

**Note:** The supplied handout explains the purpose of static analysis and the required fixes, but it does not display the four reflection questions. These draft reflections address the learning outcomes stated in the handout; adapt them if your instructor has provided separate questions.

## 1. What is static code analysis, and why is it useful?
Static code analysis examines source code without running the program. It can identify likely bugs, unsafe coding patterns, and style problems early, making software easier to maintain and review.

## 2. What did Pylint, Bandit, and Flake8 each contribute?
Pylint highlighted code-quality problems such as missing docstrings, a mutable default argument, broad exception handling, and naming issues. Bandit identified the unsafe use of `eval()` and a try/except/pass pattern. Flake8 reported style violations such as unused imports, missing blank lines, and long lines.

## 3. Which issue was most important, and how was it addressed?
The `eval()` use was important because evaluating arbitrary expressions can allow unintended code execution. It was replaced with a restricted arithmetic evaluator that accepts only numeric constants, the `days` variable, and selected arithmetic operators. Broad exception handling was also replaced with targeted handling.

## 4. What did you learn about code quality and maintainability?
Static analysis tools complement testing and code review. Fixing mutable defaults, validating inputs, documenting functions, using context managers, and following naming and formatting conventions makes the program more predictable and easier to maintain. Tool output must still be reviewed: not every warning has the same severity, and a clean report does not prove that a program is completely correct.
