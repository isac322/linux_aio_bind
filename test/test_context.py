# coding: UTF-8

import errno
from ctypes import c_long, c_uint, pointer

import unittest

from linux_aio_bind import (
    IOCB, IOCBCMD, IOEvent, aio_context_t, create_c_array, io_destroy, io_getevents, io_setup, io_submit, iocb_p
)


class TestContext(unittest.TestCase):
    def test_ctx_setup(self):
        ctx = aio_context_t()
        io_setup(c_uint(10), pointer(ctx))
        self.assertNotEqual(0, ctx.value)

        io_destroy(ctx)

    def test_exceed_max_nr(self):
        with open('/proc/sys/fs/aio-max-nr') as fp:
            max_nr = int(fp.read())

        with self.assertRaises(OSError) as assertion:
            ctx = aio_context_t()
            io_setup(c_uint(max_nr + 1), pointer(ctx))

        self.assertEqual(errno.EAGAIN, assertion.exception.errno)

    def test_double_destroy(self):
        ctx = aio_context_t()
        io_setup(c_uint(1), pointer(ctx))
        self.assertNotEqual(0, ctx.value)

        io_destroy(ctx)

        with self.assertRaises(OSError) as assertion:
            io_destroy(ctx)

        self.assertEqual(errno.EINVAL, assertion.exception.errno)

    def test_setup_with_invalid_ctx(self):
        with self.assertRaises(OSError) as assertion:
            ctx = c_uint(100)
            io_setup(c_uint(1), pointer(ctx))

        self.assertEqual(errno.EINVAL, assertion.exception.errno)

    def test_submit_with_invalid_ctx(self):
        with self.assertRaises(OSError) as assertion:
            with open('/etc/passwd') as fp:
                iocb = IOCB(aio_lio_opcode=IOCBCMD.PREAD, aio_fildes=fp.fileno())

                submit_ret = io_submit(aio_context_t(10), c_long(1), create_c_array(iocb_p, (pointer(iocb),)))

                self.assertEqual(1, submit_ret)

        self.assertEqual(errno.EINVAL, assertion.exception.errno)

    def test_invalid_getevents(self):
        ctx = aio_context_t()
        io_setup(c_uint(1), pointer(ctx))

        with self.assertRaises(OSError) as assertion:
            io_getevents(ctx, c_long(-1), c_long(1), None, None)

        self.assertEqual(errno.EINVAL, assertion.exception.errno)

    def test_empty_submit(self):
        ctx = aio_context_t()
        io_setup(c_uint(10), pointer(ctx))
        self.assertNotEqual(0, ctx.value)

        ret = io_submit(ctx, c_long(0), create_c_array(iocb_p, (), 0))
        self.assertEqual(0, ret)

        io_destroy(ctx)

    def test_empty_getevents(self):
        ctx = aio_context_t()
        io_setup(c_uint(10), pointer(ctx))
        self.assertNotEqual(0, ctx.value)

        ret = io_getevents(ctx, c_long(0), c_long(100), create_c_array(IOEvent, (), 0), None)
        self.assertEqual(0, ret)

        io_destroy(ctx)

    def test_empty_submit_n_getevents(self):
        ctx = aio_context_t()
        io_setup(c_uint(10), pointer(ctx))
        self.assertNotEqual(0, ctx.value)

        ret = io_submit(ctx, c_long(0), create_c_array(iocb_p, (), 0))
        self.assertEqual(0, ret)

        ret = io_getevents(ctx, c_long(0), c_long(100), create_c_array(IOEvent, (), 0), None)
        self.assertEqual(0, ret)

        io_destroy(ctx)


if __name__ == '__main__':
    unittest.main()
