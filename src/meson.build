subdir('java_config_2')

py_bins = [
  'depend-java-query',
  'gjl',
  'java-config-2',
]

# It might seem sensible to use py.install_sources() to install the Python
# scripts, but it's really just a wrapper around install_data that forces the
# install_dir. Meson 1.2.0 and later also optimize to bytecode, but Gentoo does
# this in the ebuild.
install_data(
    py_bins,
    install_dir: get_option('bindir'),
    install_mode: 'rwxr-xr-x',
)

if python_only
  subdir_done()
endif

launcherdir_rel =  'share' / 'java-config-2' / 'launcher'
launcherdir = system_wide ? eprefix / launcherdir_rel \
                         : datadir / eprefix / launcherdir_rel

launcher_bash = configure_file(
  input: 'launcher.bash',
  output: 'launcher.bash',
  configuration: conf_data,
)

install_data(
  [launcher_bash],
  install_dir: launcherdir,
)
