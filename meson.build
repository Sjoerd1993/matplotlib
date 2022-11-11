project(
  'matplotlib',
  'c', 'cpp',
  version: '3.6.0.dev0',
  license: 'Python-2.0.1 AND OFL AND Apache-1.1 AND Bitstream-Vera AND CC0-1.0 AND Qhull AND MIT AND 0BSD',
)

cc = meson.get_compiler('c')
cpp = meson.get_compiler('cpp')

# https://mesonbuild.com/Python-module.html
py_mod = import('python')
py3 = py_mod.find_installation()
py3_dep = py3.dependency()

subdir('extern')
subdir('src')
subdir('lib')
