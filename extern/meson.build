# Bundled code.
subdir('agg24-svn')
subdir('ttconv')

# External code.

# FreeType 2.3 has libtool version 9.11.3 as can be checked from the tarball.
# For FreeType>=2.4, there is a conversion table in docs/VERSIONS.txt in the
# FreeType source tree.
freetype_dep = dependency('freetype2', version: '>=9.11.3')

qhull_dep = cc.find_library('qhull_r')
