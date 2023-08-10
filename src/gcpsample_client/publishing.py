# Commented imports are illustrative and may not exist yet
from openassetio.log import ConsoleLogger, SeverityFilter
from openassetio.hostApi import HostInterface, Manager, ManagerFactory
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory
from openassetio import Context
from openassetio_mediacreation.traits.content import LocatableContentTrait
from openassetio_mediacreation.traits.managementPolicy import ManagedTrait, ResolvesFutureEntitiesTrait
from openassetio_mediacreation.specifications.files import TextFileSpecification

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

# As ever, an appropriately configured context is required
context = manager.createContext()
context.access = context.kWrite

# The first step is to see if the manager wants to manage text files
policy = manager.managementPolicy([TextFileSpecification.kTraitSet], context)[0]

if not ManagedTrait.isImbuedTo(policy):
  # The manager doesn't care about this type of asset
  print("Trait is not imbued")
  exit(0)

# Not all managers can tell us where to put files (irksome).
# The reality of handling this is somewhat more challenging, and
# depends on the nature of the task in hand. One for further discussion.
save_path = os.path.join(os.path.expanduser('~'), 'test/greeting.txt')
encoding = "utf-8"

# Whenever we make new data, we always tell the manager first,
# This allows it to create a placeholder version or similar.
# NOTE: It is critical to always use the working_ref from now on.
working_ref = manager.preflight(
        entity_ref, TextFileSpecification.kTraitSet, context)

# We then check if the manager can tell us where to save the file.
if ResolvesFutureEntitiesTrait.isImbuedTo(policy):
    working_data = manager.resolve(
            working_ref, TextFileSpecification.kTraitSet, context)
    working_spec = TextFileSpecification(working_data)
    if save_url := working_spec.locatableContentTrait().getLocation():
        save_path = pathFromURL(save_url)  # URL decode etc
    if custom_encoding := working_spec.textEncodingTrait().getEncoding():
        encoding = custom_encoding

# Now we can write the file
with open(save_path, 'w', encoding=encoding) as f:
   f.write("Hello from the documentation example\n")

# Prepare the entity specification to register, with the data about
# where we actually wrote the data to, and with what encoding.
file_spec = TextFileSpecification.create()
file_spec.locatableContentTrait().setLocation(pathToURL(save_path))
file_spec.textEncodingTrait().setEncoding(encoding)

# Now the data has been written, we register the file and the publish
# is complete. Update the context retention to denote that we're going
# to save a reference to this entity in our user's history.
context.retention = context.kPermanent
final_ref = manager.register(working_ref, file_spec.traitsData(), context)

# We can persist this reference as we used the kPermanent retention
with open(os.path.join(os.path.expanduser('~'), 'history', 'a') as f:
    f.write(f"{final_ref}\n")