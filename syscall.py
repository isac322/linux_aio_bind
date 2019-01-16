# coding: UTF-8

from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
        'linux_aio._syscall',
        r'#include <sys/syscall.h>'
)

ffibuilder.cdef(r'''
    #define SYS_io_setup ...
    #define SYS_io_destroy ...
    #define SYS_io_getevents ...
    #define SYS_io_submit ...
    #define SYS_io_cancel ...
    // #define SYS_io_pgetevents ...
''')
