import unittest

class ImportTestCase(unittest.TestCase):
    def test_import(self):
        import aupyom

    def test_import_all(self):
        from aupyom import *
