# coding: UTF-8

from ctypes import CDLL, POINTER, Structure, c_int64, c_long, c_uint64, c_ulong

from ctypes.util import find_library

from ._syscall import lib
from .error import cancel_err_map, destroy_err_map, get_events_err_map, handle_error, setup_err_map, submit_err_map
from .iocb import IOCB

with open('/proc/sys/fs/aio-max-nr') as fp:
    _JOB_LIMIT = int(fp.read())

_libc = CDLL(find_library('c'), use_errno=True)
_syscall = _libc.syscall


class Timespec(Structure):
    """
    .. versionadded:: 1.0.0
    """
    _fields_ = (
        ('tv_sec', c_long),
        ('tv_nsec', c_long),
    )


class IOEvent(Structure):
    """
    .. versionadded:: 1.0.0
    """
    _fields_ = (
        ('data', c_uint64),
        ('obj', c_uint64),
        ('res', c_int64),
        ('res2', c_int64),
    )


aio_context_t = c_ulong
aio_context_t_p = POINTER(aio_context_t)
iocb_p = POINTER(IOCB)
iocb_pp = POINTER(iocb_p)
io_event_p = POINTER(IOEvent)
timespec_p = POINTER(Timespec)


def io_setup(max_jobs, context_p):
    """
    .. versionadded:: 1.0.0
    """
    ret = _syscall(lib.SYS_io_setup, max_jobs, context_p)

    if ret is not 0:
        handle_error(setup_err_map, max_jobs.value, _JOB_LIMIT, context_p.contents)


def io_destroy(context):
    """
    .. versionadded:: 1.0.0
    """
    ret = _syscall(lib.SYS_io_destroy, context)

    if ret is not 0:
        handle_error(destroy_err_map, context.value)


def io_submit(context, num_jobs, iocb_p_list):
    """
    .. versionadded:: 1.0.0
    """
    ret = _syscall(lib.SYS_io_submit, context, num_jobs, iocb_p_list)

    if ret < 0:
        handle_error(submit_err_map, context.value)

    return ret


def io_getevents(context, min_jobs, max_jobs, events, timeout):
    """
    return value can be less than min_jobs. because io_getevents can be interrupted by signal during processing
    (io_pgetevents does not, but not fully implemented yet)

    .. versionadded:: 1.0.0
    """
    ret = _syscall(lib.SYS_io_getevents, context, min_jobs, max_jobs, events, timeout)

    if ret < 0:
        handle_error(get_events_err_map, context.value, min_jobs.value, max_jobs.value)

    return ret


def io_cancel(context, iocb, result):
    """
    .. versionadded:: 1.0.0
    """
    ret = _syscall(lib.SYS_io_cancel, context, iocb, result)

    if ret is not 0:
        handle_error(cancel_err_map, context.value)
