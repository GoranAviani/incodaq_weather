from django.test import TestCase

# Create your tests here.
from .processing import split_by_char


class ProcessingFile(TestCase):
    
    def test_split_by_char(self):
        result = split_by_char("15:33", ":")
        self.assertEqual(result, ("stringWasSplitted", ["15","33"]))

