"""
Tests for `workbench` module.
"""
    
class TestWorkbench(object):
    ''' Test Workbench Class '''

    def test_worker(self, worker, workbench_db):
        # Invoke worker test
        print 'Testing %s...' % worker
        assert workbench_db.test_worker(worker)
