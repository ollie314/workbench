"""
Tests for `workbench` module.
"""

import zerorpc
import multiprocessing
import workbench.server.workbench as workbench_server
import pytest
import time

# Fixme: There are lots of bad things in this file need to fix them

# Fixme: Make this a more formal singleton class/method
process = None
def start_database():
    global process
    if not process:
        print '\nStarting up the Workbench server...'
        process = multiprocessing.Process(target=workbench_server.run)
        process.start()
    return process

@pytest.yield_fixture(scope='session')
def workbench_db():
    ''' Workbench Database  '''

    # Run the workbench server
    process = start_database()

    # Start up workbench connection
    workbench_conn = zerorpc.Client(timeout=300)
    workbench_conn.connect('tcp://localhost:4242')

    # Hand over the workbench connection to tests who need it
    yield workbench_conn

    # Close the workbench connection
    workbench_conn.close()

    # Terminate the workbench server process
    print '\nShutting down the Workbench server...'
    process.terminate()

def worker_list():
    ''' Get the worker list from the workbench database '''

    # Run the workbench server
    print '\nStarting up the Workbench server...'
    process = start_database()

    # Start up workbench connection
    workbench_conn = zerorpc.Client()
    workbench_conn.connect('tcp://localhost:4242')

    # Get all the workers
    workers = workbench_conn.list_all_workers()

    # Close the workbench connection
    workbench_conn.close()

    # Return worker list
    return workers

def pytest_generate_tests(metafunc):
    if 'worker' in metafunc.fixturenames:
        print 'Getting worker list...'
        workers = worker_list()
        metafunc.parametrize('worker', workers)
    else:
        print 'WTF %s' % metafunc.fixturenames
