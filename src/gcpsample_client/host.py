from openassetio.log import ConsoleLogger, SeverityFilter
from openassetio.hostApi import HostInterface, Manager, ManagerFactory
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory
from openassetio import Context
from openassetio_mediacreation.traits.content import LocatableContentTrait

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
    print(manager)

# Once we know which manager we wish to use, we can ask the factory
# to create one for us.
manager = managerFactory.createManager('google.manager.gcpsample_asset_manager')

# We now have an instance of the requested manager, but it is not
# quite ready for use yet. The manager returned by the
# ManagerFactory needs to be initialized before it can be used to
# query or publish assets. Setup is split into two stages to allow
# adjustments to its settings to be made prior to use if required.

# A manager's current (or in this case default) settings can be
# queried if needed:
settings = manager.settings()

# Finally, we can initialize the manager with the desired settings,
# preparing it for use. Note that this may include non-trivial
# amounts of work. Settings updates are sparse, so if you don't have
# any custom settings, you can pass an empty dictionary here.
manager.initialize(settings)

# Note: this will raise an exception if given a string that is not
# recognized by this manager as a valid entity reference (ValueError
# in Python, std::domain_error in C++). Consider
# createEntityReferenceIfValid, if unsure of the string.
entity_reference = manager.createEntityReference("location")

# All calls to the manager must have a Context, these should always
# be created by the target manager. The Context expresses the host's
# intent, and ensure that any manager state is properly managed
# between API calls.
context = manager.createContext()

# We describe what we want to do with the asset
context.access = context.access.kRead

# We describe the lifetime of the returned reference
# as persistent retention may require a more stable value.
context.retention = context.retention.kTransient

# We can now resolve a token we may have if it is a reference. In
# this example, we'll attempt to resolve the LocatableContent trait
# for the entity.
resolved_asset = manager.resolve(
        entity_reference, {LocatableContentTrait.kId}, context)
url = LocatableContentTrait(resolved_asset).getLocation()  # May be None
