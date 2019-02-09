# -*- coding: utf-8 -*-
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
        detail = 'Method fake_method is not exported by this server'
        errors = [
            {
                "field": "interests",
                "message": "Schema describes object, array found instead",
            }
        ]
        exc = MailChimpException(code, detail, errors)
        self.assertEqual(exc.code, code)
        self.assertEqual(exc.detail, detail)
        self.assertEqual(exc.errors, errors)
        self.assertIn(detail, exc.__str__())
        self.assertIn('interests', exc.__str__())
