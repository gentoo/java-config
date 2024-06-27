project(
  'java-config',
  version: '2.3.5-SNAPSHOT',
  license: 'GPL-2.0',
  meson_version: '>=1.1.1'
)

py_mod = import('python')
py = py_mod.find_installation(pure : true)

system_wide = get_option('system-wide')
python_only = get_option('python-only')

eprefix = get_option('eprefix')
datadir = get_option('datadir')

sysconfdir = system_wide ? get_option('sysconfdir') \
                         : datadir / 'etc'

conf_data = configuration_data({
  'VERSION': meson.project_version(),
  'EPREFIX': eprefix
})

subdir('src')
subdir('tests')

if python_only
  subdir_done()
endif

subdir('config')

if not system_wide
  subdir_done()
endif

subdir('man')
