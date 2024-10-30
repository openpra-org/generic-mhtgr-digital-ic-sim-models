# generic-mhtgr-digital-ic-sim-models
Digital Instrumentation &amp; Control (I&amp;C) simulations used in the generic Modular High-Temperature Gas-Cooled Reactor (MHTGR)

## Install

### on macOS
```zsh
brew install icarus-verilog
brew install scansion
````
## Build

```bash
docker build --target=build --tag=mhtgr-ic:build  .
```