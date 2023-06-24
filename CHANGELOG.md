# Changelog

<!--next-version-placeholder-->

## v0.2.2 (2023-06-24)

### Fix

* :bug: avoid importing viewer in main process ([`8e88303`](https://github.com/kahojyun/wave-viewer/commit/8e883039e3dc74439548f3a33eb9fa8af852fefd))

## v0.2.1 (2023-05-28)
### Performance
* :zap: imporve `add_line` performance ([`f357941`](https://github.com/kahojyun/wave-viewer/commit/f3579411258312b61fdf3296fd65cf623864507d))
* :zap: use `Queue` instead of `Pipe` for IPC ([`68705c4`](https://github.com/kahojyun/wave-viewer/commit/68705c4c3e5652e8a43f1cd67d10acfadc2077aa))

## v0.2.0 (2023-05-23)
### Feature
* :sparkles: viewer quits automatically when main process quits ([`90fd460`](https://github.com/kahojyun/wave-viewer/commit/90fd46095806d1cd3f699eedce0698ecb961e853))

### Fix
* :adhesive_bandage: add `__version__` and set up psr tool ([`25239be`](https://github.com/kahojyun/wave-viewer/commit/25239be4dd7c827c55c027954d125b5b737dd209))

## v0.1.0 (2023-05-18)

- First release of `wave-viewer`