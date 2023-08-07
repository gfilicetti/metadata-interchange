from openassetio.log import ConsoleLogger, SeverityFilter
from openassetio.hostApi import HostInterface, Manager, ManagerFactory
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory

class ExamplesHost(HostInterface):
    """
    A minimal host implementation.
    """
    def identifier(self):
        return "google.openassetio.examples"

    def displayName(self):
        return "Google OpenAssetIO Examples"

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

availableManagers = managerFactory.availableManagers()

for manager in availableManagers:
    print(manager.displayName)

exit(0)

# {
#     'org.openassetio.example.manager':
#         ManagerFactory.ManagerDetail(
#             identifier='org.openassetio.example.manager',
#             displayName='Example Asset Manager',
#             info={})
# }

# Once we know which manager we wish to use, we can ask the factory
# to create one for us.
manager = managerFactory.createManager('org.openassetio.example.manager')

# We now have an instance of the requested manager, but it is not
# quite ready for use yet. The manager returned by the
# ManagerFactory needs to be initialized before it can be used to
# query or publish assets. Setup is split into two stages to allow
# adjustments to its settings to be made prior to use if required.

# A manager's current (or in this case default) settings can be
# queried if needed:
settings = manager.settings()
# ...and updated with new values as desired.
settings["server"] = "my.server.com"

# Finally, we can initialize the manager with the desired settings,
# preparing it for use. Note that this may include non-trivial
# amounts of work. Settings updates are sparse, so if you don't have
# any custom settings, you can pass an empty dictionary here.
manager.initialize(settings)