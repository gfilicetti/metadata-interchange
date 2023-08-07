availableManagers = managerFactory.availableManagers()
{
    'org.openassetio.example.manager':
        ManagerFactory.ManagerDetail(
            identifier='org.openassetio.example.manager',
            displayName='Example Asset Manager',
            info={})
}

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