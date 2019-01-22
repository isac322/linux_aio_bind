# coding: UTF-8

from ctypes import Structure, c_int16, c_int64, c_size_t, c_uint, c_uint16, c_uint32, c_uint64, c_void_p

from enum import IntEnum

try:
    from enum import IntFlag
except ImportError:
    IntFlag = IntEnum

from typing import Tuple, Type, Union, overload

__all__ = (
    'IOCB', 'IOCBCMD', 'IOCBFlag', 'IOCBPriorityClass', 'IOCBRWFlag', 'gen_io_priority', 'IOPRIO_CLASS_SHIFT', 'IOVec'
)


# noinspection PyPep8Naming
# Little endian (32-bit)
@overload
def _PADDED(o: Type, k1: str, k2: str) -> Tuple[Tuple[str, Type], Tuple[str, Type]]: ...


# noinspection PyPep8Naming
# Little endian (64-bit)
@overload
def _PADDED(o: Type, k1: str, k2: str) -> Tuple[Tuple[str, Type], Tuple[str, Type[c_uint]]]: ...


# noinspection PyPep8Naming
# Big endian (64-bit, 32-bit)
@overload
def _PADDED(o: Type, k1: str, k2: str) -> Tuple[Tuple[str, Type[c_uint]], Tuple[str, Type]]: ...


class IOCB(Structure):
    # internal fields used by the kernel
    aio_data: Union[c_uint64, int] = ...
    aio_key: Union[c_uint, c_uint32, int] = ...
    aio_rw_flags: Union[c_uint, c_uint32, int] = ...

    # common fields
    aio_lio_opcode: Union[c_uint16, int] = ...
    aio_reqprio: Union[c_int16, int] = ...
    aio_fildes: Union[c_uint32, int] = ...

    aio_buf: Union[c_uint64, int] = ...
    aio_nbytes: Union[c_uint64, int] = ...
    aio_offset: Union[c_int64, int] = ...

    # extra parameters
    aio_reserved2: Union[c_uint64, int] = ...

    # flags for IOCB
    aio_flags: Union[c_uint32, int] = ...

    # if the IOCBFlag.RESFD flag of "aio_flags" is set, this is an eventfd to signal AIO readiness to
    aio_resfd: Union[c_uint32, int] = ...

    # noinspection PyMissingConstructor
    def __init__(self,
                 aio_data: Union[c_uint64, int] = 0,
                 aio_key: Union[c_uint, c_uint32, int] = 0,
                 aio_rw_flags: Union[c_uint, c_uint32, int] = 0,
                 aio_lio_opcode: Union[c_uint16, int] = 0,
                 aio_reqprio: Union[c_int16, int] = 0,
                 aio_fildes: Union[c_uint32, int] = 0,
                 aio_buf: Union[c_uint64, int] = 0,
                 aio_nbytes: Union[c_uint64, int] = 0,
                 aio_offset: Union[c_int64, int] = 0,
                 aio_reserved2: Union[c_uint64, int] = 0,
                 aio_flags: Union[c_uint32, int] = 0,
                 aio_resfd: Union[c_uint32, int] = 0) -> None: ...


class IOVec(Structure):
    iov_base: Union[c_void_p, int] = ...
    iov_len: Union[c_size_t, int] = ...

    # noinspection PyMissingConstructor
    def __init__(self, iov_base: Union[c_void_p, int] = 0, iov_len: Union[c_size_t, int] = 0) -> None: ...


# Define the types we need.
class _CtypesEnum:
    """A ctypes-compatible IntEnum superclass."""

    @classmethod
    def from_param(cls, obj) -> int: ...


class IOCBCMD(_CtypesEnum, IntEnum):
    PREAD = ...
    PWRITE = ...
    FSYNC = ...
    FDSYNC = ...
    # These two are experimental.
    # PREADX = ...
    POLL = ...
    # NOOP = ...
    PREADV = ...
    PWRITEV = ...


class IOCBFlag(_CtypesEnum, IntFlag):
    """ flags for :attr:`IOCB.aio_flags` """
    RESFD = ...
    IOPRIO = ...


# TODO: detail description (e.g. minimum required linux version)
class IOCBRWFlag(_CtypesEnum, IntFlag):
    """ flags for :attr:`IOCB.aio_rw_flags`. from linux code (/include/uapi/linux/fs.h) """
    HIPRI = ...
    DSYNC = ...
    SYNC = ...
    NOWAIT = ...
    APPEND = ...


# TODO: detail description (e.g. minimum required linux version, how priority value works)
class IOCBPriorityClass(_CtypesEnum, IntEnum):
    """ priority class. from linux code (/include/linux/ioprio.h) """
    NONE = ...
    RT = ...
    BE = ...
    IDLE = ...


IOPRIO_CLASS_SHIFT: int = ...


def gen_io_priority(priority_class: IOCBPriorityClass, priority: int) -> int: ...
