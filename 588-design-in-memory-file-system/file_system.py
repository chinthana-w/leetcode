"""
LeetCode 588. Design In-Memory File System

Implement a data structure that simulates an in-memory file system.
"""


class FileSystem:
    """
    In-memory file system with:
    - ls(path): list directory contents (lexicographic) or [filename] if path is a file
    - mkdir(path): create directory and any missing parents
    - addContentToFile(filePath, content): create file or append content
    - readContentFromFile(filePath): return file content as string
    """

    def __init__(self) -> None:
        self.root = Directory("")
        self.dirs = {"": self.root, "/": self.root}
        self.files = {}

    def ls(self, path: str) -> list[str]:
        """
        List directory contents at path in lexicographic order.
        If path is a file, return list containing only that file's name.
        """
        if path in self.files:
            return [self.files[path].name]
        else:
            dir = self.dirs[path]
            return sorted([i.name for i in dir.children.values()])

    def mkdir(self, path: str) -> None:
        """
        Create directory at path. Create intermediate directories as needed.
        """
        if path == "" or path == "/":
            return
        
        path_split = path.split("/")[::-1]
        cd = self.root

        while len(path_split) > 0:
            new_dir_name = path_split.pop()
            new_dir_path = cd.getPath() + "/" + new_dir_name
            if new_dir_path in self.dirs:
                new_dir = self.dirs[new_dir_path]
            else:
                new_dir = Directory(new_dir_path)
                self.dirs[new_dir_path] = new_dir
                cd.children[new_dir_path] = new_dir
                new_dir.parent = cd

            cd = new_dir

    def addContentToFile(self, filePath: str, content: str) -> None:
        """
        If filePath does not exist, create file with content.
        If filePath exists, append content to the file.
        """
        if filePath in self.files:
            self.files[filePath].content += content
        else:
            filePath = filePath.split("/")
            file_name = filePath.pop()
            filePath = "/".join(filePath)
            self.mkdir(filePath)
            cd = self.dirs[filePath]

            file = File(file_name, content)
            file.parent = cd
            filePath = filePath + "/" + file_name
            cd.children[filePath] = file
            self.files[filePath] = file

    def readContentFromFile(self, filePath: str) -> str:
        """
        Return the content of the file at filePath.
        """
        return self.files[filePath].content

class Directory:
    def __init__(self, name) -> None:
        self.name = name.split("/").pop()
        self.parent = self
        self.children = {}

    def __repr__(self) -> str:
        return f"{self.name}/"

    def getPath(self):
        if self.parent == self:
            return self.name
        else:
            return self.parent.getPath() + "/" + self.name

class File:
    def __init__(self, name, content) -> None:
        self.name = name
        self.parent = self
        self.content = content

    def getPath(self):
        return self.parent.getPath() + self.name