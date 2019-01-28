# coding: UTF-8
import errno
from ctypes import addressof, c_char, c_char_p, c_long, c_uint, c_void_p, cast, pointer

import unittest

from linux_aio_bind import (
    IOCB, IOCBCMD, IOCBFlag, IOCBPriorityClass, IOEvent, IOVec, aio_context_t, create_c_array,
    gen_io_priority, io_destroy, io_getevents, io_setup, io_submit, iocb_p
)


class TestRW(unittest.TestCase):
    def test_read(self):
        with open('/etc/passwd') as fp:
            ctx = aio_context_t()
            io_setup(c_uint(1), pointer(ctx))
            self.assertNotEqual(0, ctx.value)

            len_buf = 64
            buf = bytearray(len_buf)
            arr_t = c_char * len_buf
            arr_p = cast(arr_t.from_buffer(buf), c_void_p)
            iocb = IOCB(aio_lio_opcode=IOCBCMD.PREAD, aio_fildes=fp.fileno(),
                        aio_buf=arr_p.value, aio_offset=0, aio_nbytes=len_buf)

            submit_ret = io_submit(ctx, c_long(1), create_c_array(iocb_p, (pointer(iocb),)))
            self.assertEqual(1, submit_ret)

            event = IOEvent()
            get_event_ret = io_getevents(ctx, c_long(1), c_long(1), create_c_array(IOEvent, (event,)), None)
            self.assertEqual(1, get_event_ret)

            self.assertEqual(fp.read(len_buf), buf.strip().decode())

            io_destroy(ctx)

    def test_read_w_priority(self):
        with open('/etc/passwd') as fp:
            ctx = aio_context_t()
            io_setup(c_uint(1), pointer(ctx))
            self.assertNotEqual(0, ctx.value)

            len_buf = 64
            buf = bytearray(len_buf)
            arr_t = c_char * len_buf
            arr_p = cast(arr_t.from_buffer(buf), c_void_p)
            iocb = IOCB(aio_lio_opcode=IOCBCMD.PREAD, aio_fildes=fp.fileno(),
                        aio_buf=arr_p.value, aio_offset=0, aio_nbytes=len_buf,
                        aio_reqprio=gen_io_priority(IOCBPriorityClass.IDLE, 10),
                        aio_flags=IOCBFlag.IOPRIO)

            submit_ret = io_submit(ctx, c_long(1), create_c_array(iocb_p, (pointer(iocb),)))
            self.assertEqual(1, submit_ret)

            event = IOEvent()
            get_event_ret = io_getevents(ctx, c_long(1), c_long(1), create_c_array(IOEvent, (event,)), None)
            self.assertEqual(1, get_event_ret)

            self.assertEqual(fp.read(len_buf), buf.strip().decode())

            io_destroy(ctx)

    def test_invalid_priority_req(self):
        fp = open('/etc/passwd')
        ctx = aio_context_t()
        io_setup(c_uint(1), pointer(ctx))
        self.assertNotEqual(0, ctx.value)

        len_buf = 64
        buf = bytearray(len_buf)
        arr_t = c_char * len_buf
        arr_p = cast(arr_t.from_buffer(buf), c_void_p)
        iocb = IOCB(aio_lio_opcode=IOCBCMD.PREAD, aio_fildes=fp.fileno(),
                    aio_buf=arr_p.value, aio_offset=0, aio_nbytes=len_buf,
                    aio_resfd=5, aio_flags=IOCBFlag.RESFD)

        with self.assertRaises(OSError) as assertion:
            io_submit(ctx, c_long(1), create_c_array(iocb_p, (pointer(iocb),)))

        self.assertEqual(errno.EBADF, assertion.exception.errno)

        io_destroy(ctx)
        fp.close()

    def test_write(self):
        with open('test.txt', 'w+') as fp:
            ctx = aio_context_t()
            io_setup(c_uint(1), pointer(ctx))
            self.assertNotEqual(0, ctx.value)

            contents = 'This is a long sample text.'
            len_contents = len(contents)
            arr_p = cast(c_char_p(contents.encode()), c_void_p)
            iocb = IOCB(aio_lio_opcode=IOCBCMD.PWRITE, aio_fildes=fp.fileno(),
                        aio_buf=arr_p.value, aio_offset=0, aio_nbytes=len_contents)

            submit_ret = io_submit(ctx, c_long(1), create_c_array(iocb_p, (pointer(iocb),)))
            self.assertEqual(1, submit_ret)

            event = IOEvent()
            get_event_ret = io_getevents(ctx, c_long(1), c_long(1), create_c_array(IOEvent, (event,)), None)
            self.assertEqual(1, get_event_ret)

            self.assertEqual(contents, fp.read(len_contents))

            io_destroy(ctx)

    def test_readv(self):
        with open('/etc/passwd') as fp:
            ctx = aio_context_t()
            io_setup(c_uint(1), pointer(ctx))
            self.assertNotEqual(0, ctx.value)

            len_buf1 = 64
            buf1 = bytearray(len_buf1)
            arr_t1 = c_char * len_buf1
            arr_p1 = cast(arr_t1.from_buffer(buf1), c_void_p)

            vec1 = IOVec(arr_p1, len_buf1)

            len_buf2 = 32
            buf2 = bytearray(len_buf2)
            arr_t2 = c_char * len_buf2
            arr_p2 = cast(arr_t2.from_buffer(buf2), c_void_p)

            vec2 = IOVec(arr_p2, len_buf2)

            vec_arr = create_c_array(IOVec, (vec1, vec2))
            iocb = IOCB(aio_lio_opcode=IOCBCMD.PREADV, aio_fildes=fp.fileno(),
                        aio_buf=addressof(vec_arr), aio_offset=0, aio_nbytes=2)

            submit_ret = io_submit(ctx, c_long(1), create_c_array(iocb_p, (pointer(iocb),)))
            self.assertEqual(1, submit_ret)

            event = IOEvent()
            get_event_ret = io_getevents(ctx, c_long(1), c_long(1), create_c_array(IOEvent, (event,)), None)
            self.assertEqual(1, get_event_ret)

            self.assertEqual(fp.read(len_buf1 + len_buf2), buf1.strip().decode() + buf2.strip().decode())

            io_destroy(ctx)

    def test_writev(self):
        with open('test.txt', 'w+') as fp:
            ctx = aio_context_t()
            io_setup(c_uint(1), pointer(ctx))
            self.assertNotEqual(0, ctx.value)

            contents1 = 'This is a long sample text.'
            len_contents1 = len(contents1)
            arr_p1 = cast(c_char_p(contents1.encode()), c_void_p)

            vec1 = IOVec(arr_p1, len_contents1)

            contents2 = '\nThis is a long sample text 2.'
            len_contents2 = len(contents2)
            arr_p2 = cast(c_char_p(contents2.encode()), c_void_p)

            vec2 = IOVec(arr_p2, len_contents2)

            vec_arr = create_c_array(IOVec, (vec1, vec2))
            iocb = IOCB(aio_lio_opcode=IOCBCMD.PWRITEV, aio_fildes=fp.fileno(),
                        aio_buf=addressof(vec_arr), aio_offset=0, aio_nbytes=2)

            submit_ret = io_submit(ctx, c_long(1), create_c_array(iocb_p, (pointer(iocb),)))
            self.assertEqual(1, submit_ret)

            event = IOEvent()
            get_event_ret = io_getevents(ctx, c_long(1), c_long(1), create_c_array(IOEvent, (event,)), None)
            self.assertEqual(1, get_event_ret)

            fp.seek(0)
            self.assertEqual(contents1 + contents2, fp.read(len_contents1 + len_contents2))

            io_destroy(ctx)


if __name__ == '__main__':
    unittest.main()
