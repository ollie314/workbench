''' Spin up Workbench Server (this is a singleton module)'''

import multiprocessing
import workbench.server.workbench as workbench_server

print '\nStarting up the Workbench server...'
process = multiprocessing.Process(target=workbench_server.run)
process.start()

def shutdown():
    # Terminate the workbench server process
    print '\nShutting down the Workbench server...'
    process.terminate()
