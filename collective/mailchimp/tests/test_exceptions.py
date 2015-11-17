import unittest


class TestExceptions(unittest.TestCase):

    def test_SerializationError_captures_obj(self):
        from ..exceptions import SerializationError
        dummy_obj = object()
        error = SerializationError(dummy_obj)
        self.assertEqual(error.obj, dummy_obj)
        self.assertIn(dummy_obj.__str__(), error.__str__())

    def test_DeserializationError_captures_obj(self):
        from ..exceptions import DeserializationError
        dummy_obj = object()
        error = DeserializationError(dummy_obj)
        self.assertEqual(error.obj, dummy_obj)
        self.assertIn(dummy_obj.__str__(), error.__str__())

    def test_PostRequestError_captures_exc(self):
        from ..exceptions import PostRequestError
        exc = Exception()
        caught = PostRequestError(exc)
        self.assertEqual(caught.exc, exc)
        self.assertIn(exc.__str__(), caught.__str__())

    def test_MailChimpException_attrs(self):
        from ..exceptions import MailChimpException
        code = -90
        error = 'Method fake_method is not exported by this server'
        exc = MailChimpException(code, error)
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.error, error)
        self.assertIn(error, exc.__str__())
