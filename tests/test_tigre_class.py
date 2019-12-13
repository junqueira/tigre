from unittest import TestCase, mock
from tigre.core import Tigre


class TestTigreClassStaticAttributes(TestCase):
    def setUp(self):
        self.tigre = Tigre()

    def test_should_has_empty_caps(self):
        self.assertEqual(self.tigre.caps, {})

    def test_should_has_empty_fixed_caps(self):
        self.assertEqual(self.tigre.fixed_caps, {})

    def test_should_has_empty_capabilities_property(self):
        self.assertEqual(self.tigre.capabilities, {})

    def test_should_existis_capabilities_on_representation(self):
        self.assertEqual(
            str(self.tigre), 'Tigre(caps={})'
        )

    @mock.patch('selenium.webdriver.Remote')
    def test_build_should_call_selenium(self, mock):
        self.tigre.build()

        mock.assert_called_with(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities={}
        )


class TestTigreClassDynamicAttributes(TestCase):
    def test_should_set_new_attrs(self):
        tigre = Tigre()
        tigre.version

        self.assertTrue(tigre.version)

    def test_new_attr_should_return_callable(self):
        tigre = Tigre()
        tigre.version

        self.assertTrue(hasattr(tigre.version, '__call__'))

    def test_closure_should_return_self(self):
        tigre = Tigre()

        self.assertIs(tigre.version(None), tigre)

    def test_closure_should_insert_new_caps(self):
        tigre = Tigre()
        tigre.version(None)

        self.assertIn('version', tigre.caps)

    def test_closure_should_convert_non_booleans_caps(self):
        tigre = Tigre(default_caps=['version'])
        tigre.version(7)

        self.assertEqual(tigre.caps['version'], '7')

    def test_closure_shouldnt_convert_booleans_caps(self):
        tigre = Tigre(default_caps=['enableVNC'])
        tigre.vnc(True)

        self.assertIn(True, tigre.caps.values())

    def test_should_raises_with_wrog_caps(self):
        tigre = Tigre(default_caps=[])

        with self.assertRaises(AttributeError):
            tigre.test('test')

    def test_should_return_value_if_was_fixed(self):
        tigre = Tigre()
        tigre.fixed_caps = {'batatinha': 123}

        self.assertEqual(tigre.batatinha, 123)