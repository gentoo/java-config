arch = get_option('arch')

jdk_defaults = '*= icedtea'
if arch in ['amd64', 'x86']
    jdk_defaults = '*= icedtea6 icedtea6-bin icedtea7 icedtea7-bin'
elif arch in ['ppc-macos', 'x64-macos', 'x86-macos']
    jdk_defaults = '*= apple-jdk-bin'
elif arch in ['ppc', 'ppc64', 'ppc-linux', 'ppc-aix']
    jdk_defaults = '*= ibm-jdk-bin'
elif arch in ['arm']
    jdk_defaults = '*= icedtea-7 icedtea-6 icedtea-bin-7 icedtea-bin-6'
endif

java_config_confdir = sysconfdir / 'java-config-2'

configure_file(
  input: 'jdk-defaults.conf',
  output: 'jdk-defaults.conf',
  configuration: { 'JDK_DEFAULTS': jdk_defaults },
  install_dir: java_config_confdir,
)

install_data(
  ['virtuals'],
  install_dir: java_config_confdir
)
