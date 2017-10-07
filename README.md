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

- [gocode](https://github.com/nsf/gocode)
- [guru](https://golang.org/x/tools/cmd/guru)
- [goimports](https://golang.org/x/tools/cmd/goimports)
- [godef](https://github.com/rogpeppe/godef)
- [gometalinter](https://github.com/alecthomas/gometalinter)
- [gorename](https://golang.org/x/tools/cmd/gorename)
- [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3)

## License
[MIT](LICENSE)
