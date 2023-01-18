from unittest import TestCase


def assertIsClose(self: TestCase, a: list, b: list, precision: int = 4):
    # round to precision to avoid floating point errors
    b = [round(item, precision) for item in b]
    self.assertEqual(a, b)
