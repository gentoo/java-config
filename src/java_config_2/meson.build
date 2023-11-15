__init__py = configure_file(
    input : '__init__.py',
    output : '__init__.py',
    configuration : conf_data
)

py.install_sources(
  [
    'EnvironmentManager.py',
    'Errors.py',
    'FileParser.py',
    'OutputFormatter.py',
    'Package.py',
    'VM.py',
    'VersionManager.py',
    'Virtual.py',
    __init__py,
  ],
  subdir: 'java_config_2',
)
