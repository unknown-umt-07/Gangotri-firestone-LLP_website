import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_vercel_wsgi_entrypoint():
    os.environ['USE_FIREBASE'] = 'false'
    os.environ['VERCEL'] = '1'

    try:
        from api.index import application
    finally:
        os.environ.pop('USE_FIREBASE', None)
        os.environ.pop('VERCEL', None)

    assert application is not None
