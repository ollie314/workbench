"""
Tests for `workbench` module.
"""
import zerorpc
import multiprocessing
import workbench.server.workbench as workbench_server

class TestWorkbench(object):

    def test_workbench(self):
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
