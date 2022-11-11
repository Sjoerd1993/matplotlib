project('qhull', 'c',
  version: '2020.2',
  license: 'Qhull')

qhull_lib = static_library('qhull_r',
  'src/libqhull_r/geom2_r.c',
  'src/libqhull_r/geom_r.c',
  'src/libqhull_r/global_r.c',
  'src/libqhull_r/io_r.c',
  'src/libqhull_r/libqhull_r.c',
  'src/libqhull_r/mem_r.c',
  'src/libqhull_r/merge_r.c',
  'src/libqhull_r/poly2_r.c',
  'src/libqhull_r/poly_r.c',
  'src/libqhull_r/qset_r.c',
  'src/libqhull_r/random_r.c',
  'src/libqhull_r/rboxlib_r.c',
  'src/libqhull_r/stat_r.c',
  'src/libqhull_r/usermem_r.c',
  'src/libqhull_r/userprintf_rbox_r.c',
  'src/libqhull_r/userprintf_r.c',
  'src/libqhull_r/user_r.c',
)

qhull_dep = declare_dependency(link_with: qhull_lib)

meson.override_dependency('qhull_r', qhull_dep)
