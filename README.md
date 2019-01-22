**\[english\]** | [\[한국어 (korean)\]](https://github.com/isac322/linux_aio_bind/blob/master/README.kor.md)

# linux_aio_bind: Python binding for [Linux Kernel AIO](http://lse.sourceforge.net/io/aio.html)

[![](https://img.shields.io/travis/com/isac322/linux_aio_bind.svg?style=flat-square)](https://travis-ci.com/isac322/linux_aio_bind)
[![](https://img.shields.io/pypi/v/linux_aio_bind.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/codecov/c/github/isac322/linux_aio_bind.svg?style=flat-square)](https://codecov.io/gh/isac322/linux_aio_bind)
[![](https://img.shields.io/pypi/implementation/linux_aio_bind.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/pyversions/linux_aio_bind.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/wheel/linux_aio_bind.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/l/linux_aio_bind.svg?style=flat-square)](https://pypi.org/project/linux-aio/)

A low-level python binding module that matches the Linux kernel AIO system call.

If you are not using the [ctypes module](https://docs.python.org/ko/3/library/ctypes.html) to develop high-level python modules directly, but **you want to use AIO functionality in python**, see [High-level python wrapper](https://github.com/isac322/linux_aio).

## What is Linux Kernel AIO?

[Linux IO Models table](https://oxnz.github.io/2016/10/13/linux-aio/#io-models)

In summary, it allows non-blocking and asynchronous use of blocking IO operations such as [read(2)](http://man7.org/linux/man-pages/man2/read.2.html) and [write(2)](http://man7.org/linux/man-pages/man2/write.2.html).


### Related documents

- [Linux Asynchronous I/O](https://oxnz.github.io/2016/10/13/linux-aio/)
- [Linux Kernel AIO Design Notes](http://lse.sourceforge.net/io/aionotes.txt)
- [How to use the Linux AIO feature](https://github.com/littledan/linux-aio) (in C)


### **It is different from [POSIX AIO](http://man7.org/linux/man-pages/man7/aio.7.html)**

The POSIX AIO APIs have the `aio_` prefix, but the Linux Kernel AIO has the `io_` prefix.


There is already a POSIX AIO API for asynchronous I/O, but Linux implements it in glibc, a user-space library, which is supposed to use multi-threading internally.
So, as you can see from [the experiment](https://github.com/isac322/linux_aio#evaluation), it's much worse than using the blocking IO API.


## Implementation & Structure

- [ctypes module](https://docs.python.org/3/library/ctypes.html) is used.
- It is defined to correspond `1:1` with the C header of Linux AIO.
	- Implemented 100% of the functionality when using C.
	- All the functions shown in the man page based on [Linux man pages (4.16)](http://man7.org/linux/man-pages/man2/io_submit.2.html), and all the functions added in [4.20.3 source code](https://elixir.bootlin.com/linux/v4.20.3/source/include/uapi/linux/aio_abi.h#L71), as far as I can find them. 
- If you know how to use the [ctypes module](https://docs.python.org/3/library/ctypes.html) to operate on pointers, you can also build other types of wrappers based on this package.
	- e.g. [High-level python wrapper](https://github.com/isac322/linux_aio)
- It uses `syscall` for invoking ABI and [cffi](https://pypi.org/project/cffi/) for gathering [different syscall number by architecture](https://fedora.juszkiewicz.com.pl/syscalls.html) on module installation.
	- [refer the code](linux_aio_bind/syscall.py)
- [python stub](https://github.com/python/mypy/wiki/Creating-Stubs-For-Python-Modules) (`pyi` files - for type hint) are included.
- All error handling in the documentation (based on man-pages 4.16)


## Example

Examples can be found in the code in the [test directory](test).


## Notes & Limits

- Obviously available only on Linux
- Because it is a wrapper, it brings the constraints of Linux.
	- It can not be used for files used as a kernel interface. (e.g. `cgroup`)
	- [Sometimes it works as Blocking.](https://stackoverflow.com/questions/34572559/asynchronous-io-io-submit-latency-in-ubuntu-linux)
		- There are some things that have been solved through development after posting.
	- Some features are being added because they are still under development.
	- There are also some features that are not supported when the Linux version is low
		- You need to check [Linux man pages (4.16)](http://man7.org/linux/man-pages/man2/io_submit.2.html) and its related API documentation
		- Poll is 4.19 or higher, fsync and fdsync require 4.18 or higher kernel
