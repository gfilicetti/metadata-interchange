from openassetio.log import ConsoleLogger, SeverityFilter
from openassetio.hostApi import HostInterface, Manager, ManagerFactory
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory
from openassetio import Context
from openassetio_mediacreation.traits.content import LocatableContentTrait

class GCPSampleHost(HostInterface):
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
host_interface = GCPSampleHost()

# We can now create an OpenAssetIO ManagerFactory. The ManagerFactory
# allows us to query the available managers, and pick one to talk to.

# GF: This is the old, manual way to do things
# managerFactory = ManagerFactory(host_interface, factory_impl, logger)
# availableManagers = managerFactory.availableManagers()
# GF: Let's print the list of available managers to us. (We should only see ours)
# for manager in availableManagers:
#     print(manager)
# manager = managerFactory.createManager('google.manager.gcpsample_asset_manager')

# GF: We're going to externalize which manager we want to use in a toml file and just call this one method once
manager = ManagerFactory.defaultManagerForInterface(host_interface, factory_impl, logger)

print("Yay, it worked")
# We now have an instance of the requested manager, but it is not
# quite ready for use yet. The manager returned by the
# ManagerFactory needs to be initialized before it can be used to
# query or publish assets. Setup is split into two stages to allow
# adjustments to its settings to be made prior to use if required.

# A manager's current (or in this case default) settings can be
# queried if needed:
# ????? GF: not needed???? 
# settings = manager.settings()

# Finally, we can initialize the manager with the desired settings,
# preparing it for use. Note that this may include non-trivial
# amounts of work. Settings updates are sparse, so if you don't have
# any custom settings, you can pass an empty dictionary here.
# ????? GF: not needed???? 
# manager.initialize(settings)
