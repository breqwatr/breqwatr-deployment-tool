# Creating Offline Installation Media

While online installation is supported and technically faster, there are a
number of reasons to use offline installation anyways.

- Faster installation
- Reliably repeatable
- Air-gap / dark-site support
- Media can be scanned by your security team


## Supported Workstations

This procedure is tested against MMac OSX Ubuntu Server 18.04.

Generally BWDT should not be used on Mac OS, but building offlien media from
Mac OS is fully supported.

The `bwdt` tool must already be installed
([BWDT Installation & Requirements](/installation.html)).


## Mount removable media

Currently we recommend you have at least 128GB on the USB drive / network share
before starting. Note the location you mounted it to, it will be used below as
a command-line argument.


---


# (Optional) Apply your license

In order to download some of the licensed software, now is a good time to apply
your license key. The configuration wizard will walk you through it.

```bash
bwdt configure
```


---


# Download Container Images

## Download every image

The easiest way to go is to download all available packages. If you aren't sure
which you'll need and have both the drive space and network capacity, this is
the recommended option.

```bash
bwdt docker export-images-all
```

## Download individual images

To pull a single image, such as the latest Apt to update your hosts's packages, you can specify it as follows.

```bash
bwdt docker export-image --directory /Volumes/usb128/BWOffline/ --pull --tag latest breqwatr/apt
```

