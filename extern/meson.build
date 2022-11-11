# Bundled code.
subdir('agg24-svn')
subdir('ttconv')

# External code.

# FreeType 2.3 has libtool version 9.11.3 as can be checked from the tarball.
# For FreeType>=2.4, there is a conversion table in docs/VERSIONS.txt in the
# FreeType source tree.
if get_option('system-freetype')
  freetype_dep = dependency('freetype2', version: '>=9.11.3')
else
  freetype_proj = subproject('freetype2',
    default_options: ['default_library=static', 'zlib=internal'])
  freetype_dep = freetype_proj.get_variable('freetype_dep')
endif

if get_option('system-qhull')
  qhull_dep = cc.find_library('qhull_r')
else
  qhull_proj = subproject('qhull')
  qhull_dep = qhull_proj.get_variable('qhull_dep')
endif
