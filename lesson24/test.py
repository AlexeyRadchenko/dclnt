from quadratic_equation import discriminant, qe_roots
from testing_data import TEST_INPUTS, TEST_OUTPUT_DISCRIMINANT, TEST_OUTPUT_ROOTS
import unittest


class QuadraticEquationTest(unittest.TestCase):

    def test_discriminant_calculation(self):
        for num_test, input_data in enumerate(TEST_INPUTS):
            a, b, c = input_data
            info = 'test {}'.format(num_test)
            function_result = discriminant(a, b, c)
            self.assertEqual(TEST_OUTPUT_DISCRIMINANT[num_test], function_result, info)

    def test_qe_roots_calculation(self):
        for num_test, input_data in enumerate(TEST_INPUTS):
            a, b, c = input_data
            info = 'test {}'.format(num_test)
            function_result = qe_roots(a, b, c)
            if num_test != 2:
                self.assertEqual(TEST_OUTPUT_ROOTS[num_test], function_result, info)
            else:
                self.assertIsNone(function_result, msg=info)


if __name__ == '__main__':
    unittest.main()
