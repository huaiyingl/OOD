"""
Problem:
Design Unix File Search API to search file with different arguments as "extension", "name", "size" ...
The design should be maintainable to add new contraints.

Requirements:
- The design should be maintainable to add new contraints
- Search with different filters: extension, name, size
- Search with different operators: and, or, not

References:
https://leetcode.com/discuss/interview-question/609070/amazon-ood-design-unix-file-search-api
https://leetcode.com/discuss/interview-question/object-oriented-design/5418003/Unix-File-API-Amazon-OOD-My-Take
https://www.acwing.com/blog/content/47999/\
"""

"""
Objects:
- File
- Filter
- FileSystem: search method


Workflow:

"""

from abc import ABC, abstractmethod
from typing import List
from enum import Enum


class File:
    """Class representing a file in the file system."""
    
    def __init__(self, name: str, size: int = 0, extension: str = ""):
        self.name = name
        self.size = size
        self.extension = extension
        self.is_directory = False
        self.children: List[File] = []
    
    def add_child(self, child: 'File') -> None:
        if not self.is_directory:
            raise ValueError(f"{self.name} is not a directory")
        self.children.append(child)
    

class ComparisonOperator(Enum):
    """Enumeration of comparison operators for numerical filters."""
    EQ = "=="
    NE = "!="
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    
    def apply(self, a: int, b: int) -> bool:
        """Apply the comparison operator to two values."""
        if self == ComparisonOperator.EQ:
            return a == b
        elif self == ComparisonOperator.NE:
            return a != b
        elif self == ComparisonOperator.LT:
            return a < b
        elif self == ComparisonOperator.LE:
            return a <= b
        elif self == ComparisonOperator.GT:
            return a > b
        elif self == ComparisonOperator.GE:
            return a >= b
        else:
            raise ValueError(f"Unknown operator: {self}")


class Filter(ABC):
    """Abstract base class for all filters."""
    
    @abstractmethod
    def apply(self, file: File) -> bool:
        pass
    
    def and_filter(self, other: 'Filter') -> 'AndFilter':
        return AndFilter([self, other])
    
    def or_filter(self, other: 'Filter') -> 'OrFilter':
        return OrFilter([self, other])
    
    def not_filter(self) -> 'NotFilter':
        return NotFilter(self)
    

class AndFilter(Filter):
    """Filter that combines multiple filters with AND logic."""
    
    def __init__(self, filters: List[Filter]):
        self.filters = filters
    
    def apply(self, file: File) -> bool:
        # all() returns True if all elements of the iterable are true
        return all(filter.apply(file) for filter in self.filters)
    

class OrFilter(Filter):
    """Filter that combines multiple filters with OR logic."""
    
    def __init__(self, filters: List[Filter]):
        self.filters = filters
    
    def apply(self, file: File) -> bool:
        # any() returns True if any element of the iterable is true
        return any(filter.apply(file) for filter in self.filters)


class NotFilter(Filter):
    """Filter that negates another filter."""
    
    def __init__(self, filter: Filter):
        self.filter = filter
    
    def apply(self, file: File) -> bool:
        # not() returns True if the operand is false, and False if the operand is true
        return not self.filter.apply(file)


class NameFilter(Filter):
    """Filter that matches files by name."""
    
    def __init__(self, name: str):
        self.name = name
    
    def apply(self, file: File) -> bool:
        if file.is_directory:
            return False
        return file.name == self.name


class ExtensionFilter(Filter):
    """Filter that matches files by extension."""
    
    def __init__(self, extension: str):
        self.extension = extension
    
    def apply(self, file: File) -> bool:
        if file.is_directory:
            return False
        
        return file.extension == self.extension


class SizeFilter(Filter):
    """Filter that matches files by size."""
    
    def __init__(self, size: int, operator: ComparisonOperator):
        self.size = size
        if operator not in ComparisonOperator:
            raise ValueError(f"Invalid operator: {operator}")
        self.operator = operator
    
    def apply(self, file: File) -> bool:
        if file.is_directory:
            return False
        return self.operator.apply(file.size, self.size)



class FileSearch:
    """Class for searching files in a file system."""

    # a method that belongs to a class, rather than a specific instance of a class
    @staticmethod
    def search(root: File, filter: Filter) -> List[File]:
        if not root.is_directory:
            raise ValueError("Search root must be a directory")
        
        results = []
        
        # Helper function for DFS traversal
        def dfs(dir: File) -> None:
            # Then check all children
            for file in dir.children:
                if file.is_directory:
                    dfs(file)
                elif filter.apply(file):
                    results.append(file)
        
        dfs(root)
        return results
