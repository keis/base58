## Changelog

### v2.1.1 / 2021-10-30
- [#67](https://github.com/keis/base58/pull/67) use github actions (@keis)
- [#66](https://github.com/keis/base58/pull/66) Escape illegal special characters in error message (@hukkin)

### v2.1.0 / 2021-01-09
- [#64](https://github.com/keis/base58/pull/64) Parametrise a few tests over alphabet (@keis)
- [#63](https://github.com/keis/base58/pull/63) Made it handle any base with passing alphabet. (#63) (@tanupoo)
- [#62](https://github.com/keis/base58/pull/62) Setup cfg (@keis)
- [#61](https://github.com/keis/base58/pull/61) Add support to ppc64le (@gururajrkatti)
- [#60](https://github.com/keis/base58/pull/60) Update README.md (@alloynetworks)
- [#59](https://github.com/keis/base58/pull/59) New alias for XRP alphabet (@alloynetworks)
- [#58](https://github.com/keis/base58/pull/58) Improve invalid character message (@keis)
- [#57](https://github.com/keis/base58/pull/57) Autofix for similar letters (@keis)
- [#56](https://github.com/keis/base58/pull/56) Add performance benchmarks using pytest-benchmark (@keis)
- [#53](https://github.com/keis/base58/pull/53) Performance optimizations (@kolomenkin)

### v2.0.1 / 2020-06-06
- [#55](https://github.com/keis/base58/pull/55) Include license file in source distribution (@synapticarbors)
- [#50](https://github.com/keis/base58/pull/50) Typecheck tests now that hamcrest has typing (@keis)
- [#49](https://github.com/keis/base58/pull/49) Replace custom exception assert with hamcrest utils (@keis)

### v2.0.0 / 2020-01-14
- [#47](https://github.com/keis/base58/pull/47) Distribute type data (PEP 561) (@hukkinj1)
- [#48](https://github.com/keis/base58/pull/48) Use setup.cfg for mypy conf (@hukkinj1)
- [#46](https://github.com/keis/base58/pull/46) Allow str input to b58encode_check (@keis)
- [#44](https://github.com/keis/base58/pull/44) Type annotate public API (@hukkinj1)
- [#43](https://github.com/keis/base58/pull/43) Drop python 2.7 and 3.4 support (#43) (@hukkinj1)
- [#42](https://github.com/keis/base58/pull/42) Test py3.7 and py3.8. Set python_requires in setup.py (@hukkinj1)
- [#41](https://github.com/keis/base58/pull/41) Fix encode functions' return types in README (@hukkinj1)
- [#40](https://github.com/keis/base58/pull/40) Enhance/add alphabet param (#40) (@dannywillems)
- [#39](https://github.com/keis/base58/pull/39) accept other bytes-like types (@fametrano)

### v1.0.3 / 2018-12-28
- [#37](https://github.com/keis/base58/pull/37) Update base58.py (@pdelteil)

### v1.0.2 / 2018-09-27
- [#34](https://github.com/keis/base58/pull/34) Add bumpversion config (@keis)

### v1.0.1 / 2018-09-25
- [#31](https://github.com/keis/base58/pull/31) Include tests in PyPI tarball (@dotlambda)

### v1.0.0 / 2018-04-20
- [#27](https://github.com/keis/base58/pull/27) Use bytes for both input and output (@keis)
- [#25](https://github.com/keis/base58/pull/25) Do not strip newline from input to cli (@keis)
- [#26](https://github.com/keis/base58/pull/26) Use tox and pytest to run tests (@keis)
- [#22](https://github.com/keis/base58/pull/22) Add the packaging metadata to build the base58 snap (@elopio)
- [#17](https://github.com/keis/base58/pull/17) improved error message (@fametrano)
- [#21](https://github.com/keis/base58/pull/21) clearer padding (@fametrano)

### v0.2.5 / 2017-04-04
- [#14](https://github.com/keis/base58/pull/14) Slight optimization, version increment (@gappleto97)
- [#12](https://github.com/keis/base58/pull/12) Add integer support (#12) (@gappleto97)
- [#10](https://github.com/keis/base58/pull/10) Add more test systems (@gappleto97)

### v0.2.4 / 2016-10-28
- [#8](https://github.com/keis/base58/pull/8) Package metadata (@keis)

### v0.2.3 / 2016-06-14
- [#6](https://github.com/keis/base58/pull/6) Improve error message when the type is not bytes (@keis, @zkanda)

### v0.2.2 / 2015-04-09
- [#3](https://github.com/keis/base58/pull/3) test round trips (@oconnor663)
- [#2](https://github.com/keis/base58/pull/2) fix encoding of empty string (@keis)
