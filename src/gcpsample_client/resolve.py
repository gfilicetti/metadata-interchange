from openassetio import Context
from openassetio_mediacreation.traits.content import LocatableContentTrait
from gcpsample_client import manager_initialize

print("We're in resolve.py")
manager = manager_initialize.manager
print(manager)
exit(0)
# Note: this will raise an exception if given a string that is not
# recognized by this manager as a valid entity reference (ValueError
# in Python, std::domain_error in C++). Consider
# createEntityReferenceIfValid, if unsure of the string.
entity_reference = manager.createEntityReference(some_string)

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
