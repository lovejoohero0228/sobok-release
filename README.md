<div align="center">

# Sobok

**A desktop widget where snow piles up on your screen and you roll it into snowmen**

[![release](https://img.shields.io/github/v/release/lovejoohero0228/sobok-release?label=release&color=4a7fd6)](https://github.com/lovejoohero0228/sobok-release/releases/latest) ![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-6b7a99) [![stars](https://img.shields.io/github/stars/lovejoohero0228/sobok?style=flat&color=e8b93a)](https://github.com/lovejoohero0228/sobok/stargazers)

[Guide](https://lovejoohero0228.github.io/sobok-release/en/) · [Source code](https://github.com/lovejoohero0228/sobok) · [Report a bug](https://github.com/lovejoohero0228/sobok/issues) · [한국어](README.ko.md)

<a href="https://lovejoohero0228.github.io/sobok-release/en/"><img src="docs/hero.gif" alt="Sobok on a desktop" width="720"></a>

</div>

> **This repository is where Sobok is handed out.** The install scripts, the executables, and the guide page live here.
> The code is in the [sobok](https://github.com/lovejoohero0228/sobok) repository. If you like it, please leave a star ⭐ there.

*소복소복 (sobok-sobok) is the Korean word for snow quietly piling up.*

## Install

One line. No admin rights needed, and running it again updates to the latest version.

**Windows** — paste into PowerShell

```powershell
powershell -c "irm https://raw.githubusercontent.com/lovejoohero0228/sobok-release/main/install.ps1 | iex"
```

**macOS** — paste into Terminal

```bash
curl -fsSL https://raw.githubusercontent.com/lovejoohero0228/sobok-release/main/install-mac.sh | bash
```

Installing with an AI agent, how to play, and settings are covered in the [guide](https://lovejoohero0228.github.io/sobok-release/en/).

## Uninstall

```powershell
powershell -c "irm https://raw.githubusercontent.com/lovejoohero0228/sobok-release/main/uninstall.ps1 | iex"
```

```bash
curl -fsSL https://raw.githubusercontent.com/lovejoohero0228/sobok-release/main/uninstall-mac.sh | bash
```

## What is here

| | |
| --- | --- |
| `install.ps1`, `uninstall.ps1` | Windows install and uninstall scripts |
| `install-mac.sh`, `uninstall-mac.sh` | macOS install and uninstall scripts |
| [Releases](https://github.com/lovejoohero0228/sobok-release/releases/latest) | `sobok.exe` (Windows), `sobok-mac.zip` (macOS) |
| `docs/` | The guide page, in [English](https://lovejoohero0228.github.io/sobok-release/en/) and [Korean](https://lovejoohero0228.github.io/sobok-release/) |
| `make-en-page.py` | Builds the English page from the Korean one |

The install scripts only download the app into your user folder and start it. They are short, so you can read them before running.

<sub>Speech bubble font: HSHwalgongGulim (토끼네활자공장)</sub>
