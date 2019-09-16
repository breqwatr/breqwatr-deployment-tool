# Breqwatr Deployment Tool


## Install

### From PyPi

```python
pip install breqwatr-deployment-tool
```

### From GitHub

```python
pip install git+https://github.com/breqwatr/breqwatr-deployment-tool.git
```


## Examples

### Help

```bash
bwdt --help
```

### Launch registry

```bash
bwdt registry start
```

### Launch PXE

```bash
bwdt pxe start --interface enp0s25 --dhcp-start 10.1.0.90 --dhcp-end 10.1.0.99
```


