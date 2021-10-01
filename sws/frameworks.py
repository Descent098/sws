"""This module helps to give some details about frameworks used in a site (where available) including:

- The UI/frontend Frameworks(bulma, jquery, react, bootstrap etc.)
- Proxy systems (Nginx, apache etc.)
- Backend frameworks (Wordpress, Drupal, squarespace, wix, django etc.)


"""

from dataclasses import dataclass
from typing import List


@dataclass
class Test:
    name:str
    description:str
    successful:bool = False

    def test(self) -> bool:
        return NotImplementedError("Test subclasses must implement test()")

@dataclass
class Framework:
    likelyhood:float # The number of successful tests divided by total tests (roughly percent likelyhood)
    tests:List[Test]
    frameworks:List[Test]

    @property
    def frameworks(self) -> List[Test]:
        for current_class in Framework.__subclasses__():
            
            ...
        ...

    @property
    def likelyhood(self) -> float:
        self.likelyhood = ...
        return self.likelyhood

    def run_tests(self) -> int:
        successful_tests = 0
        for test in self.tests:
            if test.test():
                successful_tests += 1

@dataclass
class UIFramework(Framework):
    ...

@dataclass
class ProxyFramework(Framework):
    ...

@dataclass
class BackendFramework(Framework):
    ...
