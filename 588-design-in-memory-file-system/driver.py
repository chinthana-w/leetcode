"""
Driver for LeetCode 588 - Design In-Memory File System.

Runs the FileSystem implementation against test cases and reports results.
"""

from file_system import FileSystem
from test_cases import ALL_TEST_CASES


def run_step(fs: FileSystem, step: dict):
    """Execute one step (op + args) and return the result, or None for void ops."""
    op = step["op"]
    args = step["args"]
    if op == "ls":
        return fs.ls(args[0])
    if op == "mkdir":
        fs.mkdir(args[0])
        return None
    if op == "addContentToFile":
        fs.addContentToFile(args[0], args[1])
        return None
    if op == "readContentFromFile":
        return fs.readContentFromFile(args[0])
    raise ValueError(f"Unknown op: {op}")


def run_test_case(name: str, steps: list) -> tuple[bool, str | None]:
    """
    Run one test case. Return (passed, error_message).
    error_message is None if passed.
    """
    fs = FileSystem()
    for i, step in enumerate(steps):
        expected = step["expected"]
        try:
            result = run_step(fs, step)
        except Exception as e:
            return False, f"Step {i + 1} ({step['op']}{step['args']}) raised: {type(e).__name__}: {e}"
        if expected is not None and result != expected:
            return False, (
                f"Step {i + 1}: {step['op']}{step['args']} -> got {result!r}, expected {expected!r}"
            )
    return True, None


def main() -> None:
    passed = 0
    failed = 0
    for name, steps in ALL_TEST_CASES:
        ok, err = run_test_case(name, steps)
        if ok:
            passed += 1
            print(f"PASS  {name}")
        else:
            failed += 1
            print(f"FAIL  {name}: {err}")
    print()
    print(f"Total: {passed} passed, {failed} failed")


if __name__ == "__main__":
    main()
