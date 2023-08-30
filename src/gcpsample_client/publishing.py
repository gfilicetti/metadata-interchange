# Commented imports are illustrative and may not exist yet
from openassetio.log import ConsoleLogger, SeverityFilter
from openassetio.hostApi import HostInterface, Manager, ManagerFactory
from openassetio.pluginSystem import PythonPluginSystemManagerImplementationFactory
from openassetio import Context
from openassetio_mediacreation.traits.content import LocatableContentTrait
from openassetio_mediacreation.traits.auth import BearerTokenTrait
from openassetio_mediacreation.traits.identity import DisplayNameTrait
from openassetio_mediacreation.traits.managementPolicy import ManagedTrait, ResolvesFutureEntitiesTrait
from gcpsample_client import manager_initialize
# GF: This imports from our generated traits/specs
from gcpsample.specifications.video import DigitalVideoSpecification


print("We're in publishing.py")
manager = manager_initialize.manager

# As ever, an appropriately configured context is required
context = manager.createContext()
context.access = context.Access.kWrite

# The first step is to see if the manager wants to manage text files
policy = manager.managementPolicy([DigitalVideoSpecification.kTraitSet], context)[0]

if not ManagedTrait.isImbuedTo(policy):
  # The manager doesn't care about this type of asset
  print("Trait is not imbued")
  exit(0)

# Not all managers can tell us where to put files (irksome).
# The reality of handling this is somewhat more challenging, and
# depends on the nature of the task in hand. One for further discussion.
# GF: don't need this for now
# save_path = os.path.join(os.path.expanduser('~'), 'test/greeting.txt')
# encoding = "utf-8"

# Whenever we make new data, we always tell the manager first,
# This allows it to create a placeholder version or similar.
# We must provide the manager with any relevant information that the
# host owns (i.e. won't be queried from the manager during
# publishing) and can be provided up-front.
video_spec = DigitalVideoSpecification.create()
video_spec.displayNameTrait().setName("Ginos Home Video")

# GF: The entity reference is under our control, so we'll just hardcode this for now.
# entity_ref = "2023-08-23-video-ginoshomevideo"
entity_ref = "para:///video"
# GF: Resolve the entity reference
entity_reference = manager.createEntityReference(entity_ref)
# NOTE: It is critical to always use the working_ref from now on.
print("Calling preflight")
working_ref = manager.preflight(entity_reference, video_spec, context)
print("DONE calling preflight")

# We then check if the manager can tell us where to save the file.
if ResolvesFutureEntitiesTrait.isImbuedTo(policy):
    # GF: I won't be resolving
    # working_data = manager.resolve(
    #         working_ref, DigitalVideoSpecification.kTraitSet, context)
    # GF for now working spec IS the video spec
    # working_spec = DigitalVideoSpecification(working_data)
    working_spec = video_spec
    # GF: just print the display name
    print(f"This video is called: {working_spec.displayNameTrait().getName}")

    # GF: this is the old code for files, not needed for now
    # if save_url := working_spec.locatableContentTrait().getLocation():
    #     save_path = pathFromURL(save_url)  # URL decode etc
    # if custom_encoding := working_spec.textEncodingTrait().getEncoding():
    #     encoding = custom_encoding

# Now we can write the file
# GF: now we need to "do" the publish of the DigitalVideo
print("We are now publishing the Digital Video")

# GF: old code for text files
# with open(save_path, 'w', encoding=encoding) as f:
#    f.write("Hello from the documentation example\n")

# Prepare the entity specification to register, with the data about
# where we actually wrote the data to, and with what encoding.
# file_spec = TextFileSpecification.create()
# file_spec.locatableContentTrait().setLocation(pathToURL(save_path))
# file_spec.textEncodingTrait().setEncoding(encoding)

# Now the data has been written, we register the file and the publish
# is complete. Update the context retention to denote that we're going
# to save a reference to this entity in our user's history.
# GF: The "retention" concept is going away, so commenting this out for now
# context.retention = context.kPermanent
final_ref = manager.register(working_ref, working_spec.traitsData(), context)

# GF: instead lets just print to the console
print(f"The final reference is: {final_ref}")
# We can persist this reference as we used the kPermanent retention
# with open(os.path.join(os.path.expanduser('~'), 'history', 'a')) as f:
#    f.write(f"{final_ref}\n")
