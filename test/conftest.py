"""
Tests for `workbench` module.
"""

def pytest_generate_tests(metafunc):
    if 'worker' in metafunc.fixturenames:
        print 'Getting worker list...'
        workers = metafunc.cls.get_worker_list()
        metafunc.parametrize('worker', workers)
    else:
        print 'WTF %s' % metafunc.fixturenames
