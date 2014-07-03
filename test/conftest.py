"""
Tests for `workbench` module.
"""

import zerorpc
import pytest
import workbench_singleton # This spins up the server

@pytest.fixture(scope='session')
def workbench_conn(request):
    ''' Workbench Fixture '''

    # Connect to the server
    conn = zerorpc.Client(timeout=300)
    conn.connect('tcp://localhost:4242')

    # Add a finalize method
    request.addfinalizer(workbench_singleton.shutdown)

    # Return the connection
    return conn
