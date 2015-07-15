from nose.tools import raises

from .util import TestCase, load_json_fixture, load_csv

from babbage.cube import Cube
from babbage.exc import BindingException


class CubeTestCase(TestCase):

    def setUp(self):
        super(CubeTestCase, self).setUp()
        self.cra_model = load_json_fixture('models/cra.json')
        self.cra_table = load_csv('cra.csv')
        self.cube = Cube(self.engine, 'cra', self.cra_model)

    def test_table_exists(self):
        assert self.engine.has_table(self.cra_table.name)

    def test_table_load(self):
        table = self.cube._load_table(self.cra_table.name)
        assert table is not None

    def test_table_pk(self):
        pk = self.cube._get_fact_pk()
        assert pk is not None

    @raises(BindingException)
    def test_table_load_nonexist(self):
        self.cube._load_table('lalala')

    @raises(BindingException)
    def test_dimension_column_nonexist(self):
        model = self.cra_model.copy()
        model['dimensions']['cofog1']['attributes']['name']['column'] = 'lala'
        self.cube = Cube(self.engine, 'cra', model)
        self.cube.map('cofog1.name')

    def test_dimension_column_qualified(self):
        model = self.cra_model.copy()
        name = 'cra.cofog1_name'
        model['dimensions']['cofog1']['attributes']['name']['column'] = name
        self.cube = Cube(self.engine, 'cra', model)
        self.cube.map('cofog1.name')

    def test_map_ref(self):
        assert self.cube.map('amount').name == 'amount'
        assert self.cube.map('cofog1.name').name == 'cofog1_name'
        assert self.cube.map('cofog1').name == 'cofog1_name'