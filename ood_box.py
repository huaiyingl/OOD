"""
Problem Statement:
Designing a box system that can contain items and other boxes.

Requirements:
1. Box can contain items and other boxes.
2. Box can have a parent box.
3. Box can have a list of items.
"""


from abc import ABC, abstractmethod
from typing import List

# Item is the base class for all items in the box system
class Item(ABC):
    def __init__(self, name: str):
        self.name = name
        self.parent = None  
    
    @abstractmethod
    def get_type(self) -> str:
        pass

# ConcreteItem is a concrete item in the box system
class ConcreteItem(Item):
    def __init__(self, name: str):
        super().__init__(name)
    
    def get_type(self) -> str:
        return "ConcreteItem"

class Toothbrush(ConcreteItem):
    def get_type(self) -> str:
        return "Toothbrush"

class Book(ConcreteItem):
    def get_type(self) -> str:
        return "Book"

# Box can contain items and other boxes
class Box(Item):
    def __init__(self, name: str):
        super().__init__(name)
        self.items: List[Item] = []
    
    def get_type(self) -> str:
        return "Box"
    
    def add_item(self, item: Item):
        self.items.append(item)
        item.parent = self  
    
    def remove_item(self, item: Item):
        if item in self.items:
            self.items.remove(item)
            item.parent = None
    
    def get_all_concrete_items(self) -> List[ConcreteItem]:
        result = []
        
        # DFS
        for item in self.items:
            if isinstance(item, ConcreteItem):
                result.append(item)
            elif isinstance(item, Box):
                # recursion case
                items_in_box = item.get_all_concrete_items()
                result.extend(items_in_box)
        
        return result
    