from unittest import TestCase
from conftest import app

from src.covid19.blueprints.owid.owid_model_import import OwidImport


class Test(TestCase):
    def test_run_test(self):
        continents = OwidImport.get_continents()
        for continent in continents:
            app.logger.info(continent)
        self.assertTrue(True)
