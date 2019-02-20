import ifcfg
print(ifcfg.interfaces().items())
print(ifcfg.default_interface()['inet'])