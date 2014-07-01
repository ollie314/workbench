"""
Tests for `workbench` module.
"""

class TestWorkbench(object):
    ''' Test Workbench Server '''

    def test_server(self, workbench_conn):
        patch_coverage_for_gevent()

        ''' Test the workbench Server '''
        print '\nStarting up the Workbench server...'
        return True
