# Beagleboard AI-64开箱简明使用教程

Beagleboard AI-64是Beagleboard系列目前最强性能的开发板，官方网站https://beagleboard.org/。其文档详尽，有在线文档和开发板内置文档。其内容，一方面有冗余冲突，或部分内容没有一致更新，或缺乏如wifi设置等详尽操作。因此，我根据自己的开箱使用过程撰写了这篇快速使用指引，突出操作重点，希望能够以最快的速度帮您上手。

## Step 0 - 开发板简介

### 芯片特性 Texas Instruments TDA4VM SoC

- Dual 64-bit Arm Cortex-A72 microprocessor subsystem at up to 2.0 GHz
- 1MB shared L2 cache per dual-core Cortex-A72 cluster
- 32KB L1 DCache and 48KB L1 ICache per Cortex-A72 core
- C7x floating point, vector DSP, up to 1.0 GHz, 80 GFLOPS, 256 GOPS
- Deep-learning matrix multiply accelerator (MMA), up to 8 TOPS (8b) at 1.0 GHz
- Vision Processing Accelerators (VPAC) with Image Signal Processor (ISP) and multiple vision assist accelerators
- Depth and Motion Processing Accelerators (DMPAC)
- Six Arm Cortex-R5F MCUs at up to 1.0 GHz
- Two C66x floating point DSP, up to 1.35 GHz, 40 GFLOPS, 160 GOPS
- 3D GPU PowerVR Rogue 8XE GE8430, up to 750 MHz, 96 GFLOPS, 6 Gpix/sec
- Memory subsystem with up to 8MB of on-chip L3 RAM with ECC and coherency
- Twelve Multichannel Audio Serial Port (MCASP) modules

### 开发板特性
- BeagleBone® Black header compatibility for expansion with existing add-on capes
- MikroBus shuttle header giving access to hundreds of existing Click sensors and actuators
- Memory
    - 4GB LPDDR4
    - 16GB eMMC flash with high-speed interface
    - MicroSD card slot

- High-Speed Interfaces
    - M.2 E-key PCIe connector for WiFi modules
    - USB 3.0 Type-C interface for power input and data
    - 2* USB 3.0 Type-A interface
    - Gigabit Ethernet

- Camera and Display Connector
    - Mini Display Port interface for monitor displays
    - 2* 4-Lane CSI connector for popular camera options
    - 4-Lane DSI connector for flat-panel displays

- User Interfaces
    - 1* Boot button, 1* Reset Button, 1* Power button
    - 1* Power indication LED, 5* User LEDs
    - 5V DC input power
    - 2* UART debug
    - JTAG 10pin Tag-Connector for debug

## Step 1 - 下载并烧录镜像
前往 https://www.beagleboard.org/distros 下载最新镜像

截至2023-05-05最新的image是 https://www.beagleboard.org/distros/bbai64-webinar-202301，可用于烧录microSD以启动开发板。

Beagleboard AI-64开发板自带16GB eMMC，并且预烧录了可启动的系统image。若需要刷新eMMC系统image, 可下载eMMC flasher镜像。目前最新版本下载链接为 https://www.beagleboard.org/distros/bbai64-emmc-flasher-2022-11-01 

使用balenaEtcher烧录image，因后续更新系统，安装完整model zoo及docker，建议使用32GB以上microSD卡。具体烧录步骤请参考 https://beagleboard.org/getting-started 。

**扩大rootfs空间**

```
#find the SD card device entry using lsblk (Eg: /dev/sdc)
#use the following commands to expand the filesystem
#Make sure you have write permission to SD card or run the commands as root

#Unmount the BOOT and rootfs partition before using parted tool
umount /dev/sdX1
umount /dev/sdX2

#Use parted tool to resize the rootfs partition to use
#the entire remaining space on the SD card
#You might require sudo permissions to execute these steps
parted -s /dev/sdX resizepart 2 '100%'
e2fsck -f /dev/sdX2
resize2fs /dev/sdX2
#replace /dev/sdX in above commands with SD card device entry
```

## Step 2 - 使用microSD卡启动开发板
### Step 2.1 - 准备硬件环境
请参考 https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/ch03.html# “Connecting up your BeagleBone AI-64” 准备好硬件环境（USB串口，鼠标，键盘，WiFi, 显示器等）


开发板支持microSD卡或者板载eMMC启动，关于开发板的启动模式请参考开发板文档 https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/index.html 

### Step 2.2 启动系统
插入Step 1 烧录好镜像的microSD卡，连接好电源启动系统。您将看到相关LED闪烁，并在显示屏上看到Linux内核启动的log直至Xfce桌面出现。

### Step 2.3 ssh登录开发板
您可以通过串口虚拟出的网口，从host侧ssh登录到开发板。推荐host端使用MobaXterm/Putty等串口工具。

`ssh debian@192.168.7.2` 
pwd: temmpwd

### Step 2.4 设置wifi
系统预装了wpa_supplicant组件，其中wpa_gui可用于图形化配置wifi。请确保USB wifi或m.2 wifi设备正常连接，以root用户启动wpi_gui后进行配置。具体使用可参考 https://wiki.archlinux.org/title/Wpa_supplicant 


### Step 3 更新软件系统
以下内容引自 https://docs.beagleboard.org/latest/boards/beaglebone/ai-64/update.html 

```
更新系统
sudo apt update
sudo apt install --only-upgrade bb-j721e-evm-firmware generic-sys-mods
sudo apt upgrade

更新u-boot
sudo /opt/u-boot/bb-u-boot-beagleboneai64/install-emmc.sh
sudo /opt/u-boot/bb-u-boot-beagleboneai64/install-microsd.sh
sudo reboot

更新内核
sudo apt install bbb.io-kernel-5.10-ti-k3-j721e

更新xfce桌面
sudo apt install bbb.io-xfce4-desktop

更新edgeai example
sudo apt install ti-edgeai-8.2-base ti-vision-apps-8.2 ti-vision-apps-eaik-firmware-8.2

清理安装包
sudo apt autoremove --purge
```




