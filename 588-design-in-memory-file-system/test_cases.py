"""
Test cases for LeetCode 588 - Design In-Memory File System.

Each test case is a list of steps. Each step is a dict:
  - "op": one of "ls", "mkdir", "addContentToFile", "readContentFromFile"
  - "args": list of arguments (path, or filePath+content)
  - "expected": expected return value (None for void ops: mkdir, addContentToFile)
"""

# Example from problem: ls("/") -> [], mkdir("/a/b/c"), addContentToFile("/a/b/c/d", "hello"), ls("/") -> ["a"], read -> "hello"
EXAMPLE_1 = [
    {"op": "ls", "args": ["/"], "expected": []},
    {"op": "mkdir", "args": ["/a/b/c"], "expected": None},
    {"op": "addContentToFile", "args": ["/a/b/c/d", "hello"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["a"]},
    {"op": "readContentFromFile", "args": ["/a/b/c/d"], "expected": "hello"},
]

# Multiple dirs and files, ls on subdir
EXAMPLE_2 = [
    {"op": "mkdir", "args": ["/a/b/c"], "expected": None},
    {"op": "mkdir", "args": ["/a/b/d"], "expected": None},
    {"op": "addContentToFile", "args": ["/a/b/c/e", "file in c"], "expected": None},
    {"op": "ls", "args": ["/a/b"], "expected": ["c", "d"]},
    {"op": "ls", "args": ["/a/b/c"], "expected": ["e"]},
    {"op": "readContentFromFile", "args": ["/a/b/c/e"], "expected": "file in c"},
]

# Append content
EXAMPLE_3 = [
    {"op": "addContentToFile", "args": ["/root/file", "hello "], "expected": None},
    {"op": "addContentToFile", "args": ["/root/file", "world"], "expected": None},
    {"op": "readContentFromFile", "args": ["/root/file"], "expected": "hello world"},
    {"op": "ls", "args": ["/root"], "expected": ["file"]},
]

# ls on file path returns [filename]
EXAMPLE_4 = [
    {"op": "addContentToFile", "args": ["/f", "x"], "expected": None},
    {"op": "ls", "args": ["/f"], "expected": ["f"]},
]

# Lexicographic order: ls must return names sorted (problem requirement). Content length >= 1 per constraints.
LEXICOGRAPHIC_ORDER = [
    {"op": "mkdir", "args": ["/m"], "expected": None},
    {"op": "addContentToFile", "args": ["/m/z", "z"], "expected": None},
    {"op": "addContentToFile", "args": ["/m/a", "a"], "expected": None},
    {"op": "addContentToFile", "args": ["/m/b", "b"], "expected": None},
    {"op": "ls", "args": ["/m"], "expected": ["a", "b", "z"]},
]

# Root: only ls then add file at root
ROOT_ONLY = [
    {"op": "ls", "args": ["/"], "expected": []},
    {"op": "addContentToFile", "args": ["/rootfile", "at root"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["rootfile"]},
    {"op": "readContentFromFile", "args": ["/rootfile"], "expected": "at root"},
]

# Deep path (more than a/b/c)
DEEP_PATH = [
    {"op": "mkdir", "args": ["/a/b/c/d/e/f"], "expected": None},
    {"op": "addContentToFile", "args": ["/a/b/c/d/e/f/deep", "content"], "expected": None},
    {"op": "ls", "args": ["/a/b/c/d/e/f"], "expected": ["deep"]},
    {"op": "readContentFromFile", "args": ["/a/b/c/d/e/f/deep"], "expected": "content"},
]

# Same dir has both subdir and file; ls returns both in lexicographic order
DIR_AND_FILE_SAME_LEVEL = [
    {"op": "mkdir", "args": ["/x/y"], "expected": None},
    {"op": "addContentToFile", "args": ["/x/z", "file under x"], "expected": None},
    {"op": "ls", "args": ["/x"], "expected": ["y", "z"]},
    {"op": "readContentFromFile", "args": ["/x/z"], "expected": "file under x"},
]

# mkdir same path twice (idempotent); then add file
MKDIR_IDEMPOTENT = [
    {"op": "mkdir", "args": ["/p/q"], "expected": None},
    {"op": "mkdir", "args": ["/p/q"], "expected": None},
    {"op": "addContentToFile", "args": ["/p/q/r", "ok"], "expected": None},
    {"op": "readContentFromFile", "args": ["/p/q/r"], "expected": "ok"},
]

# Multiple appends (problem: append to existing file)
MULTIPLE_APPENDS = [
    {"op": "addContentToFile", "args": ["/log", "a"], "expected": None},
    {"op": "addContentToFile", "args": ["/log", "b"], "expected": None},
    {"op": "addContentToFile", "args": ["/log", "c"], "expected": None},
    {"op": "readContentFromFile", "args": ["/log"], "expected": "abc"},
]

# Interleaved ops matching problem style
INTERLEAVED = [
    {"op": "ls", "args": ["/"], "expected": []},
    {"op": "mkdir", "args": ["/go"], "expected": None},
    {"op": "mkdir", "args": ["/go/og"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["go"]},
    {"op": "ls", "args": ["/go"], "expected": ["og"]},
    {"op": "addContentToFile", "args": ["/go/og/g", "g"], "expected": None},
    {"op": "ls", "args": ["/go/og"], "expected": ["g"]},
    {"op": "readContentFromFile", "args": ["/go/og/g"], "expected": "g"},
]

# --- Additional cases matching LeetCode constraints and common judge patterns ---
# (Problem only publishes one example; these are derived from constraints and typical design-question tests.)

# addContentToFile without prior mkdir: parent dirs must be created (problem: "create that file")
ADD_FILE_WITHOUT_MKDIR = [
    {"op": "addContentToFile", "args": ["/new/dir/file", "content"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["new"]},
    {"op": "ls", "args": ["/new"], "expected": ["dir"]},
    {"op": "ls", "args": ["/new/dir"], "expected": ["file"]},
    {"op": "readContentFromFile", "args": ["/new/dir/file"], "expected": "content"},
]

# Content length 1 (constraint: 1 <= content.length <= 50)
CONTENT_LENGTH_ONE = [
    {"op": "addContentToFile", "args": ["/x", "a"], "expected": None},
    {"op": "readContentFromFile", "args": ["/x"], "expected": "a"},
    {"op": "ls", "args": ["/"], "expected": ["x"]},
]

# Single-segment path (path "/a" -> length 2; constraint path.length >= 1)
SINGLE_SEGMENT_PATH = [
    {"op": "mkdir", "args": ["/a"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["a"]},
    {"op": "addContentToFile", "args": ["/a/b", "f"], "expected": None},
    {"op": "readContentFromFile", "args": ["/a/b"], "expected": "f"},
]

# ls("/") twice on empty root (both return [])
LS_ROOT_TWICE_EMPTY = [
    {"op": "ls", "args": ["/"], "expected": []},
    {"op": "ls", "args": ["/"], "expected": []},
]

# Many entries in one directory -> lexicographic order (constraint: no duplicate names)
MANY_ENTRIES_LEXICOGRAPHIC = [
    {"op": "mkdir", "args": ["/d/m"], "expected": None},
    {"op": "mkdir", "args": ["/d/b"], "expected": None},
    {"op": "mkdir", "args": ["/d/a"], "expected": None},
    {"op": "addContentToFile", "args": ["/d/c", "c"], "expected": None},
    {"op": "addContentToFile", "args": ["/d/z", "z"], "expected": None},
    {"op": "ls", "args": ["/d"], "expected": ["a", "b", "c", "m", "z"]},
]

# Longer content (constraint: content.length <= 50)
LONGER_CONTENT = [
    {"op": "addContentToFile", "args": ["/f", "hello world from leetcode file system"], "expected": None},
    {"op": "readContentFromFile", "args": ["/f"], "expected": "hello world from leetcode file system"},
]

# Same as official example but with extra ls at each level (mirrors problem explanation)
OFFICIAL_STYLE_EXTRA_LS = [
    {"op": "ls", "args": ["/"], "expected": []},
    {"op": "mkdir", "args": ["/a/b/c"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["a"]},
    {"op": "ls", "args": ["/a"], "expected": ["b"]},
    {"op": "ls", "args": ["/a/b"], "expected": ["c"]},
    {"op": "addContentToFile", "args": ["/a/b/c/d", "hello"], "expected": None},
    {"op": "ls", "args": ["/"], "expected": ["a"]},
    {"op": "readContentFromFile", "args": ["/a/b/c/d"], "expected": "hello"},
]

ALL_TEST_CASES = [
    ("Example 1", EXAMPLE_1),
    ("Example 2", EXAMPLE_2),
    ("Append content", EXAMPLE_3),
    ("ls file path", EXAMPLE_4),
    ("Lexicographic order", LEXICOGRAPHIC_ORDER),
    ("Root only", ROOT_ONLY),
    ("Deep path", DEEP_PATH),
    ("Dir and file same level", DIR_AND_FILE_SAME_LEVEL),
    ("mkdir idempotent", MKDIR_IDEMPOTENT),
    ("Multiple appends", MULTIPLE_APPENDS),
    ("Interleaved", INTERLEAVED),
    # LeetCode-style / constraint-derived
    ("Add file without mkdir", ADD_FILE_WITHOUT_MKDIR),
    ("Content length one", CONTENT_LENGTH_ONE),
    ("Single segment path", SINGLE_SEGMENT_PATH),
    ("ls root twice empty", LS_ROOT_TWICE_EMPTY),
    ("Many entries lexicographic", MANY_ENTRIES_LEXICOGRAPHIC),
    ("Longer content", LONGER_CONTENT),
    ("Official style extra ls", OFFICIAL_STYLE_EXTRA_LS),
]
