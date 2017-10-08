# Golite
Add essential language support for the Go language to Sublime Text 3, including:
- Code completion `gocode`
- Goto Definition `godef + guru`
- Lint on save as well as lint manually `sublimeLinter + gometalinter`
- Format on save as well as format manually `gofmt + goimports`
- Rename `gorename`

## Installation

The *Golite* package is installed by using
[Package Control](https://packagecontrol.io).

 - If Package Control is not installed, follow the [Installation Instructions](https://packagecontrol.io/installation)
 - Open the Sublime Text command palette and run the `Package Control: Install
   Package` command
 - Type `Golite` and select the package to perform the installation

## Commands

- `Golite: Format` Format manually
- `Golite: Godef` Go to definition
- `Golite: Rename` Rename identifier
- `Golite: Install Dependencies` Install dependencies
- `Golite: Doctor - Audit Installation` Audits installation for common issues

## Dependencies

- [gocode](https://github.com/nsf/gocode) `An autocompletion daemon for the Go programming language`
- [guru](https://golang.org/x/tools/cmd/guru) `A tool for answering questions about Go source code`
- [goimports](https://golang.org/x/tools/cmd/goimports) `Update your Go import lines, adding missing ones and removing unreferenced ones`
- [godef](https://github.com/rogpeppe/godef) `Print where symbols are defined in Go source code`
- [gometalinter](https://github.com/alecthomas/gometalinter) `Concurrently run Go lint tools and normalise their output`
- [gorename](https://golang.org/x/tools/cmd/gorename) `Perform precise type-safe renaming of identifiers in Go source code`
- [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) `Interactive code linting framework for Sublime Text 3`

## License
[MIT](LICENSE)
