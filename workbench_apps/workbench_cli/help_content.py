"""Workbench Interactive Shell Help Content"""

import inspect
from colorama import Fore as F

class WorkbenchShellHelp(object):
    """Workbench CLI Help"""

    def __init__(self):
        ''' Workbench CLI Initialization '''

    def help_cli(self):
        """ Help on Workbench CLI """
        help = '%sWelcome to Workbench CLI Help:%s' % (F.YELLOW, F.RESET)
        help += '\n\t%s> help cli_basic %s for getting started help' % (F.GREEN, F.BLUE)
        help += '\n\t%s> help workers %s for help on available workers' % (F.GREEN, F.BLUE)
        help += '\n\t%s> help search %s for help on searching samples' % (F.GREEN, F.BLUE)
        help += '\n\t%s> help dataframe %s for help on making dataframes' % (F.GREEN, F.BLUE)
        help += '\n\t%s> help commands %s for help on workbench commands' % (F.GREEN, F.BLUE)
        help += '\n\t%s> help topic %s where topic can be a help, command or worker' % (F.GREEN, F.BLUE)
        help += '\n\n%sNote: cli commands are transformed into python calls' % (F.YELLOW)
        help += '\n\t%s> help cli_basic --> help("cli_basic")%s' % (F.GREEN, F.RESET)
        return help

    def help_cli_basic(self):
        """ Help for Workbench CLI Basics """
        help =  '%sWorkbench: Getting started...' % (F.YELLOW)
        help += '\n%sLoad in a sample:'  % (F.GREEN)
        help += '\n\t%s> load_sample /path/to/file' % (F.BLUE)
        help += '\n\n%sNotice the prompt now shows the md5 of the sample...'% (F.YELLOW)
        help += '\n%sRun workers on the sample:'  % (F.GREEN)
        help += '\n\t%s> view' % (F.BLUE)
        help += '\n%sType the \'help workers\' or the first part of the worker <tab>...'  % (F.GREEN)
        help += '\n\t%s> help workers (lists all possible workers)' % (F.BLUE)
        help += '\n\t%s> pe_<tab> (will give you pe_classifier, pe_deep_sim, pe_features, pe_indicators, pe_peid)%s' % (F.BLUE, F.RESET)
        return help

    def help_cli_search(self):
        """ Help for Workbench CLI Search """
        help =  '%sSearch: %s returns sample_sets, a sample_set is a set/list of md5s.' % (F.YELLOW, F.GREEN)
        help += '\n\n\t%sSearch for all samples in the database that are known bad pe files,'  % (F.GREEN)
        help += '\n\t%sthis command returns the sample_set containing the matching items'% (F.GREEN)
        help += '\n\t%s> my_bad_exes = search([\'bad\', \'exe\'])' % (F.BLUE)
        help += '\n\n\t%sRun workers on this sample_set:'  % (F.GREEN)
        help += '\n\t%s> pe_outputs = pe_features(my_bad_exes) %s' % (F.BLUE, F.RESET)
        help += '\n\n\t%sLoop on the generator (or make a DataFrame see >help dataframe)'  % (F.GREEN)
        help += '\n\t%s> for output in pe_outputs: %s' % (F.BLUE, F.RESET)
        help += '\n\t\t%s print output %s' % (F.BLUE, F.RESET)
        return help

    def help_dataframe(self):
        """ Help for making a DataFrame with Workbench CLI """
        help =  '%sMaking a DataFrame: %s how to make a dataframe from raw data (pcap, memory, pe files)' % (F.YELLOW, F.GREEN)
        help += '\n\t%sNote: for memory_image and pe_files see > help dataframe_memory or dataframe_pe'  % (F.GREEN)
        help += '\n\n%sPCAP Example:'  % (F.GREEN)
        help += '\n\t%s> load_sample /path/to/pcap/gold_xxx.pcap [\'bad\', \'threatglass\']' % (F.BLUE)
        help += '\n\t%s> view # view is your friend use it often' % (F.BLUE)
        help += '\n\n%sGrab the http_log from the pcap (also play around with other logs):'  % (F.GREEN)
        help += '\n\t%s> http_log_md5 = view()[\'view\'][\'bro_logs\'][\'http_log\']' % (F.BLUE)
        help += '\n\n%sGrab the http_log from the pcap (also play around with other logs):'  % (F.GREEN)
        help += '\n\t%s> http_log_md5 = view()[\'view\'][\'bro_logs\'][\'http_log\']' % (F.BLUE)
        help += '\n\n\t%sSearch for all samples in the database that are known bad pe files,'  % (F.GREEN)
        help += '\n\t%sthis command returns the sample_set containing the matching items'% (F.GREEN)
        help += '\n\t%s> my_bad_exes = search([\'bad\', \'exe\'])' % (F.BLUE)
        help += '\n\n\t%sRun workers on this sample_set:'  % (F.GREEN)
        help += '\n\t%s> pe_outputs = pe_features(my_bad_exes) %s' % (F.BLUE, F.RESET)
        help += '\n\n\t%sLoop on the generator (or make a DataFrame see > help dataframe'  % (F.GREEN)
        help += '\n\t%s> pe_df = pd.DataFrame(pe_outputs) %s' % (F.BLUE, F.RESET)
        help += '\n\t%s> pe_df.head() %s' % (F.BLUE, F.RESET)
        return help

    def help_dataframe_memory(self):
        """ Help for making a DataFrame with Workbench CLI """
        help =  '%sMaking a DataFrame: %s how to make a dataframe from raw data (pcap, memory, pe files)' % (F.YELLOW, F.GREEN)
        help += '\n\t%sNote: for memory_image and pe_files see > help dataframe_memory or dataframe_pe'  % (F.GREEN)
        help += '\n\n%sPCAP Example:'  % (F.GREEN)
        help += '\n\t%s> load_sample /path/to/pcap/gold_xxx.pcap [\'bad\', \'threatglass\']' % (F.BLUE)
        help += '\n\t%s> view # view is your friend use it often' % (F.BLUE)
        help += '\n\n%sGrab the http_log from the pcap (also play around with other logs):'  % (F.GREEN)
        help += '\n\t%s> http_log_md5 = view()[\'view\'][\'bro_logs\'][\'http_log\']' % (F.BLUE)
        help += '\n\n%sGrab the http_log from the pcap (also play around with other logs):'  % (F.GREEN)
        help += '\n\t%s> http_log_md5 = view()[\'view\'][\'bro_logs\'][\'http_log\']' % (F.BLUE)
        help += '\n\n\t%sSearch for all samples in the database that are known bad pe files,'  % (F.GREEN)
        help += '\n\t%sthis command returns the sample_set containing the matching items'% (F.GREEN)
        help += '\n\t%s> my_bad_exes = search([\'bad\', \'exe\'])' % (F.BLUE)
        help += '\n\n\t%sRun workers on this sample_set:'  % (F.GREEN)
        help += '\n\t%s> pe_outputs = pe_features(my_bad_exes) %s' % (F.BLUE, F.RESET)
        help += '\n\n\t%sLoop on the generator (or make a DataFrame see > help dataframe'  % (F.GREEN)
        help += '\n\t%s> pe_df = pd.DataFrame(pe_outputs) %s' % (F.BLUE, F.RESET)
        help += '\n\t%s> pe_df.head() %s' % (F.BLUE, F.RESET)
        return help

    def help_dataframe_pe(self):
        """ Help for making a DataFrame with Workbench CLI """
        help =  '%sMaking a DataFrame: %s how to make a dataframe from raw data (pcap, memory, pe files)' % (F.YELLOW, F.GREEN)
        help += '\n\t%sNote: for memory_image and pe_files see > help dataframe_memory or dataframe_pe'  % (F.GREEN)
        help += '\n\n%sPCAP Example:'  % (F.GREEN)
        help += '\n\t%s> load_sample /path/to/pcap/gold_xxx.pcap [\'bad\', \'threatglass\']' % (F.BLUE)
        help += '\n\t%s> view # view is your friend use it often' % (F.BLUE)
        help += '\n\n%sGrab the http_log from the pcap (also play around with other logs):'  % (F.GREEN)
        help += '\n\t%s> http_log_md5 = view()[\'view\'][\'bro_logs\'][\'http_log\']' % (F.BLUE)
        help += '\n\n%sGrab the http_log from the pcap (also play around with other logs):'  % (F.GREEN)
        help += '\n\t%s> http_log_md5 = view()[\'view\'][\'bro_logs\'][\'http_log\']' % (F.BLUE)
        help += '\n\n\t%sSearch for all samples in the database that are known bad pe files,'  % (F.GREEN)
        help += '\n\t%sthis command returns the sample_set containing the matching items'% (F.GREEN)
        help += '\n\t%s> my_bad_exes = search([\'bad\', \'exe\'])' % (F.BLUE)
        help += '\n\n\t%sRun workers on this sample_set:'  % (F.GREEN)
        help += '\n\t%s> pe_outputs = pe_features(my_bad_exes) %s' % (F.BLUE, F.RESET)
        help += '\n\n\t%sLoop on the generator (or make a DataFrame see > help dataframe'  % (F.GREEN)
        help += '\n\t%s> pe_df = pd.DataFrame(pe_outputs) %s' % (F.BLUE, F.RESET)
        help += '\n\t%s> pe_df.head() %s' % (F.BLUE, F.RESET)
        return help

    ##################
    # Introspection
    ##################
    def _all_help_methods(self):
        """ Returns a list of all the Workbench commands"""
        methods = {name:method for name, method in inspect.getmembers(self, predicate=inspect.isroutine) if not name.startswith('_')}
        return methods

def test():
    """Test the Workbench Interactive Shell Help"""
    help = WorkbenchShellHelp()

    # Now execute all the help methods
    for name, method in help._all_help_methods().iteritems():
        print '\n%s%s%s' % (F.RED, name, F.RESET)
        print '%s' % method()

if __name__ == '__main__':
    test()
