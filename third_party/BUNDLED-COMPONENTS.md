# Bundled detector component audit

The original executable is a Python 3.9 PyInstaller bundle. The following versions were recovered from embedded Python module constants on 2026-11-12. These are component identifiers, not proof that every bundled binary matches an unmodified upstream build. License labels are PyPI metadata, not a replacement for the full notices.

| Component | Reported version | PyPI license metadata | Upstream source |
| --- | --- | --- | --- |
| numpy | 1.20.3 | BSD | [PyPI files](https://pypi.org/project/numpy/1.20.3/#files) |
| scipy | 1.6.3 | BSD | [PyPI files](https://pypi.org/project/scipy/1.6.3/#files) |
| librosa | 0.8.1 | ISC | [PyPI files](https://pypi.org/project/librosa/0.8.1/#files) |
| numba | 0.53.1 | BSD | [PyPI files](https://pypi.org/project/numba/0.53.1/#files) |
| llvmlite | 0.36.0 | BSD | [PyPI files](https://pypi.org/project/llvmlite/0.36.0/#files) |
| pandas | 1.2.4 | BSD | [PyPI files](https://pypi.org/project/pandas/1.2.4/#files) |
| PyAudio | 0.2.11 | Not established | [PyPI files](https://pypi.org/project/PyAudio/0.2.11/#files) |
| SoundFile | 0.10.3 | Not established | Unverified |
| audioread | 2.1.9 | MIT | [PyPI files](https://pypi.org/project/audioread/2.1.9/#files) |
| scikit-learn | 0.24.2 | new BSD | [PyPI files](https://pypi.org/project/scikit-learn/0.24.2/#files) |
| joblib | 1.0.1 | BSD | [PyPI files](https://pypi.org/project/joblib/1.0.1/#files) |
| decorator | 5.0.9 | new BSD License | [PyPI files](https://pypi.org/project/decorator/5.0.9/#files) |
| resampy | 0.2.2 | ISC | [PyPI files](https://pypi.org/project/resampy/0.2.2/#files) |
| pooch | 1.3.0* | BSD License | [PyPI files](https://pypi.org/project/pooch/1.3.0/#files) |
| packaging | 20.9 | BSD-2-Clause or Apache-2.0 | [PyPI files](https://pypi.org/project/packaging/20.9/#files) |
| certifi | 2020.12.5 | MPL-2.0 | [PyPI files](https://pypi.org/project/certifi/2020.12.5/#files) |
| requests | 2.25.1 | Apache 2.0 | [PyPI files](https://pypi.org/project/requests/2.25.1/#files) |
| urllib3 | 1.26.5 | MIT | [PyPI files](https://pypi.org/project/urllib3/1.26.5/#files) |
| idna | 2.10 | BSD-like | [PyPI files](https://pypi.org/project/idna/2.10/#files) |
| chardet | 4.0.0 | LGPL | [PyPI files](https://pypi.org/project/chardet/4.0.0/#files) |
| six | 1.16.0 | MIT | [PyPI files](https://pypi.org/project/six/1.16.0/#files) |
| python-dateutil | 2.8.1 | Dual License | [PyPI files](https://pypi.org/project/python-dateutil/2.8.1/#files) |
| pytz | 2021.1 | MIT | [PyPI files](https://pypi.org/project/pytz/2021.1/#files) |
| threadpoolctl | 2.1.0 | BSD License | [PyPI files](https://pypi.org/project/threadpoolctl/2.1.0/#files) |
| cffi | 1.14.5 | MIT | [PyPI files](https://pypi.org/project/cffi/1.14.5/#files) |
| appdirs | 1.4.4 | MIT | [PyPI files](https://pypi.org/project/appdirs/1.4.4/#files) |
| beautifulsoup4 | 4.9.3 | MIT | [PyPI files](https://pypi.org/project/beautifulsoup4/4.9.3/#files) |
| pycparser | 2.20 | BSD | [PyPI files](https://pypi.org/project/pycparser/2.20/#files) |
| pyparsing | 2.4.7 | MIT License | [PyPI files](https://pypi.org/project/pyparsing/2.4.7/#files) |

* Pooch reports a dirty build in its embedded version metadata. The same version number does not establish identical source.

## Still unverified

- SoundFile reports `0.10.3` internally, but the corresponding PyPI distribution and exact native libsndfile build are not established.
- Exact versions and source for setuptools, soupsieve and wincertstore are not established.
- The bundled native libraries include OpenBLAS, LLVM/llvmlite, libsndfile, OpenSSL, libffi, Fortran runtime components and Microsoft runtime libraries. Their exact versions, licenses, notices and corresponding sources have not all been established.
- Full copyright/license texts and dependency notice packaging for the downloadable executable have not yet been assembled.

These gaps must be resolved before publishing the existing binary. The draft release remains private.

## Native file comparisons

On 2026-11-12, the corresponding CPython 3.9 Windows wheels were downloaded from PyPI and checked against PyPI's SHA-256 before comparing native files to the original executable. NumPy had 14/14 matching native files, SciPy 82/82, pandas 41/41, Numba 12/12, llvmlite 1/1, and scikit-learn 44/44 for matching paths under each package directory. This does not establish that unrelated DLLs, pure Python files, or other components match those wheels.

| PyPI wheel | SHA-256 |
| --- | --- |
| numpy-1.20.3-cp39-cp39-win_amd64.whl | `6690080810f77485667bfbff4f69d717c3be25e5b11bb2073e76bb3f578d99b4` |
| scipy-1.6.3-cp39-cp39-win_amd64.whl | `3274ce145b5dc416c49c0cf8b6119f787f0965cd35e22058fe1932c09fe15d77` |
| pandas-1.2.4-cp39-cp39-win_amd64.whl | `2b063d41803b6a19703b845609c0b700913593de067b552a8b24dd8eeb8c9895` |
| numba-0.53.1-cp39-cp39-win_amd64.whl | `17146885cbe4e89c9d4abd4fcb8886dee06d4591943dc4343500c36ce2fcfa69` |
| llvmlite-0.36.0-cp39-cp39-win_amd64.whl | `1dee416ea49fd338c74ec15c0c013e5273b0961528169af06ff90772614f7f6c` |
| scikit_learn-0.24.2-cp39-cp39-win_amd64.whl | `40556bea1ef26ef54bc678d00cf138a63069144a0b5f3a436eecd8f3468b903e` |
