'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_seamless_cube_map'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_seamless_cube_map',error_checker=_errors._error_checker)
GL_TEXTURE_CUBE_MAP_SEAMLESS=_C('GL_TEXTURE_CUBE_MAP_SEAMLESS',0x884F)
