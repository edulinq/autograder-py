import os

import edq.testing.unittest

import autograder.util.prepare_submission

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR: str = os.path.join(THIS_DIR, 'testdata')

class TestSubmission(edq.testing.unittest.BaseTest):
    """
    Tests for autograder submissions.
    """

    def test_prepare_simple(self):
        """ Test preparing a single (single file) submission. """

        for ext in ['py', 'ipynb']:
            path = os.path.join(DATA_DIR, 'code', 'simple.' + ext)
            submission = autograder.util.prepare_submission.prepare(path)

            self.assertIn('__all__', dir(submission))
            self.assertIn('SOME_CONSTANT', dir(submission.__all__))
            self.assertEqual(submission.__all__.SOME_CONSTANT, 1)

            self.assertIn('simple', dir(submission))
            self.assertIn('SOME_CONSTANT', dir(submission.simple))
            self.assertEqual(submission.simple.SOME_CONSTANT, 1)

    def test_prepare_nested(self):
        """ Test preparing a nested submission. """

        path = os.path.join(DATA_DIR, 'submission', 'nested')
        submission = autograder.util.prepare_submission.prepare(path)

        self.assertIn('__all__', dir(submission))
        self.assertIn('SOME_CONSTANT', dir(submission.__all__))
        self.assertEqual(submission.__all__.SOME_CONSTANT, 1)

        self.assertIn('nested1', dir(submission))
        self.assertIn('nested2', dir(submission.nested1))
        self.assertIn('nested', dir(submission.nested1.nested2))
        self.assertIn('SOME_CONSTANT', dir(submission.nested1.nested2.nested))
        self.assertEqual(submission.nested1.nested2.nested.SOME_CONSTANT, 1)
