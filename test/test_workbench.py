"""
Tests for `workbench` module.
"""

import zerorpc
import multiprocessing
import workbench.server.workbench as workbench_server

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

    def test_workbench(self):

        # Monkey path coverage so it works with gevent
        patch_coverage_for_gevent()

        # Run the workbench server
        p = multiprocessing.Process(target=workbench_server.run)
        p.start()

        # Start up workbench connection
        workbench = zerorpc.Client(timeout=300)
        workbench.connect('tcp://localhost:4242')

        # Get all the dynamically loaded workers
        workers = workbench.list_all_workers()
        for worker in workers:

            # Invoke worker tests
            print 'Testing %s...' % worker
            print workbench.test_worker(worker)

        # Close the workbench connection
        workbench.close()

        # Terminate the workbench server process
        print '\nShutting down the Workbench server...'
        p.terminate()


if __name__ == '__main__':
    test = TestWorkbench()
    test.test_workbench()
