# generic-mhtgr-digital-ic-sim-models
Digital Instrumentation &amp; Control (I&amp;C) simulations used in the generic Modular High-Temperature Gas-Cooled Reactor (MHTGR)

## Install

1. Install Docker

With Docker installed, git clone this repo and run:
```bash
docker build --tag=mhtgr:latest .
```

2. Run the container
```shell
 docker run --rm -it mhtgr:latest __main__.py
```

### on macOS
```zsh
brew install icarus-verilog
brew install scansion
````
## Build

```bash
docker build --target=build --tag=mhtgr-ic:build  .
```