
''' Help worker '''

class Help(object):
    ''' This worker computes help for any 'info' object '''
    dependencies = ['info']

    def execute(self, input_data):
        ''' Fixme: have this do something more interesting '''
        return input_data

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' help.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    input_data = workbench.info('meta')

    # Execute the worker (unit test)
    worker = Help()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    print output['output']

    # Execute the worker (server test)
    output = workbench.work_request('help', 'meta')
    print '\n<<< Server Test >>>'
    print output['help']['output']

if __name__ == "__main__":
    test()
