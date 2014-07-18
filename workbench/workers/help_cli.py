
''' HelpCLI worker '''

import colorama; colorama.init()
from colorama import Fore, Style

class HelpCLI(object):
    ''' This worker computes help (CLI, colored) for a worker '''
    dependencies = ['worker_info']

    def execute(self, input_data):
        fields = ['name', 'doc', 'dependencies', 'mod_time']
        data = input_data['worker_info']
        dependencies = str([str(dep) for dep in data['dependencies']])
        dependencies = dependencies.replace('\'','')
        output = '\n%s%s%s %s%s%s:' % (Style.BRIGHT, Fore.YELLOW, data['name'], Style.RESET_ALL, Fore.BLUE, dependencies)
        output += '%s\n%s%s' % (Fore.GREEN, data['doc'], Fore.RESET)
        return {'output': output}

# Unit test: Create the class, the proper input and run the execute() method for a test
def test():
    ''' help_cli.py: Unit test'''

    # This worker test requires a local server running
    import zerorpc
    workbench = zerorpc.Client(timeout=300, heartbeat=60)
    workbench.connect("tcp://127.0.0.1:4242")

    # Generate input for the worker
    input_data = workbench.worker_info('meta')

    # Execute the worker (unit test)
    worker = HelpCLI()
    output = worker.execute(input_data)
    print '\n<<< Unit Test >>>'
    print output['output']

    # Execute the worker (server test)
    output = workbench.work_request('help_cli', 'meta')
    print '\n<<< Server Test >>>'
    print output['help_cli']['output']

if __name__ == "__main__":
    test()
