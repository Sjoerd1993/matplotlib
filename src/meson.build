# NumPy include directory - needed in all submodules
incdir_numpy = run_command(py3,
  [
    '-c',
    'import numpy; print(numpy.get_include())'
  ],
  check: true
).stdout().strip()

numpy_dep = declare_dependency(
  compile_args: [
    '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION',
    # Allow NumPy's printf format specifiers in C++.
    '-D__STDC_FORMAT_MACROS=1',
  ],
  include_directories: include_directories(incdir_numpy),
  dependencies: py3_dep,
)

# Will only exist on Linux with older glilbc.
dl = cc.find_library('dl', required: false)

# FIXME: Actually implement these.
comctl32 = []
ole32 = []
psapi = []
shell32 = []
user32 = []

extension_data = {
  '_backend_agg': {
    'sources': files(
      'py_converters.cpp',
      '_backend_agg.cpp',
      '_backend_agg_wrapper.cpp',
    ),
    'dependencies': [agg_dep, numpy_dep, freetype_dep],
  },
  '_c_internal_utils': {
    'sources': files(
      '_c_internal_utils.c',
    ),
    'dependencies': [py3_dep, dl, ole32, shell32, user32],
  },
  'ft2font': {
    'sources': files(
      'ft2font.cpp',
      'ft2font_wrapper.cpp',
      'py_converters.cpp',
    ),
    'dependencies': [freetype_dep, numpy_dep, agg_dep.partial_dependency(includes: true)],
  },
  '_image': {
    'sources': files(
      '_image_wrapper.cpp',
      'py_converters.cpp',
    ),
    'dependencies': [numpy_dep, agg_dep],
  },
  '_path': {
    'sources': files(
      'py_converters.cpp',
      '_path_wrapper.cpp',
    ),
    'dependencies': [numpy_dep, agg_dep],
  },
  '_qhull': {
    'sources': files(
      '_qhull_wrapper.cpp',
    ),
    'dependencies': [numpy_dep, qhull_dep],
    'c_args': ['-DMPL_DEVNULL=os.devnull'],
    'cpp_args': ['-DMPL_DEVNULL=os.devnull'],
  },
  '_backend_tkagg': {
    'sources': files(
      '_tkagg.cpp',
    ),
    'include_directories': include_directories('.'),
    # psapi library needed for finding Tcl/Tk at run time.
    'dependencies': [numpy_dep, agg_dep.partial_dependency(includes: true), dl, comctl32, psapi],
  },
  '_tri': {
    'sources': files(
      'tri/_tri.cpp',
      'tri/_tri_wrapper.cpp',
    ),
    'dependencies': [numpy_dep],
  },
  '_ttconv': {
    'sources': files(
      '_ttconv.cpp',
    ),
    'dependencies': [ttconv_dep, numpy_dep],
  },
}

foreach ext, kwargs : extension_data
  py3.extension_module(ext, install: true, subdir: 'matplotlib', kwargs: kwargs)
endforeach
