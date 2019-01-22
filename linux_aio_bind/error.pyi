# coding: UTF-8

from errno import EAGAIN, EBADF, EFAULT, EINTR, EINVAL, ENOMEM, ENOSYS
from typing import Dict, Mapping, NoReturn

setup_err_map: Dict[int, str] = {
    EAGAIN: ...,
    EFAULT: ...,
    EINVAL: ...,
    ENOMEM: ...,
    ENOSYS: ...
}
"""
0: max_jobs,

1: content of `/proc/sys/fs/aio-max-nr`,

2: :const:`~linux_aio.raw.aio.aio_context_t`
"""

destroy_err_map: Dict[int, str] = {
    EFAULT: ...,
    EINVAL: ...,
    ENOSYS: ...
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`,
"""

cancel_err_map: Dict[int, str] = {
    EAGAIN: ...,
    EFAULT: ...,
    EINVAL: ...,
    ENOSYS: ...
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`,
"""

get_events_err_map: Dict[int, str] = {
    EFAULT: ...,
    EINTR: ...,
    EINVAL: ...,
    ENOSYS: ...
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`,

1: min_jobs,

2: max_jobs
"""

submit_err_map: Dict[int, str] = {
    EAGAIN: ...,
    EBADF: ...,
    EFAULT: ...,
    EINVAL: ...,
    ENOSYS: ...
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`
"""


def handle_error(error_map: Mapping[int, str], *args) -> NoReturn:
    """
    .. versionadded:: 1.0.0
    """
    ...
