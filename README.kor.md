[\[english\]](https://github.com/isac322/linux_aio_bind/blob/master/README.md) | **\[한국어 (korean)\]**

# linux_aio_bind: Python binding for [Linux Kernel AIO](http://lse.sourceforge.net/io/aio.html)

<!---
[![](https://img.shields.io/travis/com/isac322/linux_aio.svg?style=flat-square)](https://travis-ci.com/isac322/linux_aio)
[![](https://img.shields.io/pypi/v/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/codecov/c/github/isac322/linux_aio.svg?style=flat-square)](https://codecov.io/gh/isac322/linux_aio)
[![](https://img.shields.io/pypi/implementation/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/pyversions/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/wheel/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
[![](https://img.shields.io/pypi/l/linux_aio.svg?style=flat-square)](https://pypi.org/project/linux-aio/)
-->

[Linux Kernel AIO](http://lse.sourceforge.net/io/aio.html) system call에 매칭되는 low-level python binding module.

[ctypes 모듈](https://docs.python.org/ko/3/library/ctypes.html)을 사용하여 직접 high-level python module을 개발할게 아니라, **AIO기능을 python에서 사용하기 위한다면** [High-level python wrapper](https://github.com/isac322/linux_aio) 참조

## Linux Kernel AIO이란?

[Linux IO Model 정리 표](https://oxnz.github.io/2016/10/13/linux-aio/#io-models)

간단하게 줄이면 [read(2)](http://man7.org/linux/man-pages/man2/read.2.html)나 [write(2)](http://man7.org/linux/man-pages/man2/write.2.html)와 같은 Blocking IO operation들을 Non-blocking하며 비동기적으로 사용하게 해준다.


### 관련 문서

- [Linux Asynchronous I/O](https://oxnz.github.io/2016/10/13/linux-aio/)
- [Linux Kernel AIO Design Notes](http://lse.sourceforge.net/io/aionotes.txt)
- [How to use the Linux AIO feature](https://github.com/littledan/linux-aio) (in C)


### **[POSIX AIO](http://man7.org/linux/man-pages/man7/aio.7.html)와는 다르다**

POSIX AIO의 API들은 `aio_` 접두사를 가지지만, Linux Kernel AIO는 `io_` 접두사를 가진다.


비동기 입출력을 위한 [POSIX AIO API](http://man7.org/linux/man-pages/man7/aio.7.html)가 이미 존재 하지만, Linux는 user-space인 [glibc](https://www.gnu.org/software/libc/manual/html_node/Asynchronous-I_002fO.html)에서 내부적으로는 multi-threading을 사용하도록 구현하였다.
따라서, [실험](https://github.com/isac322/linux_aio/blob/master/README.kor.md#%EC%84%B1%EB%8A%A5-%EB%B9%84%EA%B5%90)에서 볼 수 있듯 blocking IO API를 사용하는것 보다 많이 안좋은 성능을 보인다.


## 구현 및 구조

- [Python의 ctypes 모듈](https://docs.python.org/ko/3/library/ctypes.html) 사용
- Linux AIO의 C header와 1:1 대응되는 정의 모음
	- C를 사용했을 때의 기능을 100% 옮김
	- [Linux man pages (4.16)](http://man7.org/linux/man-pages/man2/io_submit.2.html)기준으로 man page에 보이는 모든 기능과, [4.20.3 소스 코드](https://elixir.bootlin.com/linux/v4.20.3/source/include/uapi/linux/aio_abi.h#L71)에서 추가된 기능들을 발견할 수 있는 한 모두 옮김
- [ctypes 모듈](https://docs.python.org/ko/3/library/ctypes.html)을 사용하여 포인터 단위로 연산할줄 안다면, 이 패키지를 기반으로하여 다른 형태의 wrapper도 제작 가능
	- 예: [High-level python wrapper](https://github.com/isac322/linux_aio)
- ABI 호출은 `syscall`을 사용하며, [아키텍쳐별로 다른 syscall number](https://fedora.juszkiewicz.com.pl/syscalls.html)를 모듈 설치시에 얻기위해 [cffi](https://pypi.org/project/cffi/)를 사용
	- [소스 코드 참조](linux_aio_bind/syscall.py)
- [python stub](https://github.com/python/mypy/wiki/Creating-Stubs-For-Python-Modules) (`pyi` 파일 - for type hint) 포함
- 문서(man-pages 4.16 기준)에 나오는 모든 에러 핸들링


## 예제

[test](test)의 코드들에서 예제 확인 가능


## Notes & Limits

- 당연하게도 Linux에서만 사용 가능하다
- Binding이기 때문에 Linux의 제약을 그대로 가져온다
	- Kernel interface로 사용되는 파일에는 사용할 수 없다. (e.g. `cgroup`)
	- [때로 Blocking으로 동작하기도 함](https://stackoverflow.com/questions/34572559/asynchronous-io-io-submit-latency-in-ubuntu-linux)
		- 해당 글 포스팅 이후 개발로 완화된 것들이 있기도 하다
	- 아직 개발중인 API이기 때문에, 기능이 추가되기도 한다
	- 또한 Linux 버전이 낮은 경우 일부 지원하지 않는 기능이 있기도 하다
		- [Linux man pages (4.16)](http://man7.org/linux/man-pages/man2/io_submit.2.html)와 그 관련 API 문서 확인 필요
		- Poll은 4.19이상, fsync와 fdsync는 4.18이상의 커널이 필요함
