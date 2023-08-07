from openassetio.log import ConsoleLogger, SeverityFilter
from openassetio.hostApi import HostInterface, Manager, ManagerFactory
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory

class ExamplesHost(HostInterface):
    """
    A minimal host implementation.
    """
    def identifier(self):
        return "org.openassetio.examples"

    def displayName(self):
        return "OpenAssetIO Examples"

# For simplicity, use a filtered console logger, this logs to
# stderr based on the value of OPENASSETIO_LOGGING_SEVERITY.
# Practically you may wish to provide a bridge to your own logging
# mechanism if you have one.
logger = SeverityFilter(ConsoleLogger())

# We need to provide the mechanism by which managers are created, the
# built-in plugin system allows these to be loaded from
# OPENASSETIO_PLUGIN_PATH.
factory_impl = PythonPluginSystemManagerImplementationFactory(logger)

# We then need our implementation of the HostInterface class
host_interface = ExamplesHost()

# We can now create an OpenAssetIO ManagerFactory. The ManagerFactory
# allows us to query the available managers, and pick one to talk to.
managerFactory = ManagerFactory(host_interface, factory_impl, logger)