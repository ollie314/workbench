
""" Workbench Help System """

import inspect
import funcsigs

class HelpSystem(object):
    """ Workbench Help System """
    __version__ = 0.1

    def __init__(self, workbench_instance):
        """Initialize the Help System.

        Args:
            workbench_instance: an instance of a workbench class so that we can make
                                introspection calls and calls to help workers
        """

        # Set workbench instance
        self.my_wb = workbench_instance

        # Announce Version
        print '<<< Workbench Help System %s >>>' % self.__version__

    def help(self, cli=False):
        """ Returns help commands """

        if cli:
            help_str =  '\nWelcome to Workbench: Here\'s a list of help commands:'
            help_str += '\n\t - $ workbench help_basic : for beginner help'
            help_str += '\n\t - $ workbench help_commands : for command help'
            help_str += '\n\t - $ workbench help_workers : for a list of workers'
            help_str += '\n\t - $ workbench help_advanced : for advanced help'
            help_str += '\n\nSee http://github.com/SuperCowPowers/workbench for more information'
            return help_str

        help_str =  '\nWelcome to Workbench: Here\'s a list of help commands:'
        help_str += '\n\t - Run workbench.help_basic() for beginner help'
        help_str += '\n\t - Run workbench.help_commands() for command help'
        help_str += '\n\t - Run workbench.help_workers() for a list of workers'
        help_str += '\n\t - Run workbench.help_advanced() for advanced help'
        help_str += '\n\nSee http://github.com/SuperCowPowers/workbench for more information'
        return help_str

    def help_basic(self, cli=False):
        """ Returns basic help commands """

        if cli:
            help_str =  '\nWorkbench: Getting started...'
            help_str += '\n\t - 1) $ workbench help_commands : for a list of commands'
            help_str += '\n\t - 2) $ workbench help_command store_sample : for into on a specific command'
            help_str += '\n\t - 3) $ workbench help_workers : for a list a workers'
            help_str += '\n\t - 4) $ workbench help_worker meta : for info on a specific worker'
            help_str += '\n\t - 5) $ workbench store_sample /path/to/file.exe'
            help_str += '\n\t - 6) $ workbench meta md5 (from store sample)'
            return help_str

        help_str =  '\nWorkbench: Getting started...'
        help_str += '\n\t - 1) $ print workbench.help_commands() for a list of commands'
        help_str += '\n\t - 2) $ print workbench.help_command(\'store_sample\') for into on a specific command'
        help_str += '\n\t - 3) $ print workbench.help_workers() for a list a workers'
        help_str += '\n\t - 4) $ print workbench.help_worker(\'meta\') for info on a specific worker'
        help_str += '\n\t - 5) $ my_md5 = workbench.store_sample(...)'
        help_str += '\n\t - 6) $ output = workbench.work_request(\'meta\', my_md5)'
        return help_str

    def help_commands(self, cli=False):
        """ Returns a big string of Workbench commands and signatures """
        help_string = 'Workbench Commands:'
        for name, meth in inspect.getmembers(self.my_wb, predicate=inspect.ismethod):
            if not name.startswith('_'):
                sig = str(funcsigs.signature(meth))

                # Strip off the () from the signature and replace ',' with ''
                if cli:
                    sig = ' '+sig[1:-1].replace(',','')
                    sig = sig.replace('cli=False','')
                    sig = sig.replace('predicate={}','\'{"type_tag","exe"}\' (optional MongoDB predicate)')

                help_string += '\n\t%s%s' % (name, sig)
        return help_string

    def help_command(self, command, cli=False):
        """ Returns a specific Workbench command and docstring """
        for name, meth in inspect.getmembers(self.my_wb, predicate=inspect.ismethod):
            if name == command:
                return '\n Command: %s%s \n%s' % (name, funcsigs.signature(meth), meth.__doc__)
        return '%s command not found.. misspelled?' % command

    def help_workers(self, cli=False):
        """ Returns a big string of the loaded Workbench workers and their dependencies """
        help_string = 'Workbench Workers:'
        for worker in self.my_wb.list_all_workers():
            if cli:
                help_string += self.my_wb.work_request('help_cli', worker)['help_cli']['output']
            else:
                help_string += self.my_wb.work_request('help', worker)['help']['output']
        return help_string

    def help_worker(self, worker, cli=False):
        """ Returns a specific Workbench worker and docstring """
        if cli:
            return self.my_wb.work_request('help_cli', worker)['help_cli']['output']
        else:
            return self.my_wb.work_request('help', worker)['help']['output']

    def help_advanced(self, cli=False):
        """ Returns advanced help commands """
        help_str =  '\nWoo! Advanced... <fixme: add documentation for advanced> :)'
        help_str += '\n\nSee http://github.com/SuperCowPowers/workbench for more information'
        return help_str

    def help_everything(self, cli=False):
        """Executes help_system.py test."""

        # Call all the methods for the help system
        output = self.help()
        output += self.help_advanced()
        output += self.help_basic()

        # Yes this is verbose but useful to see what commands
        # have proper docstrings and make sure help works, etc
        output += self.help_commands()
        for command in self.my_wb.list_all_commands():
            output += self.help_command(command)

        # Yes this is verbose but useful to see what workers
        # have proper docstrings and make sure help works, etc
        output += self.help_workers()
        for worker in self.my_wb.list_all_workers():
            output += self.help_worker(worker)

        return output
