
''' A simple plugin manager. Rolling my own for three reasons:
    1) Environmental scan did not give me quite what I wanted.
    2) The super simple examples didn't support automatic/dynamic loading.
    3) I kinda wanted to understand the process :)
'''

import os, sys, time

class PluginValidator():

    def __init__(self):
        pass

    def validate(self, plugin_name):

        # It's possible the plugin has been modified and needs to be reloaded
        if plugin_name in sys.modules:
            try:
                handler = reload(sys.modules[plugin_name])
            except ImportError, error:
                print 'Failed to import plugin: %s (%s)' % (plugin_name, error)
                return None
        else:
            # Not already loaded so try to import it
            try:
                handler = __import__(plugin_name, globals(), locals(), [], -1)
            except ImportError, error:
                print 'Failed to import plugin: %s (%s)' % (plugin_name, error)
                return None

        # Every workbench plugin must have an plugin_info method
        try:
            plugin_info = handler.plugin_info()
            plugin_info['name'];plugin_info['class'];plugin_info['dependencies'];plugin_info['description']
        except (AttributeError, ValueError, TypeError), error:
            print 'Failure for plugin: %s (%s)' % (plugin_name, error)
            print 'All plugins must have an info method that returns a dictionary'
            print 'that includes key/values for name, class, dependencies, and a description'
            return None

        # Every workbench plugin must have an execute method
        try:
            plugin_class = getattr(handler, plugin_info['class'])
            plugin_info['handler'] = plugin_class
            getattr(plugin_class, 'execute')
        except AttributeError, error:
            print 'Failure for plugin: %s (%s)' % (plugin_name, error)
            print 'All plugins must have an execute method'
            return None

        # Okay, now return the plugin info
        return plugin_info

# Just create the class and run it for a test
def _test():

    # Create Plugin Validator
    pv = PluginValidator()

if __name__ == "__main__":
    _test()
