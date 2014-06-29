"""
Tests for `workbench` module.
"""
import pytest
import subprocess
import time
import zerorpc

class TestWorkbench(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_workbench(self):
        # Run the workbench server
        self.server_process = self.subprocess_manager('workbench')

        # Start up workbench connection
        workbench = zerorpc.Client()
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
        self.server_process.terminate()
        time.sleep(3)

    @classmethod
    def teardown_class(cls):
        pass

    def subprocess_manager(self, exec_args):
        try:
            process = subprocess.Popen(exec_args.split())
        except OSError:
            raise RuntimeError('Could not run workbench server (either not installed or not in path): %s' % (exec_args))
        return process


if __name__ == '__main__':
    test = TestWorkbench()
    test.test_workbench()
