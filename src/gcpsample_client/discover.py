# Commented imports are illustrative and may not exist yet
from openassetio_mediacreation.traits.managementPolicy import (
    ManagedTrait,
)
from openassetio_mediacreation.traits.content import (
    LocatableContentTrait, # TextEncodingTrait
)
from openassetio_mediacreation.specifications.files import (
    # TextFileSpecification
)

# Make sure we have the correct context
context.access = context.kRead

# We use the well-known specification for a text file to determine
# the correct trait set to query. Using the standard definition
# ensures consistent behaviour across managers/hosts.
[policy] = manager.managementPolicy([TextFileSpecification.kTraitSet], context)

# We can now check which traits were imbued in the policy, the
# absence of a trait means it is unsupported.

if not ManagedTrait.isImbuedTo(policy):
  # The manager doesn't want to handle text files, we should not
  # attempt to resolve/publish this type of entity.
  return

# As well as policy-specific traits, the result will be imbued with
# traits from the queried trait set that the manager is capable of
# providing data for. If you have additional host-specific traits,
# you can append these to the ones from the relevant specification.
# Here we check for support for the specific text file traits we are
# interested in using.

if LocatableContentTrait.isImbuedTo(policy):
  print("The manager can provide the URL for the file")

if TextEncodingTrait.isImbuedTo(policy):
  print("The manager can provide the text encoding used")