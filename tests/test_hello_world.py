import unittest

from project_name import hello_world


class TestHelloWorld(unittest.TestCase):

    def test_hello_world(self) -> None:
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.assertEqual(hello_world(), "Hello, World!")
