class PluginABC(object):
    """
    Abstract base class for plugins
    """

    def handle_message(self, obj):
        """
        Handle a new message from the web view, provided as a decoded object
        """
        print "Warning: Unhandled Message for plugin: " + str(self)
