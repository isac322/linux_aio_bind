# coding: UTF-8

import sys
from ctypes import (
    Structure, c_int16, c_int64, c_size_t, c_uint, c_uint16, c_uint32, c_uint64, c_ulong, c_void_p, sizeof
)

import os
from enum import IntEnum

try:
    from enum import IntFlag
except ImportError:
    IntFlag = IntEnum

_PADDED = {
    (4, 'little'): lambda w, x, y: ((x, w), (y, c_uint)),
    (8, 'little'): lambda w, x, y: ((x, w), (y, w)),
    (8, 'big'): lambda w, x, y: ((y, c_uint), (x, w)),
    (4, 'big'): lambda w, x, y: ((y, c_uint), (x, w)),
}[(sizeof(c_ulong), sys.byteorder)]


class IOCB(Structure):
    """
    .. versionadded:: 1.0.0
    """
    _fields_ = \
        (
            # internal fields used by the kernel
            ('aio_data', c_uint64),
        ) \
        + \
        _PADDED(c_uint32, 'aio_key', 'aio_rw_flags') \
        + \
        (
            # common fields
            ('aio_lio_opcode', c_uint16),
            ('aio_reqprio', c_int16),
            ('aio_fildes', c_uint32),

            ('aio_buf', c_uint64),
            ('aio_nbytes', c_uint64),
            ('aio_offset', c_int64),

            # extra parameters
            ('aio_reserved2', c_uint64),

            # flags for IOCB
            ('aio_flags', c_uint32),

            # if the IOCBFlag.RESFD flag of "aio_flags" is set, this is an eventfd to signal AIO readiness to
            ('aio_resfd', c_uint32),
        )


class IOVec(Structure):
    """
    .. versionadded:: 0.3.0
    """
    _fields_ = (
        ('iov_base', c_void_p),
        ('iov_len', c_size_t)
    )


class IOCBCMD(IntEnum):
    """
    .. versionadded:: 1.0.0
    """
    PREAD = 0
    PWRITE = 1
    FSYNC = 2
    """requires Linux 4.18 or above"""
    FDSYNC = 3
    """requires Linux 4.18 or above"""
    # These two are experimental.
    # PREADX = 4
    POLL = 5
    """requires Linux 4.19 or above"""
    # NOOP = 6
    PREADV = 7
    PWRITEV = 8

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class IOCBFlag(IntFlag):
    """
    flags for :attr:`IOCB.aio_flags`

    .. versionadded:: 1.0.0
    """
    RESFD = 1 << 0
    IOPRIO = 1 << 1

    @classmethod
    def from_param(cls, obj):
        return int(obj)


# TODO: detail description (e.g. minimum required linux version)
class IOCBRWFlag(IntFlag):
    """
    flags for :attr:`IOCB.aio_rw_flags`. from linux code (/include/uapi/linux/fs.h)

    .. versionadded:: 1.0.0
    """
    HIPRI = 1 << 0 if not hasattr(os, 'RWF_HIPRI') else os.RWF_HIPRI
    DSYNC = 1 << 1 if not hasattr(os, 'RWF_DSYNC') else os.RWF_DSYNC
    SYNC = 1 << 2 if not hasattr(os, 'RWF_SYNC') else os.RWF_SYNC
    NOWAIT = 1 << 3 if not hasattr(os, 'RWF_NOWAIT') else os.RWF_NOWAIT
    APPEND = 1 << 4

    @classmethod
    def from_param(cls, obj):
        return int(obj)


# TODO: detail description (e.g. minimum required linux version, how priority value works)
class IOCBPriorityClass(IntEnum):
    """
    priority class. from linux code (/include/linux/ioprio.h)

    .. versionadded:: 1.0.0
    """
    NONE = 0
    RT = 1
    BE = 2
    IDLE = 3

    @classmethod
    def from_param(cls, obj):
        return int(obj)


IOPRIO_CLASS_SHIFT = 13


def gen_io_priority(priority_class, priority):
    """
    .. versionadded:: 1.0.0
    """
    return (priority_class << IOPRIO_CLASS_SHIFT) | priority
