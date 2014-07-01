"""
Tests for `workbench` module.
"""

import zerorpc
import pytest
import workbench_single

@pytest.fixture(scope='session')
def workbench_conn(request):
    ''' Workbench Fixture '''
    import workbench_single # This spins up the server

    # Connect to the server
    conn = zerorpc.Client(timeout=300)
    conn.connect('tcp://localhost:4242')

    # Add a finalize method
    request.addfinalizer(workbench_single.shutdown)

    # Return the connection
    return conn

def pytest_generate_tests(metafunc):
    if 'worker' in metafunc.fixturenames:
        print 'Getting worker list...'
        # Connect to the server
        conn = zerorpc.Client()
        conn.connect('tcp://localhost:4242')
        workers = conn.list_all_workers()
        metafunc.parametrize('worker', workers)
    else:
        print 'WTF %s' % metafunc.fixturenames
