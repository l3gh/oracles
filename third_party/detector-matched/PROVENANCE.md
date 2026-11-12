# Detector source comparison

Source revision: [65f9c587b0f42f7bb292be5cdf8394ba23393710](https://github.com/PyrexPi/prophet/tree/65f9c587b0f42f7bb292be5cdf8394ba23393710), retrieved 2026-11-12. The included files are unchanged upstream source and license. File hashes are in SOURCE.json.

The original executable is a Python 3.9 PyInstaller bundle. Its embedded `main`, `model` and `resource_path` code objects were extracted with PyInstaller's archive reader. Each corresponding file from this revision was compiled using CPython 3.9.13. The module code and nested code objects matched on bytecode, constants, names, variables and function flags. Filename, timestamps, line-number metadata and full executable build were not compared. This confirms the three detector modules match this revision at bytecode level; it does not identify the bundled third-party dependency versions or establish a reproducible binary build.

The later source snapshot in `../detector/` is retained for provenance but contains changes absent from the supplied executable. Bundled dependency notices and exact dependency sources still require verification before public binary distribution.
