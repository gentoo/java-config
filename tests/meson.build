py_test_env = environment()
tests_python_paths = [
  meson.project_source_root(),
  meson.project_source_root() / 'src',
]
py_test_env.append('PYTHONPATH', tests_python_paths)

py_tests = [
  'EnvironmentManager',
  'Package',
  'VM',
  'VersionManager',
  'VersionManagerEnv2',
  'Virtual',
]

foreach py_test : py_tests
  test(
    'python-unittest-' + py_test,
    py,
    args: ['-m', 'unittest', 'tests.testsuite.' + py_test],
    env: py_test_env,
  )
endforeach
