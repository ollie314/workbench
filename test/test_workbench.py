"""
Tests for `workbench` module.
"""

class TestWorkbench(object):
    ''' Test Workbench Class '''

    def test_worker(self, worker, workbench_conn):
        ''' Test a specific worker '''
        print 'Testing %s...' % worker
        assert workbench_conn.test_worker(worker)
