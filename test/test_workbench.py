"""
Tests for `workbench` module.
"""

import zerorpc
import multiprocessing
import workbench.server.workbench as workbench_server
import pytest

# Credit for this patching code goes to
# Vadim Fint (mocksoul)  thanks a bunch you rock
def patch_coverage_for_gevent():
    from coverage import collector as _collector, control as _control
    import collections as _collections
    import gevent as _gevent
    _PyTracer = _collector.PyTracer

    class DataStack(object):
        def __init__(self):
            self.__data = _collections.defaultdict(list)

        def __idx(self):
            return hash(_gevent.getcurrent())

        def pop(self):
            return self.__data[self.__idx()].pop()

        def append(self, value):
            return self.__data[self.__idx()].append(value)

    class PyTracer(_PyTracer):
        def __init__(self):
            _PyTracer.__init__(self)
            self.data_stack = DataStack()

    _collector.PyTracer = PyTracer

    # Patch coverage, so it uses timid simple tracer by default after monkey patching
    _coverage = _control.coverage

    class coverage(_coverage):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('timid', True)
            super(coverage, self).__init__(*args, **kwargs)

    __import__('pyjack').replace_all_refs(_coverage, coverage)


class TestWorkbench(object):

    # Class variables
    workbench_conn = None
    process = None

    @classmethod
    def setup_class(cls):
        # Monkey path coverage so it works with gevent
        # patch_coverage_for_gevent()
        cls.start_workbench()

    @classmethod
    def teardown_class(cls):
        # Close the workbench connection
        TestWorkbench.workbench_conn.close()

        # Terminate the workbench server process
        print '\nShutting down the Workbench server...'
        TestWorkbench.process.terminate()

    @classmethod
    def start_workbench(cls):
        if not TestWorkbench.workbench_conn:
            # Run the workbench server
            print '\nStarting up the Workbench server...'
            TestWorkbench.process = multiprocessing.Process(target=workbench_server.run)
            TestWorkbench.process.start()

            # Start up workbench connection
            TestWorkbench.workbench_conn = zerorpc.Client(timeout=300)
            TestWorkbench.workbench_conn.connect('tcp://localhost:4242')

    @classmethod
    def get_worker_list(cls):
        # Get a list of workers from the workbench server
        cls.start_workbench()
        return TestWorkbench.workbench_conn.list_all_workers()

    def test_worker(self, worker):
        # Invoke worker test
        print 'Testing %s...' % worker
        assert(TestWorkbench.workbench_conn.test_worker(worker))


if __name__ == '__main__':
    test = TestWorkbench()
    test.setup_class()
    test.test_worker('view')
    test.teardown_class()
