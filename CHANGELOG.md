Changelog
=========
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

[Unreleased](https://github.com/jshwi/constcheck/compare/v0.7.0...HEAD)
------------------------------------------------------------------------
### Added
- Add py.typed

[0.7.0](https://github.com/jshwi/constcheck/releases/tag/v0.7.0) - 2022-12-25
------------------------------------------------------------------------
### Added
- Add support for `pre-commit`

[0.6.1](https://github.com/jshwi/constcheck/releases/tag/v0.6.1) - 2022-11-16
------------------------------------------------------------------------
### Fixed
- Fixes multiline strings split by curly brackets

[0.6.0](https://github.com/jshwi/constcheck/releases/tag/v0.6.0) - 2022-11-12
------------------------------------------------------------------------
### Added
- Adds function to find top-level pyproject.toml

### Remove
- Removes kwargs from `constcheck.main`

[0.5.0](https://github.com/jshwi/constcheck/releases/tag/v0.5.0) - 2022-11-11
------------------------------------------------------------------------
### Added
- Adds `constcheck.constcheck`

### Changed
- Removes `path` keyword argument from `constcheck.constcheck`
- Renames `len` arg to `length`
- Updates help
- Renames `--no-color` to `--no-ansi`

### Removed
- Removes `-f/--filter` argument

[0.4.2](https://github.com/jshwi/constcheck/releases/tag/v0.4.2) - 2022-11-09
------------------------------------------------------------------------
### Fixed
- Fixes multiline strings split by square brackets

[0.4.1](https://github.com/jshwi/constcheck/releases/tag/v0.4.1) - 2022-04-26
------------------------------------------------------------------------
### Fixed
- Files can also be used as path arguments

[0.4.0](https://github.com/jshwi/constcheck/releases/tag/v0.4.0) - 2022-04-25
------------------------------------------------------------------------
### Added
- Allows for multiple path arguments

### Changed
- Paths do not need to be in version control

[0.3.1](https://github.com/jshwi/constcheck/releases/tag/v0.3.1) - 2022-04-25
------------------------------------------------------------------------
### Fixed
- Ensures default lists and dicts are added to and not overridden
- Fixes up typing for `ignore_from`
- Fixes up typing for `ignore_strings`

[0.3.0](https://github.com/jshwi/constcheck/releases/tag/v0.3.0) - 2022-04-23
------------------------------------------------------------------------
### Added
- add: Adds `--ignore-from`
- Adds non-zero exit status for results
- Allows for escaping comma delimiter

[0.2.0](https://github.com/jshwi/constcheck/releases/tag/v0.2.0) - 2022-04-22
------------------------------------------------------------------------
### Added
- Adds support for pyproject.toml
- Adds `-I/--ignore-files`
- Adds `-i/--ignore-strings`
- Adds `constcheck.__version__` and `--version` arg

### Changed
- Updates help

[0.1.0](https://github.com/jshwi/constcheck/releases/tag/v0.1.0) - 2022-04-15
------------------------------------------------------------------------
### Added
- Initial release
