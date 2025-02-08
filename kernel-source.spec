


%define srcversion 6.11
%define patchversion 6.11.0
%define git_commit 78175ea6ca4ac148a328fabd4b5ce50ce12053a0
%define variant %{nil}

%include %_sourcedir/kernel-spec-macros

%(chmod +x %_sourcedir/{guards,apply-patches,check-for-config-changes,group-source-files.pl,split-modules,modversions,kabi.pl,mkspec,compute-PATCHVERSION.sh,arch-symbols,log.sh,try-disable-staging-driver,compress-vmlinux.sh,mkspec-dtb,check-module-license,klp-symbols,splitflist,mergedep,moddep,modflist,kernel-subpackage-build})

Name:           kernel-source
Version:        6.11.0
%if 0%{?is_kotd}
Release:        8.27.g78175ea
%else
Release:        8.27
%endif
Summary:        The Linux Kernel Sources
License:        GPL-2.0-only
Group:          Development/Sources
URL:            https://www.kernel.org/
AutoReqProv:    off
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150300
BuildRequires:  bash-sh
%endif
BuildRequires:  coreutils
BuildRequires:  fdupes
BuildRequires:  sed
%if ! 0%{?is_kotd} || ! %{?is_kotd_qa}%{!?is_kotd_qa:0}
BuildArch:      noarch
%else
ExclusiveArch:  do_not_build
%endif
Prefix:         /usr/src

%define src_install_dir usr/src/linux-%kernelrelease%variant

%if %{undefined _rpmmacrodir}
%define _rpmmacrodir /etc/rpm
%endif

Source0:        https://www.kernel.org/pub/linux/kernel/v6.x/linux-%srcversion.tar.xz
%if "https://www.kernel.org/pub/linux/kernel/v6.x/" != ""
Source1:        https://www.kernel.org/pub/linux/kernel/v6.x/linux-%srcversion.tar.sign
Source2:        linux.keyring
%endif
Source3:        kernel-source.rpmlintrc
Source14:       series.conf
Source16:       guards
Source17:       apply-patches
Source19:       kernel-binary-conflicts
Source20:       obsolete-kmps
Source21:       config.conf
Source23:       supported.conf
Source33:       check-for-config-changes
Source35:       group-source-files.pl
Source36:       README.PATCH-POLICY.SUSE
Source37:       README.SUSE
Source38:       README.KSYMS
Source40:       source-timestamp
Source46:       split-modules
Source47:       modversions
Source48:       macros.kernel-source
Source49:       kernel-module-subpackage
Source50:       kabi.pl
Source51:       mkspec
Source52:       kernel-source%variant.changes
Source53:       kernel-source.spec.in
Source54:       kernel-binary.spec.in
Source55:       kernel-syms.spec.in
Source56:       kernel-docs.spec.in
Source57:       kernel-cert-subpackage
Source58:       constraints.in
Source60:       config.sh
Source61:       compute-PATCHVERSION.sh
Source62:       old-flavors
Source63:       arch-symbols
Source64:       package-descriptions
Source65:       kernel-spec-macros
Source67:       log.sh
Source68:       host-memcpy-hack.h
Source69:       try-disable-staging-driver
Source70:       kernel-obs-build.spec.in
Source71:       kernel-obs-qa.spec.in
Source72:       compress-vmlinux.sh
Source73:       dtb.spec.in.in
Source74:       mkspec-dtb
Source75:       release-projects
Source76:       check-module-license
Source77:       klp-symbols
Source78:       modules.fips
Source79:       splitflist
Source80:       mergedep
Source81:       moddep
Source82:       modflist
Source83:       kernel-subpackage-build
Source84:       kernel-subpackage-spec
Source85:       kernel-default-base.spec.txt
Source86:       old_changelog.txt
Source100:      config.tar.bz2
Source101:      config.addon.tar.bz2
Source102:      patches.arch.tar.bz2
Source103:      patches.drivers.tar.bz2
Source104:      patches.fixes.tar.bz2
Source105:      patches.rpmify.tar.bz2
Source106:      patches.suse.tar.bz2
Source108:      patches.addon.tar.bz2
Source109:      patches.kernel.org.tar.bz2
Source110:      patches.apparmor.tar.bz2
Source111:      patches.rt.tar.bz2
Source113:      patches.kabi.tar.bz2
Source114:      patches.drm.tar.bz2
Source120:      kabi.tar.bz2
Source121:      sysctl.tar.bz2
Requires(post): coreutils sed
Requires:       kernel-devel%variant = %version-%source_rel
Provides:       %name = %version-%source_rel
Provides:       %name-srchash-%git_commit
Provides:       linux
Provides:       multiversion(kernel)
Recommends:     bc
Recommends:     bison
Recommends:     flex
Recommends:     libelf-devel
Recommends:     openssl-devel
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150300
Recommends:     dwarves >= 1.22
%endif
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150300
Recommends:     kernel-install-tools
%endif
%obsolete_rebuilds %name

%define _binary_payload w9.bzdio

%define symbols %(set -- $([ -e %_sourcedir/extra-symbols ] && cat %_sourcedir/extra-symbols) ; echo $*)

%define do_vanilla "%variant" == ""

%description
Linux kernel sources with many fixes and improvements.


%source_timestamp

%post
%relink_function

relink linux-%kernelrelease%variant /usr/src/linux%variant

%files -f nondevel.files

%package -n kernel-devel%variant
Summary:        Development files needed for building kernel modules
Group:          Development/Sources
AutoReqProv:    off
Provides:       kernel-devel%variant = %version-%source_rel
Provides:       multiversion(kernel)
Requires:       kernel-macros
Requires(post): coreutils
%obsolete_rebuilds kernel-devel%variant

%description -n kernel-devel%variant
Kernel-level headers and Makefiles required for development of
external kernel modules.


%source_timestamp

%post -n kernel-devel%variant
%relink_function

relink linux-%kernelrelease%variant /usr/src/linux%variant

%files -n kernel-devel%variant -f devel.files
%ghost /usr/src/linux%variant
%doc /usr/share/doc/packages/*

%package -n kernel-macros
Summary:        RPM macros for building Kernel Module Packages
Group:          Development/Sources
Provides:       kernel-subpackage-macros

%description -n kernel-macros
This package provides the rpm macros and templates for Kernel Module Packages


%source_timestamp

%if "%variant" == ""
%files -n kernel-macros
%{_rpmmacrodir}/macros.kernel-source
/usr/lib/rpm/kernel-*-subpackage
%dir /usr/lib/rpm/kernel
/usr/lib/rpm/kernel/*
%endif

%package vanilla
%obsolete_rebuilds %name-vanilla
Summary:        Vanilla Linux kernel sources with minor build fixes
Group:          Development/Sources
AutoReqProv:    off
Provides:       %name-vanilla = %version-%source_rel
Provides:       multiversion(kernel)
Requires:       kernel-macros
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150300
Recommends:     kernel-install-tools
%endif

%description vanilla
Vanilla Linux kernel sources with minor build fixes.


%source_timestamp

%if %do_vanilla
%files vanilla
/usr/src/linux-%kernelrelease-vanilla
%endif

%prep

echo "Symbol(s): %symbols"

%setup -q -c -T -a 100 -a 101 -a 102 -a 103 -a 104 -a 105 -a 106 -a 108 -a 109 -a 110 -a 111 -a 113 -a 114 -a 120 -a 121

%build
%install
mkdir -p %{buildroot}/usr/src
pushd %{buildroot}/usr/src

tar -xf %{S:0}
find . -xtype l -delete -printf "deleted '%f'\n"
if test "%srcversion" != "%kernelrelease%variant"; then
	mv linux-%srcversion linux-%kernelrelease%variant
fi

%if %do_vanilla
	cp -al \
	linux-%kernelrelease%variant linux-%kernelrelease-vanilla
cd linux-%kernelrelease-vanilla
%_sourcedir/apply-patches --vanilla %_sourcedir/series.conf %my_builddir %symbols
rm -f $(find . -name ".gitignore")
%fdupes $PWD
cd ..
%endif

cd linux-%kernelrelease%variant
%_sourcedir/apply-patches %_sourcedir/series.conf %my_builddir %symbols
rm -f $(find . -name ".gitignore")

if [ -f %_sourcedir/localversion ] ; then
    cat %_sourcedir/localversion > localversion
fi
%fdupes $PWD
cd ..
popd

DOC=/usr/share/doc/packages/%name-%kernelrelease
mkdir -p %buildroot/$DOC
cp %_sourcedir/README.SUSE %buildroot/$DOC
ln -s $DOC/README.SUSE %buildroot/%src_install_dir/

%if "%variant" == ""
install -m 755 -d %{buildroot}%{_rpmmacrodir}
install -m 644 %_sourcedir/macros.kernel-source %{buildroot}%{_rpmmacrodir}
echo "%%kernel_module_directory %{kernel_module_directory}" >> %{buildroot}%{_rpmmacrodir}/macros.kernel-source

install -m 755 -d %{buildroot}/usr/lib/rpm
install -m 644 %_sourcedir/kernel-{module,cert}-subpackage \
    %{buildroot}/usr/lib/rpm/
install -m 755 -d %{buildroot}/usr/lib/rpm/kernel
install -m 755 %_sourcedir/{splitflist,mergedep,moddep,modflist,kernel-subpackage-build} %{buildroot}/usr/lib/rpm/kernel
install -m 644 %_sourcedir/kernel-subpackage-spec %{buildroot}/usr/lib/rpm/kernel
install -m 644 %_sourcedir/kernel-spec-macros %{buildroot}/usr/lib/rpm/kernel
install -m 644 -T %_sourcedir/kernel-default-base.spec.txt %{buildroot}/usr/lib/rpm/kernel/kernel-default-base.spec
%endif

pushd "%buildroot"
perl "%_sourcedir/group-source-files.pl" \
	-D "$OLDPWD/devel.files" -N "$OLDPWD/nondevel.files" \
	-L "%src_install_dir"
popd

find %{buildroot}/usr/src/linux* -type f -name '*.[ch]' -perm /0111 -exec chmod -v a-x {} +
grep -Elr '^#! */usr/bin/env ' %{buildroot}/usr/src/linux* | while read f; do
    sed -re '1 { s_^#! */usr/bin/env +/_#!/_ ; s_^#! */usr/bin/env +([^/])_#!/usr/bin/\1_ }' -i "$f"
done
ts="$(head -n1 %_sourcedir/source-timestamp)"
find %buildroot/usr/src/linux* ! -type l -print0 | xargs -0 touch -d "$ts"

%changelog
* Sun Sep 15 2024 mkubecek@suse.cz
- update to 6.11 final
- refresh configs (headers only)
- commit 78175ea
* Sun Sep 15 2024 mkubecek@suse.cz
- config: update and reenable armv6hl configs
- options mirrored from armv7hl or other architectures
- commit 8ea4570
* Sun Sep 15 2024 mkubecek@suse.cz
- config: update and reenable armv7hl configs
- options mirrored from arm64 or other architectures except
  - TURRIS_OMNIA_MCU=m
  - TURRIS_OMNIA_MCU_GPIO=y
  - TURRIS_OMNIA_MCU_SYSOFF_WAKEUP=y
  - TURRIS_OMNIA_MCU_WATCHDOG=y
  - TURRIS_OMNIA_MCU_TRNG=y
- commit 3bfbb8e
* Sun Sep 15 2024 mkubecek@suse.cz
- config: update and reenable arm64 configs
- options mirrored from other architectures except
  - COMPRESSED_INSTALL=n
  - PCIE_ROCKCHIP_DW_EP=y
  - QCOM_TZMEM_MODE_GENERIC=1
  - MARVELL_CN10K_DPI=m
  - NET_AIROHA=m
  - I2C_MT7621=m
  - PINCTRL_IMX_SCMI=m
  - PINCTRL_IMX91=y
  - PINCTRL_MA35D1=n
  - PINCTRL_SM4250_LPASS_LPI=m
  - REGULATOR_QCOM_PM8008=m
  - REGULATOR_RZG2L_VBCTRL=m
  - DRM_STM_LVDS=m
  - STM32_DMA3=m
  - EC_LENOVO_YOGA_C630=m
  - COMMON_CLK_C3_PLL=m
  - COMMON_CLK_C3_PERIPHERALS=m
  - CLK_QCM2290_GPUCC=m
  - IPQ_NSSCC_QCA8K=m
  - SM_CAMCC_7150=m
  - SM_CAMCC_8650=m
  - SM_DISPCC_7150=m
  - SM_VIDEOCC_7150=m
  - QCOM_CPUCP_MBOX=m
  - QCOM_PD_MAPPER=m
  - MEDIATEK_MT6359_AUXADC=m
  - PWM_AXI_PWMGEN=m
  - STM32MP_EXTI=m
  - RESET_IMX8MP_AUDIOMIX=m
  - PHY_AIROHA_PCIE=m
  - PHY_FSL_IMX8QM_HSIO=m
  - INTERCONNECT_MTK=y
  - INTERCONNECT_QCOM_MSM8953=m
  - BATTERY_LENOVO_YOGA_C630=m
  - UCSI_LENOVO_YOGA_C630=m
- commit 7f8bc5b
* Mon Sep  9 2024 mkubecek@suse.cz
- update to 6.11-rc7
- refresh configs
- commit 5661bfe
* Mon Sep  2 2024 msuchanek@suse.de
- Update config files (jsc#PED-10537).
  ppc64le: NR_CPUS=8192
  This alings with x86.
- commit 20a31e9
* Sun Sep  1 2024 mkubecek@suse.cz
- update to 6.11-rc6
- refresh configs
- commit f1c4491
* Fri Aug 30 2024 jslaby@suse.cz
- Update config files. Disable BTF on 32bit architectures (bsc#1229450)
- commit c02f88f
* Mon Aug 26 2024 msuchanek@suse.de
- rpm/check-for-config-changes: Exclude ARCH_USING_PATCHABLE_FUNCTION_ENTRY
  gcc version dependent, at least on ppc
- commit 16da158
* Sun Aug 25 2024 mkubecek@suse.cz
- update to 6.11-rc5
- update configs
  - RANDOMIZE_IDENTITY_BASE=n (s390x only)
- commit 74d649b
* Fri Aug 23 2024 jslaby@suse.cz
- drm/amd/display: Fix Synaptics Cascaded DSC Determination
  (bsc#1228093 #3495).
- commit 295e3d0
* Mon Aug 19 2024 mpdesouza@suse.com
- livepatch: Add -fdump-ipa-clones to build (jsc#SLE-17360
  bsc#1190003 bsc#1229042).
- commit f06435b
* Mon Aug 19 2024 jslaby@suse.cz
- drm/amd/display: Fix a typo in revert commit (bsc#1228093
- commit 5ad0c94
* Mon Aug 19 2024 mkubecek@suse.cz
- update to 6.11-rc4
- drop 1 mainline patch
  - patches.suse/drm-amd-display-Take-Synaptics-Cascaded-Topology-int.patch (338567d17627)
- update configs
  - NETFS_DEBUG=n (=y in */debug)
- commit 7b0cb95
* Thu Aug 15 2024 mhocko@suse.com
- disable CONFIG_MEMCG_V1 (jsc#PED-10113)
  cgroup v1 is deprecated for a long time
- commit 81d83d0
* Mon Aug 12 2024 jslaby@suse.cz
- rpm/kernel-binary.spec.in: fix klp_symbols macro
  The commit below removed openSUSE filter from %%ifs of the klp_symbols
  definition. But it removed -c of grep too and that causes:
  error: syntax error in expression:  01 && (  || 1 )
  error:                                        ^
  error: unmatched (:  01 && (  || 1 )
  error:                     ^
  error: kernel-default.spec:137: bad %%if condition:  01 && (  || 1 )
  So reintroduce -c to the PTF's grep.
  Fixes: fd0b293bebaf (kernel-binary.spec.in: Enable klp_symbols on openSUSE Tumbleweed (boo#1229042).)
- commit 4a36fe3
* Mon Aug 12 2024 mkubecek@suse.cz
- update to 6.11-rc3
- commit b7fed99
* Sat Aug 10 2024 tiwai@suse.de
- rpm/kernel-binary.spec.in: Fix build regression
  The previous fix forgot to take over grep -c option that broke the
  conditional expression
- commit d29edf2
* Fri Aug  9 2024 mpdesouza@suse.com
- kernel-binary.spec.in: Enable klp_symbols on openSUSE Tumbleweed (boo#1229042).
  After the Jump project the kernel used by SLE and openSUSE Leap are the
  same. As consequence the klp_symbols variable is set, enabling
  kernel-default-livepatch-devel on both SLE and openSUSE.
  The current rules to avoid enabling the package exclude openSUSE
  Tumbleweed alone, which doesn't makes sense for now. Enabling
  kernel-default-livepatch-devel on TW makes it easier to test the
  creation of kernel livepatches of the next SLE versions.
- commit fd0b293
* Thu Aug  8 2024 mvetter@suse.com
- kernel-binary: generate and install compile_commands.json (bsc#1228971)
  This file contains the command line options used to compile every C file.
  It's useful for the livepatching team.
- commit f1b9586
* Wed Aug  7 2024 mkoutny@suse.com
- packaging: Add case-sensitive perl option parsing
  A recent change in Getopt::Long [1]:
  Changes in version 2.55
  - ----------------------
  * Fix long standing bug that duplicate options were not detected
  when the options differ in case while ignore_case is in effect.
  This will now yield a warning and become a fatal error in a future
  release.
  perl defaults to ignore_case by default, switch it off to avoid
  accidental misparsing of options.
  This was suggested after similar change in scripts/.
- commit e978477
* Mon Aug  5 2024 mkubecek@suse.cz
- check-for-config-changes: ignore also GCC_ASM_GOTO_OUTPUT_BROKEN
  Mainline commit f2f6a8e88717 ("init/Kconfig: remove
  CONFIG_GCC_ASM_GOTO_OUTPUT_WORKAROUND") replaced
  GCC_ASM_GOTO_OUTPUT_WORKAROUND with GCC_ASM_GOTO_OUTPUT_BROKEN. Ignore both
  when checking config changes.
- commit b60be3e
* Mon Aug  5 2024 mkubecek@suse.cz
- update to 6.11-rc2
- update configs
  - FBNIC=m (x86_64 only)
- commit 5b048b7
* Sat Aug  3 2024 mkubecek@suse.cz
- config: disable PROC_PID_CPUSET also in arm configs
  kernel-source commit 80a84db74f07 ("Update config files (bsc#1228801)")
  disabled PROC_PID_CPUSET in all currently enabled configs. Disable this
  config options also in arm configs which are disabled at the moment and are
  going to be reenabled once updated for the 6.11 cycle.
- commit 0d4db5c
* Fri Aug  2 2024 mkoutny@suse.com
- Update config files (bsc#1228801)
  cpuset filesystem is a relic older than cgroup v1, keep it around (to
  have cpuset controller) but disable CONFIG_PROC_PID_CPUSET to hide
  /proc/$pid/cpuset that serves nothing nowadays.
- commit 80a84db
* Tue Jul 30 2024 shung-hsi.yu@suse.com
- rpm/guards: fix precedence issue with control flow operator
  With perl 5.40 it report the following error on rpm/guards script:
  Possible precedence issue with control flow operator (exit) at scripts/guards line 208.
  Fix the issue by adding parenthesis around ternary operator.
- commit 07b8b4e
* Mon Jul 29 2024 mkubecek@suse.cz
- update to 6.11-rc1
- drop 12 patches (all stable)
  - patches.kernel.org/*
- refresh
  - patches.rpmify/BTF-Don-t-break-ABI-when-debuginfo-is-disabled.patch
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/drm-amd-display-Take-Synaptics-Cascaded-Topology-int.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/kernel-add-release-status-to-kernel-build.patch
  - patches.suse/panic-do-not-print-uninitialized-taint_flags.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - General setup
  - CONFIG_MEMCG_V1=y
  - Memory Management options
  - CONFIG_SLAB_BUCKETS=y
  - NVME Support
  - CONFIG_NVME_TARGET_DEBUGFS=n
  - Misc devices
  - CONFIG_KEBA_CP500=m
  - Multiple devices driver support (RAID and LVM)
  - CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG_PLATFORM_KEYRING=y
  - Network device support
  - CONFIG_IDPF_SINGLEQ=n
  - CONFIG_NET_VENDOR_META=y
  - CONFIG_TEHUTI_TN40=m
  - CONFIG_RTL8192DU=m
  - GPIO Support
  - CONFIG_GPIO_SLOPPY_LOGIC_ANALYZER=n
  - CONFIG_GPIO_VIRTUSER=m
  - CONFIG_POWER_SEQUENCING=m
  - CONFIG_POWER_SEQUENCING=m
  - Power supply class support
  - CONFIG_BATTERY_MAX1720X=m
  - CONFIG_CHARGER_CROS_CONTROL=m
  - Hardware Monitoring support
  - CONFIG_SENSORS_CROS_EC=m
  - CONFIG_SENSORS_MP2891=m
  - CONFIG_SENSORS_MP2993=m
  - CONFIG_SENSORS_MP5920=m
  - CONFIG_SENSORS_MP9941=m
  - CONFIG_SENSORS_SPD5118=m
  - CONFIG_SENSORS_SPD5118_DETECT=y
  - Multifunction device drivers
  - CONFIG_MFD_CS40L50_I2C=n
  - CONFIG_MFD_CS40L50_SPI=n
  - Multimedia support
  - CONFIG_VIDEO_GC05A2=m
  - CONFIG_VIDEO_GC08A3=m
  - CONFIG_VIDEO_IMX283=m
  - Graphics support
  - CONFIG_DRM_AMD_ISP=y
  - CONFIG_DRM_I915_REPLAY_GPU_HANGS_API=n
  - CONFIG_BACKLIGHT_LM3509=m
  - Sound card support
  - CONFIG_SND_HDA_CODEC_SENARYTECH=m
  - CONFIG_SND_SOC_AK4619=n
  - CONFIG_SND_SOC_CS530X_I2C=n
  - CONFIG_SND_SOC_ES8311=n
  - CONFIG_SND_SOC_RT1320_SDW=m
  - CONFIG_SND_SOC_WCD937X_SDW=n
  - LED Support
  - CONFIG_LEDS_CROS_EC=m
  - CONFIG_LEDS_SPI_BYTE=m
  - CONFIG_LEDS_KTD202X=m
  - CONFIG_LEDS_TRIGGER_INPUT_EVENTS=m
  - vDPA drivers
  - CONFIG_OCTEONEP_VDPA=m
  - CONFIG_CZNIC_PLATFORMS=y
  - CONFIG_CZNIC_PLATFORMS=y
  - X86 Platform Specific Device Drivers
  - CONFIG_DELL_PC=m
  - CONFIG_INTEL_PLR_TPMI=m
  - Industrial I/O support
  - CONFIG_AD7380=n
  - CONFIG_TI_ADS1119=n
  - CONFIG_ENS160=n
  - CONFIG_VEML6040=n
  - Misc drivers
  - CONFIG_SPI_CH341=n
  - CONFIG_POWER_SEQUENCING_QCOM_WCN=m
  - CONFIG_QCOM_PD_MAPPER=m
  - CONFIG_PWM_GPIO=m
  - CONFIG_LAN966X_OIC=m
  - OF dependent (i386, ppc64le, riscv64)
  - MFD_88PM886_PMIC=n
  - MFD_ROHM_BD96801=n
  - VIDEO_VGXY61=m
  - VIDEO_MAX96714=m
  - VIDEO_MAX96717=m
  - DRM_PANEL_HIMAX_HX83102=n
  - DRM_PANEL_ILITEK_ILI9806E=n
  - DRM_PANEL_LINCOLNTECH_LCD197=n
  - LEDS_LP5569=m
  - LEDS_SY7802=m
  - ppc64le
  - CRYPTO_CURVE25519_PPC64=m
  - riscv64
  - RISCV_ISA_ZAWRS=y
  - RISCV_ISA_ZBA=y
  - RISCV_ISA_ZBC=y
  - RISCV_ISA_VENDOR_EXT_ANDES=y
  - DMI=y
  - MEMORY_HOTPLUG=y
  - MEMORY_HOTPLUG_DEFAULT_ONLINE=n
  - MEMORY_HOTREMOVE=y
  - ZONE_DEVICE=y
  - DEVICE_PRIVATE=y
  - PCI_P2PDMA=y
  - PCIE_STARFIVE_HOST=m
  - CXL_ACPI=m
  - STARFIVE_STARLINK_CACHE=y
  - DMIID=y
  - DMI_SYSFS=m
  - EFI_SOFT_RESERVE=y
  - RTSN=m
  - VIDEO_E5010_JPEG_ENC=m
  - VIDEO_RASPBERRYPI_PISP_BE=m
  - DRM_NOUVEAU_SVM=y
  - VIRTIO_MEM=m
  - CLK_SOPHGO_SG2042_PLL=m
  - CLK_SOPHGO_SG2042_CLKGEN=m
  - CLK_SOPHGO_SG2042_CLKGEN=m
  - CLK_THEAD_TH1520_AP=y
  - PHY_STARFIVE_JH7110_DPHY_TX=m
  - NVDIMM_PFN=y
  - NVDIMM_DAX=y
  - DEV_DAX_PMEM=m
  - DEV_DAX_HMEM=m
  - DEV_DAX_KMEM=m
  - FS_DAX=y
  - FUSE_DAX=y
  - GCC_PLUGIN_STACKLEAK=n
  - MEMORY_NOTIFIER_ERROR_INJECT=m
  - TEST_HMM=n
  - ACPI_HOTPLUG_MEMORY=y
  - */debug
  - XFS_DEBUG_EXPENSIVE=n
- commit c7e21a2
* Thu Jul 25 2024 jslaby@suse.cz
- drm/amd/display: Take Synaptics Cascaded Topology into Account
  (bsc#1228093 #3495).
- commit a4c3703
* Thu Jul 25 2024 jslaby@suse.cz
- Linux 6.10.1 (bsc#1012628).
- thermal: core: Allow thermal zones to tell the core to ignore
  them (bsc#1012628).
- io_uring: fix error pbuf checking (bsc#1012628).
- ASoC: cs35l56: Limit Speaker Volume to +12dB maximum
  (bsc#1012628).
- ASoC: cs35l56: Use header defines for Speaker Volume control
  definition (bsc#1012628).
- tpm: Use auth only after NULL check in
  tpm_buf_check_hmac_response() (bsc#1012628).
- cifs: Fix setting of zero_point after DIO write (bsc#1012628).
- cifs: Fix server re-repick on subrequest retry (bsc#1012628).
- cifs: fix noisy message on copy_file_range (bsc#1012628).
- cifs: Fix missing fscache invalidation (bsc#1012628).
- cifs: Fix missing error code set (bsc#1012628).
- ext4: use memtostr_pad() for s_volume_name (bsc#1012628).
- commit a57275a
* Mon Jul 15 2024 mkubecek@suse.cz
- update to 6.10 final
- refresh configs (headers only)
- commit b8b0277
* Wed Jul 10 2024 mkubecek@suse.cz
- config: update arm configs
- arm64 and armv7hl
  - DRM_MSM_VALIDATE_XML=n ("unsure")
- commit 92abc10
* Tue Jul  9 2024 msuchanek@suse.de
- kernel-binary: vdso: Own module_dir
- commit ff69986
* Tue Jul  9 2024 svarbanov@suse.de
- config: update and reenable armv6hl configs
  Option values mirrored from armv7hl
- commit c5191d9
* Tue Jul  9 2024 svarbanov@suse.de
- config: update and reenable armv7hl configs
  Option values from arm64 and x86.
- commit 3e8ca13
* Mon Jul  8 2024 svarbanov@suse.de
- config: update and reenable arm64 configs
  Options mirrored from x86_64, except:
  +CONFIG_SCHED_HW_PRESSURE=y
  +CONFIG_ARCH_AIROHA=y
  +CONFIG_ARM64_WORKAROUND_SPECULATIVE_SSBS=y
  +CONFIG_ARM64_ERRATUM_3194386=y
  +CONFIG_ARM64_ERRATUM_3312417=y
  +CONFIG_ARCH_WANTS_EXECMEM_LATE=y
  +CONFIG_STM32_FIREWALL=y
  +CONFIG_SPI_AIROHA_SNFI=m
  +CONFIG_PINCTRL_SCMI=m
  +CONFIG_GPIO_SWNODE_UNDEFINED=y
  +CONFIG_GPIO_EN7523=m
  +CONFIG_REGULATOR_SUN20I=m
  +CONFIG_VIDEO_BCM2835_UNICAM=m
  +CONFIG_DRM_DISPLAY_DP_AUX_BUS=m
  +CONFIG_DRM_PANEL_LG_SW43408=m
  +CONFIG_DRM_PANEL_RAYDIUM_RM69380=m
  +CONFIG_DRM_PANEL_SAMSUNG_S6E3FA7=m
  +CONFIG_DRM_PANTHOR=m
  +CONFIG_SND_SOC_MT8186_MT6366=m
  +CONFIG_SND_SOC_RK3308=m
  +CONFIG_USB_ONBOARD_DEV=m
  +CONFIG_ARM64_PLATFORM_DEVICES=y
  +CONFIG_EC_ACER_ASPIRE1=m
  +CONFIG_COMMON_CLK_EN7523=y
  +CONFIG_CLK_IMX95_BLK_CTL=m
  +CONFIG_COMMON_CLK_MESON_VCLK=y
  +CONFIG_COMMON_CLK_STM32MP257=y
  +CONFIG_ARM_MHU_V3=m
  +CONFIG_ARCH_R9A09G057=y
  +CONFIG_AD7173=m
  +CONFIG_AD7944=m
  +CONFIG_AD9739A=m
  +CONFIG_ADI_AXI_DAC=m
  +CONFIG_APDS9306=m
  +CONFIG_STM32_EXTI=y
  +CONFIG_PHY_FSL_SAMSUNG_HDMI_PHY=m
  +CONFIG_PHY_ROCKCHIP_USBDP=m
  +CONFIG_ARM_TSTEE=m
  +CONFIG_TRUSTED_KEYS_DCP=y
  +CONFIG_CRYPTO_DEV_TEGRA=m
- commit aacb786
* Mon Jul  8 2024 mkubecek@suse.cz
- update to 6.10-rc7
- refresh
  - patches.suse/drivers-firmware-skip-simpledrm-if-nvidia-drm.modese.patch
- commit 45f4681
* Mon Jul  1 2024 mkubecek@suse.cz
- update to 6.10-rc6
- commit 3c2a141
* Sun Jun 23 2024 mkubecek@suse.cz
- update to 6.10-rc5
- refresh configs
- commit 0c5f39a
* Sun Jun 16 2024 mkubecek@suse.cz
- update to 6.10-rc4
- update configs
  - SERIAL_SC16IS7XX_CORE renamed to SERIAL_SC16IS7XX
- commit 3306b36
* Thu Jun 13 2024 fvogt@suse.de
- rpm/kernel-obs-build.spec.in: Add iso9660 (bsc#1226212)
  Some builds don't just create an iso9660 image, but also mount it during
  build.
- commit aaee141
* Wed Jun 12 2024 fvogt@suse.de
- rpm/kernel-obs-build.spec.in: Add networking modules for docker
  (bsc#1226211)
  docker needs more networking modules, even legacy iptable_nat and _filter.
- commit 415e132
* Sun Jun  9 2024 mkubecek@suse.cz
- update to 6.10-rc3
- drop 1 mainline patch
  - patches.suse/scsi-core-alua-I-O-errors-for-ALUA-state-transitions.patch
- commit 751e4fb
* Mon Jun  3 2024 mkubecek@suse.cz
- update to 6.10-rc2
- commit 068a181
* Thu May 30 2024 mkubecek@suse.cz
- update to 6.10-rc1
- drop 11 patches (5 mainline, 6 stable)
  - patches.kernel.org/*
  - patches.suse/ACPI-video-Add-backlight-native-quirk-for-Lenovo-Sli.patch
  - patches.suse/btrfs-re-introduce-norecovery-mount-option.patch
  - patches.suse/bus-mhi-host-add-mhi_power_down_no_destroy.patch
  - patches.suse/net-qrtr-support-suspend-hibernation.patch
  - patches.suse/wifi-ath11k-support-hibernation.patch
- refresh
  - patches.rpmify/Add-ksym-provides-tool.patch
  - patches.suse/btrfs-provide-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - General setup
  - BASE_SMALL=n
  - Processor type and features
  - X86_POSTED_MSI=n
  - Virtualization
  - KVM_INTEL_PROVE_VE=n
  - Networking support
  - SMC_LO=n
  - BT_INTEL_PCIE=m
  - File systems
  - EROFS_FS_ZIP_ZSTD=y
  - Security options
  - INIT_MLOCKED_ON_FREE_DEFAULT_ON=n
  - Kernel hacking
  - FTRACE_VALIDATE_RCU_IS_WATCHING=n
  - Network device support
  - PFCP=m
  - AIR_EN8811H_PHY=m
  - PSE_PD692X0=m
  - PSE_TPS23881=m
  - RTW88_8723CS=m
  - RTW89_8922AE=m
  - Hardware Monitoring support
  - SENSORS_LENOVO_EC=m
  - SENSORS_ADP1050=m
  - SENSORS_XDP710=m
  - SENSORS_PWM_FAN=m
  - Graphics support
  - DRM_DISPLAY_DP_AUX_CEC=y
  - DRM_DISPLAY_DP_AUX_CHARDEV=y
  - DRM_WERROR=n
  - Sound card support
  - SND_SOC_AMD_ACP63_TOPLEVEL=m
  - SND_SOC_PCM6240=n
  - X86 Platform Specific Device Drivers
  - YT2_1380=m
  - AMD_MP2_STB=y
  - DELL_UART_BACKLIGHT=m
  - ACPI_QUICKSTART=m
  - MEEGOPAD_ANX7428=m
  - MSI_WMI_PLATFORM=m
  - LENOVO_WMI_CAMERA=m
  - Industrial I/O support
  - AD7173=n
  - AD7944=n
  - AD9739A=n
  - ADI_AXI_DAC=n
  - APDS9306=n
  - Misc drivers
  - TCG_TPM2_HMAC=y
  - I2C_ZHAOXIN=m
  - GPIO_GRANITERAPIDS=m
  - LENOVO_SE10_WDT=m
  - VIDEO_INTEL_IPU6=m
  - HID_WINWING=m
  - RTC_DRV_RX8111=m
  - QAT_VFIO_PCI=m
  - VIRTIO_DEBUG=n
  - FPGA_MGR_XILINX_SELECTMAP=m
  - OF dependent (i386, ppc64le, riscv64)
  - DRM_PANEL_LG_SW43408=n
  - DRM_PANEL_RAYDIUM_RM69380=n
  - DRM_PANEL_SAMSUNG_S6E3FA7=n
  - USB_ONBOARD_DEV=m
  - i386
  - ARM_MHU_V3=m
  - i386/default
  - NET_SB1000=n
  - CAN_SJA1000_ISA=n
  - ppc64le
  - CRASH_HOTPLUG=y
  - CRASH_MAX_MEMORY_RANGES=8192 (default)
  - SERIAL_SC16IS7XX_CORE=n
  - VMGENID=y
  - SOFTLOCKUP_DETECTOR_INTR_STORM=y
  - TEST_FPU=n
  - s390x
  - KERNEL_IMAGE_BASE=0x3FFE0000000 (default)
  - AP=y
  - AP_DEBUG=n
  - HAMRADIO=n
  - SERIAL_SC16IS7XX_CORE=n
  - VMGENID=y
  - s390x/zfcpdump
  - BPF_JIT=n
  - KPROBES=n
  - MEM_ALLOC_PROFILING=n
  - TEST_BITOPS=n
  - riscv64
  - KERNEL_GZIP=y
  - ARCH_MICROCHIP=y
  - I2C_CADENCE=m
  - REGULATOR_SUN20I=m
  - DRM_AMD_SECURE_DISPLAY=n
  - CLK_SOPHGO_CV1800=m
  - ARM_MHU_V3=m
  - TEST_FPU=n
- commit 6be9abf
* Wed May 29 2024 colyli@suse.de
- Update config files to enable CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG (bsc#1223544)
- commit 1b34643
* Mon May 27 2024 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section:
  - patches.suse/btrfs-re-introduce-norecovery-mount-option.patch
- commit a9b6c1b
* Sun May 26 2024 tiwai@suse.de
- Workaround for amdgpu hard freeze (bsc#1225147).
- commit b14bc87
* Thu May 23 2024 mwilck@suse.com
- scsi: core: alua: I/O errors for ALUA state transitions
  (bsc#1189970).
- commit 030909a
* Thu May 23 2024 mwilck@suse.com
- Delete patches.suse/scsi-retry-alua-transition-in-progress. (bsc#1189970)
- commit ead9897
* Thu May 23 2024 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and resort:
  - patches.suse/ACPI-video-Add-backlight-native-quirk-for-Lenovo-Sli.patch
  - patches.suse/bus-mhi-host-add-mhi_power_down_no_destroy.patch
  - patches.suse/net-qrtr-support-suspend-hibernation.patch
  - patches.suse/wifi-ath11k-support-hibernation.patch
- commit c7821e3
* Tue May 21 2024 tiwai@suse.de
- drm/nouveau/disp: Fix missing backlight control on Macbook 5,1 (bsc#1223838).
- commit db10868
* Tue May 21 2024 jslaby@suse.cz
- btrfs: re-introduce 'norecovery' mount option (bsc#1222429).
- commit e5b30a1
* Tue May 21 2024 jslaby@suse.cz
- rpm/kernel-obs-build.spec.in: remove reiserfs from OBS initrd
  We disabled the FS in bug 1202309. And we actively blacklist it in:
  /usr/lib/modprobe.d/60-blacklist_fs-reiserfs.conf
  This, as a side-effect, fixes obs-build's warning:
  dracut-pre-udev[1463]: sh: line 1: /usr/lib/module-init-tools/unblacklist: No such file or directory
  Exactly due to the above 60-blacklist_fs-reiserfs.conf trying to call the
  above unblacklist.
  We should likely drop ext2+ext3 from the list too, as we don't build
  them at all. But that's a different story.
- commit 9e1a078
* Tue May 21 2024 jslaby@suse.cz
- Linux 6.9.1 (bsc#1012628).
- wifi: mt76: mt7915: add missing chanctx ops (bsc#1012628).
- keys: Fix overwrite of key expiration on instantiation
  (bsc#1012628).
- dmaengine: idxd: add a write() method for applications to
  submit work (bsc#1012628).
- dmaengine: idxd: add a new security check to deal with a
  hardware erratum (bsc#1012628).
- VFIO: Add the SPR_DSA and SPR_IAX devices to the denylist
  (bsc#1012628).
- commit 6d0f67e
* Tue May 14 2024 jslaby@suse.cz
- Revert "Update config files (boo#1224053)."
  This reverts commit 59423a933cb917b60a84fa090a2804997c95e450.
  See boo#1224053:
  Michal, please revert this patch. You've just disabled the kernel
  console entirely.
- commit 553f7b7
* Tue May 14 2024 jslaby@suse.cz
- ACPI: video: Add backlight=native quirk for Lenovo Slim 7 16ARH7
  (bsc#1217750).
- commit 760002e
* Tue May 14 2024 jslaby@suse.cz
- bus: mhi: host: Add mhi_power_down_keep_dev() API to support
  system suspend/hibernation (bsc#1207948).
- Refresh patches.suse/net-qrtr-support-suspend-hibernation.patch.
- Refresh patches.suse/wifi-ath11k-support-hibernation.patch.
  Update to upstream versions (v7):
  https://lore.kernel.org/all/20240305021320.3367-1-quic_bqiang@quicinc.com/
  And move to sorted section.
- commit 9e598bf
* Mon May 13 2024 msuchanek@suse.de
- Update config files (boo#1224053).
  DRM_FBDEV_EMULATION=n
- commit 59423a9
* Sun May 12 2024 mkubecek@suse.cz
- update to 6.9 final
- refresh configs
- commit e4714c6
* Fri May 10 2024 msuchanek@suse.de
- Update ppc64le config files (bsc#1223982).
  drop support for agpgart, there is no driver enabled
  drop extcon support, it is not used
  drop support for pinctrl drivers, these are not used
  drop support for i2c leds, timers, multiplexors, watchdogs, sensors, displays, HID - these are not used
  drop support for platform-specific DMA found on other platforms
  drop support for Freescale USB controller, it's not used
  drop support for DSA, it's not used
  drop regulater support, there are no regulators exposed
  drop support for random SoC bits, we do not support SoCs
  drop support for Intel QAT
  drop support for PATA
- commit 92e64cf
* Thu May  9 2024 schwab@suse.de
- config: riscv64: SERIAL_DEV_BUS=y
  This is needed for BT_HCIUART_BCM.
- commit 25b9325
* Sun May  5 2024 mkubecek@suse.cz
- update to 6.9-rc7
- update configs
  - DRM_PANEL_ILITEK_ILI9341=n (x86_64)
- commit df64d6f
* Sun Apr 28 2024 mkubecek@suse.cz
- update to 6.9-rc6
- update configs
  - CPU_MITIGATIONS=y (x86)
  - NTFS_FS=m (except s390x/zfcpdump)
  - ERRATA_THEAD_MAE=y (riscv64)
- commit 5967f99
* Sun Apr 21 2024 mkubecek@suse.cz
- update to 6.9-rc5
- eliminate 1 patch
  - patches.suse/Workaround-broken-chacha-crypto-fallback.patch (69630926011c)
- commit 7ee1174
* Fri Apr 19 2024 jslaby@suse.cz
- Update config files. Disable N_GSM (bsc#1223134).
- commit bbf9614
* Wed Apr 17 2024 macpaul.lin@mediatek.com
- Update config files: re-enable arm64 regulator modules for MediaTek boards (bsc#1222818).
  This re-enable some regulator modules, pinctrl and RTC drivers for
  MediaTek boards which has been disabled when merging config file from
  master to stable (kernel 6.5.9->6.6) branch.
  This re-applies commit b197b3604a7b (Update config files: enable arm64
  regulator modules for MediaTek boards.)
  [js] set also KEYBOARD_MTK_PMIC=m, POWER_RESET_MT6323=n, LEDS_MT6323=n,
    and MFD_MT6397=m -- the same as commit b197b3604a7b.
- commit d11a210
* Mon Apr 15 2024 duwe@suse.de
- Update arm* configs to 6.9-rc4. Mostly new SoC and component support enabled as modules.
- Re-enable arm in config.conf
- commit 4804f5c
* Sun Apr 14 2024 mkubecek@suse.cz
- update to 6.9-rc4
- update configs
  - MITIGATION_SPECTRE_BHI=y (x86 only)
- commit 750564f
* Sun Apr  7 2024 mkubecek@suse.cz
- update to 6.9-rc3
- commit 761535f
* Fri Apr  5 2024 tiwai@suse.de
- Input: psmouse: add NULL check to psmouse_from_serio()
  (bsc#1219522).
- commit 2e2b394
* Mon Apr  1 2024 mkubecek@suse.cz
- update to 6.9-rc2
- refresh
  - patches.suse/0003-efi-Lock-down-the-kernel-if-booted-in-secure-boot-mode.patch
- update configs
- commit 0788112
* Thu Mar 28 2024 msuchanek@suse.de
- powerpc/crypto/chacha-p10: Fix failure on non Power10
  (boo#1218114).
- commit 47aaf44
* Mon Mar 25 2024 mkubecek@suse.cz
- update to 6.9-rc1
- drop 19 patches (14 mainline, 5 stable)
  - patches.kernel.org/*
  - patches.suse/Bluetooth-btmtk-Add-MODULE_FIRMWARE-for-MT7922.patch
  - patches.suse/btrfs-fix-race-when-detecting-delalloc-ranges-during.patch
  - patches.suse/iwlwifi-cfg-Add-missing-MODULE_FIRMWARE-for-pnvm.patch
  - patches.suse/net-mdio-add-2.5g-and-5g-related-PMA-speed-constants.patch
  - patches.suse/net-phy-realtek-add-5Gbps-support-to-rtl822x_config_.patch
  - patches.suse/net-phy-realtek-add-support-for-RTL8126A-integrated-.patch
  - patches.suse/net-phy-realtek-use-generic-MDIO-constants.patch
  - patches.suse/r8169-add-support-for-RTL8126A.patch
  - patches.suse/wifi-ath11k-do-not-dump-SRNG-statistics-during-resum.patch
  - patches.suse/wifi-ath11k-fix-warning-on-DMA-ring-capabilities-eve.patch
  - patches.suse/wifi-ath11k-rearrange-IRQ-enable-disable-in-reset-pa.patch
  - patches.suse/wifi-ath11k-remove-MHI-LOOPBACK-channels.patch
  - patches.suse/wifi-ath11k-thermal-don-t-try-to-register-multiple-t.patch
  - patches.suse/wifi-brcmfmac-Fix-use-after-free-bug-in-brcmf_cfg802.patch
- refresh
  - patches.suse/0001-security-lockdown-expose-a-hook-to-lock-the-kernel-down.patch
  - patches.suse/Restore-kABI-for-NVidia-vGPU-driver.patch
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/bus-mhi-host-add-mhi_power_down_no_destroy.patch
  - patches.suse/drivers-firmware-skip-simpledrm-if-nvidia-drm.modese.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - Processor type and features
  - X86_FRED=y
  - Mitigations for speculative execution vulnerabilities
  - MITIGATION_PAGE_TABLE_ISOLATION=y
  - MITIGATION_RETPOLINE=y
  - MITIGATION_RETHUNK=y
  - MITIGATION_UNRET_ENTRY=y
  - MITIGATION_CALL_DEPTH_TRACKING=y
  - MITIGATION_IBPB_ENTRY=y
  - MITIGATION_IBRS_ENTRY=y
  - MITIGATION_SRSO=y
  - MITIGATION_SLS=y
  - MITIGATION_GDS_FORCE=n
  - Power management and ACPI options
  - HIBERNATION_COMP_LZO=y
  - HIBERNATION_COMP_LZ4=n
  - General architecture-dependent options
  - PAGE_SIZE_4KB=y
  - File systems
  - FUSE_PASSTHROUGH=y
  - Cryptographic API
  - CRYPTO_DEV_QAT_ERROR_INJECTION=n
  - Network device support
  - OCTEON_EP_VF=m
  - QCA83XX_PHY=m
  - QCA808X_PHY=m
  - CAN_ESD_402_PCI=m
  - Input device support
  - TOUCHSCREEN_GOODIX_BERLIN_I2C=m
  - TOUCHSCREEN_GOODIX_BERLIN_SPI=m
  - Hardware Monitoring support
  - SENSORS_ASUS_ROG_RYUJIN=m
  - SENSORS_CHIPCAP2=m
  - SENSORS_LTC4282=m
  - SENSORS_NZXT_KRAKEN3=m
  - SENSORS_MPQ8785=m
  - SENSORS_PT5161L=m
  - SENSORS_SURFACE_FAN=m
  - Graphics support
  - MAX6959=n
  - SEG_LED_GPIO=n
  - DRM_I915_DP_TUNNEL=y
  - BACKLIGHT_KTD2801=m
  - Sound card support
  - SND_SOC_AMD_SOUNDWIRE=m
  - SND_SOC_SOF_AMD_SOUNDWIRE=m
  - SND_SOC_WCD939X_SDW=n
  - USB support
  - USB_DEFAULT_AUTHORIZATION_MODE=1
  - TYPEC_MUX_IT5205=m
  - Industrial I/O support
  - AD9467=n
  - ADI_AXI_ADC=n
  - PAC1934=n
  - TI_ADS1298=n
  - ADMFM2000=n
  - Reliability, Availability and Serviceability (RAS) features
  - AMD_ATL=m
  - RAS_FMPM=m
  - Misc drivers
  - MTD_UBI_NVMEM=m
  - DM_VDO=m
  - PTP_1588_CLOCK_FC3W=m
  - GPIO_CROS_EC=m
  - W1_MASTER_UART=m
  - CROS_EC_WATCHDOG=m
  - QCOM_PBS=m
  - RESET_GPIO=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - DRM_PANEL_BOE_TH101MB31UIG002_28A=n
  - DRM_PANEL_HIMAX_HX83112A=n
  - DRM_PANEL_NOVATEK_NT36672E=n
  - LEDS_NCP5623=m
  - i386
  - QCA807X_PHY=m
  - PINCTRL_AW9523=m
  - DRM_XE=m
  - DRM_XE_* copied from x86_64
  - SND_SOC_FRAMER=m
  - AF8133J=n
  - ppc64le
  - NET_DSA_REALTEK_MDIO=y
  - NET_DSA_REALTEK_SMI=y
  - QCA807X_PHY=m
  - PINCTRL_AW9523=m
  - s390x
  - DRM_DEBUG_MM=n
  - DEBUG_VIRTUAL=n
  - riscv64
  - RISCV_PROBE_UNALIGNED_ACCESS=y
  - HIBERNATION=y
  - HIBERNATION_SNAPSHOT_DEV=y
  - PM_STD_PARTITION=""
  - ACPI_CPPC_CPUFREQ=m
  - ACPI_CPPC_CPUFREQ_FIE=y
  - ACPI_PROCESSOR=y
  - ACPI_THERMAL=m
  - RANDOMIZE_KSTACK_OFFSET=y
  - RANDOMIZE_KSTACK_OFFSET_DEFAULT=y
  - NET_DSA_REALTEK_MDIO=y
  - NET_DSA_REALTEK_SMI=y
  - SND_SOC_FRAMER=m
  - MMC_DW_HI3798MV200=m
  - AF8133J=n
  - STARFIVE_JH8100_INTC=y
  - STARFIVE_STARLINK_PMU=y
  - ANDES_CUSTOM_PMU=y
  - CRYPTO_*_RISCV64=m
- commit ffd2471
* Thu Mar 21 2024 msuchanek@suse.de
- Workaround broken chacha crypto fallback (boo#1218114).
- commit 0ace635
* Mon Mar 18 2024 jslaby@suse.cz
- Linux 6.8.1 (bsc#1012628).
- Rename to
  patches.kernel.org/6.8.1-001-x86-mmio-Disable-KVM-mitigation-when-X86_FEATUR.patch.
- Rename to
  patches.kernel.org/6.8.1-002-Documentation-hw-vuln-Add-documentation-for-RFD.patch.
- Rename to
  patches.kernel.org/6.8.1-003-x86-rfds-Mitigate-Register-File-Data-Sampling-R.patch.
- Rename to
  patches.kernel.org/6.8.1-004-KVM-x86-Export-RFDS_NO-and-RFDS_CLEAR-to-guests.patch.
- commit 74a8025
* Thu Mar 14 2024 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and move into sorted section:
  - patches.suse/iwlwifi-cfg-Add-missing-MODULE_FIRMWARE-for-pnvm.patch
  - patches.suse/wifi-ath11k-do-not-dump-SRNG-statistics-during-resum.patch
  - patches.suse/wifi-ath11k-fix-warning-on-DMA-ring-capabilities-eve.patch
  - patches.suse/wifi-ath11k-rearrange-IRQ-enable-disable-in-reset-pa.patch
  - patches.suse/wifi-ath11k-remove-MHI-LOOPBACK-channels.patch
  - patches.suse/wifi-ath11k-thermal-don-t-try-to-register-multiple-t.patch
- commit 96ac51b
* Thu Mar 14 2024 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and resort:
  - patches.suse/Bluetooth-btmtk-Add-MODULE_FIRMWARE-for-MT7922.patch
  - patches.suse/net-mdio-add-2.5g-and-5g-related-PMA-speed-constants.patch
  - patches.suse/net-phy-realtek-add-5Gbps-support-to-rtl822x_config_.patch
  - patches.suse/net-phy-realtek-add-support-for-RTL8126A-integrated-.patch
  - patches.suse/net-phy-realtek-use-generic-MDIO-constants.patch
  - patches.suse/r8169-add-support-for-RTL8126A.patch
  - patches.suse/wifi-brcmfmac-Fix-use-after-free-bug-in-brcmf_cfg802.patch
- commit 63b2803
* Wed Mar 13 2024 mkubecek@suse.cz
- series.conf: cleanup
- update upstream status and move to sorted section:
  - patches.suse/btrfs-fix-race-when-detecting-delalloc-ranges-during.patch
- commit e863123
* Wed Mar 13 2024 jslaby@suse.cz
- KVM/x86: Export RFDS_NO and RFDS_CLEAR to guests (bsc#1213456
  CVE-2023-28746).
- x86/rfds: Mitigate Register File Data Sampling (RFDS)
  (bsc#1213456 CVE-2023-28746).
- Update config files. Set MITIGATION_RFDS=y.
- Documentation/hw-vuln: Add documentation for RFDS (bsc#1213456
  CVE-2023-28746).
- x86/mmio: Disable KVM mitigation when X86_FEATURE_CLEAR_CPU_BUF
  is set (bsc#1213456 CVE-2023-28746).
- commit d8d0d20
* Tue Mar 12 2024 jslaby@suse.cz
- btrfs: fix race when detecting delalloc ranges during fiemap
  (btrfs-fix).
- commit 5e23030
* Mon Mar 11 2024 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and move into sorted section:
  - patches.suse/wifi-brcmfmac-Fix-use-after-free-bug-in-brcmf_cfg802.patch
  - patches.suse/net-phy-realtek-add-support-for-RTL8126A-integrated-.patch
  - patches.suse/r8169-add-support-for-RTL8126A.patch
  - patches.suse/net-mdio-add-2.5g-and-5g-related-PMA-speed-constants.patch
  - patches.suse/net-phy-realtek-use-generic-MDIO-constants.patch
  - patches.suse/net-phy-realtek-add-5Gbps-support-to-rtl822x_config_.patch
  - patches.suse/Bluetooth-btmtk-Add-MODULE_FIRMWARE-for-MT7922.patch
- commit 002260c
* Mon Mar 11 2024 jslaby@suse.cz
- rpm/mkspec-dtb: resolve packaging conflicts better
  The merge commit ad1679b2612f left both %%ifs in place. Remove the one
  which d26c540d7eed was removing originally.
  This fixes errors like:
  dtb-armv7l.spec : error: line 1442: Unclosed %%if
  The commit also removed SUBPKG_CASE. Reintroduce it, otherwise we see
  shell garbage in the description
- commit e4b3d06
* Sun Mar 10 2024 mkubecek@suse.cz
- Update to 6.8 final
- update configs
- commit a551d7b
* Sun Mar 10 2024 mkubecek@suse.cz
- config: update and reenable armv6hl configs
- option values mirrored from armv7hl
- commit be3b67b
* Sun Mar 10 2024 mkubecek@suse.cz
- config: update and reenable armv7hl configs
- option values mirrored from arm64 or other architectures
- commit 336405e
* Sun Mar 10 2024 mkubecek@suse.cz
- config: update and reenable arm64 configs
- most options mirrored from other architectures except
  - ARM64_ERRATUM_3117295=y
  - TEE_STMM_EFI=m
  - PINCTRL_SM4450=m
  - PINCTRL_SM8650=m
  - PINCTRL_X1E80100=m
  - PINCTRL_SM8650_LPASS_LPI=m
  - GPIO_NPCM_SGPIO=y
  - GPIO_RTD=m
  - VIDEO_STM32_DCMIPP=m
  - DRM_POWERVR=m
  - SND_SOC_X1E80100=m
  - RTC_DRV_MA35D1=m
  - COMMON_CLK_MT7988=m
  - CLK_X1E80100_GCC=m
  - SC_CAMCC_8280XP=m
  - QDU_ECPRICC_1000=m
  - SM_DISPCC_8650=m
  - SM_GCC_8650=m
  - SM_GPUCC_8650=m
  - SM_TCSRCC_8650=m
  - COMMON_CLK_STM32MP=y
  - INTERCONNECT_QCOM_SM6115=m
  - INTERCONNECT_QCOM_SM8650=m
  - INTERCONNECT_QCOM_X1E80100=m
  - KASAN_EXTRA_INFO=n (arm64/debug only)
- commit 99c97ec
* Thu Mar  7 2024 msuchanek@suse.de
- group-source-files.pl: Quote filenames (boo#1221077).
  The kernel source now contains a file with a space in the name.
  Add quotes in group-source-files.pl to avoid splitting the filename.
  Also use -print0 / -0 when updating timestamps.
- commit a005e42
* Wed Mar  6 2024 msuchanek@suse.de
- kernel-binary: Fix i386 build
  Fixes: 89eaf4cdce05 ("rpm templates: Move macro definitions below buildrequires")
- commit f7c6351
* Wed Mar  6 2024 msuchanek@suse.de
- kernel-binary: vdso: fix filelist for non-usrmerged kernel
  Fixes: a6ad8af207e6 ("rpm templates: Always define usrmerged")
- commit fb3f221
* Mon Mar  4 2024 petr.pavlu@suse.com
- doc/README.SUSE: Update information about module support status
  (jsc#PED-5759)
  Following the code change in SLE15-SP6 to have externally supported
  modules no longer taint the kernel, update the respective documentation
  in README.SUSE:
  * Describe that support status can be obtained at runtime for each
  module from /sys/module/$MODULE/supported and for the entire system
  from /sys/kernel/supported. This provides a way how to now check that
  the kernel has any externally supported modules loaded.
  * Remove a mention that externally supported modules taint the kernel,
  but keep the information about bit 16 (X) and add a note that it is
  still tracked per module and can be read from
  /sys/module/$MODULE/taint. This per-module information also appears in
  Oopses.
- commit 9ed8107
* Mon Mar  4 2024 tiwai@suse.de
- Bluetooth: btmtk: Add MODULE_FIRMWARE() for MT7922
  (bsc#1214133).
- commit 8b861a8
* Sun Mar  3 2024 mkubecek@suse.cz
- Update to 6.8-rc7
- eliminate 1 mainline patch
  - patches.rpmify/net-ethernet-adi-move-PHYLIB-from-vendor-to-driver-s.patch (943d4bd67950)
- update riscv64 configs
  - RISCV_ISA_V=y
  - RISCV_ISA_V_DEFAULT_ENABLE=y
  - RISCV_ISA_V_UCOPY_THRESHOLD=768
  - RISCV_ISA_V_PREEMPTIVE=y
  - RISCV_ISA_ZBB=y
- commit ed0a227
* Tue Feb 27 2024 tiwai@suse.de
- Update ath11k hibernation patches for v2 series (bsc#1207948)
- commit 6668923
* Mon Feb 26 2024 tiwai@suse.de
- wifi: ath11k: support hibernation (bsc#1207948).
- net: qrtr: support suspend/hibernation (bsc#1207948).
- bus: mhi: host: add mhi_power_down_no_destroy() (bsc#1207948).
- commit 4021880
* Mon Feb 26 2024 tiwai@suse.de
- wifi: ath11k: thermal: don't try to register multiple times
  (bsc#1207948).
- wifi: ath11k: fix warning on DMA ring capabilities event
  (bsc#1207948).
- wifi: ath11k: do not dump SRNG statistics during resume
  (bsc#1207948).
- wifi: ath11k: remove MHI LOOPBACK channels (bsc#1207948).
- wifi: ath11k: rearrange IRQ enable/disable in reset path
  (bsc#1207948).
- commit 14ad705
* Mon Feb 26 2024 tiwai@suse.de
- Drop ath11k hibernation patches for refreshing to the new patch set (bsc#1207948)
- commit 6620772
* Mon Feb 26 2024 mkubecek@suse.cz
- net: ethernet: adi: move PHYLIB from vendor to driver symbol.
  Fix config dependencies.
- restore config options from before 6.8-rc6:
  - NET_VENDOR_ADI=y
  - ADIN1110=m
- commit 2aa849d
* Mon Feb 26 2024 mkubecek@suse.cz
- Update to 6.8-rc6
- update configs
  - DRM_NOUVEAU_GSP_DEFAULT=n
  - disable NET_VENDOR_ADI (mainline commit a9f80df4f514 would force many
    other config options to "Y")
- commit 0883557
* Thu Feb 22 2024 msuchanek@suse.de
- rpm templates: Always define usrmerged
  usrmerged is now defined in kernel-spec-macros and not the distribution.
  Only check if it's defined in kernel-spec-macros, not everywhere where
  it's used.
- commit a6ad8af
* Wed Feb 21 2024 msuchanek@suse.de
- rpm templates: Move macro definitions below buildrequires
  Many of the rpm macros defined in the kernel packages depend directly or
  indirectly on script execution. OBS cannot execute scripts which means
  values of these macros cannot be used in tags that are required for OBS
  to see such as package name, buildrequires or buildarch.
  Accumulate macro definitions that are not directly expanded by mkspec
  below buildrequires and buildarch to make this distinction clear.
- commit 89eaf4c
* Wed Feb 21 2024 jslaby@suse.cz
- rpm/check-for-config-changes: add GCC_ASM_GOTO_OUTPUT_WORKAROUND to IGNORED_CONFIGS_RE
  Introduced by commit 68fb3ca0e408 ("update workarounds for gcc "asm
  goto" issue").
- commit be1bdab
* Tue Feb 20 2024 mkubecek@suse.cz
- Update to 6.8-rc5
- update configs
  - HDC3020=n
- commit 9b37ede
* Mon Feb 19 2024 mkoutny@suse.com
- Update config files.
  Disable CONFIG_RT_GROUP_SCHED on all archs (bsc#950955 bsc#1153228).
- commit 4821c9f
* Mon Feb 19 2024 msuchanek@suse.de
- compute-PATCHVERSION: Do not produce output when awk fails
  compute-PATCHVERSION uses awk to produce a shell script that is
  subsequently executed to update shell variables which are then printed
  as the patchversion.
  Some versions of awk, most notably bysybox-gawk do not understand the
  awk program and fail to run. This results in no script generated as
  output, and printing the initial values of the shell variables as
  the patchversion.
  When the awk program fails to run produce 'exit 1' as the shell script
  to run instead. That prevents printing the stale values, generates no
  output, and generates invalid rpm spec file down the line. Then the
  problem is flagged early and should be easier to diagnose.
- commit 8ef8383
* Wed Feb 14 2024 msuchanek@suse.de
- kernel-binary: Move build script to the end
  All other spec templates have the build script at the end, only
  kernel-binary has it in the middle. Align with the other templates.
- commit 98cbdd0
* Wed Feb 14 2024 msuchanek@suse.de
- rpm templates: Aggregate subpackage descriptions
  While in some cases the package tags, description, scriptlets and
  filelist are located together in other cases they are all across the
  spec file. Aggregate the information related to a subpackage in one
  place.
- commit 8eeb08c
* Wed Feb 14 2024 msuchanek@suse.de
- rpm templates: sort rpm tags
  The rpm tags in kernel spec files are sorted at random.
  Make the order of rpm tags somewhat more consistent across rpm spec
  templates.
- commit 8875c35
* Mon Feb 12 2024 tiwai@suse.de
- Update config files: disable broken ATOMISP drivers (bsc#1210639)
  It's been broken over a year, better to disable it before hitting another victim
- commit aa68e1a
* Mon Feb 12 2024 vbabka@suse.cz
- Update config files. Enable CONFIG_READ_ONLY_THP_FOR_FS (bsc#1219593).
- commit 8f5ed7a
* Sun Feb 11 2024 mkubecek@suse.cz
- Update to 6.8-rc4
- commit 9b23bf2
* Sat Feb 10 2024 tiwai@suse.de
- net: phy: realtek: add 5Gbps support to rtl822x_config_aneg()
  (bsc#1217417).
- net: phy: realtek: use generic MDIO constants (bsc#1217417).
- net: mdio: add 2.5g and 5g related PMA speed constants
  (bsc#1217417).
- commit 5c78291
* Thu Feb  8 2024 msuchanek@suse.de
- kernel-binary: certs: Avoid trailing space
- commit bc7dc31
* Wed Feb  7 2024 jslaby@suse.cz
- rpm/kernel-binary.spec.in: install scripts/gdb when enabled in config
  (bsc#1219653)
  They are put into -devel subpackage. And a proper link to
  /usr/share/gdb/auto-load/ is created.
- commit 1dccf2a
* Tue Feb  6 2024 jslaby@suse.cz
- rpm/mkspec: sort entries in _multibuild
  Otherwise it creates unnecessary diffs when tar-up-ing. It's of course
  due to readdir() using "random" order as served by the underlying
  filesystem.
  See for example:
  https://build.opensuse.org/request/show/1144457/changes
- commit d1155de
* Mon Feb  5 2024 jslaby@suse.cz
- Refresh
  patches.suse/net-phy-realtek-add-support-for-RTL8126A-integrated-.patch.
- Refresh patches.suse/r8169-add-support-for-RTL8126A.patch.
- Refresh
  patches.suse/Bluetooth-btmtk-Add-MODULE_FIRMWARE-for-MT7922.patch.
  Update upstream statuses (all in maintainers repo now).
- commit 2dfb213
* Sun Feb  4 2024 mkubecek@suse.cz
- Update to 6.8-rc3
- eliminate 1 patch
  - patches.suse/mm-huge_memory-don-t-force-huge-page-alignment-on-32.patch
- refresh configs
- commit ae4495f
* Fri Feb  2 2024 mkubecek@suse.cz
- config: add missing USELIB=n to arm configs
  ARM configs were not refreshed properly after commit 077d05a10ddb ("Update
  config files: disable CONFIG_USELIB (bsc#1219222)") because they are
  disabled at the moment. Add missing lines for (now disabled) CONFIG_USELIB
  option.
- commit 3d7309c
* Fri Feb  2 2024 tiwai@suse.de
- net: phy: realtek: add support for RTL8126A-integrated 5Gbps
  PHY (bsc#1217417).
- r8169: add support for RTL8126A (bsc#1217417).
- commit 12eff81
* Fri Feb  2 2024 tiwai@suse.de
- Update config files: disable CONFIG_USELIB (bsc#1219222)
  It's only for the old libc5. Let's reduce the possible attack surfaces.
- commit 077d05a
* Wed Jan 31 2024 msuchanek@suse.de
- kernel-source: Fix description typo
- commit 8abff35
* Tue Jan 30 2024 tiwai@suse.de
- wifi: brcmfmac: Fix use-after-free bug in brcmf_cfg80211_detach
  (CVE-2023-47233 bsc#1216702).
- commit b9432ba
* Tue Jan 30 2024 jslaby@suse.cz
- rpm/constraints.in: set jobs for riscv to 8
  The same workers are used for x86 and riscv and the riscv builds take
  ages. So align the riscv jobs count to x86.
- commit b2c82b9
* Tue Jan 30 2024 jslaby@suse.cz
- Refresh
  patches.suse/mm-huge_memory-don-t-force-huge-page-alignment-on-32.patch.
  Update upstream status and move to sorted section.
- commit ab524e9
* Tue Jan 30 2024 jslaby@suse.cz
- Update config files. (bsc#1219328)
  Synchronize PSTORE_CONSOLE, PSTORE_PMSG, and PSTORE_FTRACE with
  SLE15-SP6.
- commit 116df61
* Mon Jan 29 2024 mkubecek@suse.cz
- Update to 6.8-rc2
- eliminate 1 patch
  - patches.suse/futex-Avoid-reusing-outdated-pi_state.patch (e626cb02ee83)
- refresh configs
- commit 023a12a
* Fri Jan 26 2024 msuchanek@suse.de
- mkspec: Use variant in constraints template
  Constraints are not applied consistently with kernel package variants.
  Add variant to the constraints template as appropriate, and expand it
  in mkspec.
- commit cc68ab9
* Fri Jan 26 2024 jslaby@suse.cz
- rpm/constraints.in: add static multibuild packages
  Commit 841012b049a5 (rpm/mkspec: use kernel-source: prefix for
  constraints on multibuild) added "kernel-source:" prefix to the
  dynamically generated kernels. But there are also static ones like
  kernel-docs. Those fail to build as the constraints are still not
  applied.
  So add the prefix also to the static ones.
  Note kernel-docs-rt is given kernel-source-rt prefix. I am not sure it
  will ever be multibuilt...
- commit c2e0681
* Thu Jan 25 2024 msuchanek@suse.de
- Revert "Limit kernel-source build to architectures for which the kernel binary"
  This reverts commit 08a9e44c00758b5f3f3b641830ab6affff041132.
  The fix for bsc#1108281 directly causes bsc#1218768, revert.
- commit 2943b8a
* Thu Jan 25 2024 msuchanek@suse.de
- mkspec: Include constraints for both multibuild and plain package always
  There is no need to check for multibuild flag, the constraints can be
  always generated for both cases.
- commit 308ea09
* Thu Jan 25 2024 jslaby@suse.cz
- rpm/mkspec: use kernel-source: prefix for constraints on multibuild
  Otherwise the constraints are not applied with multibuild enabled.
- commit 841012b
* Wed Jan 24 2024 jslaby@suse.cz
- rpm/kernel-source.rpmlintrc: add action-ebpf
  Upstream commit a79d8ba734bd (selftests: tc-testing: remove buildebpf
  plugin) added this precompiled binary blob. Adapt rpmlintrc for
  kernel-source.
- commit b5ccb33
* Tue Jan 23 2024 tiwai@suse.de
- scripts/tar-up.sh: don't add spurious entry from kernel-sources.changes.old
  The previous change added the manual entry from kernel-sources.change.old
  to old_changelog.txt unnecessarily.  Let's fix it.
- commit fb033e8
* Tue Jan 23 2024 jslaby@suse.cz
- rpm/kernel-docs.spec.in: fix build with 6.8
  Since upstream commit f061c9f7d058 (Documentation: Document each netlink
  family), the build needs python yaml.
- commit 6a7ece3
* Mon Jan 22 2024 mkubecek@suse.cz
- Update to 6.8-rc1
- drop 3 patches (all mainline)
  - patches.rpmify/media-solo6x10-replace-max-a-min-b-c-by-clamp-b-a-c.patch (31e97d7c9ae3)
  - patches.suse/0001-bsc-1204315-Disable-sysfb-before-creating-simple-fra.patch
  (3310288f6135)
  - patches.suse/keys-dns-Fix-size-check-of-V1-server-list-header.patch
- disable (conflict)
  - patches.suse/btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch
- refresh
  - patches.suse/0001-security-lockdown-expose-a-hook-to-lock-the-kernel-down.patch
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/btrfs-provide-super_operations-get_inode_dev
  - patches.suse/genksyms-add-override-flag.diff
  - patches.suse/vfs-add-super_operations-get_inode_dev
- fix patch metadata
  - patches.suse/btrfs-provide-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - Virtualization
  - CONFIG_KVM_SW_PROTECTED_VM=y
  - CONFIG_KVM_HYPERV=y
  - Enable the block layer
  - CONFIG_BLK_DEV_WRITE_MOUNTED=y
  - Memory Management options
  - CONFIG_ZSWAP_SHRINKER_DEFAULT_ON=n
  - CONFIG_TRANSPARENT_HUGEPAGE_NEVER=n
  - File systems
  - CONFIG_BCACHEFS_SIX_OPTIMISTIC_SPIN=y
  - CONFIG_EROFS_FS_ONDEMAND=n
  - CONFIG_NFSD_LEGACY_CLIENT_TRACKING=n
  - Cryptographic API
  - CONFIG_CRYPTO_DEV_QAT_420XX=m
  - CONFIG_CRYPTO_DEV_IAA_CRYPTO=m
  - CONFIG_CRYPTO_DEV_IAA_CRYPTO_STATS=n
  - Library routines
  - CONFIG_STACKDEPOT_MAX_FRAMES=64
  - Misc devices
  - CONFIG_NSM=m
  - CONFIG_INTEL_MEI_VSC_HW=m
  - CONFIG_INTEL_MEI_VSC=m
  - Network device support
  - CONFIG_ICE_HWMON=y
  - CONFIG_DP83TG720_PHY=m
  - CONFIG_FRAMER=m
  - Pin controllers
  - CONFIG_PINCTRL_INTEL_PLATFORM=m
  - CONFIG_PINCTRL_METEORPOINT=m
  - Hardware Monitoring support
  - CONFIG_SENSORS_GIGABYTE_WATERFORCE=m
  - CONFIG_SENSORS_LTC4286=n
  - CONFIG_SENSORS_MP2856=m
  - CONFIG_SENSORS_MP5990=m
  - Multimedia support
  - CONFIG_VIDEO_ALVIUM_CSI2=m
  - CONFIG_VIDEO_GC0308=m
  - CONFIG_VIDEO_GC2145=m
  - CONFIG_VIDEO_OV64A40=m
  - CONFIG_VIDEO_THP7312=m
  - CONFIG_VIDEO_TW9900=m
  - Graphics support
  - CONFIG_DRM_I915_DEBUG_WAKEREF=n
  - CONFIG_DRM_XE=m
  - CONFIG_DRM_XE_DISPLAY=y
  - CONFIG_DRM_XE_FORCE_PROBE=""
  - CONFIG_DRM_XE_WERROR=n
  - CONFIG_DRM_XE_DEBUG=n
  - CONFIG_DRM_XE_DEBUG_VM=n
  - CONFIG_DRM_XE_DEBUG_SRIOV=n
  - CONFIG_DRM_XE_DEBUG_MEM=n
  - CONFIG_DRM_XE_SIMPLE_ERROR_CAPTURE=n
  - CONFIG_DRM_XE_LARGE_GUC_BUFFER=n
  - CONFIG_DRM_XE_USERPTR_INVAL_INJECT=n
  - CONFIG_DRM_XE_JOB_TIMEOUT_MAX=10000
  - CONFIG_DRM_XE_JOB_TIMEOUT_MIN=1
  - CONFIG_DRM_XE_TIMESLICE_MAX=10000000
  - CONFIG_DRM_XE_TIMESLICE_MIN=1
  - CONFIG_DRM_XE_PREEMPT_TIMEOUT=640000
  - CONFIG_DRM_XE_PREEMPT_TIMEOUT_MAX=10000000
  - CONFIG_DRM_XE_PREEMPT_TIMEOUT_MIN=1
  - CONFIG_DRM_XE_ENABLE_SCHEDTIMEOUT_LIMIT=y
  - CONFIG_BACKLIGHT_MP3309C=m
  - Real Time Clock
  - CONFIG_RTC_DRV_MAX31335=m
  - CONFIG_RTC_DRV_TPS6594=m
  - VFIO Non-Privileged userspace driver framework
  - CONFIG_VFIO_DEBUGFS=n
  - CONFIG_VIRTIO_VFIO_PCI=m
  - X86 Platform Specific Device Drivers
  - CONFIG_AMD_WBRF=y
  - CONFIG_SILICOM_PLATFORM=m
  - Industrial I/O support
  - CONFIG_AD7091R8=n
  - CONFIG_MAX34408=n
  - CONFIG_AOSONG_AGS02MA=n
  - CONFIG_MCP4821=n
  - CONFIG_BMI323_I2C=m
  - CONFIG_BMI323_SPI=m
  - CONFIG_ISL76682=n
  - CONFIG_LTR390=n
  - CONFIG_VEML6075=n
  - CONFIG_HSC030PA=n
  - CONFIG_MLX90635=m
  - CONFIG_MCP9600=m
  - Misc drivers
  - CONFIG_MTD_UBI_FAULT_INJECTION=n
  - CONFIG_ZRAM_TRACK_ENTRY_ACTIME=n
  - CONFIG_JOYSTICK_SEESAW=m
  - CONFIG_W1_MASTER_AMD_AXI=m
  - CONFIG_THERMAL_DEBUGFS=n
  - CONFIG_REGULATOR_NETLINK_EVENTS=y
  - CONFIG_SND_AMD_ASOC_ACP70=m
  - CONFIG_HID_MCP2200=m
  - CONFIG_TYPEC_MUX_WCD939X_USBSS=m
  - CONFIG_QCOM_PMIC_PDCHARGER_ULOG=m
  - CONFIG_DWC_PCIE_PMU=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - PINCTRL_TPS6594=n
  - DRM_PANEL_ILITEK_ILI9805=n
  - DRM_PANEL_SYNAPTICS_R63353=n
  - LEDS_MAX5970=m
  - i386
  - FRAMER_PEF2256=m
  - PINCTRL_PEF2256=n
  - s390x
  - DRM_DP_AUX_CHARDEV=y
  - DRM_DP_CEC=y
  - DRM_PANEL_RASPBERRYPI_TOUCHSCREEN=n
  - MEDIA_CEC_RC=n
  - s390x/zfcpdump
  - HW_RANDOM_VIRTIO=n
  - HW_RANDOM_S390=y
  - riscv64
  - PARAVIRT=y
  - PARAVIRT_TIME_ACCOUNTING=n
  - POLARFIRE_SOC_AUTO_UPDATE=m
  - FRAMER_PEF2256=m
  - SERIAL_EARLYCON_RISCV_SBI=y
  - HVC_RISCV_SBI=y
  - PINCTRL_PEF2256=n
  - DRM_PANEL_RASPBERRYPI_TOUCHSCREEN=m
  - DRM_PANEL_*=n (except above)
  - LEDS_SUN50I_A100=m
  - VIDEO_STARFIVE_CAMSS=m
- commit c2014a1
* Mon Jan 22 2024 jslaby@suse.cz
- futex: Prevent the reuse of stale pi_state (bsc#1218841).
  Update upstream status (Queued in subsystem maintainer repository).
- commit a3ee207
* Sun Jan 21 2024 colyli@suse.de
- Update config files, enable CONFIG_IMA_DISABLE_HTABLE in all archs for
  Tumbleweed as SLE15-SP6 kernel does (bsc#1218400).
- commit 020caa6
* Fri Jan 19 2024 jslaby@suse.cz
- media: solo6x10: replace max(a, min(b, c)) by clamp(b, a, c)
  (fix build and make it faster).
- Delete
  patches.rpmify/Revert-minmax-allow-comparisons-of-int-against-unsig.patch.
- Delete
  patches.rpmify/Revert-minmax-allow-min-max-clamp-if-the-arguments-h.patch.
- Delete
  patches.rpmify/Revert-minmax-fix-indentation-of-__cmp_once-and-__cl.patch.
- Delete
  patches.rpmify/Revert-minmax-relax-check-to-allow-comparison-betwee.patch.
  Replace the reverts by an upstream workaround.
- commit 9bff21f
* Fri Jan 19 2024 jslaby@suse.cz
- mm: huge_memory: don't force huge page alignment on 32 bit
  (bsc#1218841).
- Delete
  patches.suse/Revert-mm-align-larger-anonymous-mappings-on-THP-bou.patch.
  Replace the revert by an upstream fix.
- commit d54abef
* Fri Jan 19 2024 jslaby@suse.cz
- Update patches.suse/futex-Avoid-reusing-outdated-pi_state.patch
  (bsc#1218801).
  Update to v2.
- commit eeba83a
* Wed Jan 17 2024 jslaby@suse.cz
- Revert "mm: align larger anonymous mappings on THP boundaries"
  (bsc#1218841).
- commit 69537e9
* Tue Jan 16 2024 jslaby@suse.cz
- futex: Avoid reusing outdated pi_state (bsc#1218841).
- commit 9859079
* Thu Jan 11 2024 tiwai@suse.de
- Store the old kernel changelog entries in kernel-docs package (bsc#1218713)
  The old entries are found in kernel-docs/old_changelog.txt in docdir.
  rpm/old_changelog.txt can be an optional file that stores the similar
  info like rpm/kernel-sources.changes.old.  It can specify the commit
  range that have been truncated.  scripts/tar-up.sh expands from the
  git log accordingly.
- commit c9a2566
* Thu Jan 11 2024 jslaby@suse.cz
- keys, dns: Fix size check of V1 server-list header (git-fixes).
- commit 9e5e777
* Mon Jan  8 2024 msuchanek@suse.de
- Limit kernel-source build to architectures for which the kernel binary
  is built (bsc#1108281).
- commit 08a9e44
* Mon Jan  8 2024 jslaby@suse.cz
- Revert "minmax: allow min()/max()/clamp() if the arguments
  have the same signedness." (fix build and make it faster).
- Revert "minmax: fix indentation of __cmp_once() and
  __clamp_once()" (fix build and make it faster).
- commit 7b7f72a
* Mon Jan  8 2024 jslaby@suse.cz
- Revert "minmax: allow comparisons of 'int' against 'unsigned
  char/short'" (fix build and make it faster).
- Revert "minmax: relax check to allow comparison between unsigned
  arguments and signed constants" (fix build and make it faster).
- commit a7cbb4e
* Mon Jan  8 2024 jslaby@suse.cz
- Refresh
  patches.suse/bus-mhi-host-add-mhi_power_down_no_destroy.patch.
- Refresh
  patches.suse/bus-mhi-host-add-new-interfaces-to-handle-MHI-channe.patch.
- Refresh
  patches.suse/wifi-ath11k-do-not-dump-SRNG-statistics-during-resum.patch.
- Refresh
  patches.suse/wifi-ath11k-fix-warning-on-DMA-ring-capabilities-eve.patch.
- Refresh
  patches.suse/wifi-ath11k-handle-irq-enable-disable-in-several-cod.patch.
- Refresh
  patches.suse/wifi-ath11k-remove-MHI-LOOPBACK-channels.patch.
- Refresh patches.suse/wifi-ath11k-support-hibernation.patch.
- Refresh
  patches.suse/wifi-ath11k-thermal-don-t-try-to-register-multiple-t.patch.
  Note the branch name the patches are in.
- commit 9538a8b
* Sun Jan  7 2024 mkubecek@suse.cz
- Update to 6.7
- refresh configs (only headers)
- commit e615918
* Fri Jan  5 2024 petr.pavlu@suse.com
- Delete doc/config-options.changes (jsc#PED-5021)
  Following on adedbd2a5c6 ("kernel-source: Remove config-options.changes
  (jsc#PED-5021)"), remove the now unused file from the tree.
- commit d25d3f2
* Thu Jan  4 2024 msuchanek@suse.de
- config: ppc64le: CONFIG_MEM_SOFT_DIRTY=y (bsc#1218286 ltc#204519).
- commit c8c5229
* Wed Jan  3 2024 msuchanek@suse.de
- mkspec: Add multibuild support (JSC-SLE#5501, boo#1211226, bsc#1218184)
  When MULTIBUILD option in config.sh is enabled generate a _multibuild
  file listing all spec files.
- commit f734347
* Wed Jan  3 2024 msuchanek@suse.de
- Build in the correct KOTD repository with multibuild
  (JSC-SLE#5501, boo#1211226, bsc#1218184)
  With multibuild setting repository flags is no longer supported for
  individual spec files - see
  https://github.com/openSUSE/open-build-service/issues/3574
  Add ExclusiveArch conditional that depends on a macro set up by
  bs-upload-kernel instead. With that each package should build only in
  one repository - either standard or QA.
  Note: bs-upload-kernel does not interpret rpm conditionals, and only
  uses the first ExclusiveArch line to determine the architectures to
  enable.
- commit aa5424d
* Wed Jan  3 2024 msuchanek@suse.de
- rpm/config.sh: Enable multibuild.
- commit c909ebd
* Mon Jan  1 2024 mkubecek@suse.cz
- Update to 6.7-rc8
- update configs
  - s390x/zfcpdump:
  - KEXEC_FILE=y
- commit 521bba4
* Sun Dec 24 2023 mkubecek@suse.cz
- Update to 6.7-rc7
- refresh configs
- commit 65d9931
* Mon Dec 18 2023 mkubecek@suse.cz
- Update to 6.7-rc6
- refresh configs
- commit 8a25837
* Sat Dec 16 2023 dmueller@suse.com
- config: update riscv64
- sync few options with arm
- config.conf: reenable armv6hl/armv7hl
- Update config files.
- commit 4466ed8
* Sat Dec 16 2023 dmueller@suse.com
- config.conf: Reenable arm64
- Update config files for arm64. Take settings from x86_64, enable
  everthing that can be enabled as modules.
- commit 979aa1b
* Mon Dec 11 2023 mkubecek@suse.cz
- Update to 6.7-rc5
- refresh configs
- commit 91bd996
* Fri Dec  8 2023 petr.pavlu@suse.com
- kernel-source: Remove config-options.changes (jsc#PED-5021)
  The file doc/config-options.changes was used in the past to document
  kernel config changes. It was introduced in 2010 but haven't received
  any updates on any branch since 2015. The file is renamed by tar-up.sh
  to config-options.changes.txt and shipped in the kernel-source RPM
  package under /usr/share/doc. As its content now only contains outdated
  information, retaining it can lead to confusion for users encountering
  this file.
  Config changes are nowadays described in associated Git commit messages,
  which get automatically collected and are incorporated into changelogs
  of kernel RPM packages.
  Drop then this obsolete file, starting with its packaging logic.
  For branch maintainers: Upon merging this commit on your branch, please
  correspondingly delete the file doc/config-options.changes.
- commit adedbd2
* Fri Dec  8 2023 petr.pavlu@suse.com
- doc/README.SUSE: Simplify the list of references (jsc#PED-5021)
  Reduce indentation in the list of references, make the style consistent
  with README.md.
- commit 70e3c33
* Thu Dec  7 2023 petr.pavlu@suse.com
- doc/README.SUSE: Add how to update the config for module signing
  (jsc#PED-5021)
  Configuration files for SUSE kernels include settings to integrate with
  signing support provided by the Open Build Service. This creates
  problems if someone tries to use such a configuration file to build
  a "standalone" kernel as described in doc/README.SUSE:
  * Default configuration files available in the kernel-source repository
  unset CONFIG_MODULE_SIG_ALL to leave module signing to
  pesign-obs-integration. In case of a "standalone" build, this
  integration is not available and the modules don't get signed.
  * The kernel spec file overrides CONFIG_MODULE_SIG_KEY to
  ".kernel_signing_key.pem" which is a file populated by certificates
  provided by OBS but otherwise not available. The value ends up in
  /boot/config-$VERSION-$RELEASE-$FLAVOR and /proc/config.gz. If someone
  decides to use one of these files as their base configuration then the
  build fails with an error because the specified module signing key is
  missing.
  Add information on how to enable module signing and where to find the
  relevant upstream documentation.
- commit a699dc3
* Wed Dec  6 2023 petr.pavlu@suse.com
- doc/README.SUSE: Remove how to build modules using kernel-source
  (jsc#PED-5021)
  Remove the first method how to build kernel modules from the readme. It
  describes a process consisting of the kernel-source installation,
  configuring this kernel and then performing an ad-hoc module build.
  This method is not ideal as no modversion data is involved in the
  process. It results in a module with no symbol CRCs which can be wrongly
  loaded on an incompatible kernel.
  Removing the method also simplifies the readme because only two main
  methods how to build the modules are then described, either doing an
  ad-hoc build using kernel-devel, or creating a proper Kernel Module
  Package.
- commit 9285bb8
* Sun Dec  3 2023 mkubecek@suse.cz
- Update to 6.7-rc4
- update configs
  - BCACHEFS_ERASURE_CODING=n
- commit 900d9a2
* Fri Dec  1 2023 msuchanek@suse.de
- kernel-binary: suse-module-tools is also required when installed
  Requires(pre) adds dependency for the specific sciptlet.
  However, suse-module-tools also ships modprobe.d files which may be
  needed at posttrans time or any time the kernel is on the system for
  generating ramdisk. Add plain Requires as well.
- commit 8c12816
* Fri Dec  1 2023 msuchanek@suse.de
- rpm: Use run_if_exists for all external scriptlets
  With that the scriptlets do not need to be installed for build.
- commit 25edd65
* Thu Nov 30 2023 jslaby@suse.cz
- README.SUSE: fix patches.addon use
  It's series, not series.conf in there.
  And make it more precise on when the patches are applied.
- commit cb8969c
* Wed Nov 29 2023 bwiedemann@suse.de
- Do not store build host name in initrd
  Without this patch, kernel-obs-build stored the build host name
  in its .build.initrd.kvm
  This patch allows for reproducible builds of kernel-obs-build and thus
  avoids re-publishing the kernel-obs-build.rpm when nothing changed.
  Note that this has no influence on the /etc/hosts file
  that is used during other OBS builds.
  https://bugzilla.opensuse.org/show_bug.cgi?id=1084909
- commit fd3a75e
* Wed Nov 29 2023 tiwai@suse.de
- Update ath11k hibernation patches from the latest code (bsc#1207948)
- commit 9b910a2
* Mon Nov 27 2023 duwe@suse.de
- rpm/mkspec-dtb: build DTBs for Sophgo based riscv64 systems.
  These are new in 6.7 and required for the Milk-V Pioneer.
- commit c86e052
* Mon Nov 27 2023 mkubecek@suse.cz
- Update to 6.7-rc3
- refresh configs
- commit e7296f9
* Fri Nov 24 2023 fcrozat@suse.com
- Ensure ia32_emulation is always enabled for kernel-obs-build
  If ia32_emulation is disabled by default, ensure it is enabled
  back for OBS kernel to allow building 32bit binaries (jsc#PED-3184)
  [ms: Always pass the parameter, no need to grep through the config which
  may not be very reliable]
- commit 56a2c2f
* Wed Nov 22 2023 tiwai@suse.de
- Update config files: CONFIG_SND_SOC_WSA883X=m for Thinkpad X13s audio (bsc#1217412)
- commit 9bf78b1
* Wed Nov 22 2023 msuchanek@suse.de
- rpm: Define git commit as macro
- commit bcc92c8
* Wed Nov 22 2023 msuchanek@suse.de
- kernel-source: Move provides after sources
- commit dbbf742
* Mon Nov 20 2023 mkubecek@suse.cz
- Update to 6.7-rc2
- refresh
  - patches.suse/firmware-qemu_fw_cfg-Do-not-hard-depend-on-CONFIG_HA.patch
- update configs
  - riscv64
  - FW_CFG_SYSFS=m
  - FW_CFG_SYSFS_CMDLINE=y
- commit e1d4442
* Wed Nov 15 2023 tiwai@suse.de
- Refresh patches.suse/iwlwifi-cfg-Add-missing-MODULE_FIRMWARE-for-pnvm.patch
  Add entries for more *.pnvm files
- commit 880a670
* Mon Nov 13 2023 schwab@suse.de
- rpm/check-for-config-changes: add HAVE_SHADOW_CALL_STACK to IGNORED_CONFIGS_RE
  Not supported by our compiler.
- commit eb32b5a
* Mon Nov 13 2023 mkubecek@suse.cz
- Update to 6.7-rc1
- drop 36 patches (31 stable, 5 mainline)
  - patches.kernel.org/*
  - patches.rpmify/kbuild-dummy-tools-pretend-we-understand-fpatchable-.patch
  - patches.suse/firmware-Add-support-for-Qualcomm-UEFI-Secure-Applic.patch
  - patches.suse/firmware-qcom_scm-Add-support-for-Qualcomm-Secure-Ex.patch
  - patches.suse/lib-ucs2_string-Add-UCS-2-strscpy-function.patch
  - patches.suse/wifi-ath11k-rename-the-sc-naming-convention-to-ab.patch
- refresh
  - patches.rpmify/Add-ksym-provides-tool.patch
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
  - patches.suse/wifi-ath11k-support-hibernation.patch
- fix patch metadata
  - patches.rpmify/Add-ksym-provides-tool.patch
- disable ARM architectures (need config update)
- new config options
  - Processor type and features
  - CONFIG_INTEL_TDX_HOST=n
  - Binary Emulations
  - CONFIG_IA32_EMULATION_DEFAULT_DISABLED=n
  - Virtualization
  - CONFIG_KVM_MAX_NR_VCPUS=4096
  - Enable loadable module support
  - CONFIG_MODULE_SIG_SHA3_256=n
  - CONFIG_MODULE_SIG_SHA3_384=n
  - CONFIG_MODULE_SIG_SHA3_512=n
  - Memory Management options
  - CONFIG_PCP_BATCH_SCALE_MAX=5
  - Networking support
  - CONFIG_TCP_AO=y
  - File systems
  - CONFIG_BCACHEFS_FS=m
  - CONFIG_BCACHEFS_QUOTA=y
  - CONFIG_BCACHEFS_POSIX_ACL=y
  - CONFIG_BCACHEFS_DEBUG_TRANSACTIONS=n
  - CONFIG_BCACHEFS_DEBUG=n
  - CONFIG_BCACHEFS_TESTS=n
  - CONFIG_BCACHEFS_LOCK_TIME_STATS=n
  - CONFIG_BCACHEFS_NO_LATENCY_ACCT=n
  - Cryptographic API
  - CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_2=y
  - CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_128=n
  - CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_1024=n
  - CONFIG_CRYPTO_JITTERENTROPY_MEMSIZE_8192=n
  - CONFIG_CRYPTO_JITTERENTROPY_OSR=1
  - CONFIG_SECONDARY_TRUSTED_KEYRING_SIGNED_BY_BUILTIN=n
  - Library routines
  - CONFIG_LWQ_TEST=n
  - Kernel hacking
  - CONFIG_DEBUG_CLOSURES=n
  - CONFIG_TEST_OBJPOOL=n
  - PCI support
  - CONFIG_PCIEAER_CXL=y
  - NVME Support
  - CONFIG_NVME_TCP_TLS=y
  - CONFIG_NVME_HOST_AUTH=y
  - CONFIG_NVME_TARGET_TCP_TLS=y
  - Network device support
  - CONFIG_NETKIT=y
  - CONFIG_IDPF=m
  - CONFIG_MLX5_DPLL=m
  - CONFIG_MCTP_TRANSPORT_I3C=m
  - CONFIG_MT7925E=m
  - CONFIG_MT7925U=m
  - Hardware Monitoring support
  - CONFIG_SENSORS_POWERZ=m
  - CONFIG_SENSORS_LTC2991=m
  - Multimedia support
  - CONFIG_VIDEO_MGB4=m
  - CONFIG_VIDEO_MT9M114=m
  - Sound card support
  - CONFIG_SND_AMD_ASOC_ACP63=m
  - CONFIG_SND_SOC_INTEL_AVS_MACH_RT5514=m
  - CONFIG_SND_SOC_INTEL_SOF_DA7219_MACH=m
  - CONFIG_SND_SOC_SOF_AMD_ACP63=m
  - CONFIG_SND_SOC_AW87390=n
  - CONFIG_SND_SOC_AW88399=n
  - CONFIG_SND_SOC_RTQ9128=m
  - USB support
  - CONFIG_USB_PCI_AMD=y
  - CONFIG_USB_LJCA=m
  - CONFIG_TYPEC_MUX_PTN36502=m
  - Industrial I/O support
  - CONFIG_LTC2309=n
  - CONFIG_MCP3564=n
  - CONFIG_ROHM_BM1390=n
  - Misc drivers
  - CONFIG_I2C_LJCA=m
  - CONFIG_SPI_LJCA=m
  - CONFIG_GPIO_LJCA=m
  - CONFIG_FUEL_GAUGE_MM8013=m
  - CONFIG_REGULATOR_MAX77503=m
  - CONFIG_LEDS_TRIGGER_GPIO=m
  - CONFIG_XEN_PRIVCMD_EVENTFD=y
  - CONFIG_INSPUR_PLATFORM_PROFILE=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - DRM_PANEL_ILITEK_ILI9882T=n
  - DRM_PANEL_JDI_LPM102A188A=n
  - DRM_PANEL_RAYDIUM_RM692E5=n
  - LEDS_KTD202X=m
  - ppc64le
  - PROBE_EVENTS_BTF_ARGS=y
  - s390x/zfcdump
  - CERT_STORE=y
  - BLK_SED_OPAL=n
  - DNS_RESOLVER=n
  - QUOTA_NETLINK_INTERFACE=n
  - KEYS_REQUEST_CACHE=n
  - PERSISTENT_KEYRINGS=n
  - TRUSTED_KEYS=n
  - ENCRYPTED_KEYS=n
  - KEY_DH_OPERATIONS=n
  - KEY_NOTIFICATIONS=n
  - ASYMMETRIC_KEY_TYPE=n
  - SYSTEM_BLACKLIST_KEYRING=n
  - RAID6_PQ_BENCHMARK=n
  - riscv64
  - ARCH_SOPHGO=y
  - RISCV_MISALIGNED=y
  - SHADOW_CALL_STACK=y
  - PCIE_RCAR_GEN4_HOST=m
  - PCIE_RCAR_GEN4_EP=m
  - SND_SOC_JH7110_PWMDAC=m
  - RUNTIME_KERNEL_TESTING_MENU=n
  - copied from arm64
  - SERIO_AMBAKMI=n
  - SERIAL_AMBA_PL010=y
  - SERIAL_AMBA_PL011=y
  - I2C_NOMADIK=n
  - SPI_PL022=m
  - GPIO_PL061=y
  - MMC_ARMMMCI=m
  - MMC_SDHI_INTERNAL_DMAC=m
  - RTC_DRV_PL030=y
  - RTC_DRV_PL031=y
  - AMBA_PL08X=n
  - PL330_DMA=m
  - ARM_MHU=n
  - ARM_MHU_V2=m
  - PL320_MBOX=n
  - ARM_PL172_MPMC=m
  - SERIAL_AMBA_PL010_CONSOLE=y
  - SERIAL_AMBA_PL011_CONSOLE=y
  - MMC_STM32_SDMMC=y
- commit 47d658a
* Fri Nov 10 2023 jdelvare@suse.de
- Disable Loongson drivers
  Loongson is a mips architecture, I don't think it makes sense to
  build Loongson drivers on other architectures.
- commit 4d5bd14
* Fri Nov 10 2023 tiwai@suse.de
- wifi: ath11k: support hibernation (bsc#1207948).
- wifi: ath11k: thermal: don't try to register multiple times
  (bsc#1207948).
- wifi: ath11k: fix warning on DMA ring capabilities event
  (bsc#1207948).
- wifi: ath11k: do not dump SRNG statistics during resume
  (bsc#1207948).
- wifi: ath11k: remove MHI LOOPBACK channels (bsc#1207948).
- wifi: ath11k: handle irq enable/disable in several code path
  (bsc#1207948).
- bus: mhi: host: add new interfaces to handle MHI channels
  directly (bsc#1207948).
- bus: mhi: host: add mhi_power_down_no_destroy() (bsc#1207948).
- commit 10bbcec
* Fri Nov 10 2023 tiwai@suse.de
- wifi: ath11k: rename the sc naming convention to ab
  (bsc#1207948).
- commit e66948e
* Fri Nov 10 2023 tiwai@suse.de
- Drop ath11k hibernation patch set once for renewal (bsc#1207948)
- commit 9ecdaa5
* Thu Nov  9 2023 jslaby@suse.cz
- Linux 6.6.1 (bsc#1012628).
- ASoC: SOF: sof-pci-dev: Fix community key quirk detection
  (bsc#1012628).
- ALSA: hda: intel-dsp-config: Fix JSL Chromebook quirk detection
  (bsc#1012628).
- serial: core: Fix runtime PM handling for pending tx
  (bsc#1012628).
- misc: pci_endpoint_test: Add deviceID for J721S2 PCIe EP device
  support (bsc#1012628).
- dt-bindings: serial: rs485: Add rs485-rts-active-high
  (bsc#1012628).
- tty: 8250: Add Brainboxes Oxford Semiconductor-based quirks
  (bsc#1012628).
- tty: 8250: Add support for Intashield IX cards (bsc#1012628).
- tty: 8250: Add support for additional Brainboxes PX cards
  (bsc#1012628).
- tty: 8250: Fix up PX-803/PX-857 (bsc#1012628).
- tty: 8250: Fix port count of PX-257 (bsc#1012628).
- tty: 8250: Add support for Intashield IS-100 (bsc#1012628).
- tty: 8250: Add support for Brainboxes UP cards (bsc#1012628).
- tty: 8250: Add support for additional Brainboxes UC cards
  (bsc#1012628).
- tty: 8250: Remove UC-257 and UC-431 (bsc#1012628).
- tty: n_gsm: fix race condition in status line change on dead
  connections (bsc#1012628).
- Bluetooth: hci_bcm4377: Mark bcm4378/bcm4387 as BROKEN_LE_CODED
  (bsc#1012628).
- usb: raw-gadget: properly handle interrupted requests
  (bsc#1012628).
- usb: typec: tcpm: Fix NULL pointer dereference in tcpm_pd_svdm()
  (bsc#1012628).
- usb: typec: tcpm: Add additional checks for contaminant
  (bsc#1012628).
- usb: storage: set 1.50 as the lower bcdDevice for older "Super
  Top" compatibility (bsc#1012628).
- PCI: Prevent xHCI driver from claiming AMD VanGogh USB3 DRD
  device (bsc#1012628).
- ALSA: usb-audio: add quirk flag to enable native DSD for
  McIntosh devices (bsc#1012628).
- eventfs: Use simple_recursive_removal() to clean up dentries
  (bsc#1012628).
- eventfs: Delete eventfs_inode when the last dentry is freed
  (bsc#1012628).
- eventfs: Save ownership and mode (bsc#1012628).
- eventfs: Remove "is_freed" union with rcu head (bsc#1012628).
- tracing: Have trace_event_file have ref counters (bsc#1012628).
- perf evlist: Avoid frequency mode for the dummy event
  (bsc#1012628).
- power: supply: core: Use blocking_notifier_call_chain to avoid
  RCU complaint (bsc#1012628).
- drm/amd/display: Don't use fsleep for PSR exit waits
  (bsc#1012628).
- commit 758e4f0
* Mon Nov  6 2023 mkubecek@suse.cz
- update patch metadata
- update upstream reference
  - patches.rpmify/kbuild-dummy-tools-pretend-we-understand-fpatchable-.patch
- commit 93ae682
* Thu Nov  2 2023 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and move into sorted section:
  - patches.suse/firmware-Add-support-for-Qualcomm-UEFI-Secure-Applic.patch
  - patches.suse/firmware-qcom_scm-Add-support-for-Qualcomm-Secure-Ex.patch
  - patches.suse/lib-ucs2_string-Add-UCS-2-strscpy-function.patch
- commit 157ac85
* Thu Nov  2 2023 jslaby@suse.cz
- kbuild: dummy-tools: pretend we understand
  - fpatchable-function-entry (ppc64le-build-fix).
- Delete
  patches.rpmify/kbuild-dummy-tools-Add-support-for-fpatchable-functi.patch.
  Replace the latter with the former (upstream accepted solution).
- commit 8050c17
* Wed Nov  1 2023 schwab@suse.de
- riscv: enable CONFIG_PCI_HOST_GENERIC
  Needed for the pci host controller emulated by qemu.
- commit ebb7db3
* Wed Nov  1 2023 jslaby@suse.cz
- Delete patches.rpmify/x86-Let-AS_WRUSS-depend-on-X86_64.patch.
- Update config files.
  This effectively reverts 9ab2e0780c8a2fb9a84db5bad59fbe3ab526a6c3. The
  patch was not accepted upstream:
  https://lore.kernel.org/all/20231031140504.GCZUEJkMPXSrEDh3MA@fat_crate.local/
  Instead, we merged the packaging branch which fixes this in
  rpm/check-for-config-changes instead.
- rpm/check-for-config-changes: add AS_WRUSS to IGNORED_CONFIGS_RE
  Add AS_WRUSS as an IGNORED_CONFIGS_RE entry in check-for-config-changes
  to fix build on x86_32.
  There was a fix submitted to upstream but it was not accepted:
  https://lore.kernel.org/all/20231031140504.GCZUEJkMPXSrEDh3MA@fat_crate.local/
  So carry this in IGNORED_CONFIGS_RE instead.
- commit ce5bc31
* Tue Oct 31 2023 petr@tesarici.cz
- config: enable NFS_V4_2_READ_PLUS (bsc#1216736)
  This option was introduced and disabled by default because of unresolved
  issues. As stated in mainline commit 9cf2744d2491 ("NFS: Enable the
  READ_PLUS operation by default") which changes the upstream default to
  enabled, these issues are addressed so that it is safe to enable the
  option and as it allows to transfer sparse files more efficiently, it is
  desirable to do so.
- commit c4f1dc1
* Tue Oct 31 2023 jslaby@suse.cz
- x86: Let AS_WRUSS depend on X86_64 (i386-build-fix).
- Update config files.
- commit 9ab2e07
* Mon Oct 30 2023 msuchanek@suse.de
- kbuild: dummy-tools: Add support for -fpatchable-function-entry (dummy-tools).
  Update config files.
- commit 494c209
* Mon Oct 30 2023 jslaby@suse.cz
- Delete
  patches.suse/ACPI-video-Add-backlight-native-DMI-quirk-for-Lenovo.patch.
  Already present in 6.6-rc1. This was applied twice due to too few
  context in the diff. But it did not hurt...
- commit 2a844dc
* Mon Oct 30 2023 mkubecek@suse.cz
- Update to 6.6 final
- refresh configs (headers only)
- commit e0904b6
* Sun Oct 29 2023 mkubecek@suse.cz
- update and reenable armv7hl configs
  Where possible, new values are copied from arm64. The rest is guessed,
  mostly based on existing values of similar config options.
- armv7hl specific config options:
  - TI_ICSS_IEP=m
- commit 09e0fd1
* Mon Oct 23 2023 mkubecek@suse.cz
- Update to 6.6-rc7
- refresh configs
- commit 4a117b4
* Fri Oct 20 2023 dmueller@suse.com
- config.conf: Reenable arm64
- Update config files:
  * Same settings like x86_64, plus all ARM specific errata turned on
  * rest all mod
- commit 5e5e96e
* Thu Oct 19 2023 mbrugger@suse.com
- arm64: Update config files.
  Make iMX93 clock and pinctrl driver build-in.
- commit e54b1e1
* Sun Oct 15 2023 mkubecek@suse.cz
- Update to 6.6-rc6
- refresh configs
- commit 8f5995d
* Sat Oct 14 2023 matwey.kornilov@gmail.com
- config: Reenable Rockchip RK8XX hardware
  In Linux commit
    c20e8c5b1203 ("mfd: rk808: Split into core and i2c")
  CONFIG_MFD_RK808 was renamed to CONFIG_MFD_RK8XX.
  Reenable options required to boot kernel 6.5 on Rock64 board.
- commit 41037b9
* Mon Oct  9 2023 svarbanov@suse.de
- config/arm64: Unset default IOMMU passthrough option (jsc#PED-7009)
  This will effectively enable ARM64 SMMU translation by default,
  which will help to avoid installation and runtime issues on some
  platforms. The passtrhough mode could still be enabled by kernel
  cmdline.
- commit d8da3f8
* Mon Oct  9 2023 schwab@suse.de
- mkspec-dtb: add toplevel symlinks also on arm
- commit ed29cae
* Sun Oct  8 2023 mkubecek@suse.cz
- Update to 6.6-rc5
- update configs
  - IMA_BLACKLIST_KEYRING=n
  - IMA_LOAD_X509=n
  - IPU_BRIDGE=m (new on riscv64)
- commit a59832f
* Sat Oct  7 2023 petr.pavlu@suse.com
- doc/README.PATCH-POLICY.SUSE: Convert the document to Markdown
  (jsc#PED-5021)
- commit c05cfc9
* Sat Oct  7 2023 petr.pavlu@suse.com
- doc/README.SUSE: Convert the document to Markdown (jsc#PED-5021)
- commit bff5e3e
* Tue Oct  3 2023 petr.pavlu@suse.com
- doc/README.PATCH-POLICY.SUSE: Remove the list of links (jsc#PED-5021)
  All links have been incorporated into the text. Remove now unnecessary
  list at the end of the document.
- commit 43d62b1
* Tue Oct  3 2023 petr.pavlu@suse.com
- doc/README.SUSE: Adjust heading style (jsc#PED-5021)
  * Underscore all headings as a preparation for Markdown conversion.
  * Use title-style capitalization for the document name and
  sentence-style capitalization for section headings, as recommended in
  the current SUSE Documentation Style Guide.
- commit 11e3267
* Mon Oct  2 2023 mkubecek@suse.cz
- Update to 6.6-rc4
- eliminate 1 patch
  - patches.suse/Revert-101bd907b424-misc-rtsx-judge-ASPM-Mode-to-set.patch (0e4cac557531)
- commit 019d4ec
* Tue Sep 26 2023 petr.pavlu@suse.com
- doc/README.PATCH-POLICY.SUSE: Reflow text to 80-column width
  (jsc#PED-5021)
- commit be0158c
* Tue Sep 26 2023 petr.pavlu@suse.com
- doc/README.PATCH-POLICY.SUSE: Update information about the tools
  (jsc#PED-5021)
  * Replace bugzilla.novell.com with bugzilla.suse.com and FATE with Jira.
  * Limit the range of commits in the exportpatch example to prevent it
  from running for too long.
  * Incorporate URLs directly into the text.
  * Fix typos and improve some wording, in particular avoid use of "there
  is/are" and prefer the present tense over the future one.
- commit c0bea0c
* Tue Sep 26 2023 petr.pavlu@suse.com
- doc/README.PATCH-POLICY.SUSE: Update information about the patch
  format (jsc#PED-5021)
  * Replace bugzilla.novell.com with bugzilla.suse.com and FATE with Jira.
  * Remove references to links to the patchtools and kernel source. They
  are incorporated in other parts of the text.
  * Use sentence-style capitalization for section headings, as recommended
  in the current SUSE Documentation Style Guide.
  * Fix typos and some wording, in particular avoid use of "there is/are".
- commit ce98345
* Tue Sep 26 2023 petr.pavlu@suse.com
- doc/README.PATCH-POLICY.SUSE: Update the summary and background
  (jsc#PED-5021)
  * Drop information about patches being split into directories per
  a subsystem because that is no longer the case.
  * Remove the mention that the expanded tree is present since SLE11-SP2
  as that is now only a historical detail.
  * Incorporate URLs and additional information in parenthenses directly
  into the text.
  * Fix typos and improve some wording.
- commit 640988f
* Mon Sep 25 2023 msuchanek@suse.de
- kernel-binary: Move build-time definitions together
  Move source list and build architecture to buildrequires to aid in
  future reorganization of the spec template.
- commit 30e2cef
* Sun Sep 24 2023 mkubecek@suse.cz
- Update to 6.6-rc3
- commit 15b4ad8
* Wed Sep 20 2023 msuchanek@suse.de
- kernel-binary: python3 is needed for build
  At least scripts/bpf_helpers_doc.py requires python3 since Linux 4.18
  Other simimlar scripts may exist.
- commit c882efa
* Tue Sep 19 2023 schwab@suse.de
- riscv: enable CONFIG_MEDIA_PLATFORM_SUPPORT
  - MEDIA_PLATFORM_SUPPORT=y
  - V4L2_H264=m
  - V4L2_VP9=m
  - MEDIA_PLATFORM_DRIVERS=y
  - V4L_PLATFORM_DRIVERS=y
  - SDR_PLATFORM_DRIVERS=y
  - DVB_PLATFORM_DRIVERS=y
  - V4L_MEM2MEM_DRIVERS=y
  - VIDEO_MEM2MEM_DEINTERLACE=m
  - VIDEO_MUX=m
  - VIDEO_CADENCE_CSI2RX=m
  - VIDEO_CADENCE_CSI2TX=m
  - VIDEO_CAFE_CCIC=m
  - VIDEO_RCAR_ISP=m
  - VIDEO_RCAR_CSI2=m
  - VIDEO_RCAR_VIN=m
  - VIDEO_RZG2L_CSI2=m
  - VIDEO_RZG2L_CRU=m
  - VIDEO_RENESAS_FCP=m
  - VIDEO_RENESAS_FDP1=m
  - VIDEO_RENESAS_JPU=m
  - VIDEO_RENESAS_VSP1=m
  - VIDEO_RCAR_DRIF=m
  - VIDEO_SUN4I_CSI=m
  - VIDEO_SUN6I_CSI=m
  - VIDEO_SUN6I_MIPI_CSI2=m
  - VIDEO_SUN8I_A83T_MIPI_CSI2=m
  - VIDEO_SUN8I_DEINTERLACE=m
  - VIDEO_SUN8I_ROTATE=m
  - VIDEO_HANTRO=m
  - VIDEO_HANTRO_SUNXI=y
  - VIDEO_XILINX=m
  - VIDEO_XILINX_CSI2RXSS=m
  - VIDEO_XILINX_TPG=m
  - VIDEO_XILINX_VTC=m
  - SMS_SDIO_DRV=m
  - SMS_SIANO_DEBUGFS=n
  - VIDEO_SUN6I_ISP=m
- commit 337896e
* Mon Sep 18 2023 petr.pavlu@suse.com
- doc/README.SUSE: Reflow text to 80-column width (jsc#PED-5021)
- commit e8f2c67
* Mon Sep 18 2023 tiwai@suse.de
- Update config files: make SCSI/ATA drivers modules again
  As discussed on opensuse-kernel ML, we want to make SCSI and ATA
  drivers from built-in back to modules again:
  https://lists.opensuse.org/archives/list/kernel@lists.opensuse.org/thread/MLRQW7RFEAKTAP63NMPFFIYTXAF7E3I3/
  They were made as built-in many many years ago just for boot speed up
  and a slight hope of initrd-less systems.  But it makes more sense to
  align with the SLE configurations.
- commit 8c848c4
* Mon Sep 18 2023 petr.pavlu@suse.com
- doc/README.SUSE: Minor content clean up (jsc#PED-5021)
  * Mark the user's build directory as a variable, not a command:
  'make -C $(your_build_dir)' -> 'make -C $YOUR_BUILD_DIR'.
  * Unify how to get the current directory: 'M=$(pwd)' -> 'M=$PWD'.
  * 'GIT' / 'git' -> 'Git'.
- commit 1cb4ec8
* Mon Sep 18 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update information about module paths
  (jsc#PED-5021)
  * Use version variables to describe names of the
  /lib/modules/$VERSION-$RELEASE-$FLAVOR/... directories
  instead of using specific example versions which get outdated quickly.
  * Note: Keep the /lib/modules/ prefix instead of using the new
  /usr/lib/modules/ location for now. The updated README is expected to
  be incorporated to various branches that are not yet usrmerged.
- commit 7eba2f0
* Mon Sep 18 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update information about custom patches
  (jsc#PED-5021)
  * Replace mention of various patches.* directories with only
  patches.suse as the typical location for patches.
  * Replace i386 with x86_64 in the example how to define a config addon.
  * Fix some typos and wording.
- commit 2997d22
* Mon Sep 18 2023 mkubecek@suse.cz
- Update to 6.6-rc2
- eliminate 1 patch
  - patches.rpmify/kbuild-avoid-long-argument-lists-in-make-modules_ins.patch
- refresh configs
- commit 8a1f7fd
* Fri Sep 15 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update information about config files
  (jsc#PED-5021)
  * Use version variables to describe a name of the /boot/config-... file
  instead of using specific example versions which get outdated quickly.
  * Replace removed silentoldconfig with oldconfig.
  * Mention that oldconfig can automatically pick a base config from
  "/boot/config-$(uname -r)".
  * Avoid writing additional details in parentheses, incorporate them
  instead properly in the text.
- commit cba5807
* Fri Sep 15 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update the patch selection section
  (jsc#PED-5021)
  * Make the steps how to obtain expanded kernel source more generic in
  regards to version numbers.
  * Use '#' instead of '$' as the command line indicator to signal that
  the steps need to be run as root.
  * Update the format of linux-$SRCVERSION.tar.bz2 to xz.
  * Improve some wording.
- commit e14852c
* Fri Sep 15 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update information about (un)supported modules
  (jsc#PED-5021)
  * Update the list of taint flags. Convert it to a table that matches the
  upstream documentation format and describe specifically flags that are
  related to module support status.
  * Fix some typos and wording.
- commit e46f0df
* Fri Sep 15 2023 petr.pavlu@suse.com
- doc/README.SUSE: Bring information about compiling up to date
  (jsc#PED-5021)
  * When building the kernel, don't mention to initially change the
  current directory to /usr/src/linux because later description
  discourages it and specifies to use 'make -C /usr/src/linux'.
  * Avoid writing additional details in parentheses, incorporate them
  instead properly in the text.
  * Fix the obsolete name of /etc/modprobe.d/unsupported-modules ->
  /etc/modprobe.d/10-unsupported-modules.conf.
  * Drop a note that a newly built kernel should be added to the boot
  manager because that normally happens automatically when running
  'make install'.
  * Update a link to the Kernel Module Packages Manual.
  * When preparing a build for external modules, mention use of the
  upstream recommended 'make modules_prepare' instead of a pair of
  'make prepare' + 'make scripts'.
  * Fix some typos+grammar.
- commit b9b7e79
* Wed Sep 13 2023 petr.pavlu@suse.com
- doc/README.SUSE: Bring the overview section up to date
  (jsc#PED-5021)
  * Update information in the overview section that was no longer
  accurate.
  * Improve wording and fix some typos+grammar.
- commit 798c075
* Wed Sep 13 2023 jslaby@suse.cz
- sysctl/defaults: increase vm.max_map_count (bsc#1214445)
- commit 2d8cc17
* Wed Sep 13 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update the references list (jsc#PED-5021)
  * Remove the reference to Linux Documentation Project. It has been
  inactive for years and mostly contains old manuals that aren't
  relevant for contemporary systems and hardware.
  * Update the name and link to LWN.net. The original name "Linux Weekly
  News" has been deemphasized over time by its authors.
  * Update the link to Kernel newbies website.
  * Update the reference to The Linux Kernel Module Programming Guide. The
  document has not been updated for over a decade but it looks its
  content is still relevant for today.
  * Point Kernel Module Packages Manual to the current version.
  * Add a reference to SUSE SolidDriver Program.
- commit 0edac75
* Wed Sep 13 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update title information (jsc#PED-5021)
  * Drop the mention of kernel versions from the readme title.
  * Remove information about the original authors of the document. Rely as
  in case of other readmes on Git metadata to get information about all
  contributions.
  * Strip the table of contents. The document is short and easy to
  navigate just by scrolling through it.
- commit 06f5139
* Wed Sep 13 2023 petr.pavlu@suse.com
- doc/README.SUSE: Update information about DUD (jsc#PED-5021)
  Remove a dead link to description of Device Update Disks found
  previously on novell.com. Replace it with a short section summarizing
  what DUD is and reference the mkdud + mksusecd tools and their
  documentation for more information.
- commit 7eeba4e
* Wed Sep 13 2023 jslaby@suse.cz
- config.conf: Drop ppc64 (BE)
- Delete config/ppc64/debug.
- Delete config/ppc64/default.
- Delete config/ppc64/kvmsmall.
- Delete config/ppc64/vanilla.
  The ppc64 builds are being stopped in OBS. Stop producing the big endian
  kernel too.
  See also:
  https://build.opensuse.org/request/show/1110638
  https://lists.opensuse.org/archives/list/factory@lists.opensuse.org/message/G6IJ4GAEHXL23FYDPZ4J6ML4Z2WY7ARF/
  https://lists.opensuse.org/archives/list/factory@lists.opensuse.org/message/SELOVYRDN5ZDDQ2EN7CXNS7BH33XACLU/
- commit 4396bc9
* Wed Sep 13 2023 clin@suse.com
- Update config files: add QSEECOM support for Lenovo X13s (bsc#1215268)
- commit 574861d
* Wed Sep 13 2023 clin@suse.com
- firmware: Add support for Qualcomm UEFI Secure Application
  (bsc#1215268).
- firmware: qcom_scm: Add support for Qualcomm Secure Execution
  Environment SCM interface (bsc#1215268).
- lib/ucs2_string: Add UCS-2 strscpy function (bsc#1215268).
- commit 2eb2d4b
* Tue Sep 12 2023 tiwai@suse.de
- Update config files: enable audio on Lenovo X13s (bsc#1215256)
  Enable CONFIG_SND_SOC_LPASS_*_MACRO for arm64.
- commit 7859b9e
* Tue Sep 12 2023 petr.pavlu@suse.com
- rpm/kernel-binary.spec.in: Drop use of KBUILD_OVERRIDE=1
  Genksyms has functionality to specify an override for each type in
  a symtypes reference file. This override is then used instead of an
  actual type and allows to preserve modversions (CRCs) of symbols that
  reference the type. It is kind of an alternative to doing kABI fix-ups
  with '#ifndef __GENKSYMS__'. The functionality is hidden behind the
  genksyms --preserve option which primarily tells the tool to strictly
  verify modversions against a given reference file or fail.
  Downstream patch patches.suse/genksyms-add-override-flag.diff which is
  present in various kernel-source branches separates the override logic.
  It allows it to be enabled with a new --override flag and used without
  specifying the --preserve option. Setting KBUILD_OVERRIDE=1 in the spec
  file is then a way how the build is told that --override should be
  passed to all invocations of genksyms. This was needed for SUSE kernels
  because their build doesn't use --preserve but instead resulting CRCs
  are later checked by scripts/kabi.pl.
  However, this override functionality was not utilized much in practice
  and the only use currently to be found is in SLE11-SP1-LTSS. It means
  that no one should miss this option and KBUILD_OVERRIDE=1 together with
  patches.suse/genksyms-add-override-flag.diff can be removed.
  Notes for maintainers merging this commit to their branches:
  * Downstream patch patches.suse/genksyms-add-override-flag.diff can be
  dropped after merging this commit.
  * Branch SLE11-SP1-LTSS uses the mentioned override functionality and
  this commit should not be merged to it, or needs to be reverted
  afterwards.
- commit 4aa02b8
* Mon Sep 11 2023 mkubecek@suse.cz
- Update to 6.6-rc1
- drop 47 patches (44 stable, 3 mainline)
  - patches.kernel.org/*
  - patches.rpmify/Revert-kbuild-Hack-for-depmod-not-handling-X.Y-versi.patch
  - patches.rpmify/kbuild-dummy-tools-support-make-MPROFILE_KERNEL-chec.patch
  - patches.suse/wifi-rtw89-Fix-loading-of-compressed-firmware.patch
- refresh
  - patches.suse/0001-bsc-1204315-Disable-sysfb-before-creating-simple-fra.patch
  - patches.suse/0002-efi-Add-an-EFI_SECURE_BOOT-flag-to-indicate-secure-boot-mode.patch
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/wifi-ath11k-add-support-for-suspend-in-power-down-st.patch
- add build failure fix
  - patches.rpmify/kbuild-avoid-long-argument-lists-in-make-modules_ins.patch
- disable ARM architectures (need config update)
- new config options
  - General setup
  - CRASH_HOTPLUG=y
  - CRASH_MAX_MEMORY_RANGES=8192
  - Processor type and features
  - X86_USER_SHADOW_STACK=n
  - Virtualization
  - KVM_PROVE_MMU=n
  - Memory Management options
  - RANDOM_KMALLOC_CACHES=n
  - File systems
  - OVERLAY_FS_DEBUG=n
  - TMPFS_QUOTA=y
  - EROFS_FS_ZIP_DEFLATE=y
  - Security options
  - SECURITY_SELINUX_DEBUG=n
  - LIST_HARDENED=n
  - Library routines
  - SWIOTLB_DYNAMIC=n
  - DMA_NUMA_CMA=y
  - Multiple devices driver support (RAID and LVM)
  - MD_BITMAP_FILE=y
  - Network device support
  - NETCONSOLE_EXTENDED_LOG=n
  - MLX5_MACSEC=y
  - MARVELL_88Q2XXX_PHY=m
  - Hardware Monitoring support
  - SENSORS_HS3001=m
  - SENSORS_MP2975_REGULATOR=y
  - Multifunction device drivers
  - MFD_CS42L43_I2C=m
  - MFD_CS42L43_SDW=m
  - Voltage and Current Regulator Support
  - REGULATOR_AW37503=m
  - REGULATOR_MAX77857=m
  - REGULATOR_RTQ2208=m
  - Multimedia support
  - INTEL_VSC=m
  - VIDEO_CAMERA_SENSOR=y
  - VIDEO_DW9719=m
  - Graphics support
  - DRM_LOONGSON=m
  - FB_DEVICE=y
  - Sound card support
  - SND_HDA_SCODEC_CS35L56_I2C=m
  - SND_HDA_SCODEC_CS35L56_SPI=m
  - SND_HDA_SCODEC_TAS2781_I2C=m
  - SND_SOC_INTEL_AVS_MACH_ES8336=m
  - SND_SOC_INTEL_AVS_MACH_RT5663=m
  - SND_SOC_SOF_AMD_VANGOGH=m
  - SND_SOC_SOF_LUNARLAKE=m
  - SND_SOC_AUDIO_IIO_AUX=n
  - SND_SOC_AW88261=n
  - SND_SOC_CS42L43=m
  - SND_SOC_CS42L43_SDW=m
  - SND_SOC_RT1017_SDCA_SDW=m
  - LED Support
  - LEDS_PCA995X=m
  - LEDS_SIEMENS_SIMATIC_IPC_ELKHARTLAKE=m
  - X86 Platform Specific Device Drivers
  - HP_BIOSCFG=m
  - SIEMENS_SIMATIC_IPC_BATT=m
  - SIEMENS_SIMATIC_IPC_BATT_APOLLOLAKE=m
  - SIEMENS_SIMATIC_IPC_BATT_ELKHARTLAKE=m
  - SIEMENS_SIMATIC_IPC_BATT_F7188X=m
  - SEL3350_PLATFORM=m
  - Industrial I/O support
  - MCP4728=n
  - IRSD200=n
  - PHY Subsystem
  - PHY_RTK_RTD_USB2PHY=m
  - PHY_RTK_RTD_USB3PHY=m
  - Counter support
  - 104_QUAD_8=m
  - INTEL_QEP=m
  - INTERRUPT_CNT=m
  - Misc drivers
  - TOUCHSCREEN_IQS7211=m
  - I2C_ATR=m
  - SPI_CS42L43=n
  - PTP_1588_CLOCK_MOCK=m
  - PINCTRL_CS42L43=m
  - GPIO_DS4520=m
  - HID_GOOGLE_STADIA_FF=m
  - USB_CONFIGFS_F_MIDI2=y
  - XILINX_DMA=m
  - PDS_VFIO_PCI=m
  - XEN_PRIVCMD_IRQFD=y
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - PCI_DYNAMIC_OF_NODES=y
  - REGULATOR_MAX5970=m
  - VIDEO_DS90UB913=m
  - VIDEO_DS90UB953=m
  - VIDEO_DS90UB960=m
  - DRM_PANEL_STARTEK_KD070FHFID015=n
  - DRM_PANEL_VISIONOX_R66451=n
  - LEDS_GROUP_MULTICOLOR=m
  - COMMON_CLK_VC3=m
  - ppc64 / ppc64le
  - FSI_MASTER_I2CR=n
  - INTEGRITY_MACHINE_KEYRING=y
  - ppc64le
  - CRYPTO_CHACHA20_P10=m
  - CRYPTO_POLY1305_P10=m
  - s390x
  - CERT_STORE=y
  - S390_HYPFS=y
  - FUNCTION_GRAPH_RETVAL=y
  - riscv64
  - PREEMPT_DYNAMIC=y
  - RANDOMIZE_BASE=y
  - RISCV_ISA_FALLBACK=y
  - CFI_CLANG=n
  - CAN_SUN4I=m
  - CEC_GPIO=m
  - CLK_STARFIVE_JH7110_STG=m
  - SUN20I_GPADC=n
  - PHY_STARFIVE_JH7110_DPHY_RX=m
  - PHY_STARFIVE_JH7110_PCIE=m
  - PHY_STARFIVE_JH7110_USB=m
  - DEBUG_FORCE_FUNCTION_ALIGN_64B=n
  - DEBUG_PREEMPT=n
  - PREEMPT_TRACER=n
  - CEC_PIN_ERROR_INJ=n
- commit 8c17599
* Fri Sep  8 2023 jslaby@suse.cz
- Linux 6.5.2 (bsc#1012628).
- drm/amdgpu: correct vmhub index in GMC v10/11 (bsc#1012628).
- erofs: ensure that the post-EOF tails are all zeroed
  (bsc#1012628).
- ksmbd: fix wrong DataOffset validation of create context
  (bsc#1012628).
- ksmbd: fix slub overflow in ksmbd_decode_ntlmssp_auth_blob()
  (bsc#1012628).
- ksmbd: replace one-element array with flex-array member in
  struct smb2_ea_info (bsc#1012628).
- ksmbd: reduce descriptor size if remaining bytes is less than
  request size (bsc#1012628).
- ARM: pxa: remove use of symbol_get() (bsc#1012628).
- mmc: au1xmmc: force non-modular build and remove symbol_get
  usage (bsc#1012628).
- net: enetc: use EXPORT_SYMBOL_GPL for enetc_phc_index
  (bsc#1012628).
- rtc: ds1685: use EXPORT_SYMBOL_GPL for ds1685_rtc_poweroff
  (bsc#1012628).
- modules: only allow symbol_get of EXPORT_SYMBOL_GPL modules
  (bsc#1012628).
- USB: serial: option: add Quectel EM05G variant (0x030e)
  (bsc#1012628).
- USB: serial: option: add FOXCONN T99W368/T99W373 product
  (bsc#1012628).
- ALSA: usb-audio: Fix init call orders for UAC1 (bsc#1012628).
- usb: dwc3: meson-g12a: do post init to fix broken usb after
  resumption (bsc#1012628).
- usb: chipidea: imx: improve logic if samsung,picophy-* parameter
  is 0 (bsc#1012628).
- HID: wacom: remove the battery when the EKR is off
  (bsc#1012628).
- staging: rtl8712: fix race condition (bsc#1012628).
- wifi: mt76: mt7921: do not support one stream on secondary
  antenna only (bsc#1012628).
- wifi: mt76: mt7921: fix skb leak by txs missing in AMSDU
  (bsc#1012628).
- wifi: ath11k: Don't drop tx_status when peer cannot be found
  (bsc#1012628).
- wifi: ath11k: Cleanup mac80211 references on failure during
  tx_complete (bsc#1012628).
- serial: qcom-geni: fix opp vote on shutdown (bsc#1012628).
- serial: sc16is7xx: fix broken port 0 uart init (bsc#1012628).
- serial: sc16is7xx: fix bug when first setting GPIO direction
  (bsc#1012628).
- firmware: stratix10-svc: Fix an NULL vs IS_ERR() bug in probe
  (bsc#1012628).
- fsi: master-ast-cf: Add MODULE_FIRMWARE macro (bsc#1012628).
- tcpm: Avoid soft reset when partner does not support get_status
  (bsc#1012628).
- dt-bindings: sc16is7xx: Add property to change GPIO function
  (bsc#1012628).
- tracing: Zero the pipe cpumask on alloc to avoid spurious -EBUSY
  (bsc#1012628).
- nilfs2: fix WARNING in mark_buffer_dirty due to discarded
  buffer reuse (bsc#1012628).
- usb: typec: tcpci: clear the fault status bit (bsc#1012628).
- Rename to
  patches.kernel.org/6.5.2-021-wifi-rtw88-usb-kill-and-free-rx-urbs-on-probe-f.patch.
- Rename to
  patches.kernel.org/6.5.2-034-pinctrl-amd-Don-t-show-Invalid-config-param-err.patch.
- commit e785fd6
* Wed Sep  6 2023 mkubecek@suse.cz
- update patch metadata
- update upstream references
  - patches.rpmify/Revert-kbuild-Hack-for-depmod-not-handling-X.Y-versi.patch
  - patches.rpmify/kbuild-dummy-tools-support-make-MPROFILE_KERNEL-chec.patch
- commit aaab89b
* Wed Sep  6 2023 mkubecek@suse.cz
- config: refresh
- commit bd40664
* Tue Sep  5 2023 msuchanek@suse.de
- Update config files.
  IPR is powerpc-only driver, disable on other architectures.
- commit 62fd4da
* Mon Sep  4 2023 jslaby@suse.cz
- Linux 6.5.1 (bsc#1012628).
- ACPI: thermal: Drop nocrt parameter (bsc#1012628).
- module: Expose module_init_layout_section() (bsc#1012628).
- arm64: module: Use module_init_layout_section() to spot init
  sections (bsc#1012628).
- ARM: module: Use module_init_layout_section() to spot init
  sections (bsc#1012628).
- module/decompress: use vmalloc() for zstd decompression
  workspace (bsc#1012628).
- lockdep: fix static memory detection even more (bsc#1012628).
- kallsyms: Fix kallsyms_selftest failure (bsc#1012628).
- commit d232ff6
* Thu Aug 31 2023 tiwai@suse.de
- firmware: qemu_fw_cfg: Do not hard depend on
  CONFIG_HAS_IOPORT_MAP (bsc#1214773).
- Update config files: enable CONFIG_FW_CFG_SYSFS for armv7hl
- commit b5edcad
* Thu Aug 31 2023 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section
  - patches.suse/pinctrl-amd-Don-t-show-Invalid-config-param-errors.patch
- update upstream references and resort
  - patches.suse/wifi-rtw89-Fix-loading-of-compressed-firmware.patch
  - patches.suse/wifi-rtw88-usb-kill-and-free-rx-urbs-on-probe-failure.patch
- commit de97d09
* Wed Aug 30 2023 jslaby@suse.cz
- rpm/mkspec-dtb: dtbs have moved to vendor sub-directories in 6.5
  By commit 724ba6751532 ("ARM: dts: Move .dts files to vendor
  sub-directories").
  So switch to them.
- rpm/mkspec-dtb: support for nested subdirs
  Commit 724ba6751532 ("ARM: dts: Move .dts files to vendor
  sub-directories") moved the dts to nested subdirs, add a support for
  that. That is, generate a %%dir entry in %%files for them.
- commit 7aee36a
* Wed Aug 30 2023 jslaby@suse.cz
- ipv6: remove hard coded limitation on ipv6_pinfo (ipv6-breakage
  20230829174957.0ae84f41@kernel.org).
- commit 7f2ff2a
* Tue Aug 29 2023 jslaby@suse.cz
- kbuild: dummy-tools: support make MPROFILE_KERNEL checks work
  on BE (ppc64-build-fix).
- Update config files.
  Fix ppc64 build and update configs accordingly (values taken from
  ppc64le).
- commit 6df272d
* Tue Aug 29 2023 mkubecek@suse.cz
- series.conf: cleanup
- move an unsortable patch out of sorted section
  - patches.suse/Revert-101bd907b424-misc-rtsx-judge-ASPM-Mode-to-set.patch
- update upstream references and move into sorted section
  - patches.suse/wifi-rtw89-Fix-loading-of-compressed-firmware.patch
  - patches.suse/wifi-rtw88-usb-kill-and-free-rx-urbs-on-probe-failure.patch
- commit 940b0a2
* Tue Aug 29 2023 mkubecek@suse.cz
- config: refresh
- commit 1042651
* Mon Aug 28 2023 jack@suse.cz
- patches.suse/add-suse-supported-flag.patch: Add CONFIG_MODULES dependency
- commit d5be025
* Mon Aug 28 2023 mkubecek@suse.cz
- Update to 6.5 final
- refresh configs (headers only)
- commit 2844291
* Fri Aug 25 2023 msuchanek@suse.de
- Revert 101bd907b424 ("misc: rtsx: judge ASPM Mode to set
  PETXCFG Reg") (boo#1214428 boo#1214397).
- commit 1b02b15
* Thu Aug 24 2023 msuchanek@suse.de
- Update ppc64 config
  - CONFIG_COMPAT_32BIT_TIME=n
  - CONFIG_IMA_ARCH_POLICY=y
  - CONFIG_IMA_DISABLE_HTABLE=y
  - CONFIG_IMA_KEXEC=y
  - CONFIG_IMA_KEYRINGS_PERMIT_SIGNED_BY_BUILTIN_OR_SECONDARY=y
  - CONFIG_LOAD_PPC_KEYS=y
  - CONFIG_PPC_SECURE_BOOT=y
  - CONFIG_PPC_SECVAR_SYSFS=y
- commit 2b1052f
* Thu Aug 24 2023 tiwai@suse.de
- wifi: rtw88: usb: kill and free rx urbs on probe failure
  (bsc#1214385).
- commit 5c3979f
* Wed Aug 23 2023 msuchanek@suse.de
- old-flavors: Drop 2.6 kernels.
  2.6 based kernels are EOL, upgrading from them is no longer suported.
- commit 7bb5087
* Sun Aug 20 2023 mkubecek@suse.cz
- Update to 6.5-rc7
- commit 869afb7
* Fri Aug 18 2023 msuchanek@suse.de
- mkspec: Allow unsupported KMPs (bsc#1214386)
- commit 55d8b82
* Fri Aug 18 2023 msuchanek@suse.de
- check-for-config-changes: ignore BUILTIN_RETURN_ADDRESS_STRIPS_PAC (bsc#1214380).
  gcc7 on SLE 15 does not support this while later gcc does.
- commit 5b41c27
* Wed Aug 16 2023 msuchanek@suse.de
- kernel-binary: Common dependencies cleanup
  Common dependencies are copied to a subpackage, there is no need for
  copying defines or build dependencies there.
- commit 254b03c
* Wed Aug 16 2023 msuchanek@suse.de
- kernel-binary: Drop code for kerntypes support
  Kerntypes was a SUSE-specific feature dropped before SLE 12.
- commit 2c37773
* Sun Aug 13 2023 mkubecek@suse.cz
- Update to 6.5-rc6
- update configs
  - x86
  - GDS_FORCE_MITIGATION=n
  - x86_64
  - CPU_SRSO=y
- commit c65258c
* Sat Aug 12 2023 tiwai@suse.de
- pinctrl: amd: Don't show `Invalid config param` errors
  (bsc#1214212).
- commit e95f7e7
* Mon Aug  7 2023 mkubecek@suse.cz
- rpm/config.sh: switch to openSUSE.org repos for IBS
  Mirrored openSUSE repositories are long term more reliable than
  SUSE:Factory:HEAD we use now for IBS builds. Dropping the IBS_PROJECT*
  variables is the simplest way to switch to them as MyBS.pm prepends
  "openSUSE.org:" to the corresponding OBS_PROJECT* variable in their
  absence.
  This is a combination of kernel-source commits 21cafd1fd12a
  ("rpm/config.sh: switch to openSUSE.org repos for IBS") and 294d54140dd0
  ("rpm/config.sh: remove IBS repos completely") from stable branch.
- commit 997a7e4
* Mon Aug  7 2023 mkubecek@suse.cz
- Update to 6.5-rc5
- commit b685771
* Sun Jul 30 2023 mkubecek@suse.cz
- Update to 6.5-rc4
- refresh configs
- commit 2390421
* Fri Jul 28 2023 msuchanek@suse.de
- kernel-binary.spec.in: Remove superfluous %%%% in Supplements
  Fixes: 02b7735e0caf ("rpm/kernel-binary.spec.in: Add Enhances and Supplements tags to in-tree KMPs")
- commit 264db74
* Thu Jul 27 2023 tiwai@suse.de
- wifi: rtw89: Fix loading of compressed firmware (bsc#1212808).
- commit 6cc40be
* Wed Jul 26 2023 tiwai@suse.de
- bus: mhi: host: add destroy_device argument to mhi_power_down()
  (bsc#1207948).
- commit fad4ac5
* Wed Jul 26 2023 tiwai@suse.de
- wifi: ath11k: remove MHI LOOPBACK channels (bsc#1207948).
- wifi: ath11k: handle thermal device registeration together
  with MAC (bsc#1207948).
- wifi: ath11k: handle irq enable/disable in several code path
  (bsc#1207948).
- wifi: ath11k: add support for suspend in power down state
  (bsc#1207948).
- bus: mhi: add new interfaces to handle MHI channels directly
  (bsc#1207948).
- commit 5408d73
* Mon Jul 24 2023 mkubecek@suse.cz
- Delete patches.suse/Revert-io_uring-Adjust-mapping-wrt-architecture-alia.patch.
  As confirmed by JiĹ™Ă­ SlabĂ˝, the issue should be fixed by mainline commit
  32832a407a71 ("io_uring: Fix io_uring mmap() by using architecture-provided
  get_unmapped_area()") present in 6.5-rc3 so that the revert is no longer
  needed.
- commit c2a47b2
* Mon Jul 24 2023 jslaby@suse.cz
- Update config files. (bsc#1213592)
  Disable old unmaintained serial drivers
- commit 6254189
* Mon Jul 24 2023 mkubecek@suse.cz
- Update to 6.5-rc2
- disable
  patches.suse/Revert-io_uring-Adjust-mapping-wrt-architecture-alia.patch
- commit de7235b
* Sun Jul 23 2023 schwab@suse.de
- rpm/mkspec-dtb: add riscv64 dtb-thead subpackage
- commit 5f4d0a7
* Sun Jul 23 2023 schwab@suse.de
- rpm/mkspec-dtb: add riscv64 dtb-allwinner subpackage
- commit ec82ffc
* Tue Jul 18 2023 msuchanek@suse.de
- Revert "kbuild: Hack for depmod not handling X.Y versions" (bsc#1212835).
- Refresh patches.rpmify/usrmerge-Adjust-module-path-in-the-kernel-sources.patch.
- commit 8a9c423
* Tue Jul 18 2023 jslaby@suse.cz
- ACPI: video: Add backlight=native DMI quirk for Lenovo Ideapad
  Z470 (bsc#1208724).
- commit 54e3bad
* Mon Jul 17 2023 msuchanek@suse.de
- rpm: Update dependency to match current kmod.
- Refresh patches.rpmify/usrmerge-Adjust-module-path-in-the-kernel-sources.patch.
  Update to match current kmod (bsc#1212835).
- commit d687dc3
* Mon Jul 17 2023 mkubecek@suse.cz
- Update to 6.5-rc2
- eliminate 1 patch
  - patches.rpmify/objtool-initialize-all-of-struct-elf.patch (9f71fbcde282)
- commit c159bc5
* Thu Jul 13 2023 msuchanek@suse.de
- depmod: Handle installing modules under a prefix (bsc#1212835).
- commit b2abe86
* Wed Jul 12 2023 jgross@suse.com
- Restore kABI for NVidia vGPU driver (bsc#1210825).
- commit 01c9bbd
* Mon Jul 10 2023 schwab@suse.de
- rpm/check-for-config-changes: ignore also RISCV_ISA_* and DYNAMIC_SIGFRAME
  They depend on CONFIG_TOOLCHAIN_HAS_*.
- commit 1007103
* Mon Jul 10 2023 mkubecek@suse.cz
- refresh vanilla configs
- commit ab4066a
* Mon Jul 10 2023 jslaby@suse.cz
- Delete
  patches.suse/Revert-x86-mm-try-VMA-lock-based-page-fault-handling.patch.
- Update config files.
  It was fixed in 6.5-rc1 by commits:
  fb49c455 fork: lock VMAs of the parent process when forking
  2b4f3b49 fork: lock VMAs of the parent process when forking
  1c7873e3 mm: lock newly mapped VMA with corrected ordering
  33313a74 mm: lock newly mapped VMA which can be modified after it becomes visible
  c137381f mm: lock a vma before stack expansion
  So drop the downstream revert and reset the configs -- leave STATS off
  as per default.
- commit 50f64ca
* Mon Jul 10 2023 mkubecek@suse.cz
- Update to 6.5-rc1
- drop 34 patches (33 stable, 1 mainline)
  - patches.kernel.org/*
  - patches.suse/HID-microsoft-Add-rumble-support-to-latest-xbox-cont.patch
- refresh
  - patches.suse/0003-efi-Lock-down-the-kernel-if-booted-in-secure-boot-mode.patch
  - patches.suse/0004-efi-Lock-down-the-kernel-at-the-integrity-level-if-b.patch
  - patches.suse/HID-microsoft-Add-rumble-support-to-latest-xbox-cont.patch
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/iwlwifi-cfg-Add-missing-MODULE_FIRMWARE-for-pnvm.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- add build failure fix
  - patches.rpmify/objtool-initialize-all-of-struct-elf.patch
- disable ARM architectures (need config update)
- new config options
  - General setup
  - CACHESTAT_SYSCALL=y
  - Power management and ACPI options
  - X86_AMD_PSTATE_DEFAULT_MODE=3
  - Memory Management options
  - ZSWAP_EXCLUSIVE_LOADS_DEFAULT_ON=n
  - SLAB_DEPRECATED=n
  - Cryptographic API
  - CRYPTO_JITTERENTROPY_TESTINTERFACE=n
  - Kernel hacking
  - HARDLOCKUP_DETECTOR_PREFER_BUDDY=n
  - WQ_CPU_INTENSIVE_REPORT=n
  - FUNCTION_GRAPH_RETVAL=y
  - FPROBE_EVENTS=y
  - PROBE_EVENTS_BTF_ARGS=y
  - PCI support
  - PCI_EPF_MHI=m
  - CXL_PMU=m
  - Misc devices
  - INTEL_MEI_GSC_PROXY=m
  - TPS6594_ESM=m
  - TPS6594_PFSM=m
  - Network device support
  - CAN_F81604=m
  - PPPOE_HASH_BITS_1=n
  - PPPOE_HASH_BITS_2=n
  - PPPOE_HASH_BITS_4=y
  - PPPOE_HASH_BITS_8=n
  - RTW88_8723DS=m
  - RTW89_8851BE=m
  - Hardware Monitoring support
  - MAX31827=m
  - SENSORS_HP_WMI=m
  - Multifunction device drivers
  - MFD_MAX77541=n
  - MFD_TPS6594_I2C=m
  - MFD_TPS6594_SPI=m
  - Sound card support
  - SND_SEQ_UMP=y
  - SND_UMP_LEGACY_RAWMIDI=y
  - SND_PCMTEST=m
  - SND_USB_AUDIO_MIDI_V2=y
  - SND_SOC_CHV3_I2S=m
  - SND_SOC_CHV3_CODEC=m
  - SND_SOC_MAX98388=m
  - SND_SOC_RT722_SDCA_SDW=m
  - SND_SOC_TAS2781_I2C=n
  - SND_SOC_WSA884X=n
  - HID bus support
  - HID_NVIDIA_SHIELD=m
  - NVIDIA_SHIELD_FF=y
  - USB support
  - USB_CDNS2_UDC=m
  - TYPEC_MUX_NB7VPQ904M=m
  - LED Support
  - LEDS_AW200XX=m
  - LEDS_CHT_WCOVE=m
  - LEDS_SIEMENS_SIMATIC_IPC_APOLLOLAKE=m
  - LEDS_SIEMENS_SIMATIC_IPC_F7188X=m
  - X86 Platform Specific Device Drivers
  - YOGABOOK=m
  - AMD_PMF_DEBUG=n
  - Industrial I/O support
  - ROHM_BU27008=m
  - OPT4001=n
  - X9250=m
  - MPRLS0025PA=n
  - Misc devices
  - INTEL_MEI_GSC_PROXY=m
  - TPS6594_ESM=m
  - TPS6594_PFSM=m
  - THERMAL_DEFAULT_GOV_BANG_BANG=n
  - REGULATOR_RAA215300=m
  - VIDEO_OV01A10=m
  - DRM_AMDGPU_WERROR=n
  - PDS_VDPA=m
  - INTEL_RAPL_TPMI=m
  - CXL_PMU=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - MFD_MAX5970=m
  - MFD_RK8XX_I2C=n
  - MFD_RK8XX_SPI=n
  - REGULATOR_TPS6287X=m
  - REGULATOR_TPS6594=m
  - DRM_PANEL_SAMSUNG_S6D7AA0=n
  - i386
  - SND_SOC_SSM3515=n
  - i386/default
  - TOUCHSCREEN_MK712=m
  - s390x
  - RFKILL_GPIO=m
  - TI_ST=m
  - GP_PCI1XXXX=m
  - MDIO_GPIO=m
  - ISDN=n
  - I2C_CBUS_GPIO=m
  - I2C_GPIO=m
  - I2C_GPIO_FAULT_INJECTOR=n
  - GPIOLIB_FASTPATH_LIMIT=512
  - DEBUG_GPIO=n
  - GPIO_SYSFS=y
  - GPIO_CDEV_V1=y
  - GPIO_DWAPB=n
  - GPIO_GENERIC_PLATFORM=m
  - GPIO_MB86S7X=n
  - GPIO_AMD_FCH=m
  - GPIO_FXL6408=m
  - GPIO_MAX7300=m
  - GPIO_MAX732X=m
  - GPIO_PCA953X=m
  - GPIO_PCA953X_IRQ=y
  - GPIO_PCA9570=m
  - GPIO_PCF857X=m
  - GPIO_TPIC2810=m
  - GPIO_BT8XX=n
  - GPIO_PCI_IDIO_16=m
  - GPIO_PCIE_IDIO_24=m
  - GPIO_RDC321X=n
  - GPIO_AGGREGATOR=m
  - GPIO_LATCH=m
  - GPIO_MOCKUP=m
  - GPIO_VIRTIO=m
  - GPIO_SIM=m
  - SENSORS_LTC2992=n
  - SENSORS_SHT15=m
  - MEN_A21_WDT=m
  - SSB_DRIVER_GPIO=y
  - TPS65010=m
  - REGULATOR_GPIO=m
  - REGULATOR_TPS65132=m
  - FB_SSD1307=n
  - HD44780=m
  - PANEL_CHANGE_MESSAGE=n
  - EXTCON_GPIO=m
  - EXTCON_MAX3355=m
  - EXTCON_PTN5150=m
  - EXTCON_USB_GPIO=n
  - MUX_GPIO=n
  - s390x/zfcpdump
  - NVME_TARGET=y
  - NVME_TARGET_LOOP=y
  - NVME_TARGET_FC=y
  - NVME_TARGET_AUTH=n
  - NVME_MULTIPATH=y
  - NVME_VERBOSE_ERRORS=n
  - NVME_AUTH=n
  - NVME_TARGET_PASSTHRU=n
  - MOST=n
  - riscv64
  - LD_DEAD_CODE_DATA_ELIMINATION=n
  - ARCH_THEAD=y
  - IRQ_STACKS=y
  - THREAD_SIZE_ORDER=2
  - SUSPEND=y
  - SUSPEND_SKIP_SYNC=n
  - PM_AUTOSLEEP=n
  - PM_USERSPACE_AUTOSLEEP=n
  - PM_WAKELOCKS=n
  - PM_TEST_SUSPEND=n
  - ACPI=y
  - ACPI_DEBUGGER=n
  - ACPI_SPCR_TABLE=y
  - ACPI_EC_DEBUGFS=m
  - ACPI_AC=m
  - ACPI_BATTERY=m
  - ACPI_BUTTON=m
  - ACPI_TINY_POWER_BUTTON=m
  - ACPI_TINY_POWER_BUTTON_SIGNAL=38
  - ACPI_VIDEO=m
  - ACPI_FAN=m
  - ACPI_TAD=m
  - ACPI_DOCK=y
  - ACPI_IPMI=m
  - ACPI_CUSTOM_DSDT_FILE=""
  - ACPI_DEBUG=y
  - ACPI_PCI_SLOT=y
  - ACPI_CONTAINER=y
  - ACPI_HED=y
  - ACPI_CUSTOM_METHOD=m
  - ACPI_NFIT=m
  - NFIT_SECURITY_DEBUG=n
  - ACPI_CONFIGFS=m
  - ACPI_PFRUT=m
  - ACPI_FFH=y
  - PMIC_OPREGION=y
  - BT_HCIUART_RTL=y
  - PCIE_EDR=y
  - HOTPLUG_PCI_ACPI=y
  - HOTPLUG_PCI_ACPI_IBM=m
  - CXL_ACPI=m
  - FW_CACHE=y
  - ISCSI_IBFT=m
  - EFI_CUSTOM_SSDT_OVERLAYS=y
  - PNP_DEBUG_MESSAGES=n
  - ATA_ACPI=y
  - SATA_ZPODD=y
  - PATA_ACPI=m
  - NET_SB1000=n
  - FUJITSU_ES=m
  - TOUCHSCREEN_CHIPONE_ICN8505=m
  - INPUT_SOC_BUTTON_ARRAY=m
  - SERIAL_8250_PNP=y
  - TCG_INFINEON=m
  - ACPI_I2C_OPREGIOSENSORS_ACPI_POWERN=y
  - I2C_AMD_MP2=m
  - I2C_SCMI=m
  - SPI_RZV2M_CSI=m
  - PINCTRL_AMD=y
  - GPIO_AMDPT=m
  - SENSORS_NCT6775=m
  - SENSORS_ACPI_POWER=m
  - WDAT_WDT=m
  - IR_ENE=m
  - IR_FINTEK=m
  - IR_ITE_CIR=m
  - IR_NUVOTON=m
  - VIDEO_OV2740=m
  - VIDEO_OV9734=m
  - DRM_SHMOBILE=n
  - SND_HDA_SCODEC_CS35L41_I2C=m
  - SND_HDA_SCODEC_CS35L41_SPI=m
  - SND_SOC_AMD_CZ_DA7219MX98357_MACH=m
  - SND_SOC_AMD_ST_ES8336_MACH=m
  - SND_SOC_SOF_ACPI=m
  - SND_SOC_STARFIVE=m
  - SND_SOC_JH7110_TDM=m
  - SND_SOC_SSM3515=n
  - I2C_HID_ACPI=m
  - USB_CDNS3_PCI_WRAP=m
  - USB_CDNS3_STARFIVE=m
  - USB_CDNSP_PCI=m
  - USB_CDNSP_HOST=y
  - UCSI_ACPI=m
  - MMC_SDHCI_ACPI=m
  - VMGENID=m
  - PCC=y
  - ACPI_ALS=m
  - PWM_MICROCHIP_CORE=m
  - INTEL_TH_ACPI=m
  - CRYPTO_DEV_JH7110=m
  - PER_VMA_LOCK_STATS=y
  - HARDLOCKUP_DETECTOR=y
  - BOOTPARAM_HARDLOCKUP_PANIC=y
  - ACPI_PCC=y
  - SENSORS_XGENE=m
- commit fe612b0
* Mon Jul  3 2023 msuchanek@suse.de
- Remove more packaging cruft for SLE < 12 SP3
- commit a16781c
* Mon Jul  3 2023 jslaby@suse.cz
- Linux 6.4.1 (bsc#1012628).
- x86/microcode/AMD: Load late on both threads too (bsc#1012628).
- x86/smp: Make stop_other_cpus() more robust (bsc#1012628).
- x86/smp: Dont access non-existing CPUID leaf (bsc#1012628).
- x86/smp: Remove pointless wmb()s from native_stop_other_cpus()
  (bsc#1012628).
- x86/smp: Use dedicated cache-line for mwait_play_dead()
  (bsc#1012628).
- x86/smp: Cure kexec() vs. mwait_play_dead() breakage
  (bsc#1012628).
- cpufreq: amd-pstate: Make amd-pstate EPP driver name hyphenated
  (bsc#1012628).
- can: isotp: isotp_sendmsg(): fix return error fix on TX path
  (bsc#1012628).
- maple_tree: fix potential out-of-bounds access in
  mas_wr_end_piv() (bsc#1012628).
- mm: introduce new 'lock_mm_and_find_vma()' page fault helper
  (bsc#1012628).
- mm: make the page fault mmap locking killable (bsc#1012628).
- arm64/mm: Convert to using lock_mm_and_find_vma() (bsc#1012628).
- powerpc/mm: Convert to using lock_mm_and_find_vma()
  (bsc#1012628).
- mips/mm: Convert to using lock_mm_and_find_vma() (bsc#1012628).
- riscv/mm: Convert to using lock_mm_and_find_vma() (bsc#1012628).
- arm/mm: Convert to using lock_mm_and_find_vma() (bsc#1012628).
- mm/fault: convert remaining simple cases to
  lock_mm_and_find_vma() (bsc#1012628).
- powerpc/mm: convert coprocessor fault to lock_mm_and_find_vma()
  (bsc#1012628).
- mm: make find_extend_vma() fail if write lock not held
  (bsc#1012628).
- execve: expand new process stack manually ahead of time
  (bsc#1012628).
- mm: always expand the stack with the mmap write lock held
  (bsc#1012628).
- HID: wacom: Use ktime_t rather than int when dealing with
  timestamps (bsc#1012628).
- gup: add warning if some caller would seem to want stack
  expansion (bsc#1012628).
- mm/khugepaged: fix regression in collapse_file() (bsc#1012628).
- fbdev: fix potential OOB read in fast_imageblit() (bsc#1012628).
- HID: hidraw: fix data race on device refcount (bsc#1012628).
- HID: logitech-hidpp: add HIDPP_QUIRK_DELAYED_INIT for the T651
  (bsc#1012628).
- Revert "thermal/drivers/mediatek: Use devm_of_iomap to avoid
  resource leak in mtk_thermal_probe" (bsc#1012628).
- sparc32: fix lock_mm_and_find_vma() conversion (bsc#1012628).
- parisc: fix expand_stack() conversion (bsc#1012628).
- csky: fix up lock_mm_and_find_vma() conversion (bsc#1012628).
- xtensa: fix NOMMU build with lock_mm_and_find_vma() conversion
  (bsc#1012628).
- Refresh
  patches.suse/Revert-x86-mm-try-VMA-lock-based-page-fault-handling.patch.
- Update config files (CONFIG_LOCK_MM_AND_FIND_VMA=y).
  There is no choice.
- commit eb53035
* Fri Jun 30 2023 msuchanek@suse.de
- Get module prefix from kmod (bsc#1212835).
- Refresh patches.rpmify/usrmerge-Adjust-module-path-in-the-kernel-sources.patch.
  Get module prefix from kmod (bsc#1212835).
- commit f6691b0
* Fri Jun 30 2023 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section:
  - patches.suse/HID-microsoft-Add-rumble-support-to-latest-xbox-cont.patch
- commit ce0878a
* Fri Jun 30 2023 mkubecek@suse.cz
- rpm/check-for-config-changes: ignore also PAHOLE_HAS_*
  We now also have options like CONFIG_PAHOLE_HAS_LANG_EXCLUDE.
- commit 86b52c1
* Thu Jun 29 2023 msuchanek@suse.de
- usrmerge: Adjust module path in the kernel sources (bsc#1212835).
  With the module path adjustment applied as source patch only
  ALP/Tumbleweed kernel built on SLE/Leap needs the path changed back to
  non-usrmerged.
- commit dd9a820
* Thu Jun 29 2023 jslaby@suse.cz
- Revert "x86/mm: try VMA lock-based page fault handling first"
  (bsc#1212775).
- Update config files.
- commit 43c9b6b
* Wed Jun 28 2023 jslaby@suse.cz
- Revert "io_uring: Adjust mapping wrt architecture aliasing
  requirements" (bsc#1212773).
- commit d2e19af
* Mon Jun 26 2023 msuchanek@suse.de
- kernel-docs: Use python3 together with python3-Sphinx (bsc#1212741).
- commit 95a40a6
* Mon Jun 26 2023 jslaby@suse.cz
- Refresh
  patches.suse/HID-microsoft-Add-rumble-support-to-latest-xbox-cont.patch.
  Update upstream status and move to upstream-soon section.
- commit 1a327c7
* Mon Jun 26 2023 mkubecek@suse.cz
- Update to 6.4 final
- refresh configs (headers only)
- commit 4b7bbac
* Sun Jun 18 2023 mkubecek@suse.cz
- Update to 6.4-rc7
- commit a8abd7d
* Thu Jun 15 2023 msuchanek@suse.de
- kernel-docs: Add buildrequires on python3-base when using python3
  The python3 binary is provided by python3-base.
- commit c5df526
* Tue Jun 13 2023 dmueller@suse.com
- config.conf: reenable armv6 configs
- Update config files (same settings like armv7hl)
- commit d3ab761
* Sun Jun 11 2023 mkubecek@suse.cz
- Update to 6.4-rc6
- refresh configs
- commit e5bdb6f
* Sun Jun 11 2023 mkubecek@suse.cz
- config: refresh arm64/vanilla
- commit 3087200
* Sun Jun 11 2023 dmueller@suse.com
- config.conf: reenable armv7hl
- Update config files for armv7hl/6.4.0rc6
- commit 782615b
* Sun Jun 11 2023 dmueller@suse.com
- config.conf: Reenable arm64 configs
- config: Update to 6.4-rc5:
  * this includes lowering the ARCH_FORCE_MAX_ORDER by one given the
    change of definition in mainline commit 23baf831a32c
    ("mm, treewide: redefine MAX_ORDER sanely")
  * config change from x86_64 adopted for arm64. Enabled all erratas,
    rest compile as modules
- commit 084e86f
* Fri Jun  9 2023 msuchanek@suse.de
- Move setting %%%%build_html to config.sh
- commit dd39da3
* Fri Jun  9 2023 msuchanek@suse.de
- Fix missing top level chapter numbers on SLE12 SP5 (bsc#1212158).
- commit 7ebcbd5
* Thu Jun  8 2023 msuchanek@suse.de
- Move setting %%%%split_optional to config.sh
- commit 8b0828d
* Thu Jun  8 2023 msuchanek@suse.de
- Move setting %%%%supported_modules_check to config.sh
- commit 3fcb4e0
* Thu Jun  8 2023 msuchanek@suse.de
- rpm/kernel-docs.spec.in: pass PYTHON=python3 to fix build error (bsc#1160435)
- commit 799f050
* Thu Jun  8 2023 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Fix compatibility wth newer rpm
- commit 334fb4d
* Wed Jun  7 2023 msuchanek@suse.de
- Also include kernel-docs build requirements for ALP
- commit 114d088
* Wed Jun  7 2023 msuchanek@suse.de
- Move the kernel-binary conflicts out of the spec file.
  Thie list of conflicting packages varies per release.
  To reduce merge conflicts move the list out of the spec file.
- commit 4d81125
* Wed Jun  7 2023 msuchanek@suse.de
- Avoid unsuported tar parameter on SLE12
- commit f11765a
* Wed Jun  7 2023 msuchanek@suse.de
- Move obsolete KMP list into a separate file.
  The list of obsoleted KMPs varies per release, move it out of the spec
  file.
- commit 016bc55
* Wed Jun  7 2023 msuchanek@suse.de
- Trim obsolete KMP list.
  SLE11 is out of support, we do not need to handle upgrading from SLE11
  SP1.
- commit 08819bb
* Wed Jun  7 2023 msuchanek@suse.de
- Generalize kernel-docs build requirements.
- Generalize kernel-doc build requirements.
- commit c80fe12
* Tue Jun  6 2023 msuchanek@suse.de
- Refresh patches.suse/add-suse-supported-flag.patch.
  Fix table alignment.
- commit 819a7ec
* Tue Jun  6 2023 msuchanek@suse.de
- kernel-binary: Add back kernel-default-base guarded by option
  Add configsh option for splitting off kernel-default-base, and for
  not signing the kernel on non-efi
- commit 28c22af
* Sun Jun  4 2023 mkubecek@suse.cz
- Update to 6.4-rc5
- refresh configs
- commit 2cab33e
* Fri Jun  2 2023 msuchanek@suse.de
- usrmerge: Compatibility with earlier rpm (boo#1211796)
- commit 2191d32
* Thu Jun  1 2023 msuchanek@suse.de
- Fix usrmerge error (boo#1211796)
- commit da84579
* Thu Jun  1 2023 jslaby@suse.cz
- Update config files -- X86_KERNEL_IBT=y (bsc#1211890).
- commit 7a5e7e4
* Mon May 29 2023 msuchanek@suse.de
- Remove usrmerge compatibility symlink in buildroot (boo#1211796)
  Besides Makefile depmod.sh needs to be patched to prefix /lib/modules.
  Requires corresponding patch to kmod.
- commit b8e00c5
* Sun May 28 2023 mkubecek@suse.cz
- Update to 6.4-rc4
- refresh configs
- commit 2e9e157
* Fri May 26 2023 mkoutny@suse.com
- supported.conf: Add a guard for unsupported rose module
- commit ffa03aa
* Fri May 26 2023 jlee@suse.com
- Revert "Disable lockdown. (bsc#1209006)"
  This reverts commit 44ca817f15b215421a4c788790dd5351c186d1df.
  Let's enable kernel lockdown function in master branch again.
  This time we will test with NVIDIA KMP.
- commit 0d0e269
* Fri May 26 2023 jlee@suse.com
- Revert "Revert "Update config files." (bsc#1211166)"
  This reverts commit 944713a45f59680c926e1a4d51798970f8af1767.
  Let's enable kernel lockdown function in master branch again.
  This time we will test with NVIDIA KMP.
- commit 1bf0f73
* Thu May 25 2023 mkoutny@suse.com
- supported.conf: Add guard against future CVE-2016-3695 (bsc#1023051)
  Just add more comment in support.conf, no change.
- commit 3326f7f
* Mon May 22 2023 msuchanek@suse.de
- kernel-source: Remove unused macro variant_symbols
- commit 915ac72
* Sun May 21 2023 mkubecek@suse.cz
- Update to 6.4-rc3
- eliminate 1 patch
  - patches.suse/SUNRPC-Fix-encoding-of-rejected-RPCs.patch (29cd2927fb91)
- update configs
  - VFIO_CCW=m (s390x only)
- commit 02bdb8c
* Sun May 14 2023 mkubecek@suse.cz
- Update to 6.4-rc2
- eliminate 1 patch
  - patches.suse/0001-firmware-sysfb-Fix-VESA-format-selection.patch
- commit 679133f
* Fri May 12 2023 tiwai@suse.de
- HID: microsoft: Add rumble support to latest xbox controllers
  (bsc#1211280).
- commit 512d474
* Fri May 12 2023 dmueller@suse.com
- config: align all architectures on CONFIG_HZ=300 (bsc#1196438)
- commit 9b7c645
* Thu May 11 2023 tzimmermann@suse.com
- firmware/sysfb: Fix VESA format selection (bsc#1211119)
- commit 975df95
* Tue May  9 2023 schwab@suse.de
- rpm/constraints.in: Increase disk size constraint for riscv64 to 52GB
- commit 1c1a4cd
* Tue May  9 2023 jslaby@suse.cz
- Revert "Update config files." (bsc#1211166)
  This reverts commit 90a46594a115a4abf9381bd4c327fd875ac0da0b.
  Lockdown is not ready and was disabled in stable. Since this is still
  not resolved in 6.3/6.4-rc, let's disable it in master completely too.
  And let's retry once everything is ready.
- commit f3816e6
* Mon May  8 2023 mkubecek@suse.cz
- config: use ARCH_FORCE_MAX_ORDER=8 on ppc64/ppc64le
  Mainline commit 23baf831a32c ("mm, treewide: redefine MAX_ORDER sanely")
  redefined the meaning of MAX_ORDER, and therefore also related
  ARCH_FORCE_MAX_ORDER config option to be one lower than the old value so
  that having ARCH_FORCE_MAX_ORDER=9 with 64KB pages results in build time
  error "Allocator MAX_ORDER exceeds SECTION_SIZE".
  Update the values on ppc64 and ppc64le architectures from 9 to 8 to
  preserve the old behaviour and fix the build error.
- commit 668187d
* Sun May  7 2023 mkubecek@suse.cz
- Update to 6.4-rc1
- drop 14 patches (12 stable, 2 mainline)
  - patches.kernel.org/*
  - patches.suse/ath11k-pci-Add-more-MODULE_FIRMWARE-entries.patch
  - patches.suse/usbtv-usbtv_set_regs-the-pipe-is-output.patch
- refresh
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/0001-regulator-mt6360-Add-OF-match-table.patch
  - patches.suse/0001-security-lockdown-expose-a-hook-to-lock-the-kernel-down.patch
  - patches.suse/0002-regulator-mt6358-Add-OF-match-table.patch
  - patches.suse/0003-regulator-mt6323-Add-OF-match-table.patch
  - patches.suse/iwlwifi-cfg-Add-missing-MODULE_FIRMWARE-for-pnvm.patch
- disable ARM architectures (need config update)
- new config options
  - Processor type and features
  - ADDRESS_MASKING=y
  - Enable loadable module support
  - MODULE_DEBUG=n
  - Memory Management options
  - DMAPOOL_TEST=n
  - Networking support
  - MAX_SKB_FRAGS=17
  - BT_NXPUART=m
  - File systems
  - XFS_SUPPORT_ASCII_CI=y
  - Security options
  - INTEGRITY_CA_MACHINE_KEYRING=n
  - Kernel hacking
  - PER_VMA_LOCK_STATS=y
  - USER_EVENTS=n
  - FAULT_INJECTION_CONFIGFS=n
  - Generic Driver Options
  - FW_LOADER_DEBUG=y
  - FW_DEVLINK_SYNC_STATE_TIMEOUT=n
  - Block devices
  - BLKDEV_UBLK_LEGACY_OPCODES=y
  - Serial ATA and Parallel ATA drivers (libata)
  - PATA_PARPORT_BPCK6=m
  - Generic Target Core Mod (TCM) and ConfigFS Infrastructure
  - REMOTE_TARGET=m
  - Network device support
  - NET_DSA_MT7530_MDIO=m
  - NET_DSA_MT7530_MMIO=m
  - NET_DSA_QCA8K_LEDS_SUPPORT=y
  - PDS_CORE=m
  - MICROCHIP_T1S_PHY=m
  - NXP_CBTX_PHY=m
  - RTW88_8822BS=m
  - RTW88_8822CS=m
  - RTW88_8821CS=m
  - GPIO Support
  - GPIO_FXL6408=m
  - GPIO_ELKHARTLAKE=m
  - Voltage and Current Regulator Support
  - REGULATOR_RT4803=m
  - REGULATOR_RT5739=m
  - Sound card support
  - SND_SOC_CS35L56_I2C=m
  - SND_SOC_CS35L56_SPI=m
  - SND_SOC_CS35L56_SDW=m
  - SND_SOC_MAX98363=m
  - SND_SOC_RT712_SDCA_DMIC_SDW=m
  - X86 Platform Specific Device Drivers
  - LENOVO_YMC=m
  - INTEL_BYTCRC_PWRSRC=m
  - MSI_EC=m
  - Industrial I/O support
  - TI_ADS1100=n
  - ROHM_BU27034=n
  - NVMEM Support
  - NVMEM_LAYOUT_SL28_VPD=m
  - NVMEM_LAYOUT_ONIE_TLV=m
  - Misc drivers
  - TOUCHSCREEN_NOVATEK_NVT_TS=m
  - PTP_DFL_TOD=m
  - SENSORS_ACBEL_FSG032=m
  - DRM_VIRTIO_GPU_KMS=y
  - DRM_ACCEL_QAIC=m
  - I2C_HID_OF=m
  - LEDS_BD2606MVV=m
  - HYPERV_VTL_MODE=n
  - SOUNDWIRE_AMD=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - MFD_MAX597X=m
  - REGULATOR_MAX597X=m
  - DRM_PANEL_MAGNACHIP_D53E6EA8966=n
  - DRM_PANEL_NOVATEK_NT36523=n
  - DRM_PANEL_SONY_TD4353_JDI=n
  - DRM_SAMSUNG_DSIM=n
  - UCSI_PMIC_GLINK=m
  - COMMON_CLK_SI521XX=m
  - i386
  - CAN_BXCAN=m
  - ppc64le
  - CRYPTO_AES_GCM_P10=m
  - s390x
  - SECRETMEM=y
  - SCSI_IPR=m
  - SCSI_IPR_TRACE=y
  - SCSI_IPR_DUMP=y
  - GCC_PLUGIN_STACKLEAK=n
  - DEBUG_FORCE_FUNCTION_ALIGN_64B=n
  - riscv64
  - SCHED_MC=y
  - RISCV_ISA_SVNAPOT=y
  - RISCV_ISA_ZICBOZ=y
  - RELOCATABLE=y
  - HIBERNATION=y
  - HIBERNATION_SNAPSHOT_DEV=y
  - PM_STD_PARTITION=""
  - PM_AUTOSLEEP=n
  - PM_USERSPACE_AUTOSLEEP=n
  - PM_WAKELOCKS=n
  - FW_CACHE=y
  - DWMAC_STARFIVE=m
  - CAN_BXCAN=m
  - AIRO=m
  - SPI_CADENCE_QUADSPI=m
  - SENSORS_SFCTEMP=m
  - STARFIVE_WATCHDOG=m
  - RZ_MTU3=n
  - SND_SOC_MAX98090=n
  - CLK_STARFIVE_JH7110_SYS=y
  - CLK_STARFIVE_JH7110_AON=m
- commit 5685b1d
* Fri May  5 2023 msuchanek@suse.de
- Remove obsolete rpm spec constructs
  defattr does not need to be specified anymore
  buildroot does not need to be specified anymore
- commit c963185
* Fri May  5 2023 msuchanek@suse.de
- kernel-spec-macros: Fix up obsolete_rebuilds_subpackage to generate
  obsoletes correctly (boo#1172073 bsc#1191731).
  rpm only supports full length release, no provides
- commit c9b5bc4
* Thu May  4 2023 msuchanek@suse.de
- kernel-binary: install expoline.o (boo#1210791 bsc#1211089)
- commit d6c8c20
* Wed May  3 2023 oneukum@suse.com
- usbtv: usbtv_set_regs: the pipe is output (bsc#1209334).
- commit 98c1e01
* Wed May  3 2023 jslaby@suse.cz
- SUNRPC: Fix encoding of rejected RPCs (bsc#1210995).
- commit 9aec45d
* Mon May  1 2023 jslaby@suse.cz
- Linux 6.3.1 (bsc#1012628).
- wifi: brcmfmac: slab-out-of-bounds read in brcmf_get_assoc_ies()
  (bsc#1012628).
- fsverity: reject FS_IOC_ENABLE_VERITY on mode 3 fds
  (bsc#1012628).
- drm/fb-helper: set x/yres_virtual in drm_fb_helper_check_var
  (bsc#1012628).
- fsverity: explicitly check for buffer overflow in
  build_merkle_tree() (bsc#1012628).
- gpiolib: acpi: Add a ignore wakeup quirk for Clevo NL5xNU
  (bsc#1012628).
- bluetooth: Perform careful capability checks in hci_sock_ioctl()
  (bsc#1012628).
- wifi: brcmfmac: add Cypress 43439 SDIO ids (bsc#1012628).
- btrfs: fix uninitialized variable warnings (bsc#1012628).
- USB: serial: option: add UNISOC vendor and TOZED LT70C product
  (bsc#1012628).
- driver core: Don't require dynamic_debug for initcall_debug
  probe timing (bsc#1012628).
- commit 4fd5b5c
* Fri Apr 28 2023 jslaby@suse.cz
- mm/mremap: fix vm_pgoff in vma_merge() case 3 (bsc#1210903).
  Update upstream status.
- commit 602ef9b
* Thu Apr 27 2023 vbabka@suse.cz
- [PATCH for v6.3 regression] mm/mremap: fix vm_pgoff in
  vma_merge() case 3 (bsc#1210903).
- commit 1fc982b
* Thu Apr 27 2023 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section
  - patches.suse/ath11k-pci-Add-more-MODULE_FIRMWARE-entries.patch
- commit 5408aa8
* Thu Apr 27 2023 mkubecek@suse.cz
- update and reenable armv6hl configs
  New values are copied from arvm7hl.
- commit 1d2204b
* Thu Apr 27 2023 mkubecek@suse.cz
- update and reenable armv7hl configs
  Where possible, new values are copied from arm64. The rest is guessed,
  mostly based on existing values of similar config options.
- commit 6bca092
* Thu Apr 27 2023 mkubecek@suse.cz
- update and reenable arm64 configs
  Where possible, new values are copied from x86_64, i386 or riscv64. The
  rest is guessed, mostly based on existing values of similar config options.
- commit 3f00e19
* Wed Apr 26 2023 jslaby@suse.cz
- config.sh: add :LegacyX86
  To pull i586 and build against that.
- commit 723ba5c
* Sun Apr 23 2023 mkubecek@suse.cz
- Update to 6.3 final
- update configs
- commit 9cc1a40
* Mon Apr 17 2023 mkubecek@suse.cz
- Update to 6.3-rc7
- commit 9e073da
* Fri Apr 14 2023 msuchanek@suse.de
- k-m-s: Drop Linux 2.6 support
- commit 22b2304
* Fri Apr 14 2023 msuchanek@suse.de
- Remove obsolete KMP obsoletes (bsc#1210469).
- commit 7f325c6
* Thu Apr 13 2023 tiwai@suse.de
- iwlwifi: cfg: Add missing MODULE_FIRMWARE() for *.pnvm
  (bsc#1207553).
- commit 2a07952
* Sun Apr  9 2023 mkubecek@suse.cz
- Update to 6.3-rc6
- commit 97dd3d4
* Tue Apr  4 2023 msuchanek@suse.de
- Define kernel-vanilla as source variant
  The vanilla_only macro is overloaded. It is used for determining if
  there should be two kernel sources built as well as for the purpose of
  determmioning if vanilla kernel should be used for kernel-obs-build.
  While the former can be determined at build time the latter needs to be
  baked into the spec file template. Separate the two while also making
  the latter more generic.
  $build_dtbs is enabled on every single rt and azure branch since 15.3
  when the setting was introduced, gate on the new $obs_build_variant
  setting as well.
- commit 36ba909
* Tue Apr  4 2023 jdelvare@suse.de
- Update config files: disable CONFIG_SENSORS_OCC_P8_I2C and CONFIG_SENSORS_OCC_P9_SBE
  These drivers are intended to run on the BMC of Power systems, not on
  the host, so they are useless in our distribution.
- commit 8dba174
* Mon Apr  3 2023 tiwai@suse.de
- rpm/constraints.in: increase the disk size for armv6/7 to 24GB
  It grows and the build fails recently on SLE15-SP4/5.
- commit 41ac816
* Sun Apr  2 2023 mkubecek@suse.cz
- Update to 6.3-rc5
- eliminate 1 patch
  - patches.rpmify/s390-reintroduce-expoline-dependence-to-scripts.patch (7bb2107e63d8)
- commit e8c15b9
* Sat Apr  1 2023 schwab@suse.de
- rpm/check-for-config-changes: add TOOLCHAIN_NEEDS_* to IGNORED_CONFIGS_RE
  This new form was added in commit e89c2e815e76 ("riscv: Handle
  zicsr/zifencei issues between clang and binutils").
- commit 234baea
* Fri Mar 31 2023 msuchanek@suse.de
- Disable compat options on ppc64le (jsc#PED-3184).
  CONFIG_PPC_TRANSACTIONAL_MEM=n
  CONFIG_COMPAT=n
- commit 2e176f2
* Fri Mar 31 2023 tiwai@suse.de
- ath11k: pci: Add more MODULE_FIRMWARE() entries (bsc#1209965).
  [js] update upstream status
- commit 33c2186
* Tue Mar 28 2023 ykaukab@suse.de
- supported.conf: add missing modules
  Mark most modules as unsupported by default
- commit 994ed9c
* Mon Mar 27 2023 mkubecek@suse.cz
- Update to 6.3-rc4
- eliminate 1 patch
  - patches.suse/arm64-efi-Use-SMBIOS-processor-ID-to-key-off-Altra-q.patch (eb684408f3ea)
- refresh configs
- commit f77c350
* Sun Mar 19 2023 mkubecek@suse.cz
- Update to 6.3-rc3
- eliminate 1 patch
  - patches.suse/powerpc-mm-Fix-false-detection-of-read-faults.patch (f2c7e3562b4c)
- refresh configs
- commit d72bdba
* Thu Mar 16 2023 jslaby@suse.cz
- s390: reintroduce expoline dependence to scripts (s390 expolines
  & fixdep).
- commit a0e8ac4
* Thu Mar 16 2023 shung-hsi.yu@suse.com
- rpm/group-source-files.pl: Fix output difference when / is in location
  While previous attempt to fix group-source-files.pl in 6d651362c38
  "rpm/group-source-files.pl: Deal with {pre,post}fixed / in location"
  breaks the infinite loop, it does not properly address the issue. Having
  prefixed and/or postfixed forward slash still result in different
  output.
  This commit changes the script to use the Perl core module File::Spec
  for proper path manipulation to give consistent output.
- commit 4161bf9
* Tue Mar 14 2023 msuchanek@suse.de
- Require suse-kernel-rpm-scriptlets at all times.
  The kernel packages call scriptlets for each stage, add the dependency
  to make it clear to libzypp that the scriptlets are required.
  There is no special dependency for posttrans, these scriptlets run when
  transactions are resolved. The plain dependency has to be used to
  support posttrans.
- commit 56c4dbe
* Tue Mar 14 2023 msuchanek@suse.de
- Replace mkinitrd dependency with dracut (bsc#1202353).
  Also update mkinitrd refrences in documentation and comments.
- commit e356c9b
* Tue Mar 14 2023 msuchanek@suse.de
- rpm/kernel-obs-build.spec.in: Remove SLE11 cruft
- commit 871eeb4
* Mon Mar 13 2023 mkubecek@suse.cz
- series.conf: whitespace cleanup
- commit af164d0
* Mon Mar 13 2023 mkubecek@suse.cz
- Update to 6.3-rc2
- eliminate 1 patch
  - patches.suse/cpumask-fix-incorrect-cpumask-scanning-result-checks.patch
- update configs
  - FEALNX=m (x86, riscv64), =n otherwise (restored from < 6.2-rc1)
- commit 4015adb
* Fri Mar 10 2023 mkubecek@suse.cz
- series.conf: cleanup
- move an unsortable patch out of sorted section
  patches.suse/powerpc-mm-Fix-false-detection-of-read-faults.patch
- commit 60a3726
* Fri Mar 10 2023 msuchanek@suse.de
- powerpc/mm: Fix false detection of read faults (bsc#1208864).
- commit 0f51cbf
* Thu Mar  9 2023 jslaby@suse.cz
- Disable lockdown. (bsc#1209006 bsc#1211166)
  This somehow doesn't play good wrt to external modules.
  When all is ready again, we can revert this revert.
- commit 77c9b15
* Thu Mar  9 2023 jlee@suse.com
- Update config files.
  Add the following config to x86_64, arm64 and i386.
  CONFIG_IMA_ARCH_POLICY=y
  CONFIG_IMA_SECURE_AND_OR_TRUSTED_BOOT=y
  This config be used to detect secure boot. (bsc#1209006)
- commit 90a4659
* Wed Mar  8 2023 jlee@suse.com
- KEYS: Make use of platform keyring for module signature verify
  (FATE#314508, FATE#316531, bsc#1209006).
- commit 261191e
* Wed Mar  8 2023 msuchanek@suse.de
- Do not sign the vanilla kernel (bsc#1209008).
- commit cee4d89
* Tue Mar  7 2023 shung-hsi.yu@suse.com
- rpm/group-source-files.pl: Deal with {pre,post}fixed / in location
  When the source file location provided with -L is either prefixed or
  postfixed with forward slash, the script get stuck in a infinite loop
  inside calc_dirs() where $path is an empty string.
  user@localhost:/tmp> perl "$HOME/group-source-files.pl" -D devel.files -N nondevel.files -L /usr/src/linux-5.14.21-150500.41/
  ...
  path = /usr/src/linux-5.14.21-150500.41/Documentation/Kconfig
  path = /usr/src/linux-5.14.21-150500.41/Documentation
  path = /usr/src/linux-5.14.21-150500.41
  path = /usr/src
  path = /usr
  path =
  path =
  path =
  ... # Stuck in an infinite loop
  This workarounds the issue by breaking out the loop once path is an
  empty string. For a proper fix we'd want something that
  filesystem-aware, but this workaround should be enough for the rare
  occation that this script is ran manually.
  Link: http://mailman.suse.de/mlarch/SuSE/kernel/2023/kernel.2023.03/msg00024.html
- commit 6d65136
* Tue Mar  7 2023 mkubecek@suse.cz
- cpumask: fix incorrect cpumask scanning result checks
  (https://lkml.iu.edu/hypermail/linux/kernel/2303.0/05801.html).
- commit f6f6da4
* Mon Mar  6 2023 msuchanek@suse.de
- kernel-module-subpackage: Fix expansion with -b parameter (bsc#1208179).
  When -b is specified the script is prefixed with KMP_NEEDS_MKINITRD=1
  which sets the variable for a simple command.
  However, the script is no longer a simple command. Export the variable
  instead.
- commit 152a069
* Mon Mar  6 2023 mkubecek@suse.cz
- Update to 6.3-rc1
- drop 32 patches (30 stable, 2 mainline)
  - patches.kernel.org/*
  - patches.rpmify/bpf_doc-Fix-build-error-with-older-python-versions.patch
  - patches.suse/objtool-Check-that-module-init-exit-function-is-an-i.patch
- refresh
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - General setup
  - BOOT_CONFIG_FORCE=n
  - Memory Management options
  - ZSMALLOC_CHAIN_SIZE=8
  - Networking support
  - AF_RXRPC_INJECT_RX_DELAY=n
  - File systems
  - EROFS_FS_PCPU_KTHREAD=n
  - RPCSEC_GSS_KRB5_ENCTYPES_DES=n
  - RPCSEC_GSS_KRB5_ENCTYPES_AES_SHA1=y
  - RPCSEC_GSS_KRB5_ENCTYPES_CAMELLIA=y
  - RPCSEC_GSS_KRB5_ENCTYPES_AES_SHA2=y
  - Cryptographic API
  - CRYPTO_ARIA_AESNI_AVX2_X86_64=m
  - CRYPTO_ARIA_GFNI_AVX512_X86_64=m
  - Kernel hacking
  - NMI_CHECK_CPU=y
  - RCU_CPU_STALL_CPUTIME=y
  - TEST_DHRY=n
  - Serial ATA and Parallel ATA drivers (libata)
  - PATA_PARPORT renamed from PARIDE
  - PATA_PARPORT_* renamed from PARIDE_*
  - Network device support
  - NET_DSA_MICROCHIP_KSZ_PTP=y
  - NET_DSA_MSCC_OCELOT_EXT=m
  - NCN26000_PHY=m
  - ATH12K=m
  - ATH12K_DEBUG=n
  - ATH12K_TRACING=n
  - Character devices
  - SERIAL_8250_PCI1XXXX=y
  - SERIAL_8250_DFL=m
  - Power supply class support
  - CHARGER_RT9467=m
  - CHARGER_RT9471=m
  - Hardware Monitoring support
  - SENSORS_MC34VR500=m
  - SENSORS_MPQ7932=m
  - SENSORS_MPQ7932_REGULATOR=y
  - SENSORS_TDA38640=m
  - SENSORS_TDA38640_REGULATOR=y
  - Multifunction device drivers
  - MFD_INTEL_M10_BMC_SPI=n
  - MFD_INTEL_M10_BMC_PMCI=n
  - Multimedia support
  - VIDEO_IMX296=m
  - VIDEO_OV8858=m
  - Graphics support
  - DRM_PANEL_AUO_A030JTN01=n
  - DRM_PANEL_ORISETECH_OTA5601A=n
  - BACKLIGHT_KTZ8866=m
  - Compute Acceleration Framework
  - DRM_ACCEL_HABANALABS=m
  - DRM_ACCEL_IVPU=m
  - Sound card support
  - SND_HDA_CTL_DEV_ID=n
  - SND_SOC_AW88395=n
  - SND_SOC_CS42L42_SDW=m
  - SND_SOC_IDT821034=n
  - SND_SOC_PEB2466=n
  - SND_SOC_RT712_SDCA_SDW=m
  - SND_SOC_SMA1303=n
  - HID_SUPPORT=y
  - HID_SUPPORT=y
  - HID_EVISION=m
  - STEAM_FF=y
  - HID_BPF=y
  - I2C_HID=m
  - vDPA drivers
  - MLX5_VDPA_STEERING_DEBUG=n
  - SNET_VDPA=m
  - Industrial I/O support
  - TI_ADS7924=n
  - TI_LMP92064=n
  - MAX5522=n
  - TI_TMAG5273=n
  - Misc devices
  - REGULATOR_MAX20411=m
  - TYPEC_MUX_GPIO_SBU=m
  - XILINX_XDMA=m
  - CROS_EC_UART=m
  - INTEL_TPMI=m
  - INTEL_IOMMU_PERF_EVENTS=y
  - WPCM450_SOC=m
  - DEV_DAX_CXL=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - VIDEO_IMX415=m
  - DRM_PANEL_HIMAX_HX8394=n
  - DRM_PANEL_VISIONOX_VTDR6130=n
  - QCOM_PMIC_GLINK=m
  - BATTERY_QCOM_BATTMGR=m
  - ppc64le / ppc64
  - KCSAN=n
  - s390x
  - FPROBE=y
  - s390x/zfcpdump
  - GLOB_SELFTEST=n
  - riscv64
  - ARCH_SUNXI=y
  - RISCV_ISA_ZBB=y
  - SUN50I_DE2_BUS=n
  - SUNXI_RSB=m
  - MTD_NAND_SUNXI=m
  - AHCI_SUNXI=m
  - NET_VENDOR_ALLWINNER=y
  - SUN4I_EMAC=m
  - DWMAC_SUNXI=m
  - DWMAC_SUN8I=m
  - KEYBOARD_SUN4I_LRADC=m
  - TOUCHSCREEN_SUN4I=m
  - SERIO_SUN4I_PS2=m
  - SERIAL_EARLYCON_SEMIHOST=y
  - HW_RANDOM_JH7110=m
  - I2C_MV64XXX=m
  - SPI_SUN4I=m
  - SPI_SUN6I=m
  - PINCTRL_STARFIVE_JH7110_SYS=m
  - PINCTRL_STARFIVE_JH7110_AON=m
  - PINCTRL_SUN*=y
  - SUN8I_THERMAL=m
  - SUNXI_WATCHDOG=m
  - MFD_SUN4I_GPADC=n
  - MFD_AC100=n
  - MFD_AXP20X_RSB=n
  - MFD_SUN6I_PRCM=n
  - IR_SUNXI=m
  - DRM_SUN4I=n
  - SND_SUN4I_CODEC=m
  - SND_SUN4I_I2S=m
  - SND_SUN4I_SPDIF=m
  - SND_SUN50I_DMIC=m
  - MMC_DW_STARFIVE=m
  - MMC_SUNXI=m
  - RTC_DRV_SUN6I=n
  - DMA_SUN6I=m
  - VIDEO_SUNXI=y
  - VIDEO_SUNXI_CEDRUS=m
  - SUNXI_CCU=m
  - SUN20I_D1_CCU=m
  - SUN20I_D1_R_CCU=m
  - SUN6I_RTC_CCU=m
  - SUN8I_DE2_CCU=m
  - HWSPINLOCK_SUN6I=m
  - SUN6I_MSGBOX=m
  - SUN50I_IOMMU=y
  - JH71XX_PMU=n
  - SUN20I_PPU=n
  - ARM_SUN8I_A33_MBUS_DEVFREQ=m
  - PWM_SUN4I=m
  - PHY_SUN4I_USB=m
  - PHY_SUN6I_MIPI_DPHY=m
  - PHY_SUN9I_USB=m
  - PHY_SUN50I_USB3=m
  - NVMEM_SUNXI_SID=m
  - HUGETLB_PAGE_OPTIMIZE_VMEMMAP_DEFAULT_ON=n
  - CRYPTO_DEV_ALLWINNER=y
  - CRYPTO_DEV_SUN4I_SS=m
  - CRYPTO_DEV_SUN4I_SS_PRNG=y
  - CRYPTO_DEV_SUN4I_SS_DEBUG=n
  - CRYPTO_DEV_SUN8I_CE=m
  - CRYPTO_DEV_SUN8I_CE_DEBUG=n
  - CRYPTO_DEV_SUN8I_CE_HASH=y
  - CRYPTO_DEV_SUN8I_CE_PRNG=y
  - CRYPTO_DEV_SUN8I_CE_TRNG=y
  - CRYPTO_DEV_SUN8I_SS=m
  - CRYPTO_DEV_SUN8I_SS_DEBUG=n
  - CRYPTO_DEV_SUN8I_SS_PRNG=y
  - CRYPTO_DEV_SUN8I_SS_HASH=y
  - USB_MUSB_SUNXI=m
- commit f3bbae4
* Fri Mar  3 2023 jslaby@suse.cz
- Linux 6.2.2 (bsc#1012628).
- USB: core: Don't hold device lock while reading the
  "descriptors" sysfs file (bsc#1012628).
- usb: typec: pd: Remove usb_suspend_supported sysfs from sink
  PDO (bsc#1012628).
- arm64: dts: uniphier: Fix property name in PXs3 USB node
  (bsc#1012628).
- usb: gadget: u_serial: Add null pointer check in gserial_resume
  (bsc#1012628).
- USB: serial: option: add support for VW/Skoda "Carstick LTE"
  (bsc#1012628).
- usb: dwc3: pci: add support for the Intel Meteor Lake-M
  (bsc#1012628).
- wifi: rtw88: usb: drop now unnecessary URB size check
  (bsc#1012628).
- wifi: rtw88: usb: send Zero length packets if necessary
  (bsc#1012628).
- wifi: rtw88: usb: Set qsel correctly (bsc#1012628).
- scripts/tags.sh: fix incompatibility with PCRE2 (bsc#1012628).
- drm/amd/display: Properly reuse completion structure
  (bsc#1012628).
- drm/amd/display: Move DCN314 DOMAIN power control to DMCUB
  (bsc#1012628).
- vc_screen: don't clobber return value in vcs_read (bsc#1012628).
- bpf: bpf_fib_lookup should not return neigh in NUD_FAILED state
  (bsc#1012628).
- crypto: arm64/sm4-gcm - Fix possible crash in GCM cryption
  (bsc#1012628).
- ALSA: hda: cs35l41: Correct error condition handling
  (bsc#1012628).
- commit ec730fa
* Wed Mar  1 2023 jslaby@suse.cz
- Update config files. Disable old pcmcia drivers (bsc#1208780).
- commit 789fdf4
* Wed Mar  1 2023 jslaby@suse.cz
- Update config files. Disable old pcmcia socket drivers (bsc#1208780).
- commit 27af844
* Wed Mar  1 2023 jslaby@suse.cz
- Delete
  patches.suse/char-pcmcia-cm4000_cs-Fix-use-after-free-in-cm4000_f.patch.
- Delete
  patches.suse/char-pcmcia-cm4040_cs-Fix-use-after-free-in-reader_f.patch.
- Delete
  patches.suse/char-pcmcia-scr24x_cs-Fix-use-after-free-in-scr24x_f.patch.
  These drivers are now disabled, so remove the non-upstream patches. See
  bsc#1208775.
- commit 03a39b9
* Wed Mar  1 2023 jslaby@suse.cz
- Update config files. Disable char/pcmcia drivers (bsc#1208775).
- commit a2a5aac
* Wed Mar  1 2023 jslaby@suse.cz
- arm64: efi: Use SMBIOS processor ID to key off Altra quirk
  (bsc#1208750).
- commit 533dcdd
* Tue Feb 28 2023 schwab@suse.de
- config: riscv64: enable SPI_SPIDEV and SPI_SLAVE
- commit 8cad76a
* Mon Feb 27 2023 jslaby@suse.cz
- Linux 6.2.1 (bsc#1012628).
- bpf: add missing header file include (bsc#1012628).
- randstruct: disable Clang 15 support (bsc#1012628).
- ext4: Fix function prototype mismatch for ext4_feat_ktype
  (bsc#1012628).
- platform/x86: nvidia-wmi-ec-backlight: Add force module
  parameter (bsc#1012628).
- platform/x86/amd/pmf: Add depends on CONFIG_POWER_SUPPLY
  (bsc#1012628).
- audit: update the mailing list in MAINTAINERS (bsc#1012628).
- wifi: mwifiex: Add missing compatible string for SD8787
  (bsc#1012628).
- HID: mcp-2221: prevent UAF in delayed work (bsc#1012628).
- x86/static_call: Add support for Jcc tail-calls (bsc#1012628).
- x86/alternatives: Teach text_poke_bp() to patch Jcc.d32
  instructions (bsc#1012628).
- x86/alternatives: Introduce int3_emulate_jcc() (bsc#1012628).
- uaccess: Add speculation barrier to copy_from_user()
  (bsc#1012628).
- commit 15796ef
* Fri Feb 24 2023 msuchanek@suse.de
- Disable PS3 support
  The PS3 hardware cannot be used with up-to-date firmware.
- commit 484fa63
* Fri Feb 24 2023 tzimmermann@suse.com
- uvesafb: Disable fbdev driver (boo#1208662)
  A VESA-based driver. Dropped in favor of generic DRM drivers.
- commit f0d0f1a
* Fri Feb 24 2023 tzimmermann@suse.com
- ocfb: Disable fbdev driver (boo#1208660)
  The OpenCores fbdev driver is for an old homebrew chip design. Probably
  unused.
- commit 00dd263
* Fri Feb 24 2023 tzimmermann@suse.com
- udlfb: Disable fbdev driver (boo#1208658)
  We've long shipped the DRM-based udl driver, which handles the same
  devices.
- commit 8a53173
* Fri Feb 24 2023 tzimmermann@suse.com
- ssd1307fb: Replace with ssd130x (boo#1208656)
  Replace fbdev's ssd1307fb driver with the new DRM-based driver
  ssd130x. Adds support for SPI and Wayland-based userspace.
- commit 1fe1b4c
* Fri Feb 24 2023 tzimmermann@suse.com
- vfb: Disable fbdev driver (boo#1208646)
  The vfb fbdev driver is backed by system memory and only relevant for
  testing. Disable it. There is DRM's vkms, if a software-only driver is
  required.
- commit b1c9331
* Fri Feb 24 2023 tzimmermann@suse.com
- Disable gxt4500 fbdev driver (boo#1208642)
  The gxt4500 driver serves a 20yrs-old graphics hardware for
  IBM RS/6000 system. Probably not in use any longer.
- commit 5313a19
* Tue Feb 21 2023 jslaby@suse.cz
- blacklist.conf: clean up
  Remove the only (5.5) entry. It was needed only years ago.
- commit de1e630
* Mon Feb 20 2023 mkubecek@suse.cz
- Update to 6.2 final
- refresh configs
- commit 28fe266
* Sat Feb 18 2023 jlee@suse.com
- arm64: lock down kernel in secure boot mode (jsc#SLE-15020, bsc#1198101).
- efi: Lock down the kernel at the integrity level if booted in
  secure boot mode (jsc#SLE-9870, bsc#1198101).
- efi: Lock down the kernel if booted in secure boot mode
  (jsc#SLE-9870, bsc#1198101).
- Update config files.
  - The shim for openSUSE Tumbleweed needs to be reviewed by upstream
    and signed by Microsoft. So we need to lockdown kernel on x86_64
    and arm64 because EFI secure boot.
  - We disable CONFIG_LOCK_DOWN_IN_EFI_SECURE_BOOT in other
    architectures.
- efi: Add an EFI_SECURE_BOOT flag to indicate secure boot mode
  (jsc#SLE-9870, bsc#1198101).
- security: lockdown: expose a hook to lock the kernel down
  (jsc#SLE-9870, bsc#1198101).
- commit a7d5b50
* Thu Feb 16 2023 mkoutny@suse.com
- Update config files.
  Disable CONFIG_BLK_CGROUP_IOPRIO.
  io.prio.class is a misdesigned mechanism that doesn't fit well with the
  cgroup (especially v2):
- it's not properly hierarchical
  - cgroup-wise: parent cgroup has no contol over child cgroup
  - task-wise: priority impact outside of a cgroup (i.e. affects
    cousins competition)
- it's not device dependent (device oblivious)
  Disable it in openSUSE Tumbleweed (and future products) so that we don't
  teach users to use it and force ourselves to support it.
- commit 35713cd
* Tue Feb 14 2023 jslaby@suse.cz
- Update config files.
  Just run oldconfig.
- commit f33197d
* Tue Feb 14 2023 jslaby@suse.cz
- Update config files. Enable budget-ci module (bsc#1206774)
  Needed for saa7146 support.
- commit 130e9da
* Tue Feb 14 2023 jlee@suse.com
- Removed the support of EINJ (bsc#1023051, CVE-2016-3695)
- Update config files.
- supported.conf: removed drivers/acpi/apei/einj support.
- commit c2c7791
* Mon Feb 13 2023 mkubecek@suse.cz
- Update to 6.2-rc8
- commit 3c381aa
* Mon Feb  6 2023 mkubecek@suse.cz
- Update to 6.2-rc7
- commit 225bfb7
* Mon Jan 30 2023 mkubecek@suse.cz
- Update to 6.2-rc6
- eliminate 1 patch
  - patches.suse/0001-Revert-mm-compaction-fix-set-skip-in-fast_find_migra.patch
- commit 4fa09ed
* Sun Jan 22 2023 mkubecek@suse.cz
- objtool: Check that module init/exit function is an indirect
  call target.
- commit 39a491d
* Sun Jan 22 2023 mkubecek@suse.cz
- Update to 6.2-rc5
- refresh configs
- commit e1e1e9c
* Fri Jan 20 2023 jslaby@suse.cz
- Update config files. Set saa7146 to pre-6.1 state (bsc#1206774).
  The driver was moved to staging and disabled by us in 6.1. Now it turned
  out it is actually used. So the driver is getting cleaned up. So enable
  it even when it is in staging, so that users can use it properly.
- commit 99101ef
* Mon Jan 16 2023 schwab@suse.de
- rpm/mkspec-dtb: add riscv64 dtb-renesas subpackage
- commit 6020754
* Mon Jan 16 2023 msuchanek@suse.de
- Refresh patches.rpmify/bpf_doc-Fix-build-error-with-older-python-versions.patch.
- commit df46e81
* Sun Jan 15 2023 mkubecek@suse.cz
- Update to 6.2-rc4
- eliminate 2 patches
  - patches.suse/docs-Fix-the-docs-build-with-Sphinx-6.0.patch
  - patches.suse/drm-amdgpu-fix-pipeline-sync-v2.patch
- update configs
  - ARM64_ERRATUM_2645198=y (arm64)
  - SND_SOC_APQ8016_SBC=m (armv7hl/default, value from arm64)
  - SND_SOC_MSM8996=m (armv7hl/default, value from arm64)
  - SND_SOC_SC7180=m (armv7hl/default, value from arm64)
- commit b1ecb39
* Fri Jan 13 2023 vbabka@suse.cz
- Revert "mm/compaction: fix set skip in fast_find_migrateblock"
  (bsc#1206848).
- commit 5049637
* Fri Jan 13 2023 mkubecek@suse.cz
- drm/amdgpu: fix pipeline sync v2
  (https://gitlab.freedesktop.org/drm/amd/-/issues/2323).
- Delete
  patches.suse/Revert-drm-amdgpu-move-explicit-sync-check-into-the-.patch.
- Delete
  patches.suse/Revert-drm-amdgpu-use-scheduler-dependencies-for-CS.patch.
- Delete
  patches.suse/Revert-drm-scheduler-remove-drm_sched_dependency_opt.patch.
  Replace reverts of offending commits by queued upstream fix.
- commit 90ac672
* Mon Jan  9 2023 svarbanov@suse.de
- Update armv7 to 6.2.0-rc3
- update configs
- re-enable armv7
- commit e578e47
* Mon Jan  9 2023 svarbanov@suse.de
- Update arm64 to 6.2.0-rc3
- update configs
- re-enable arm64
- commit 72fe5c3
* Mon Jan  9 2023 svarbanov@suse.de
- Update armv6 to 6.2.0-rc3
- update configs
- reenable armv6
- commit ed1892b
* Mon Jan  9 2023 jslaby@suse.cz
- docs: Fix the docs build with Sphinx 6.0 (sphinx_6.0-staging_E).
- commit ba4d8f4
* Sun Jan  8 2023 mkubecek@suse.cz
- Revert "drm/amdgpu: move explicit sync check into the CS"
  (https://gitlab.freedesktop.org/drm/amd/-/issues/2323).
- Revert "drm/amdgpu: use scheduler dependencies for CS"
  (https://gitlab.freedesktop.org/drm/amd/-/issues/2323).
- Revert "drm/scheduler: remove drm_sched_dependency_optimized"
  (https://gitlab.freedesktop.org/drm/amd/-/issues/2323).
- commit 13b3e26
* Sun Jan  8 2023 mkubecek@suse.cz
- Update to 6.2-rc3
- eliminate 1 patch
  - patches.suse/tcp-Add-TIME_WAIT-sockets-in-bhash2.patch
- refresh
  - patches.suse/add-suse-supported-flag.patch
- update configs
  - CDROM_PKTCDVD=m (restored, except s390x)
  - CDROM_PKTCDVD_BUFFERS=8 (restored, except s390x)
  - CDROM_PKTCDVD_WCACHE=y (restored, except s390x)
- commit 8fc2af0
* Fri Jan  6 2023 jeffm@suse.com
- rpm/kernel-binary.spec.in: Add Enhances and Supplements tags to in-tree KMPs
  This makes in-tree KMPs more consistent with externally built KMPs and
  silences several rpmlint warnings.
- commit 02b7735
* Fri Jan  6 2023 mkubecek@suse.cz
- rpm/check-for-config-changes: add OBJTOOL and FTRACE_MCOUNT_USE_*
  Dummy gcc pretends to support -mrecord-mcount option but actual gcc on
  ppc64le does not. Therefore ppc64le builds of 6.2-rc1 and later in OBS
  enable FTRACE_MCOUNT_USE_OBJTOOL and OBJTOOL config options, resulting in
  check failure.
  As we already have FTRACE_MCOUNT_USE_CC and FTRACE_MCOUNT_USE_RECORDMCOUNT
  in the exception list, replace them with a general pattern. And add OBJTOOL
  as well.
- commit 887416f
* Fri Jan  6 2023 msuchanek@suse.de
- bpf_doc: Fix build error with older python versions
  (TypeError: '_sre.SRE_Match' object is not subscriptable).
- commit 37f7888
* Thu Jan  5 2023 jeffm@suse.com
- supported-flag: fix build failures with SUSE_KERNEL_SUPPORTED=y
  Upstream commit 425937381ec (kbuild: re-run modpost when it is updated)
  added an expectation that the MODPOST variable would only point to the
  modpost executable and moved arguments to the modpost-args variable.
  Also removed some legacy stuff, like the assumption that MODVERDIR would
  exist (and then later creating it and using it) when the only two
  places we ever care about Module.supported being located are the directory
  in which an external module is being built and the current directory.
- commit b03fb04
* Thu Jan  5 2023 jeffm@suse.com
- config: Added product codes to suse_version.h for comparison
  Refreshed
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch.
- commit a26a81f
* Thu Jan  5 2023 jeffm@suse.com
- config: Added support for ALP releases in product identifiers
- Refresh patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch.
- commit 0f442bb
* Mon Jan  2 2023 jslaby@suse.cz
- Refresh patches.suse/tcp-Add-TIME_WAIT-sockets-in-bhash2.patch.
  Update upstream status.
- commit 810f419
* Mon Jan  2 2023 msuchanek@suse.de
- ppc64: Swap out FB_OF for OFDRM (boo#1193476)
  FB_OF=n
  AGP=n
  OFDRM=y
  DRM=y
  This disables support for the Apple UniNorth AGP bridge.
  yast does not support installing on Apple hardware anyway.
- commit eebb76b
* Mon Jan  2 2023 schwab@suse.de
- config: riscv64: disable CONFIG_IPMMU_VMSA
  This is an ARM-only driver.
- commit dc8fbaa
* Mon Jan  2 2023 mkubecek@suse.cz
- Update to 6.2-rc2
- refresh
  - patches.suse/add-suse-supported-flag.patch
- commit 8e1570b
* Mon Dec 26 2022 mkubecek@suse.cz
- Update to 6.2-rc1
- drop 32 patches (25 stable, 7 mainline)
  - patches.kernel.org/*
  - patches.suse/NFSD-fix-use-after-free-in-__nfs42_ssc_open.patch
  - patches.suse/char-xillybus-Fix-trivial-bug-with-mutex.patch
  - patches.suse/char-xillybus-Prevent-use-after-free-due-to-race-con.patch
  - patches.suse/io_uring-net-ensure-compat-import-handlers-clear-fre.patch
  - patches.suse/media-dvb-core-Fix-UAF-due-to-refcount-races-at-rele.patch
  - patches.suse/misc-sgi-gru-fix-use-after-free-error-in-gru_set_con.patch
  - patches.suse/mm-mremap-fix-mremap-expanding-vma-with-addr-inside-.patch
- refresh
  - patches.suse/Input-elan_i2c-Add-deny-list-for-Lenovo-Yoga-Slim-7.patch
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/crasher.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - General setup
  - RCU_LAZY=n
  - KALLSYMS_SELFTEST=n
  - Processor type and features
  - EFI_HANDOVER_PROTOCOL=y
  - Mitigations for speculative execution vulnerabilities
  - CALL_DEPTH_TRACKING=y
  - CALL_THUNKS_DEBUG=n
  - Power management and ACPI options
  - ACPI_FFH=y
  - Virtualization
  - KVM_SMM=y
  - Memory Management options
  - SLOB_DEPRECATED=n
  - SLUB_TINY=n
  - Networking support
  - BT_LE_L2CAP_ECRED=y
  - BT_HCIBTUSB_POLL_SYNC=y
  - BT_HCIBCM4377=m
  - RXPERF=m
  - File systems
  - SQUASHFS_CHOICE_DECOMP_BY_MOUNT=y
  - NFSD_V2=n
  - Kernel hacking
  - DEBUG_INFO_COMPRESSED_NONE=y
  - DEBUG_INFO_COMPRESSED_ZLIB=n
  - DEBUG_CGROUP_REF=n
  - FAULT_INJECTION_STACKTRACE_FILTER=n
  - Network device support
  - NFP_NET_IPSEC=y
  - MT7996E=m
  - RTW88_8822BU=m
  - RTW88_8822CU=m
  - RTW88_8723DU=m
  - RTW88_8821CU=m
  - RTW89_8852BE=m
  - Input device support
  - TOUCHSCREEN_CYTTSP5=m
  - TOUCHSCREEN_HYNITRON_CSTXXX=m
  - TOUCHSCREEN_HIMAX_HX83112B=m
  - Hardware Monitoring support
  - SENSORS_OCC_P8_I2C=m
  - SENSORS_OXP=m
  - Multimedia support
  - VIDEO_OV08X40=m
  - VIDEO_OV4689=m
  - VIDEO_TC358746=m
  - Graphics support
  - DRM_I915_PREEMPT_TIMEOUT_COMPUTE=7500
  - DRM_ACCEL=y
  - DRM_ACCEL=y
  - Sound card support
  - SND_SOC_INTEL_AVS_MACH_MAX98927=m
  - SND_SOC_INTEL_AVS_MACH_PROBE=m
  - SND_SOC_WM8961=n
  - X86 Platform Specific Device Drivers
  - DELL_WMI_DDV=m
  - X86_PLATFORM_DRIVERS_HP=y
  - INTEL_IFS=m
  - Industrial I/O support
  - IIO_KX022A_SPI=n
  - IIO_KX022A_I2C=n
  - AD4130=n
  - MAX11410=n
  - AD74115=n
  - ADF4377=n
  - MAX30208=m
  - Misc devices
  - CXL_REGION_INVALIDATION_TEST=n
  - ZRAM_MULTI_COMP=y
  - LEGACY_TIOCSTI=n
  - SPI_PCI1XXXX=n
  - GPIO_LATCH=m
  - ADVANTECH_EC_WDT=m
  - MFD_SMPRO=n
  - REGULATOR_RT6190=m
  - MANA_INFINIBAND=m
  - TDX_GUEST_DRIVER=m
  - CROS_HPS_I2C=m
  - IOMMUFD=n
  - NVDIMM_SECURITY_TEST=n
  - FPGA_MGR_LATTICE_SYSCONFIG_SPI=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - SPI_SN_F_OSPI=n
  - MFD_TPS65219=n
  - VIDEO_ST_VGXY61=m
  - DRM_PANEL_JADARD_JD9365DA_H3=n
  - DRM_PANEL_NEWVISION_NV3051D=n
  - i386
  - SND_SOC_RT1318_SDW=n
  - ppc64le / ppc64
  - SSIF_IPMI_BMC=m
  - SENSORS_OCC_P9_SBE=m
  - DRM_OFDRM=m
  - ppc64
  - PPC64_BIG_ENDIAN_ELF_ABI_V2=y
  - s390x
  - VCAP=y
  - HUGETLB_PAGE_OPTIMIZE_VMEMMAP_DEFAULT_ON=n
  - riscv64
  - ARCH_RENESAS=y
  - ERRATA_THEAD_PMU=y
  - CPU_FREQ=y
  - CPU_FREQ_STAT=y (arm64)
  - CPU_FREQ_DEFAULT_GOV_ONDEMAND=y (arm64)
  - CPU_FREQ_GOV_POWERSAVE=m
  - CPU_FREQ_GOV_USERSPACE=m
  - CPU_FREQ_GOV_CONSERVATIVE=m
  - CPU_FREQ_GOV_SCHEDUTIL=y
  - CPUFREQ_DT=m
  - PCIE_RCAR_HOST=y
  - PCIE_RCAR_EP=y
  - MTD_NAND_RENESAS=m
  - SCSI_LPFC=m
  - SCSI_LPFC_DEBUG_FS=n
  - SATA_RCAR=m
  - SH_ETH=m
  - RAVB=m
  - RENESAS_ETHER_SWITCH=m
  - CAN_RCAR=m
  - CAN_RCAR_CANFD=m
  - SERIAL_8250_EM=y
  - SERIAL_SH_SCI=n
  - I2C_RIIC=m
  - I2C_RZV2M=m
  - I2C_SH_MOBILE=m
  - I2C_RCAR=m
  - I2C_SLAVE_EEPROM=m
  - I2C_SLAVE_TESTUNIT=n
  - SPI_RSPI=m
  - SPI_SH_MSIOF=m
  - SPI_SH_HSPI=m
  - GPIO_RCAR=m
  - CPU_FREQ_THERMAL=y
  - RCAR_THERMAL=m
  - RCAR_GEN3_THERMAL=m
  - RZG2L_THERMAL=m
  - RENESAS_WDT=m
  - RENESAS_RZAWDT=m
  - RENESAS_RZN1WDT=m
  - RENESAS_RZG2LWDT=m
  - DRM_RZG2L_MIPI_DSI=n
  - FB_SH_MOBILE_LCDC=n
  - SND_SOC_SH4_FSI=n
  - SND_SOC_RCAR=n
  - MMC_SDHI=m
  - MMC_SDHI_SYS_DMAC=m
  - MMC_SH_MMCIF=m
  - SCSI_UFS_RENESAS=m
  - RTC_DRV_SH=m
  - RCAR_DMAC=m
  - RENESAS_USB_DMAC=m
  - CLK_RCAR_USB2_CLOCK_SEL=y
  - RENESAS_OSTM=y
  - IPMMU_VMSA=y
  - ARCH_R9A07G043=y
  - RENESAS_RPCIF=m
  - RZG2L_ADC=n
  - PWM_RCAR=m
  - PWM_RENESAS_TPU=m
  - RESET_RZG2L_USBPHY_CTRL=m
  - PHY_R8A779F0_ETHERNET_SERDES=m
  - PHY_RCAR_GEN2=m
  - PHY_RCAR_GEN3_PCIE=m
  - PHY_RCAR_GEN3_USB2=m
  - PHY_RCAR_GEN3_USB3=m
  - FPROBE=y
  - UCLAMP_TASK=n
  - ENERGY_MODEL=y
  - MCTP_TRANSPORT_I2C=m
  - INPUT_IBM_PANEL=m
  - IPMI_IPMB=m
  - SSIF_IPMI_BMC=m
  - IPMB_DEVICE_INTERFACE=m
  - SPI_RPCIF=m
  - THERMAL_GOV_POWER_ALLOCATOR=n
  - SND_SOC_RZ=n
  - RZ_DMAC=m
  - IOMMU_IO_PGTABLE_LPAE_SELFTEST=n
  - DTPM_CPU=y
  - DTPM_DEVFREQ=y
- commit 769d7ad
* Thu Dec 22 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section:
  - patches.suse/io_uring-net-ensure-compat-import-handlers-clear-fre.patch
- commit a76dc2b
* Thu Dec 22 2022 jslaby@suse.cz
- Linux 6.1.1 (bsc#1012628).
- KEYS: encrypted: fix key instantiation with user-provided data
  (bsc#1012628).
- cifs: fix oops during encryption (bsc#1012628).
- usb: dwc3: pci: Update PCIe device ID for USB3 controller on
  CPU sub-system for Raptor Lake (bsc#1012628).
- usb: typec: ucsi: Resume in separate work (bsc#1012628).
- igb: Initialize mailbox message for VF reset (bsc#1012628).
- staging: r8188eu: fix led register settings (bsc#1012628).
- xhci: Apply XHCI_RESET_TO_DEFAULT quirk to ADL-N (bsc#1012628).
- ALSA: hda/realtek: fix mute/micmute LEDs for a HP ProBook
  (bsc#1012628).
- USB: serial: f81534: fix division by zero on line-speed change
  (bsc#1012628).
- USB: serial: f81232: fix division by zero on line-speed change
  (bsc#1012628).
- USB: serial: cp210x: add Kamstrup RF sniffer PIDs (bsc#1012628).
- USB: serial: option: add Quectel EM05-G modem (bsc#1012628).
- usb: gadget: uvc: Prevent buffer overflow in setup handler
  (bsc#1012628).
- udf: Fix extending file within last block (bsc#1012628).
- udf: Do not bother looking for prealloc extents if i_lenExtents
  matches i_size (bsc#1012628).
- udf: Fix preallocation discarding at indirect extent boundary
  (bsc#1012628).
- udf: Discard preallocation before extending file with a hole
  (bsc#1012628).
- irqchip/ls-extirq: Fix endianness detection (bsc#1012628).
- mips: ralink: mt7621: do not use kzalloc too early
  (bsc#1012628).
- mips: ralink: mt7621: soc queries and tests as functions
  (bsc#1012628).
- mips: ralink: mt7621: define MT7621_SYSC_BASE with __iomem
  (bsc#1012628).
- PCI: mt7621: Add sentinel to quirks table (bsc#1012628).
- libbpf: Fix uninitialized warning in btf_dump_dump_type_data
  (bsc#1012628).
- x86/vdso: Conditionally export __vdso_sgx_enter_enclave()
  (bsc#1012628).
- commit 181a470
* Wed Dec 21 2022 jslaby@suse.cz
- tcp: Add TIME_WAIT sockets in bhash2 (bsc#1206466).
- commit d8defbe
* Wed Dec 21 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and resort:
  - patches.suse/NFSD-fix-use-after-free-in-__nfs42_ssc_open.patch
- commit bf66071
* Tue Dec 20 2022 jslaby@suse.cz
- io_uring/net: ensure compat import handlers clear free_iov
  (bsc#1206509).
- commit 747fc96
* Mon Dec 19 2022 neilb@suse.de
- NFSD: fix use-after-free in __nfs42_ssc_open() (bsc#1206209
  CVE-2022-4379).
- commit 338ca73
* Fri Dec 16 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and move into sorted section:
  - patches.suse/char-xillybus-Fix-trivial-bug-with-mutex.patch
  - patches.suse/char-xillybus-Prevent-use-after-free-due-to-race-con.patch
  - patches.suse/media-dvb-core-Fix-UAF-due-to-refcount-races-at-rele.patch
  - patches.suse/misc-sgi-gru-fix-use-after-free-error-in-gru_set_con.patch
- commit 7f1864f
* Fri Dec 16 2022 vbabka@suse.cz
- mm, mremap: fix mremap() expanding vma with addr inside
  vma (bsc#1206359).
- commit b61d296
* Mon Dec 12 2022 jslaby@suse.cz
- series.conf: remove stale comment
- commit ab17686
* Mon Dec 12 2022 mkubecek@suse.cz
- Update to 6.1 final
- refresh configs (headers only)
- commit d1335c0
* Fri Dec  9 2022 jslaby@suse.cz
- Delete
  patches.suse/Input-synaptics-retry-query-upon-error.patch.
  The patch is not needed (bsc#1194086 comment 50).
- commit d03b675
* Fri Dec  9 2022 jslaby@suse.cz
- Delete patches.suse/iwlwifi-module-firmware-ucode-fix.patch.
  Not needed anymore. kernel-firmware contains -72s since 06dbfbc74388
  released in 20221109 already.
- commit e1d0837
* Fri Dec  9 2022 jslaby@suse.cz
- Delete
  patches.suse/drm-sched-Fix-kernel-NULL-pointer-dereference-error.patch.
  This can be dropped thanks to commit bafaf67c42f4 (Revert "drm/sched:
  Use parent fence instead of finished") in v6.1-rc1.
- commit 15d1c2b
* Fri Dec  9 2022 jslaby@suse.cz
- Refresh
  patches.suse/media-dvb-core-Fix-UAF-due-to-refcount-races-at-rele.patch.
  Update upstream status.
- commit d504053
* Fri Dec  9 2022 jslaby@suse.cz
- Delete patches.suse/dm-mpath-no-partitions-feature. (bsc#1189976)
- commit e544c6d
* Fri Dec  9 2022 jslaby@suse.cz
- Refresh
  patches.suse/misc-sgi-gru-fix-use-after-free-error-in-gru_set_con.patch.
  Update to final version and update upstream status.
- commit dd048d9
* Fri Dec  9 2022 jslaby@suse.cz
- Delete patches.suse/suse-hv-guest-os-id.patch. (bsc#1189965)
- commit de46b50
* Fri Dec  9 2022 jslaby@suse.cz
- Delete patches.suse/dm-mpath-leastpending-path-update. (bsc#1189962)
- commit fb9bee7
* Fri Dec  9 2022 jslaby@suse.cz
- Delete patches.suse/dm-table-switch-to-readonly. (bsc#1189963)
- commit 3a71c4d
* Fri Dec  9 2022 jslaby@suse.cz
- Delete patches.suse/kbd-ignore-gfx.patch. (bsc#1189975)
- commit 900ecbb
* Thu Dec  8 2022 jeffm@suse.com
- Revert "config: update CONFIG_LSM defaults"
  This reverts commit a05e86cb8200d8cf785b866375a4c9d06c09ab47.
  Commit 0a20128a486 (Revert "config: Enable BPF LSM" (bsc#1197746))
  indicates this needs more specific testing before merging.
- commit 7453fbc
* Thu Dec  8 2022 jeffm@suse.com
- config: update CONFIG_LSM defaults (bsc#1205603).
  CONFIG_LSM determines what the default order of LSM usage is.  The
  default order is set based on whether AppArmor or SELinux is preferred
  in the config (we still prefer AppArmor).  The default set has changed
  over time and we haven't updated it, leading to things like bpf LSMs
  not working out of the box.
  This change just updates CONFIG_LSM to what the default would be now.
- config: update CONFIG_LSM defaults
  CONFIG_LSM determines what the default order of LSM usage is.  The
  default order is set based on whether AppArmor or SELinux is preferred
  in the config (we still prefer AppArmor).  The default set has changed
  over time and we haven't updated it, leading to things like bpf LSMs
  not working out of the box.
  This change just updates CONFIG_LSM to what the default would be now.
- commit b74aeb0
* Mon Dec  5 2022 mkubecek@suse.cz
- Update to 6.1-rc8
- commit 6ba05d3
* Wed Nov 30 2022 nstange@suse.de
- Add support for enabling livepatching related packages on -RT (jsc#PED-1706)
- commit 9d41244
* Wed Nov 30 2022 jslaby@suse.cz
- char: xillybus: Fix trivial bug with mutex (bsc#1205764
  CVE-2022-45888).
- char: xillybus: Prevent use-after-free due to race condition
  (bsc#1205764 CVE-2022-45888).
- commit 8ba91a0
* Tue Nov 29 2022 afaerber@suse.com
- config: arm64: Fix Freescale LPUART dependency (boo#1204063)
  Commit 8d7f37c61a07 inserted CONFIG_SERIAL_FSL_LPUART_CONSOLE=y
  but forgot to change CONFIG_SERIAL_FSL_LPUART=m to =y as dependency,
  as the upstream Kconfig appears to be missing it for this driver.
- commit d33b52e
* Mon Nov 28 2022 mkubecek@suse.cz
- Update to 6.1-rc7
- update configs
  - x86: X86_AMD_PSTATE=y (was "m")
- commit bd1d686
* Wed Nov 23 2022 mbrugger@suse.com
- arm64: Update config files.
  Enable configs for tegra234 serial console to work.
- commit 64cc6c4
* Wed Nov 23 2022 dmueller@suse.com
- config.conf: enable armv6/armv7hl configs
- armv6/7hl: Update config files.
- commit 93e7e5c
* Mon Nov 21 2022 mkubecek@suse.cz
- Update to 6.1-rc6
- eliminate 1 patch
  - patches.suse/Input-i8042-Apply-probe-defer-to-more-ASUS-ZenBook-m.patch
- update configs
  - INET_TABLE_PERTURB_ORDER=16 (default, previous value)
- commit 4c01546
* Tue Nov 15 2022 msuchanek@suse.de
- Update config files (bsc#1205447).
  INTEGRITY_MACHINE_KEYRING=y
  IMA_KEYRINGS_PERMIT_SIGNED_BY_BUILTIN_OR_SECONDARY=n
- commit bbfbe90
* Mon Nov 14 2022 mkubecek@suse.cz
- Update to 6.1-rc5
- update configs
  - CONFIG_DRM_RCAR_USE_MIPI_DSI=n (y on arm64, like DRM_RCAR_MIPI_DSI)
  - IOSM=n (except x86)
  - TEST_MAPLE_TREE=n
  - s390x/zfcpdump: RANDOMIZE_BASE=n
- commit 4b98107
* Thu Nov 10 2022 tzimmermann@suse.de
- Disable sysfb before creating simple-framebuffer (bsc#1204315)
- commit 85b6c0f
* Wed Nov  9 2022 jlee@suse.com
- Update config files for enabling CONFIG_SECONDARY_TRUSTED_KEYRING
  In some architectures, e.g. ppc64, riscv64, x86_64, we have enabled the
  CONFIG_SECONDARY_TRUSTED_KEYRING and children kernel config. But we didn't
  enable it in other architectures.
  In the future, the CONFIG_SECONDARY_TRUSTED_KEYRING will be used with
  IMA in different architectures. So let's enable it in Tumbleweed in
  all architectures to align with SLE/Leap. Then user can use it for
  preparing IMA functions with secondary trusted keyring. (bsc#1203739)
- commit 86a9f2f
* Tue Nov  8 2022 jslaby@suse.cz
- rpm/check-for-config-changes: add TOOLCHAIN_HAS_* to IGNORED_CONFIGS_RE
  This new form was added in commit b8c86872d1dc (riscv: fix detection of
  toolchain Zicbom support).
- commit e9f2ba6
* Mon Nov  7 2022 ludwig.nussel@suse.de
- Add suse-kernel-rpm-scriptlets to kmp buildreqs (boo#1205149)
- commit 888e01e
* Mon Nov  7 2022 mkubecek@suse.cz
- Update to 6.1-rc4
- commit 3056fb1
* Wed Nov  2 2022 jslaby@suse.cz
- char: pcmcia: cm4040_cs: Fix use-after-free in reader_fops
  (bsc#1204922 CVE-2022-44033).
- commit d6c5191
* Tue Nov  1 2022 jslaby@suse.cz
- char: pcmcia: scr24x_cs: Fix use-after-free in scr24x_fops
  (bsc#1204901 CVE-2022-44034).
- char: pcmcia: cm4000_cs: Fix use-after-free in cm4000_fops
  (bsc#1204894 CVE-2022-44032).
- commit 1e6f02d
* Mon Oct 31 2022 mkubecek@suse.cz
- Update to 6.1-rc3
- eliminate 1 patch
  - patches.suse/scsi-mpi3mr-select-CONFIG_SCSI_SAS_ATTRS.patch
- refresh configs
- commit 6cba764
* Wed Oct 26 2022 mbrugger@suse.com
- arm64: Update config files. (bsc#1203558)
  Enable Renesas serial console and earlycon.
- commit 6516615
* Mon Oct 24 2022 mkubecek@suse.cz
- Update to 6.1-rc2
- commit 796d87f
* Mon Oct 17 2022 mkubecek@suse.cz
- update submitted patch
- update to v2 and rename
  - patches.suse/scsi-mpi3mr-add-explicit-dependency-on-CONFIG_SCSI_S.patch
  - > patches.suse/scsi-mpi3mr-select-CONFIG_SCSI_SAS_ATTRS.patch
- update config/x86_64/kvmsmall
  - SCSI_SAS_ATTRS=m (new dependency in 6.1-rc1)
- commit d8f9c79
* Mon Oct 17 2022 dmueller@suse.com
- config.conf: Reenable arm64
- Update config files (arm64). copy 6.1-rc1  from x86_64, enable
  all new SOC erratas, enable all new modules.
- commit 8d7f37c
* Mon Oct 17 2022 mkubecek@suse.cz
- scsi: mpi3mr: add explicit dependency on CONFIG_SCSI_SAS_ATTRS.
  Fix x86_64/kvmsmall build failure.
- commit 2fa879f
* Mon Oct 17 2022 schwab@suse.de
- rpm/check-for-config-changes: loosen pattern for AS_HAS_*
  This is needed to handle CONFIG_AS_HAS_NON_CONST_LEB128.
- commit bdc0bf7
* Mon Oct 17 2022 mkubecek@suse.cz
- Update to 6.1-rc1
- eliminate 21 patches (18 stable, 3 mainline)
  - patches.suse/ALSA-hda-realtek-Add-quirk-for-HP-Zbook-Firefly-14-G.patch
  - patches.suse/ALSA-hda-realtek-More-robust-component-matching-for-.patch
  - patches.suse/watchdog-wdat_wdt-fix-min-max-timer-value.patch
- disable
  - patches.suse/suse-hv-guest-os-id.patch (bsc#1189965)
- refresh
  - patches.suse/Input-i8042-Apply-probe-defer-to-more-ASUS-ZenBook-m.patch
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
- add DRM crash fix
  - patches.suse/drm-sched-Fix-kernel-NULL-pointer-dereference-error.patch
- disable ARM architectures (need config update)
- new config options
  - Processor type and features
  - XEN_PV_MSR_SAFE=y
  - Power management and ACPI options
  - X86_AMD_PSTATE_UT=n
  - General architecture-dependent options
  - CFI_CLANG=n
  - Memory Management options
  - LRU_GEN=y
  - LRU_GEN_ENABLED=n
  - LRU_GEN_STATS=n
  - Cryptographic API
  - CRYPTO_ARIA_AESNI_AVX_X86_64=m
  - Library routines
  - FORCE_NR_CPUS=n
  - Kernel hacking
  - DEBUG_MAPLE_TREE=n
  - TEST_DYNAMIC_DEBUG=n
  - Network device support
  - NGBE=m
  - NET_VENDOR_ADI=y
  - ADIN1110=m
  - MLX5_EN_MACSEC=y
  - PSE_CONTROLLER=y
  - PSE_REGULATOR=m
  - Input device support
  - KEYBOARD_PINEPHONE=m
  - TOUCHSCREEN_COLIBRI_VF50=m
  - Hardware Monitoring support
  - SENSORS_MAX31760=m
  - SENSORS_TPS546D24=m
  - SENSORS_EMC2305=m
  - Multifunction device drivers
  - MFD_MT6370=n
  - MFD_OCELOT=n
  - MFD_SY7636A=n
  - MFD_RT5120=n
  - Graphics support
  - DRM_USE_DYNAMIC_DEBUG=y
  - Sound card support
  - SND_SOC_AMD_PS=m
  - SND_SOC_AMD_PS_MACH=m
  - SND_SOC_SOF_AMD_REMBRANDT=m
  - SND_SOC_SOF_SKYLAKE=m
  - SND_SOC_SOF_KABYLAKE=m
  - SND_SOC_CS42L83=n
  - SND_SOC_SRC4XXX_I2C=n
  - HID support
  - HID_VRC2=m
  - HID_PXRC=m
  - HID_TOPRE=m
  - Industrial I/O support
  - MSA311=n
  - MAX11205=n
  - RICHTEK_RTQ6056=n
  - BOSCH_BNO055_SERIAL=n
  - BOSCH_BNO055_I2C=n
  - LTRF216A=n
  - Misc devices
  - GP_PCI1XXXX=m
  - AHCI_DWC=m
  - SERIAL_FSL_LPUART_CONSOLE=y
  - I2C_PCI1XXXX=m
  - SPI_MICROCHIP_CORE_QSPI=m
  - PINCTRL_CY8C95X0=m
  - EXAR_WDT=m
  - STAGING_MEDIA_DEPRECATED=n
  - CROS_TYPEC_SWITCH=m
  - AMD_PMF=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - PATA_OF_PLATFORM=m
  - COMMON_CLK_VC7=m
  - NVMEM_U_BOOT_ENV=m
  - ppc64le / ppc64
  - ARCH_FORCE_MAX_ORDER=9 (default)
  - INPUT_IBM_PANEL=m
  - KFENCE=y
  - KFENCE_SAMPLE_INTERVAL=0
  - KFENCE_NUM_OBJECTS=255
  - KFENCE_DEFERRABLE=n
  - KFENCE_STATIC_KEYS=y
  - KFENCE_STRESS_TEST_FAULTS=0
  - riscv64
  - EFI_ZBOOT=n
  - PINCTRL_STARFIVE_JH7100=m
  - CHARGER_RK817=m
  - SND_SOC_ES8326=m
  - SIFIVE_CCACHE=y
  - RESET_POLARFIRE_SOC=y
- commit 79462df
* Fri Oct 14 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section:
  - patches.suse/watchdog-wdat_wdt-fix-min-max-timer-value.patch
- commit 64a2b58
* Wed Oct 12 2022 jslaby@suse.cz
- Linux 6.0.1 (bsc#1012628).
- xsk: Inherit need_wakeup flag for shared sockets (bsc#1012628).
- fs: fix UAF/GPF bug in nilfs_mdt_destroy (bsc#1012628).
- sparc: Unbreak the build (bsc#1012628).
- Makefile.extrawarn: Move -Wcast-function-type-strict to W=1
  (bsc#1012628).
- hardening: Remove Clang's enable flag for
  - ftrivial-auto-var-init=zero (bsc#1012628).
- docs: update mediator information in CoC docs (bsc#1012628).
- hwmon: (aquacomputer_d5next) Fix Quadro fan speed offsets
  (bsc#1012628).
- usb: mon: make mmapped memory read only (bsc#1012628).
- USB: serial: ftdi_sio: fix 300 bps rate for SIO (bsc#1012628).
- gpiolib: acpi: Add support to ignore programming an interrupt
  (bsc#1012628).
- gpiolib: acpi: Add a quirk for Asus UM325UAZ (bsc#1012628).
- RISC-V: Print SSTC in canonical order (bsc#1012628).
- bpf: Gate dynptr API behind CAP_BPF (bsc#1012628).
- net: ethernet: mtk_eth_soc: fix state in __mtk_foe_entry_clear
  (bsc#1012628).
- bpf: Fix resetting logic for unreferenced kptrs (bsc#1012628).
- Bluetooth: use hdev->workqueue when queuing
  hdev->{cmd,ncmd}_timer works (bsc#1012628).
- Update config files.
- commit 0c45fd2
* Mon Oct 10 2022 tiwai@suse.de
- misc: sgi-gru: fix use-after-free error in
  gru_set_context_option, gru_fault and gru_handle_user_call_os
  (CVE-2022-3424 bsc#1204166).
- commit cf55d04
* Fri Oct  7 2022 mkubecek@suse.cz
- series.conf: cleanup
- move upstreamed patches to sorted section:
  - patches.suse/ALSA-hda-realtek-Add-quirk-for-HP-Zbook-Firefly-14-G.patch
  - patches.suse/ALSA-hda-realtek-More-robust-component-matching-for-.patch
- commit e926c4b
* Thu Oct  6 2022 jslaby@suse.cz
- fix coredump breakage (coredump fix).
- commit 97b0626
* Wed Oct  5 2022 msuchanek@suse.de
- Revert "constraints: increase disk space for all architectures"
  (bsc#1203693).
  This reverts commit 43a9011f904bc7328d38dc340f5e71aecb6b19ca.
- commit 3d33373
* Tue Oct  4 2022 tiwai@suse.de
- ALSA: hda/realtek: More robust component matching for CS35L41
  (bsc#1203699).
- ALSA: hda/realtek: Add quirk for HP Zbook Firefly 14 G9 model
  (bsc#1203699).
- commit 25aa080
* Sun Oct  2 2022 mkubecek@suse.cz
- Update to 6.0 final
- eliminate 1 patch
  - patches.suse/vduse-prevent-uninitialized-memory-accesses.patch
- refresh configs (headers only)
- commit a7dafe3
* Tue Sep 27 2022 ykaukab@suse.de
- constraints: increase disk space for all architectures
  References: bsc#1203693
  aarch64 is already suffering. SLE15-SP5 x86_64 stats show that it is
  very close to the limit.
- commit 43a9011
* Sun Sep 25 2022 mkubecek@suse.cz
- Update to 6.0-rc7
- refresh configs
- commit 74aafe0
* Fri Sep 23 2022 dmueller@suse.com
- config(arm*): disable CONFIG_PM_AUTOSLEEP and CONFIG_PM_WAKELOCKS (bsc#1189677)
- commit 1c0b96b
* Thu Sep 22 2022 dmueller@suse.com
- config.conf: reenable armv6hl configs
- commit cd71399
* Wed Sep 21 2022 tiwai@suse.de
- media: dvb-core: Fix UAF due to refcount races at releasing
  (CVE-2022-41218 bsc#1202960).
- commit 66556c1
* Wed Sep 21 2022 dmueller@suse.com
- arm64: enable CONFIG_ARCH_RENESAS (bsc#1203558)
  Also compile everything as modules that isn't debug
  or deprecated that was previously disabled by the
  global RENESAS disablement.
- commit b1f13b9
* Wed Sep 21 2022 dmueller@suse.com
- config.conf: Reenable arm64 configs
- Update config files, taken from 6.0-rc1 update from x86_64,
  enabling all new erratas, enabling all new modules
- commit 9b3cde4
* Sun Sep 18 2022 mkubecek@suse.cz
- Update to 6.0-rc6
- commit 2132e28
* Mon Sep 12 2022 jdelvare@suse.de
- watchdog: wdat_wdt: Set the min and max timeout values properly
  (bsc#1194023).
- commit 005845a
* Sun Sep 11 2022 mkubecek@suse.cz
- Update to 6.0-rc5
- eliminate 5 patches:
  - patches.suse/ASoC-nau8540-Implement-hw-constraint-for-rates.patch
  - patches.suse/ASoC-nau8821-Implement-hw-constraint-for-rates.patch
  - patches.suse/ASoC-nau8824-Fix-semaphore-unbalance-at-error-paths.patch
  - patches.suse/ASoC-nau8824-Implement-hw-constraint-for-rates.patch
  - patches.suse/ASoC-nau8825-Implement-hw-constraint-for-rates.patch
- refresh configs
- commit f7dcc92
* Tue Sep  6 2022 tiwai@suse.de
- vduse: prevent uninitialized memory accesses (CVE-2022-2308
  bsc#1202573).
- commit 70d9c50
* Sun Sep  4 2022 mkubecek@suse.cz
- Update to 6.0-rc4
- refresh configs
- commit c26d0f0
* Thu Sep  1 2022 jslaby@suse.cz
- rpm/kernel-source.spec.in: simplify finding of broken symlinks
  "find -xtype l" will report them, so use that to make the search a bit
  faster (without using shell).
- commit 13bbc51
* Wed Aug 31 2022 msuchanek@suse.de
- mkspec: eliminate @NOSOURCE@ macro
  This should be alsways used with @SOURCES@, just include the content
  there.
- commit 403d89f
* Wed Aug 31 2022 msuchanek@suse.de
- kernel-source: include the kernel signature file
  We assume that the upstream tarball is used for released kernels.
  Then we can also include the signature file and keyring in the
  kernel-source src.rpm.
  Because of mkspec code limitation exclude the signature and keyring from
  binary packages always - mkspec does not parse spec conditionals.
- commit e76c4ca
* Wed Aug 31 2022 msuchanek@suse.de
- kernel-binary: move @NOSOURCE@ to @SOURCES@ as in other packages
- commit 4b42fb2
* Wed Aug 31 2022 msuchanek@suse.de
- dtb: Do not include sources in src.rpm - refer to kernel-source
  Same as other kernel binary packages there is no need to carry duplicate
  sources in dtb packages.
- commit 1bd288c
* Mon Aug 29 2022 mkubecek@suse.cz
- Update to 6.0-rc3
- eliminate 2 patches
  - patches.suse/0001-scsi-sd-Revert-Rework-asynchronous-resume-support.patch
  - patches.suse/Revert-zram-remove-double-compression-logic.patch
- commit 824e6f8
* Thu Aug 25 2022 mkubecek@suse.cz
- series.conf: cleanup
- move recently added patches to "almost mainline" section
  - patches.suse/Revert-zram-remove-double-compression-logic.patch
  - patches.suse/ASoC-nau8821-Implement-hw-constraint-for-rates.patch
  - patches.suse/ASoC-nau8824-Fix-semaphore-unbalance-at-error-paths.patch
  - patches.suse/ASoC-nau8824-Implement-hw-constraint-for-rates.patch
  - patches.suse/ASoC-nau8825-Implement-hw-constraint-for-rates.patch
  - patches.suse/ASoC-nau8540-Implement-hw-constraint-for-rates.patch
- commit 18ca0fb
* Thu Aug 25 2022 tiwai@suse.de
- ASoC: nau8540: Implement hw constraint for rates (bsc#1201418).
- ASoC: nau8825: Implement hw constraint for rates (bsc#1201418).
- ASoC: nau8824: Implement hw constraint for rates (bsc#1201418).
- ASoC: nau8824: Fix semaphore unbalance at error paths
  (bsc#1201418).
- ASoC: nau8821: Implement hw constraint for rates (bsc#1201418).
- commit ef72ecc
* Mon Aug 22 2022 vbabka@suse.cz
- scsi: sd: Revert "Rework asynchronous resume support"
  (rc1 testing).
- commit 4aad010
* Mon Aug 22 2022 mkubecek@suse.cz
- Update to 6.0-rc2
- drop upstreamed patch
  - patches.rpmify/kbuild-dummy-tools-pretend-we-understand-__LONG_DOUB.patch
- refresh configs
- commit 712f762
* Thu Aug 18 2022 msuchanek@suse.de
- Update config files (bsc#1201361 bsc#1192968 https://github.com/rear/rear/issues/2554).
  ppc64: NVRAM=y
- commit f0e686d
* Thu Aug 18 2022 tiwai@suse.de
- Update config files: CONFIG_SPI_AMD=m on x86 (bsc#1201418)
- commit bfec82a
* Tue Aug 16 2022 jslaby@suse.cz
- rpm/kernel-binary.spec.in: move vdso to a separate package (bsc#1202385)
  We do the move only on 15.5+.
- commit 9c7ade3
* Tue Aug 16 2022 jslaby@suse.cz
- rpm/kernel-binary.spec.in: simplify find for usrmerged
  The type test and print line are the same for both cases. The usrmerged
  case only ignores more, so refactor it to make it more obvious.
- commit 583c9be
* Mon Aug 15 2022 dmueller@suse.com
- config.conf: reenable armv7hl configs
- Update config files for armv7hl (following x86_64 settings,
  compiling as module unless DEBUG or DEPRECATED)
- commit 0329b6a
* Mon Aug 15 2022 jslaby@suse.cz
- Refresh
  patches.rpmify/kbuild-dummy-tools-pretend-we-understand-__LONG_DOUB.patch.
  Update upstream status.
- commit 7c41a14
* Mon Aug 15 2022 dmueller@suse.com
- armv7hl: rebuilt as an overlay over default config
  generated automatically with scripts/config-diff
- commit 1d75725
* Mon Aug 15 2022 dmueller@suse.com
- armv6/v7: enable BT_VIRTIO
- commit ba8dcca
* Mon Aug 15 2022 tiwai@suse.de
- Refresh and re-apply i8042 quirk patch for ASUS ZenBook (bsc#1190256)
- commit aeed1e4
* Mon Aug 15 2022 mkubecek@suse.cz
- Update to 6.0-rc1
- eliminate 4 patches (all mainline)
  - patches.suse/0001-drm-Always-warn-if-user-defined-modes-are-not-suppor.patch
  - patches.suse/0001-drm-client-Don-t-add-new-command-line-mode.patch
  - patches.suse/0001-drm-client-Look-for-command-line-modes-first.patch
  - patches.suse/ath9k-fix-use-after-free-in-ath9k_hif_usb_rx_cb.patch
- disable
  - patches.suse/Input-i8042-Apply-probe-defer-to-more-ASUS-ZenBook-m.patch
- refresh
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
  - patches.suse/Revert-zram-remove-double-compression-logic.patch
- disable ARM architectures (need config update)
- new config options
  - General setup
  - CONTEXT_TRACKING_USER_FORCE=n
  - RCU_NOCB_CPU_DEFAULT_ALL=n
  - CGROUP_FAVOR_DYNMODS=n
  - Power management and ACPI options
  - PM_USERSPACE_AUTOSLEEP=n
  - Networking support
  - NF_FLOW_TABLE_PROCFS=y
  - NET_DSA_TAG_RZN1_A5PSW=m
  - File systems
  - DLM_DEPRECATED_API=n
  - Security options
  - SECURITY_APPARMOR_INTROSPECT_POLICY=y
  - SECURITY_APPARMOR_EXPORT_BINARY=y
  - SECURITY_APPARMOR_PARANOID_LOAD=y
  - IMA_KEXEC=n
  - Cryptographic API
  - CRYPTO_FIPS_NAME="Linux Kernel Cryptographic API"
  - CRYPTO_FIPS_CUSTOM_VERSION=n
  - CRYPTO_HCTR2=m
  - CRYPTO_POLYVAL_CLMUL_NI=m
  - CRYPTO_ARIA=m
  - Kernel hacking
  - SHRINKER_DEBUG=n
  - RV=n
  - PCI support
  - PCI_EPF_VNTB=m
  - Block devices
  - BLK_DEV_UBLK=m
  - NVME Support
  - NVME_AUTH=n
  - NVME_TARGET_AUTH=n
  - Network device support
  - NET_DSA_MICROCHIP_KSZ_SPI=m
  - NET_VENDOR_WANGXUN=y
  - TXGBE=m
  - CAN_NETLINK=y
  - CAN_CAN327=m
  - CAN_ESD_USB=m
  - Sound card support
  - SND_CTL_FAST_LOOKUP=y
  - SND_CTL_INPUT_VALIDATION=n
  - SND_CTL_DEBUG=n
  - SND_SOC_AMD_ST_ES8336_MACH=m
  - SND_AMD_ASOC_REMBRANDT=m
  - SND_SOC_AMD_RPL_ACP6x=m
  - SND_SOC_INTEL_AVS_MACH_DA7219=m
  - SND_SOC_INTEL_AVS_MACH_DMIC=m
  - SND_SOC_INTEL_AVS_MACH_HDAUDIO=m
  - SND_SOC_INTEL_AVS_MACH_I2S_TEST=m
  - SND_SOC_INTEL_AVS_MACH_MAX98357A=m
  - SND_SOC_INTEL_AVS_MACH_MAX98373=m
  - SND_SOC_INTEL_AVS_MACH_NAU8825=m
  - SND_SOC_INTEL_AVS_MACH_RT274=m
  - SND_SOC_INTEL_AVS_MACH_RT286=m
  - SND_SOC_INTEL_AVS_MACH_RT298=m
  - SND_SOC_INTEL_AVS_MACH_RT5682=m
  - SND_SOC_INTEL_AVS_MACH_SSM4567=m
  - SND_SOC_SOF_METEORLAKE=m
  - SND_SOC_TAS2780=n
  - SND_SOC_WSA883X=n
  - USB support
  - UCSI_STM32G0=m
  - TYPEC_ANX7411=m
  - Microsoft Surface Platform-Specific Device Drivers
  - SURFACE_AGGREGATOR_HUB=m
  - SURFACE_AGGREGATOR_TABLET_SWITCH=m
  - Industrial I/O support
  - ENVELOPE_DETECTOR=n
  - SD_ADC_MODULATOR=n
  - VF610_ADC=n
  - Misc devices
  - TCG_TIS_I2C=m
  - SPI_MICROCHIP_CORE=m
  - PINCTRL_METEORLAKE=m
  - SENSORS_LT7182S=m
  - VIDEO_AR0521=m
  - LEDS_IS31FL319X=m
  - INFINIBAND_ERDMA=m
  - XEN_VIRTIO_FORCE_GRANT=n
  - VIDEO_STKWEBCAM=n
  - PWM_CLK=m
  - RESET_TI_TPS380X=n
  - ANDROID_BINDER_IPC=n
  - FPGA_MGR_MICROCHIP_SPI=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - VCPU_STALL_DETECTOR=m
  - DRM_PANEL_EBBG_FT8719=n
  - DRM_TI_DLPC3433=n
  - DRM_LOGICVC=n
  - DRM_IMX_LCDIF=n
  - I2C_HID_OF_ELAN=m
  - USB_ONBOARD_HUB=m
  - RTC_DRV_NCT3018Y=m
  - ppc64(le), s390x and riscv64
  - SCSI_BUSLOGIC=m
  - SCSI_FLASHPOINT=n
  - ppc64le and riscv64
  - CRYPTO_DEV_QAT_DH895xCC=m
  - CRYPTO_DEV_QAT_C3XXX=m
  - CRYPTO_DEV_QAT_C62X=m
  - CRYPTO_DEV_QAT_4XXX=m
  - CRYPTO_DEV_QAT_DH895xCCVF=m
  - CRYPTO_DEV_QAT_C3XXXVF=m
  - CRYPTO_DEV_QAT_C62XVF=m
  - ppc64 / ppc64le
  - PSERIES_PLPKS=y
  - KVM_BOOK3S_HV_P9_TIMING=n
  - KVM_BOOK3S_HV_P8_TIMING=n
  - RANDOMIZE_KSTACK_OFFSET=y
  - RANDOMIZE_KSTACK_OFFSET_DEFAULT=y
  - PSERIES_WDT=m
  - s390x
  - VFIO_PCI_ZDEV_KVM=y
  - riscv64
  - ERRATA_THEAD_CMO=y
  - NONPORTABLE=n
  - RISCV_ISA_ZICBOM=y
  - RANDOM_TRUST_CPU=y
  - I2C_MICROCHIP_CORE=m
  - SND_SOC_HDA=m
  - USB_MUSB_POLARFIRE_SOC=m
  - RTC_DRV_POLARFIRE_SOC=m
- commit c35dc38
* Fri Aug 12 2022 tiwai@suse.de
- Refresh patches.suse/iwlwifi-module-firmware-ucode-fix.patch.
  Now iwlwifi queries *-72.ucode, but again, this is non-existing version.
  Correct to the existing *-71.ucode
- commit 58a95c5
* Wed Aug 10 2022 jeffm@suse.com
- config: Disable reiserfs kernel module (bsc#1202309).
  Future access of reiserfs file systems can be done by using the FUSE
  implementation of reiserfs that ships with GRUB.
  $ grub2-mount <dev> /path/to/mountpoint
- commit db8891f
* Wed Aug 10 2022 jslaby@suse.cz
- kbuild: dummy-tools: pretend we understand __LONG_DOUBLE_128__
  (ppc config fix).
- Update config files.
  This sets PPC_LONG_DOUBLE_128 automatically and allows us to set
  DRM_AMD_SECURE_DISPLAY too. I set it to y to copy other architectures.
- commit 48dfdff
* Tue Aug  9 2022 jslaby@suse.cz
- Update config files -- set SECURITY_SELINUX_CHECKREQPROT_VALUE=0 (bsc#1202280)
- commit 6a791bc
* Tue Aug  9 2022 jslaby@suse.cz
- Revert "zram: remove double compression logic" (bsc#1202203).
- commit 9739fe2
* Tue Aug  9 2022 jslaby@suse.cz
- series.conf: remove blank line from sorted section
  It causes troubles when adding multiple patches -- the current ones are
  duplicated then.
- commit 309e362
* Fri Aug  5 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and resort:
  - patches.suse/0001-drm-Always-warn-if-user-defined-modes-are-not-suppor.patch
  - patches.suse/0001-drm-client-Don-t-add-new-command-line-mode.patch
  - patches.suse/0001-drm-client-Look-for-command-line-modes-first.patch
- update upstream references and move into sorted section:
  - patches.suse/ath9k-fix-use-after-free-in-ath9k_hif_usb_rx_cb.patch
- commit 35466a9
* Wed Aug  3 2022 msuchanek@suse.de
- Update config files (bsc#1184924).
  +RANDOM_TRUST_BOOTLOADER on arm
  This is set on all other platforms in Tumbleweed, and only on ARM in
  Leap. The ARM platform is unique in that it can have random source
  defined in EFI firmware as well as device tree, and we don't test this
  configuration in Factory because of the inverted config situation
  betwween Tumbleweed and Leap.
- commit 1275841
* Tue Aug  2 2022 msuchanek@suse.de
- Fix parsing of rpm/macros.kernel-source on SLE12 (bsc#1201019).
- commit 9816878
* Sun Jul 31 2022 mkubecek@suse.cz
- Update to 5.19 final
- refresh configs
- commit e9f89c9
* Tue Jul 26 2022 mbrugger@suse.com
- armv7hl: Update config files. (bsc#1201857)
  Enable PCI wifi chips
- commit d472a44
* Mon Jul 25 2022 tzimmermann@suse.de
- config: riscv64: Enable DRM stack for early-boot graphics (boo#1201833)
  Replace fbdev's generic drivers with DRM-based simpledrm. Enables the
  DRM graphics stack for early-boot graphics, recovery and unsupported
  chipsets.
- commit b8947d7
* Mon Jul 25 2022 tzimmermann@suse.de
- config: armv7hl: Enable DRM stack for early-boot graphics (boo#1193475)
  Replace fbdev's generic drivers with DRM-based simpledrm. Enables the
  DRM graphics stack for early-boot graphics, recovery and unsupported
  chipsets.
- commit 374bc62
* Mon Jul 25 2022 tzimmermann@suse.de
- config: armv6hl: Enable DRM stack for early-boot graphics (boo#1193475)
  Replace fbdev's generic drivers with DRM-based simpledrm. Enables the
  DRM graphics stack for early-boot graphics, recovery and unsupported
  chipsets.
- commit 07f549a
* Mon Jul 25 2022 tzimmermann@suse.de
- config: arm64: Enable DRM stack for early-boot graphics (boo#1193475)
  Replace fbdev's generic drivers with DRM-based simpledrm. Enables the
  DRM graphics stack for early-boot graphics, recovery and unsupported
  chipsets.
- commit 146fbca
* Mon Jul 25 2022 mkubecek@suse.cz
- Update to 5.19-rc8
- update configs
  - PINCTRL_AMD=y (arm64 only, no longer allowed to be a module)
- commit 96ba878
* Sun Jul 24 2022 mkubecek@suse.cz
- config: update and enable armv6hl
  Config option values were taken from global 5.19 updates while armv6hl
  configs were disabled, arm64 updates in commit 14beb34d0af9 ("config:
  update and enable arm64") and armv7hl config updates in commit 36833cf30926
  ("config: update and enable armv7hl").
- commit de516ba
* Sun Jul 24 2022 mkubecek@suse.cz
- config: update and enable armv7hl
  The list below omits config options update globally while armv7hl configs
  were disabled and config options updated on arm64 for 5.19 in commit
  14beb34d0af9 ("config: update and enable arm64").
- new config options
  - ARCH_BCMBCA=y
  - ARCH_HPE=y
  - ARCH_HPE_GXP=y
  - CPU_LITTLE_ENDIAN=y
  - ARM_ERRATA_764319=y
  - GVE=m
  - PINCTRL_IMXRT1170=y
  - GXP_WATCHDOG=m
  - MEDIA_CEC_RC=y
  - COMMON_CLK_EN7523=y
- new config options in armv7hl/lpae
  - EDAC_SYNOPSYS=m
  - XILINX_INTC=y
- commit 36833cf
* Sun Jul 24 2022 mkubecek@suse.cz
- config: update and enable arm64
  The list below omits config options updated globally while arm64 configs
  were disabled.
- new config options
  - ARM64_SME=y
  - CRYPTO_SM4_ARM64_CE_BLK=m
  - CRYPTO_SM4_ARM64_NEON_BLK=m
  - CAN_CTUCANFD_PLATFORM=m
  - QCOM_SSC_BLOCK_BUS=y
  - MTK_ADSP_IPC=m
  - MTD_NAND_ECC_MEDIATEK=m
  - NVME_APPLE=m
  - VMWARE_VMCI=m
  - SPI_MTK_SNFI=m
  - PINCTRL_IMXRT1170=m
  - PINCTRL_MT6795=y
  - PINCTRL_SC7280_LPASS_LPI=m
  - PINCTRL_SM8250_LPASS_LPI=m
  - ROCKCHIP_VOP=y
  - ROCKCHIP_VOP2=y
  - DRM_MSM_MDP4=y
  - DRM_MSM_MDP5=y
  - DRM_MSM_DPU=y
  - DRM_MSM_HDMI=y
  - DRM_PANEL_NEWVISION_NV3052C=m
  - DRM_FSL_LDB=m
  - DRM_LONTIUM_LT9211=m
  - DRM_DW_HDMI_GP_AUDIO=m
  - DRM_SSD130X_SPI=m
  - SND_SERIAL_GENERIC=m
  - SND_SOC_MT8195_MT6359=m
  - SND_SOC_SOF_MT8186=m
  - SND_SOC_TEGRA186_ASRC=m
  - LEDS_QCOM_LPG=m
  - TEGRA186_GPC_DMA=m
  - COMMON_CLK_MT8186=y
  - SC_GCC_8280XP=m
  - SC_LPASS_CORECC_7280=m
  - APPLE_RTKIT=m
  - APPLE_SART=m
  - PWM_XILINX=m
  - NVMEM_APPLE_EFUSES=m
  - INTERCONNECT_QCOM_SC8280XP=m
  - INTERCONNECT_QCOM_SDX65=m
  - HTE_TEGRA194=m
  - HTE_TEGRA194_TEST=n
  - TRUSTED_KEYS_CAAM=y
  - CRYPTO_DEV_FSL_CAAM_PRNG_API=y
  - FIPS_SIGNATURE_SELFTEST=n
  - PAGE_TABLE_CHECK=y
  - PAGE_TABLE_CHECK_ENFORCED=n
  - VMWARE_VMCI_VSOCKETS=m
- commit 14beb34
* Sat Jul 23 2022 schwab@suse.de
- riscv: enable CONFIG_STRICT_DEVMEM
- new config options
  - CONFIG_EXCLUSIVE_SYSTEM_RAM=y
  - CONFIG_IO_STRICT_DEVMEM=y
- commit 2477a0c
* Sat Jul 23 2022 schwab@suse.de
- riscv: enable CONFIG_FTRACE
  - new config options
  - CONFIG_BPF_LSM=y
  - CONFIG_TASKS_RUDE_RCU=y
  - CONFIG_TRACEPOINTS=y
  - CONFIG_KPROBES_ON_FTRACE=y
  - CONFIG_UPROBES=y
  - CONFIG_BATMAN_ADV_TRACING=n
  - CONFIG_NET_DROP_MONITOR=m
  - CONFIG_ATH5K_TRACER=n
  - CONFIG_ATH6KL_TRACING=n
  - CONFIG_WIL6210_TRACING=y
  - CONFIG_ATH10K_TRACING=n
  - CONFIG_ATH11K_TRACING=n
  - CONFIG_IWLWIFI_DEVICE_TRACING=n
  - CONFIG_STM_SOURCE_FTRACE=m
  - CONFIG_PSTORE_FTRACE=n
  - CONFIG_DEBUG_PAGE_REF=n
  - CONFIG_NOP_TRACER=y
  - CONFIG_TRACER_MAX_TRACE=y
  - CONFIG_TRACE_CLOCK=y
  - CONFIG_RING_BUFFER=y
  - CONFIG_EVENT_TRACING=y
  - CONFIG_CONTEXT_SWITCH_TRACER=y
  - CONFIG_RING_BUFFER_ALLOW_SWAP=y
  - CONFIG_TRACING=y
  - CONFIG_GENERIC_TRACER=y
  - CONFIG_BOOTTIME_TRACING=y
  - CONFIG_FUNCTION_TRACER=y
  - CONFIG_FUNCTION_GRAPH_TRACER=y
  - CONFIG_DYNAMIC_FTRACE=y
  - CONFIG_DYNAMIC_FTRACE_WITH_REGS=y
  - CONFIG_FUNCTION_PROFILER=y
  - CONFIG_STACK_TRACER=y
  - CONFIG_IRQSOFF_TRACER=n
  - CONFIG_SCHED_TRACER=y
  - CONFIG_HWLAT_TRACER=n
  - CONFIG_OSNOISE_TRACER=y
  - CONFIG_TIMERLAT_TRACER=y
  - CONFIG_FTRACE_SYSCALLS=y
  - CONFIG_TRACER_SNAPSHOT=y
  - CONFIG_TRACER_SNAPSHOT_PER_CPU_SWAP=y
  - CONFIG_BRANCH_PROFILE_NONE=y
  - CONFIG_PROFILE_ANNOTATED_BRANCHES=n
  - CONFIG_BLK_DEV_IO_TRACE=y
  - CONFIG_KPROBE_EVENTS=y
  - CONFIG_KPROBE_EVENTS_ON_NOTRACE=n
  - CONFIG_UPROBE_EVENTS=y
  - CONFIG_BPF_EVENTS=y
  - CONFIG_DYNAMIC_EVENTS=y
  - CONFIG_PROBE_EVENTS=y
  - CONFIG_BPF_KPROBE_OVERRIDE=n
  - CONFIG_FTRACE_MCOUNT_RECORD=y
  - CONFIG_FTRACE_MCOUNT_USE_CC=y
  - CONFIG_SYNTH_EVENTS=y
  - CONFIG_TRACE_EVENT_INJECT=n
  - CONFIG_TRACEPOINT_BENCHMARK=n
  - CONFIG_RING_BUFFER_BENCHMARK=m
  - CONFIG_TRACE_EVAL_MAP_FILE=n
  - CONFIG_FTRACE_RECORD_RECURSION=n
  - CONFIG_FTRACE_STARTUP_TEST=n
  - CONFIG_RING_BUFFER_STARTUP_TEST=n
  - CONFIG_RING_BUFFER_VALIDATE_TIME_DELTAS=n
  - CONFIG_PREEMPTIRQ_DELAY_TEST=m
  - CONFIG_SYNTH_EVENT_GEN_TEST=n
  - CONFIG_KPROBE_EVENT_GEN_TEST=n
- commit 9875d6f
* Thu Jul 21 2022 mbrugger@suse.com
- arm64: Update config files. (bsc#1198737)
  Enable RTC_DRV_RX8025 to support RX-8035 on Traveres Ten64 board.
- commit 0577443
* Wed Jul 20 2022 ludwig.nussel@suse.de
- kernel-obs-build: include qemu_fw_cfg (boo#1201705)
- commit e2263d4
* Tue Jul 19 2022 tiwai@suse.de
- Input: i8042 - Apply probe defer to more ASUS ZenBook models
  (bsc#1190256).
- commit 6307fb1
* Mon Jul 18 2022 tzimmermann@suse.de
- config: i386: Enable DRM stack for early-boot graphics (boo#1193474)
  Replace fbdev's generic drivers with DRM-based simpledrm. Enables the
  DRM graphics stack for early-boot graphics, recovery and unsupported
  chipsets.
- commit eab3412
* Sun Jul 17 2022 mkubecek@suse.cz
- Update to 5.19-rc7
- drop obsolete patches
  - patches.suse/tty-extract-tty_flip_buffer_commit-from-tty_flip_buf.patch
  - patches.suse/tty-use-new-tty_insert_flip_string_and_push_buffer-i.patch
- update configs (x86 only)
  - SPECULATION_MITIGATIONS=y
  - RETHUNK=y
  - CPU_UNRET_ENTRY=y
  - CPU_IBPB_ENTRY=y
  - CPU_IBRS_ENTRY=y
- commit 900302b
* Thu Jul 14 2022 jeffm@suse.com
- rpm/kernel-binary.spec.in: Require dwarves >= 1.22 on SLE15-SP3 or newer
  Dwarves 1.22 or newer is required to build kernels with BTF information
  embedded in modules.
- commit ee19e9d
* Thu Jul 14 2022 jslaby@suse.cz
- tty: use new tty_insert_flip_string_and_push_buffer() in
  pty_write() (bsc#1198829 CVE-2022-1462).
- tty: extract tty_flip_buffer_commit() from
  tty_flip_buffer_push() (bsc#1198829 CVE-2022-1462).
- commit 482cf4a
* Wed Jul 13 2022 schwab@suse.de
- config: riscv: disable RISCV_BOOT_SPINWAIT
  We now rely on the SBI HSM extension which is provided by openSBI 0.7 or
  later.
- commit 8752291
* Wed Jul 13 2022 schwab@suse.de
- config: riscv: disable RISCV_SBI_V01
  The SBI v0.1 API is obsolete.
- commit 44178e7
* Mon Jul 11 2022 mkubecek@suse.cz
- Update to 5.19-rc6
- update configs
  - s390x/zfcpdump
  - CRC32_S390=n
  - SHA512_S390=n
  - SHA1_S390=n
  - SHA256_S390=n
  - SHA3_256_S390=n
  - SHA3_512_S390=n
  - GHASH_S390=n
  - AES_S390=n
  - DES_S390=n
  - CHACHA_S390=n
  - KEXEC_FILE=n
- commit 5477bdd
* Mon Jul  4 2022 mkubecek@suse.cz
- Update to 5.19-rc5
- update contigs
  - VIRTIO_HARDEN_NOTIFICATION=n
- commit 59940d4
* Mon Jun 27 2022 mkubecek@suse.cz
- Update to 5.19-rc4
- update configs
  - FIPS_SIGNATURE_SELFTEST=n
- commit c256fc8
* Fri Jun 24 2022 mkubecek@suse.cz
- config: enable MLX90614
  MLX90614 is I2C (SMBus) remote temperature sensor.
  The boards are available for SBCs:
  https://www.waveshare.com/product/modules/sensors/temperature-humidity-barometer/infrared-temperature-sensor.htm
  Enable the driver for potential users.
  Link: https://lists.opensuse.org/archives/list/kernel@lists.opensuse.org/thread/VHBAZ4YTJZ6H2DTMELYWILNGMRBXBMPI/
- commit cfad977
* Wed Jun 22 2022 jslaby@suse.cz
- Update config files.
  Run oldconfig which unsets CC_NO_ARRAY_BOUNDS as dummy tools emulate gcc
  20. We are ignoring it thanks to update in packaging, so that real
  compilation sets this right later.
- commit e4ff964
* Wed Jun 22 2022 jslaby@suse.cz
- rpm/check-for-config-changes: ignore GCC12/CC_NO_ARRAY_BOUNDS
  Upstream commit f0be87c42cbd (gcc-12: disable '-Warray-bounds'
  universally for now) added two new compiler-dependent configs:
  * CC_NO_ARRAY_BOUNDS
  * GCC12_NO_ARRAY_BOUNDS
  Ignore them -- they are unset by dummy tools (they depend on gcc version
  == 12), but set as needed during real compilation.
- commit a14607c
* Tue Jun 21 2022 tiwai@suse.de
- ath9k: fix use-after-free in ath9k_hif_usb_rx_cb (CVE-2022-1679
  bsc#1199487).
- commit f4c43ea
* Sun Jun 19 2022 mkubecek@suse.cz
- Update to 5.19-rc3
- update configs
  - XILINX_INTC=y (OF architectures - i386, ppc64/ppc64le, riscv64)
- commit e8495ca
* Tue Jun 14 2022 mkubecek@suse.cz
- kernel-binary.spec: check s390x vmlinux location
  As a side effect of mainline commit edd4a8667355 ("s390/boot: get rid of
  startup archive"), vmlinux on s390x moved from "compressed" subdirectory
  directly into arch/s390/boot. As the specfile is shared among branches,
  check both locations and let objcopy use one that exists.
- commit cd15543
* Tue Jun 14 2022 tiwai@suse.de
- Add missing recommends of kernel-install-tools to kernel-source-vanilla (bsc#1200442)
- commit 93b1375
* Mon Jun 13 2022 mkubecek@suse.cz
- config: add CC_NO_ARRAY_BOUNDS=y
  Mainline commit f0be87c42cbd ("gcc-12: disable '-Warray-bounds' universally
  for now") adds new config option CONFIG_CC_NO_ARRAY_BOUNDS which is only
  present for gcc12 (and not future gcc >= 13). Therefore it is not added
  with dummy gcc which pretends to be gcc20 but it is with Factory gcc12,
  resulting in failed "missing config option" check.
  As a quick hack, add CONFIG_CC_NO_ARRAY_BOUNDS=y to all full configs until
  we have a more robust solution (manually added config option won't survive
  a config update with run_oldconfig.sh).
- commit b2fb712
* Mon Jun 13 2022 mkubecek@suse.cz
- config: refresh
- commit dbcb5bd
* Mon Jun 13 2022 mkubecek@suse.cz
- Update to 5.19-rc2
- drop obsolete patch
  - patches.suse/drm-amdgpu-always-flush-the-TLB-on-gfx8.patch
- update configs
  - XEN_VIRTIO=y (x86 only)
- commit 02193c9
* Fri Jun 10 2022 tzimmermann@suse.de
- Add parameter to disable simple-framebuffer devices (boo#1193472)
  Temporary workaround for simpledrm bugs.
- commit 1d1dbce
* Fri Jun 10 2022 tzimmermann@suse.de
- drivers/firmware: skip simpledrm if nvidia-drm.modeset=1 is set (boo#1193472)
  Temporary workaround for nvidia.ko with simpledrm.
- commit c35bbe0
* Fri Jun 10 2022 tzimmermann@suse.de
- drm/client: Don't add new command-line mode (boo#1193472)
  Backported for simpledrm support.
- commit 141a4fc
* Fri Jun 10 2022 tzimmermann@suse.de
- drm/client: Look for command-line modes first (boo#1193472)
  Backported for simpledrm support.
- commit 1bf947f
* Fri Jun 10 2022 tzimmermann@suse.de
- drm: Always warn if user-defined modes are not supported (boo#1193472)
  Backported for simpledrm support.
- commit 95c4112
* Wed Jun  8 2022 tiwai@suse.de
- Update config files: disable CONFIG_NET_DSA_REALTEK_* on x86_64 (bsc#1200254)
- commit 262234b
* Tue Jun  7 2022 tiwai@suse.de
- Update config files: restore CONFIG_I8K=y (bsc#1199958)
- commit 04cadbf
* Mon Jun  6 2022 mkubecek@suse.cz
- Update to 5.19-rc1
- eliminate 54 patches (48 stable, 5 mainline, 1 other)
  - patches.kernel.org/*
  - patches.rpmify/scripts-dummy-tools-add-pahole.patch
  - patches.suse/KVM-x86-avoid-calling-x86-emulator-without-a-decoded-instruction
  - patches.suse/Revert-net-af_key-add-check-for-pfkey_broadcast-in-f.patch
  - patches.suse/iommu-amd-Increase-timeout-waiting-for-GA-log-enablement
  - patches.suse/simplefb-Enable-boot-time-VESA-graphic-mode-selectio.patch
  - patches.rpmify/powerpc-64-BE-option-to-use-ELFv2-ABI-for-big-endian.patch
- refresh
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/genksyms-add-override-flag.diff
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- 5.19-rc1 regression fix
  - patches.suse/drm-amdgpu-always-flush-the-TLB-on-gfx8.patch
- disable ARM architectures (need config update)
- new config options
  - General setup
  - CONFIG_BOOT_CONFIG_EMBED=n
  - CONFIG_INITRAMFS_PRESERVE_MTIME=y
  - Processor type and features
  - CONFIG_INTEL_TDX_GUEST=y
  - CONFIG_PERF_EVENTS_AMD_BRS=y
  - CONFIG_MICROCODE_LATE_LOADING=n
  - Enable loadable module support
  - CONFIG_MODULE_UNLOAD_TAINT_TRACKING=y
  - Memory Management options
  - CONFIG_PTE_MARKER_UFFD_WP=y
  - Networking support
  - CONFIG_CAN_CTUCANFD_PCI=m
  - File systems
  - CONFIG_CACHEFILES_ONDEMAND=n
  - CONFIG_HUGETLB_PAGE_OPTIMIZE_VMEMMAP_DEFAULT_ON=n
  - Security options
  - CONFIG_TRUSTED_KEYS_TPM=y
  - CONFIG_TRUSTED_KEYS_TEE=y
  - CONFIG_RANDSTRUCT_NONE=y
  - Cryptographic API
  - CONFIG_CRYPTO_SM3_GENERIC=m
  - CONFIG_CRYPTO_SM4_GENERIC=m
  - CONFIG_SYSTEM_BLACKLIST_AUTH_UPDATE=y
  - Kernel hacking
  - CONFIG_DEBUG_NET=n
  - CONFIG_RCU_EXP_CPU_STALL_TIMEOUT=0
  - Generic Driver Options
  - CONFIG_FW_LOADER_COMPRESS_XZ=y
  - CONFIG_FW_LOADER_COMPRESS_ZSTD=y
  - CONFIG_FW_UPLOAD=y
  - Firmware Drivers
  - CONFIG_EFI_DXE_MEM_ATTRIBUTES=y
  - CONFIG_EFI_DISABLE_RUNTIME=n
  - CONFIG_EFI_COCO_SECRET=y
  - Network device support
  - CONFIG_OCTEON_EP=m
  - CONFIG_SFC_SIENA=m
  - CONFIG_SFC_SIENA_MTD=y
  - CONFIG_SFC_SIENA_MCDI_MON=y
  - CONFIG_SFC_SIENA_SRIOV=y
  - CONFIG_SFC_SIENA_MCDI_LOGGING=y
  - CONFIG_ADIN1100_PHY=m
  - CONFIG_DP83TD510_PHY=m
  - CONFIG_WLAN_VENDOR_PURELIFI=y
  - CONFIG_PLFXLC=m
  - CONFIG_RTW89_8852CE=m
  - CONFIG_WLAN_VENDOR_SILABS=y
  - CONFIG_MTK_T7XX=m
  - Input device support
  - CONFIG_JOYSTICK_SENSEHAT=m
  - CONFIG_INPUT_IQS7222=m
  - Hardware Monitoring support
  - CONFIG_SENSORS_NCT6775_I2C=m
  - CONFIG_SENSORS_XDPE152=m
  - Sound card support
  - CONFIG_SND_SOC_CS35L45_SPI=m
  - CONFIG_SND_SOC_CS35L45_I2C=m
  - CONFIG_SND_SOC_MAX98396=m
  - CONFIG_SND_SOC_WM8731_I2C=n
  - CONFIG_SND_SOC_WM8731_SPI=n
  - CONFIG_SND_SOC_WM8940=n
  - Virtualization drivers
  - CONFIG_EFI_SECRET=m
  - CONFIG_SEV_GUEST=m
  - X86 Platform Specific Device Drivers
  - CONFIG_INTEL_IFS=m
  - CONFIG_WINMATE_FM07_KEYS=m
  - Industrial I/O support
  - CONFIG_DMARD06=n
  - CONFIG_IIO_RESCALE=m
  - CONFIG_DPOT_DAC=n
  - CONFIG_VF610_DAC=n
  - CONFIG_CM3605=n
  - CONFIG_AK8974=n
  - CONFIG_IIO_MUX=m
  - CONFIG_HTE=y
  - CONFIG_HTE=y
  - Misc devices
  - CONFIG_INTEL_MEI_GSC=m
  - CONFIG_MHI_BUS_EP=m
  - CONFIG_REGULATOR_RT5759=m
  - CONFIG_HID_MEGAWORLD_FF=m
  - CONFIG_TYPEC_MUX_FSA4480=m
  - CONFIG_LEDS_PWM_MULTICOLOR=m
  - CONFIG_CHROMEOS_ACPI=m
  - CONFIG_NVSW_SN2201=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - DRM_PANEL_NEWVISION_NV3052C=n
  - DRM_FSL_LDB=n
  - DRM_LONTIUM_LT9211=n
  - SND_SERIAL_GENERIC=m
  - LEDS_QCOM_LPG=m
  - OMAP_GPMC=m
  - OMAP_GPMC_DEBUG=n
  - PWM_XILINX=m
  - i386
  - CAN_CTUCANFD_PLATFORM=m
  - ppc64/ppc64le
  - KASAN=n
  - s390x
  - S390_UV_UAPI=m
  - MUX_ADG792A=n
  - riscv64
  - ERRATA_THEAD=y
  - ERRATA_THEAD_PBMT=y
  - RISCV_ISA_SVPBMT=y
  - KEXEC_FILE=y
  - COMPAT=y
  - ARCH_MMAP_RND_COMPAT_BITS=8 (default)
  - NETFILTER_XTABLES_COMPAT=y
  - CAN_CTUCANFD_PLATFORM=m
  - HW_RANDOM_POLARFIRE_SOC=m
  - DRM_DW_HDMI_GP_AUDIO=n
  - IMA_KEXEC=y
  - STACK_HASH_ORDER=20 (default)
  - PAGE_TABLE_CHECK=y
  - PAGE_TABLE_CHECK_ENFORCED=n
  - */debug
  - DEBUG_NET=y
- commit 515f42c
* Fri Jun  3 2022 jack@suse.cz
- Remove mistakenly enabled CONFIG_JBD2_DEBUG.
- commit 7534680
* Wed Jun  1 2022 jroedel@suse.de
- iommu/amd: Increase timeout waiting for GA log enablement
  (bsc#1199052).
- commit dfccb72
* Wed Jun  1 2022 jroedel@suse.de
- KVM: x86: avoid calling x86 emulator without a decoded
  instruction (CVE-2022-1852 bsc#1199875).
- commit 01a406d
* Mon May 30 2022 jslaby@suse.cz
- Linux 5.18.1 (bsc#1012628).
- ALSA: ctxfi: Add SB046x PCI ID (bsc#1012628).
- ACPI: sysfs: Fix BERT error region memory mapping (bsc#1012628).
- random: check for signals after page of pool writes
  (bsc#1012628).
- random: wire up fops->splice_{read,write}_iter() (bsc#1012628).
- random: convert to using fops->write_iter() (bsc#1012628).
- random: convert to using fops->read_iter() (bsc#1012628).
- random: unify batched entropy implementations (bsc#1012628).
- random: move randomize_page() into mm where it belongs
  (bsc#1012628).
- random: move initialization functions out of hot pages
  (bsc#1012628).
- random: make consistent use of buf and len (bsc#1012628).
- random: use proper return types on get_random_{int,long}_wait()
  (bsc#1012628).
- random: remove extern from functions in header (bsc#1012628).
- random: use static branch for crng_ready() (bsc#1012628).
- random: credit architectural init the exact amount
  (bsc#1012628).
- random: handle latent entropy and command line from
  random_init() (bsc#1012628).
- random: use proper jiffies comparison macro (bsc#1012628).
- random: remove ratelimiting for in-kernel unseeded randomness
  (bsc#1012628).
- random: move initialization out of reseeding hot path
  (bsc#1012628).
- random: avoid initializing twice in credit race (bsc#1012628).
- random: use symbolic constants for crng_init states
  (bsc#1012628).
- siphash: use one source of truth for siphash permutations
  (bsc#1012628).
- random: help compiler out with fast_mix() by using simpler
  arguments (bsc#1012628).
- random: do not use input pool from hard IRQs (bsc#1012628).
- random: order timer entropy functions below interrupt functions
  (bsc#1012628).
- random: do not pretend to handle premature next security model
  (bsc#1012628).
- random: use first 128 bits of input as fast init (bsc#1012628).
- random: do not use batches when !crng_ready() (bsc#1012628).
- random: insist on random_get_entropy() existing in order to
  simplify (bsc#1012628).
- xtensa: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- sparc: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- um: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- x86/tsc: Use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- nios2: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- arm: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- mips: use fallback for random_get_entropy() instead of just
  c0 random (bsc#1012628).
- riscv: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- m68k: use fallback for random_get_entropy() instead of zero
  (bsc#1012628).
- timekeeping: Add raw clock fallback for random_get_entropy()
  (bsc#1012628).
- powerpc: define get_cycles macro for arch-override
  (bsc#1012628).
- alpha: define get_cycles macro for arch-override (bsc#1012628).
- parisc: define get_cycles macro for arch-override (bsc#1012628).
- s390: define get_cycles macro for arch-override (bsc#1012628).
- ia64: define get_cycles macro for arch-override (bsc#1012628).
- init: call time_init() before rand_initialize() (bsc#1012628).
- random: fix sysctl documentation nits (bsc#1012628).
- HID: amd_sfh: Add support for sensor discovery (bsc#1012628).
- lockdown: also lock down previous kgdb use (bsc#1012628).
- commit df81444
* Fri May 27 2022 msuchanek@suse.de
- Update config files -- DEBUG_INFO_DWARF5 (bsc#1199932)
  Set DEBUG_INFO_DWARF5 which makes use of dwarf5 on gcc-7 and newer.
- commit d1b0a08
* Thu May 26 2022 mkubecek@suse.cz
- Update patches.suse/Revert-net-af_key-add-check-for-pfkey_broadcast-in-f.patch
  Update to upstream version, update upstream reference and move into sorted
  section.
- commit 3ae1db7
* Thu May 26 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move into sorted section:
  - patches.suse/simplefb-Enable-boot-time-VESA-graphic-mode-selectio.patch
- commit dc762c4
* Thu May 26 2022 msuchanek@suse.de
- kernel-binary.spec: Support radio selection for debuginfo.
  To disable debuginfo on 5.18 kernel a radio selection needs to be
  switched to a different selection. This requires disabling the currently
  active option and selecting NONE as debuginfo type.
- commit 43b5dd3
* Thu May 26 2022 jslaby@suse.cz
- Update config files -- DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT (bsc#1199932)
  Set DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT which makes use of dwarf5 on
  gcc-11 and newer.
- commit f439809
* Mon May 23 2022 schwab@suse.de
- Add dtb-starfive
- commit 85335b1
* Mon May 23 2022 mkubecek@suse.cz
- Revert "net: af_key: add check for pfkey_broadcast in function
  pfkey_process" (20220523022438.ofhehjievu2alj3h@lion.mk-sys.cz).
- commit 2023975
* Sun May 22 2022 mkubecek@suse.cz
- Update to 5.18 final
- refresh configs (headers only)
- commit d0f5e4b
* Wed May 18 2022 tiwai@suse.de
- rpm/kernel-binary.spec.in: Fix missing kernel-preempt-devel and KMP Provides (bsc#1199046)
- commit 84d7ba8
* Mon May 16 2022 mkubecek@suse.cz
- Update to 5.18-rc7
- commit 1778f40
* Sun May  8 2022 mkubecek@suse.cz
- Update to 5.18-rc6
- commit ed50f8f
* Fri May  6 2022 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: Also depend on dracut-systemd (bsc#1195775)
- commit 5d4e32c
* Thu May  5 2022 jslaby@suse.cz
- Revert "build initrd without systemd" (bsc#1195775)"
  This reverts commit 3a2140fa2acded48224e1438ac9b4775340c94c2. Again,
  this breaks many packages as:
  * iproute2 is missing, and
  * kernel-obs-qa fails with:
  Timed out waiting for device /dev/disk/by-id/virtio-0.
- commit 15dd151
* Mon May  2 2022 msuchanek@suse.de
- Update config files.
  No pmem support on s390 - no such device.
- commit 9704fc2
* Mon May  2 2022 dmueller@suse.com
- config.conf: reenable armv7hl configs
- Update config files for armv7hl lpae/default
- Inherit settings from x86_64
- Use =m where available
- stick with CONFIG_UNWINDER_FRAME_POINTER=y
- commit 2821d72
* Sun May  1 2022 mkubecek@suse.cz
- Update to 5.18-rc5
- new config options:
  - BLK_DEV_FD_RAWCMD=n
- commit da18d3b
* Fri Apr 29 2022 msuchanek@suse.de
- Update config files (bsc#1199024).
  arm, i386 LIBNVDIMM y->m
  i386 X86_PMEM_LEGACY y->m
- commit ff4fa9f
* Wed Apr 27 2022 jslaby@suse.cz
- Refresh
  patches.suse/simplefb-Enable-boot-time-VESA-graphic-mode-selectio.patch.
  Update upstream status.
- commit 3b1b874
* Mon Apr 25 2022 msuchanek@suse.de
- pahole 1.22 required for full BTF features.
  also recommend pahole for kernel-source to make the kernel buildable
  with standard config
- commit 364f54b
* Mon Apr 25 2022 mkubecek@suse.cz
- Update to 5.18-rc4
- refresh configs
- commit 4ddddbd
* Fri Apr 22 2022 dmueller@suse.com
- use jobs not processors in the constraints
  jobs is the number of vcpus available to the build, while processors
  is the total processor count of the machine the VM is running on.
- commit a6e141d
* Thu Apr 21 2022 dmueller@suse.com
- config.conf: reenable armv6hl config
  Uses same config settings like x86_64
- commit 1fbebaa
* Thu Apr 21 2022 jslaby@suse.cz
- scripts: dummy-tools, add pahole (bsc#1198388).
- Update config files.
  The config files now contain the dummy PAHOLE_VERSION (9999).
- commit 8ae42ea
* Tue Apr 19 2022 fvogt@suse.de
- rpm/kernel-obs-build.spec.in: Include algif_hash, aegis128 and xts modules
  afgif_hash is needed by some packages (e.g. iwd) for tests, xts is used for
  LUKS2 volumes by default and aegis128 is useful as AEAD cipher for LUKS2.
  Wrap the long line to make it readable.
- commit bfd7db4
* Sun Apr 17 2022 mkubecek@suse.cz
- config: enable arm64 builds
- reenable arm64 configs after update to 5.18-rc2
- new arm64 config options:
  - SHADOW_CALL_STACK=n
  - RELR=n
  - KCOV=n
- commit ffb18e4
* Sun Apr 17 2022 mkubecek@suse.cz
- Update to 5.18-rc3
- update configs
  - x86_64
  - NET_DSA_REALTEK_RTL8365MB=m
  - NET_DSA_REALTEK_RTL8366RB=m
- commit 04810ad
* Fri Apr 15 2022 dmueller@suse.com
- Update config files.
  set modprobe path to /usr/sbin/modprobe after usrmerge completion
  in Tumbleweed.
- commit 767eb22
* Thu Apr 14 2022 dmueller@suse.com
- Update config files.
- set CONFIG_NO_HZ_FULL again on armv7/aarch64 (bsc#1189692)
- commit bfb0c41
* Thu Apr 14 2022 dmueller@suse.com
- Update config files.
  Disable legacy pty support (bsc#1198506)
- commit 295a9c6
* Thu Apr 14 2022 dmueller@suse.com
- Update config files.
  set CONFIG_LSM_MMAP_MIN_ADDR according to upstream default to
  32768/65536 to have a minimum protection against null pointer
  vulnerabilities. This was previously set to 0 to enable dosemu,
  but dosemu no longer requires that setting, especially not on
  non-x86.
- commit 30bf192
* Wed Apr 13 2022 mbrugger@suse.com
- arm64: Update config files to v5.18-rc2
- commit 2158d93
* Wed Apr 13 2022 tiwai@suse.de
- Update config files: set CONFIG_EFI_VARS_PSTORE_DEFAULT_DISABLE=y (bsc#1198276)
  Using efivars as the pstore default backend is dangerous, as it might fill up
  quickly with dumps, eventually resulting in a non-bootable system.
  The feature can be enabled manually via efi_pstore.pstore_disable=0 option.
- commit 7821031
* Mon Apr 11 2022 mkubecek@suse.cz
- Update to 5.18-rc2
- eliminate 1 patch
  - patches.suse/net-fungible-Fix-reference-to-__udivdi3-on-32b-build.patch
- update configs
  - SATA_LPM_POLICY renamed to SATA_MOBILE_LPM_POLICY
- commit d8f6a40
* Mon Apr  4 2022 mkubecek@suse.cz
- net/fungible: Fix reference to __udivdi3 on 32b builds.
  Fix i386 build failure.
- commit 6385d80
* Mon Apr  4 2022 mkubecek@suse.cz
- Update to 5.18-rc1
- eliminate 47 patches (42 stable, 5 mainline)
  - patches.kernel.org/*
  - patches.suse/Bluetooth-btusb-Add-missing-Chicony-device-for-Realt.patch
  - patches.suse/Revert-Input-clear-BTN_RIGHT-MIDDLE-on-buttonpads.patch
  - patches.suse/Revert-swiotlb-rework-fix-info-leak-with-DMA_FROM_DE.patch
  - patches.suse/block-restore-the-old-set_task_ioprio-behaviour-wrt-.patch
  - patches.suse/bpf-add-config-to-allow-loading-modules-with-BTF-mis.patch
- refresh
  - patches.suse/s390-export-symbols-for-crash-kmp.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
- disable ARM architectures (need config update)
- new config options
  - General setup
    CLOCKSOURCE_WATCHDOG_MAX_SKEW_US=100
  - Processor type and features
    X86_KERNEL_IBT=n
  - Binary Emulations
    X86_X32_ABI=n (renamed X86_X32)
  - General architecture-dependent options
    RANDOMIZE_KSTACK_OFFSET=y
  - Enable the block layer
    BLOCK_LEGACY_AUTOLOAD=y
  - Networking support
    PAGE_POOL_STATS=n
  - File systems
    F2FS_UNFAIR_RWSEM=n
  - Security options
    USER_DECRYPTED_DATA=n
  - Cryptographic API
    CRYPTO_DH_RFC7919_GROUPS=y
    CRYPTO_SM3_AVX_X86_64=m
  - Kernel hacking
    DEBUG_INFO_NONE=n
    DEBUG_INFO_DWARF5=n
    KFENCE_DEFERRABLE=n
    FPROBE=y
  - PCI support
    CXL_PCI=m
  - NVME Support
    NVME_VERBOSE_ERRORS=n
  - Serial ATA and Parallel ATA drivers (libata)
    SATA_LPM_POLICY=0
  - Network device support
    NET_DSA_REALTEK=m
    NET_VENDOR_DAVICOM=y
    DM9051=m
    NET_VENDOR_FUNGIBLE=y
    FUN_ETH=m
    MT7921U=m
  - Input device support
    TOUCHSCREEN_IMAGIS=m
  - Power supply class support
    IP5XXX_POWER=m
    BATTERY_SAMSUNG_SDI=n
    BATTERY_UG3105=m
  - Hardware Monitoring support
    I8K=n
    SENSORS_LM25066_REGULATOR=y
    SENSORS_PLI1209BC=m
    SENSORS_PLI1209BC_REGULATOR=y
    SENSORS_XDPE122_REGULATOR=y
    SENSORS_SY7636A=m
    SENSORS_TMP464=m
    SENSORS_ASUS_EC=m
  - Voltage and Current Regulator Support
    REGULATOR_RT5190A=m
    REGULATOR_SY7636A=m
  - Multimedia support
    VIDEO_HI847=m
    VIDEO_OG01A1B=m
    VIDEO_OV08D10=m
  - Graphics support
    DRM_PANEL_MIPI_DBI=m
    DRM_SSD130X=n
  - Sound card support
    SND_SOC_AMD_ACP_PCI=m
    SND_SOC_INTEL_AVS=m
    SND_SOC_INTEL_SOF_SSP_AMP_MACH=m
    SND_SOC_AW8738=n
    SND_SOC_TAS5805M=n
  - HID support
    HID_RAZER=m
    HID_SIGMAMICRO=m
  - USB support
    TYPEC_RT1719=m
    TYPEC_WUSB3801=m
  - Staging drivers
    VIDEO_ZORAN_DC30=y
    VIDEO_ZORAN_ZR36060=y
    VIDEO_ZORAN_BUZ=y
    VIDEO_ZORAN_DC10=y
    VIDEO_ZORAN_LML33=y
    VIDEO_ZORAN_LML33R10=y
    VIDEO_ZORAN_AVS6EYES=y
  - X86 Platform Specific Device Drivers
    AMD_HSMP=m
    INTEL_CHTWC_INT33FE=m
    INTEL_SDSI=m
    SERIAL_MULTI_INSTANTIATE=m
  - Industrial I/O support
    ADXL367_SPI=n
    ADXL367_I2C=n
    ADA4250=n
    LTC2688=n
    ADMV1014=n
    ADMV4420=n
    SX9324=n
    SX9360=n
    PECI=n
    PECI=n
  - Misc drivers
    MTD_NAND_ECC_MXIC=n
    I2C_DESIGNWARE_AMDPSP=y
    SPI_INTEL_PCI=m
    SPI_INTEL_PLATFORM=m
    INTEL_HFI_THERMAL=y
    MFD_SIMPLE_MFD_I2C=n
    MLX5_VFIO_PCI=m
    VMGENID=y
    CHROMEOS_PRIVACY_SCREEN=m
    RPMSG_CTRL=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - OPEN_DICE=m
  - MFD_MAX77714=n
  - REGULATOR_TPS6286X=m
  - VIDEO_ISL7998X=m
  - DRM_PANEL_ILITEK_ILI9341=n
  - DRM_PANEL_NOVATEK_NT35560=n
  - DRM_ITE_IT6505=n
  - COMMON_CLK_RS9_PCIE=m
  - PHY_CADENCE_DPHY_RX=m
  - i586
  - DTPM_DEVFREQ=y
  - INTEGRITY_MACHINE_KEYRING=y
  - ppc64 / ppc64le
  - NET_DSA_REALTEK_MDIO=m
  - NET_DSA_REALTEK_RTL8365MB=m
  - NET_DSA_REALTEK_RTL8366RB=m
  - MCTP_TRANSPORT_I2C=m
  - CRC64_ROCKSOFT=m
  - s390x
  - EXPOLINE_EXTERN=y
  - CRC64_ROCKSOFT=m
  - riscv64
  - RSEQ=y
  - DEBUG_RSEQ=n
  - CPU_IDLE=y
  - CPU_IDLE_GOV_LADDER=y
  - CPU_IDLE_GOV_TEO=y
  - RISCV_SBI_CPUIDLE=y
  - CPU_IDLE_GOV_MENU=y
  - PARPORT_PC=m
  - PARPORT_SERIAL=m
  - PARPORT_PC_FIFO=y
  - PARPORT_PC_PCMCIA=n
  - PARIDE=m
  - PARIDE_*=m (PARIDE_EPATC8=y
  - SCSI_PPA=m
  - SCSI_IMM=m
  - SCSI_IZIP_EPP16=n
  - SCSI_IZIP_SLOW_CTR=n
  - NET_DSA_REALTEK_MDIO=m
  - NET_DSA_REALTEK_RTL8365MB=m
  - NET_DSA_REALTEK_RTL8366RB=m
  - KS0108=n
  - CLK_STARFIVE_JH7100_AUDIO=m
  - POLARFIRE_SOC_SYS_CTRL=m
  - IDLE_INJECT=y
  - RISCV_PMU=y
  - RISCV_PMU_LEGACY=y
  - RISCV_PMU_SBI=y
  - CPU_IDLE_THERMAL=y
- commit e499f10
* Sun Apr  3 2022 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and move into sorted section:
  - patches.suse/Revert-Input-clear-BTN_RIGHT-MIDDLE-on-buttonpads.patch
  - patches.suse/block-restore-the-old-set_task_ioprio-behaviour-wrt-.patch
- commit 6038bd3
* Thu Mar 31 2022 mkubecek@suse.cz
- Revert "config: Enable BPF LSM" (bsc#1197746)
  This reverts commit c2c25b18721866d6211054f542987036ed6e0a50.
  This config change was reported to break boot if SELinux is enabled. Revert
  until we have a fix.
- commit 0a20128
* Wed Mar 30 2022 msuchanek@suse.de
- Refresh patches.rpmify/powerpc-64-BE-option-to-use-ELFv2-ABI-for-big-endian.patch.
- Refresh config files.
- commit bd4767f
* Tue Mar 29 2022 jslaby@suse.cz
- Refresh
  patches.suse/block-restore-the-old-set_task_ioprio-behaviour-wrt-.patch.
  Update to upstream version.
- commit eed8aee
* Mon Mar 28 2022 tiwai@suse.de
- Revert "swiotlb: rework "fix info leak with DMA_FROM_DEVICE""
  (bsc#1197460).
- commit ffd9dce
* Mon Mar 28 2022 jslaby@suse.cz
- block: restore the old set_task_ioprio() behaviour wrt
  PF_EXITING (bsc#1197582).
- commit c349fed
* Mon Mar 28 2022 jslaby@suse.cz
- Linux 5.17.1 (bsc#1012628).
- llc: only change llc->dev when bind() succeeds (bsc#1012628).
- drm/msm/gpu: Fix crash on devices without devfreq support (v2)
  (bsc#1012628).
- nds32: fix access_ok() checks in get/put_user (bsc#1012628).
- m68k: fix access_ok for coldfire (bsc#1012628).
- wcn36xx: Differentiate wcn3660 from wcn3620 (bsc#1012628).
- tpm: use try_get_ops() in tpm-space.c (bsc#1012628).
- tpm: fix reference counting for struct tpm_chip (bsc#1012628).
- mac80211: fix potential double free on mesh join (bsc#1012628).
- uaccess: fix integer overflow on access_ok() (bsc#1012628).
- rcu: Don't deboost before reporting expedited quiescent state
  (bsc#1012628).
- jbd2: fix use-after-free of transaction_t race (bsc#1012628).
- drm/virtio: Ensure that objs is not NULL in
  virtio_gpu_array_put_free() (bsc#1012628).
- Revert "ath: add support for special 0x0 regulatory domain"
  (bsc#1012628).
- Bluetooth: btusb: Use quirk to skip HCI_FLT_CLEAR_ALL on fake
  CSR controllers (bsc#1012628).
- Bluetooth: hci_sync: Add a new quirk to skip HCI_FLT_CLEAR_ALL
  (bsc#1012628).
- Bluetooth: btusb: Add one more Bluetooth part for the Realtek
  RTL8852AE (bsc#1012628).
- crypto: qat - disable registration of algorithms (bsc#1012628).
- ACPI: video: Force backlight native for Clevo NL5xRU and NL5xNU
  (bsc#1012628).
- ACPI: battery: Add device HID and quirk for Microsoft Surface
  Go 3 (bsc#1012628).
- ACPI / x86: Work around broken XSDT on Advantech DAC-BJ01 board
  (bsc#1012628).
- netfilter: nf_tables: validate registers coming from userspace
  (bsc#1012628).
- netfilter: nf_tables: initialize registers in nft_do_chain()
  (bsc#1012628).
- drivers: net: xgene: Fix regression in CRC stripping
  (bsc#1012628).
- ALSA: pci: fix reading of swapped values from pcmreg in AC97
  codec (bsc#1012628).
- ALSA: cmipci: Restore aux vol on suspend/resume (bsc#1012628).
- ALSA: usb-audio: Add mute TLV for playback volumes on RODE
  NT-USB (bsc#1012628).
- ALSA: pcm: Add stream lock during PCM reset ioctl operations
  (bsc#1012628).
- ALSA: pcm: Fix races among concurrent prealloc proc writes
  (bsc#1012628).
- ALSA: pcm: Fix races among concurrent prepare and
  hw_params/hw_free calls (bsc#1012628).
- ALSA: pcm: Fix races among concurrent read/write and buffer
  changes (bsc#1012628).
- ALSA: pcm: Fix races among concurrent hw_params and hw_free
  calls (bsc#1012628).
- ALSA: hda/realtek: Add quirk for ASUS GA402 (bsc#1012628).
- ALSA: hda/realtek - Fix headset mic problem for a HP machine
  with alc671 (bsc#1012628).
- ALSA: hda/realtek: Add quirk for Clevo NP50PNJ (bsc#1012628).
- ALSA: hda/realtek: Add quirk for Clevo NP70PNJ (bsc#1012628).
- ALSA: usb-audio: add mapping for new Corsair Virtuoso SE
  (bsc#1012628).
- ALSA: oss: Fix PCM OSS buffer allocation overflow (bsc#1012628).
- ASoC: sti: Fix deadlock via snd_pcm_stop_xrun() call
  (bsc#1012628).
- llc: fix netdevice reference leaks in llc_ui_bind()
  (bsc#1012628).
- Bluetooth: btusb: Add another Realtek 8761BU (bsc#1012628).
- tpm: Fix error handling in async work (bsc#1012628).
- commit e830013
* Fri Mar 25 2022 mkubecek@suse.cz
- series.conf: cleanup
- update mainline references and move into sorted section:
  - patches.suse/Bluetooth-btusb-Add-missing-Chicony-device-for-Realt.patch
  - patches.suse/bpf-add-config-to-allow-loading-modules-with-BTF-mis.patch
- commit 62d2682
* Fri Mar 25 2022 tiwai@suse.de
- Revert "Input: clear BTN_RIGHT/MIDDLE on buttonpads"
  (bsc#1197243).
- commit 7257225
* Fri Mar 25 2022 tiwai@suse.de
- Drop HID multitouch fix patch (bsc#1197243)
  Delete patches.suse/HID-multitouch-fix-Dell-Precision-7550-and-7750-butt.patch.
  Replaced with another revert patch.
- commit 01821ca
* Mon Mar 21 2022 dmueller@suse.com
- rpm/constraints.in: skip SLOW_DISK workers for kernel-source
- commit e84694f
* Mon Mar 21 2022 msuchanek@suse.de
- macros.kernel-source: Fix conditional expansion.
  Fixes: bb95fef3cf19 ("rpm: Use bash for %%() expansion (jsc#SLE-18234).")
- commit 7e857f7
* Mon Mar 21 2022 jslaby@suse.cz
- Refresh
  patches.suse/Bluetooth-btusb-Add-missing-Chicony-device-for-Realt.patch.
  Update upstream status.
- commit 36a1351
* Sun Mar 20 2022 mkubecek@suse.cz
- Update to 5.17 final
- refresh configs (headers only)
- commit be2cbd1
* Sat Mar 19 2022 msuchanek@suse.de
- rpm: Use bash for %%() expansion (jsc#SLE-18234).
  Since 15.4 alternatives for /bin/sh are provided by packages
  <something>-sh. While the interpreter for the build script can be
  selected the interpreter for %%() cannot.
  The kernel spec files use bashisms in %%().
  While this could technically be fixed there is more serious underlying
  problem: neither bash nor any of the alternatives are 100%% POSIX
  compliant nor bug-free.
  It is not my intent to maintain bug compatibility with any number of
  shells for shell scripts embedded in the kernel spec file. The spec file
  syntax is not documented so embedding the shell script in it causes some
  unspecified transformation to be applied to it. That means that
  ultimately any changes must be tested by building the kernel, n times if
  n shells are supported.
  To reduce maintenance effort require that bash is used for kernel build
  always.
- commit bb95fef
* Sat Mar 19 2022 tiwai@suse.de
- HID: multitouch: fix Dell Precision 7550 and 7750 button type
  (bsc#1197243).
- commit 5500e44
* Wed Mar 16 2022 ailiop@suse.com
- config: enable XFS_RT (bsc#1197190)
- commit 253c423
* Wed Mar 16 2022 msuchanek@suse.de
- rpm: Run external scriptlets on uninstall only when available
  (bsc#1196514 bsc#1196114 bsc#1196942).
  When dependency cycles are encountered package dependencies may not be
  fulfilled during zypper transaction at the time scriptlets are run.
  This is a problem for kernel scriptlets provided by suse-module-tools
  when migrating to a SLE release that provides these scriptlets only as
  part of LTSS. The suse-module-tools that provides kernel scriptlets may
  be removed early causing migration to fail.
- commit ab8dd2d
* Wed Mar 16 2022 dmueller@suse.com
- rpm/*.spec.in: remove backtick usage
- commit 87ca1fb
* Wed Mar 16 2022 msuchanek@suse.de
- rpm: SC2006: Use $(...) notation instead of legacy backticked `...`.
- commit f0d0e90
* Tue Mar 15 2022 dmueller@suse.com
- rpm/kernel-source.spec.in: call fdupes per subpackage
  It is a waste of time to do a global fdupes when we have
  subpackages.
- commit 1da8439
* Mon Mar 14 2022 mkubecek@suse.cz
- Update to 5.17-rc8
- update configs
  - arm64
  - MITIGATE_SPECTRE_BRANCH_HISTORY=y
  - armv7hl
  - HARDEN_BRANCH_HISTORY=y
- commit 9555b2a
* Thu Mar 10 2022 dmueller@suse.com
- rpm/arch-symbols,guards,*driver: Replace Novell with SUSE.
- commit 174a64f
* Thu Mar 10 2022 dmueller@suse.com
- rpm/kernel-docs.spec.in: use %%%%license for license declarations
  Limited to SLE15+ to avoid compatibility nightmares.
- commit 73d560e
* Wed Mar  9 2022 dmueller@suse.com
- rpm/*.spec.in: Use https:// urls
- commit 77b5f8e
* Wed Mar  9 2022 tiwai@suse.de
- Bluetooth: btusb: Add missing Chicony device for Realtek
  RTL8723BE (bsc#1196779).
- commit 47faa85
* Mon Mar  7 2022 mkubecek@suse.cz
- Update to 5.17-rc7
- commit 04b7727
* Fri Mar  4 2022 mkubecek@suse.cz
- config: refresh
  Since commit bb988d4625a3 ("kernel-binary: Do not include sourcedir in
  certificate path."), MODULE_SIG_HASH config option is mandatory in diff
  configs.
- commit 191d88f
* Thu Mar  3 2022 pvorel@suse.cz
- config: ppc64{,le}: build vmx-crypto as module (bsc#1195768)
  Building CONFIG_CRYPTO_DEV_VMX_ENCRYPT as module is the default in
  mainline since v4.8, we use it in SLES and already in
  config/ppc64/default. Thus unify it in the other configs.
  There are build dependencies which has been fixed in mainline
  647d41d3952d ("crypto: vmx - add missing dependencies")
  (currently still at maintainer herbert/cryptodev-2.6 tree)
  But instead of waiting commit to be accepted or backporting it we just
  unify configs, which is useful anyway
- commit 4df4932
* Wed Mar  2 2022 msuchanek@suse.de
- kernel-binary.spec: Also exclude the kernel signing key from devel package.
  There is a check in OBS that fails when it is included. Also the key is
  not reproducible.
  Fixes: bb988d4625a3 ("kernel-binary: Do not include sourcedir in certificate path.")
- commit 68fa069
* Wed Mar  2 2022 msuchanek@suse.de
- rpm/check-for-config-changes: Ignore PAHOLE_VERSION.
- commit 88ba5ec
* Mon Feb 28 2022 mkubecek@suse.cz
- Update to 5.17-rc6
- commit 3bbcd8f
* Sun Feb 27 2022 mkubecek@suse.cz
- config: update vanilla configs
  FB_BOOT_VESA_SUPPORT was replaced BOOT_VESA_SUPPORT by a patch but this
  patch is not applied to vanilla flavor so that we have to keep the option
  in */vanilla configs until the patch reaches mainline.
- commit 22f5560
* Sun Feb 27 2022 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: add systemd-initrd and terminfo dracut module (bsc#1195775)
- commit d9a821b
* Wed Feb 23 2022 msuchanek@suse.de
- bpf: add config to allow loading modules with BTF mismatches (bsc#1194501).
- Update config files.
- commit 37e7f35
* Wed Feb 23 2022 msuchanek@suse.de
- simplefb: Enable boot time VESA graphic mode selection (bsc#1193250).
- Update config files.
- commit 89f218d
* Mon Feb 21 2022 iivanov@suse.de
- Revert: reset: raspberrypi: Don't reset USB if already up (bsc#1180336)
- commit f3fe985
* Mon Feb 21 2022 mkubecek@suse.cz
- Update to 5.17-rc5
- refresh configs
- commit a9b2c1d
* Wed Feb 16 2022 tzimmermann@suse.de
- Revert "config: x86-64: Enable DRM stack for early-boot graphics (boo#1193472)"
  This reverts commit a6b1e6089c7fbcb3dc149eb1a005a32f0345fa13.
  Going back to efifb/vesafb for now. See boo#1195885 and boo#1195887.
- commit 230a3c7
* Wed Feb 16 2022 dmueller@suse.com
- config: Disable CONFIG_READ_ONLY_THP_FOR_FS (bsc#1195774)
- commit 1713d4e
* Wed Feb 16 2022 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: use default dracut modules (bsc#1195926,
  bsc#1198484)
  Let's iron out the reduced initrd optimisation in Tumbleweed.
  Build full blown dracut initrd with systemd for SLE15 SP4.
- commit ea76821
* Tue Feb 15 2022 dmueller@suse.com
- config.conf: reenable armv6hl/armv7hl and aarch64
- Update config files:
  Taken choices from x86_64/default for all new options
  Otherwise =m where possible, =y otherwise unless DEBUG or EXPERIMENTAL
- commit 2ab3225
* Sun Feb 13 2022 mkubecek@suse.cz
- Update to 5.17-rc4
- commit 660988d
* Fri Feb 11 2022 msuchanek@suse.de
- kernel-binary: Do not include sourcedir in certificate path.
  The certs macro runs before build directory is set up so it creates the
  aggregate of supplied certificates in the source directory.
  Using this file directly as the certificate in kernel config works but
  embeds the source directory path in the kernel config.
  To avoid this symlink the certificate to the build directory and use
  relative path to refer to it.
  Also fabricate a certificate in the same location in build directory
  when none is provided.
- commit bb988d4
* Fri Feb 11 2022 msuchanek@suse.de
- BTF: Don't break ABI when debuginfo is disabled.
- commit 9ff5fa4
* Fri Feb 11 2022 msuchanek@suse.de
- constraints: Also adjust disk requirement for x86 and s390.
- commit 9719db0
* Fri Feb 11 2022 msuchanek@suse.de
- constraints: Increase disk space for aarch64
- commit 09c2882
* Sun Feb  6 2022 mkubecek@suse.cz
- Update to 5.17-rc3
- eliminate 1 patch
  - patches.suse/cifs-fix-workstation_name-for-multiuser-mounts.patch
- update configs
  - FRAMEBUFFER_CONSOLE_LEGACY_ACCELERATION=n (y on i386)
- commit 335402f
* Sat Feb  5 2022 tiwai@suse.de
- Refresh patches.suse/Input-elan_i2c-Add-deny-list-for-Lenovo-Yoga-Slim-7.patch
  Fix section mistmatch warning
- commit 672f0d5
* Wed Feb  2 2022 jslaby@suse.cz
- cifs: fix workstation_name for multiuser mounts (bsc#1195360).
- commit d3a2311
* Tue Feb  1 2022 tiwai@suse.de
- Input: synaptics: retry query upon error (bsc#1194086).
- commit cfcc1f5
* Tue Feb  1 2022 tiwai@suse.de
- Input: elan_i2c: Add deny list for Lenovo Yoga Slim 7
  (bsc#1193064).
- commit 26e60ad
* Mon Jan 31 2022 ludwig.nussel@suse.de
- kernel-obs-build: include 9p (boo#1195353)
  To be able to share files between host and the qemu vm of the build
  script, the 9p and 9p_virtio kernel modules need to be included in
  the initrd of kernel-obs-build.
- commit 0cfe67a
* Mon Jan 31 2022 tzimmermann@suse.de
- config: x86-64: Enable DRM stack for early-boot graphics (boo#1193472)
  Replace fbdev's generic drivers with DRM-based simpledrm. Enables the
  DRM graphics stack for early-boot graphics, recovery and unsupported
  chipsets.
- commit 89d164b
* Sun Jan 30 2022 mkubecek@suse.cz
- Update to 5.17-rc2
- eliminate 3 patches
  - patches.suse/s390-uaccess-fix-compile-error.patch
  - patches.suse/tcp-Add-a-stub-for-sk_defer_free_flush.patch
  - patches.suse/tcp-add-a-missing-sk_defer_free_flush-in-tcp_splice_.patch
- refresh configs
- commit e736c55
* Fri Jan 28 2022 mkubecek@suse.cz
- tcp: add a missing sk_defer_free_flush() in tcp_splice_read()
  (git-fixes).
- commit f8aca60
* Fri Jan 28 2022 mkubecek@suse.cz
- tcp: Add a stub for sk_defer_free_flush().
  Fix another s390x/zfcpdump build failure.
- commit 235f271
* Fri Jan 28 2022 mkubecek@suse.cz
- s390/uaccess: fix compile error.
  Fix s390x/zfcpdump build.
- commit d01fea5
* Fri Jan 28 2022 mkubecek@suse.cz
- config: disable REGULATOR_MAX20086 on s390x
  This driver seems to make little sense on s390x and it also fails to build
  due to disabled CONFIG_GPIOLIB.
- commit 5152409
* Thu Jan 27 2022 tiwai@suse.de
- Delete patches.suse/Bluetooth-Apply-initial-command-workaround-for-more-.patch
  The upstream had already the fix
- commit 59dcb9d
* Wed Jan 26 2022 tiwai@suse.de
- Update config files: disable CONFIG_INTEL_IDXD_COMPAT (bsc#1194858)
  The compat support is rather unwanted, and this allows us to build
  idxd bus as module, too.
- commit 527268a
* Tue Jan 25 2022 mrostecki@suse.de
- config: Enable BPF LSM
  This LSM might get more adoption both in core system projects and
  container/k8s works and it would be good to be ready to support them.
  BPF LSM is a feature available since kernel 5.7 which allows to write
  BPF programs attached to LSM hooks and allowing/denying a particular
  event.
  BPF LSM is already adopted in a (not yet default) restrict-fs feature in
  systemd[0].
  BPF LSM is also used in the lockc[1] project which we develop at SUSE.
  There should be no functional or performance changes for users who don't
  load any BPF LSM programs. BPF LSM works only if some BPF programs is
  explicitly loaded.
  [0] https://github.com/systemd/systemd/blob/main/src/core/bpf/restrict_fs/restrict-fs.bpf.c
  [1] https://github.com/rancher-sandbox/lockc
- commit c2c25b1
* Mon Jan 24 2022 msuchanek@suse.de
- kernel-binary.spec.in: Move 20-kernel-default-extra.conf to the correctr
  directory (bsc#1195051).
- commit c80b5de
* Mon Jan 24 2022 mkubecek@suse.cz
- Update to 5.17-rc1
- eliminated 73 patches (67 stable, 6 mainline)
  - patches.kernel.org/*
  - patches.suse/0001-usb-Add-Xen-pvUSB-protocol-description.patch
  - patches.suse/0002-usb-Introduce-Xen-pvUSB-frontend-xen-hcd.patch
  - patches.suse/ALSA-usb-audio-Add-minimal-mute-notion-in-dB-mapping.patch
  - patches.suse/ALSA-usb-audio-Fix-dB-level-of-Bose-Revolve-SoundLin.patch
  - patches.suse/ALSA-usb-audio-Use-int-for-dB-map-values.patch
  - patches.suse/mwifiex-Fix-skb_over_panic-in-mwifiex_usb_recv.patch
- refresh
  - patches.rpmify/powerpc-64-BE-option-to-use-ELFv2-ABI-for-big-endian.patch
  - patches.suse/iwlwifi-module-firmware-ucode-fix.patch
  - patches.suse/vfs-add-super_operations-get_inode_dev
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
- disable ARM architectures (need config update)
- new config options
  - Power management and ACPI options
  - ACPI_PFRUT=m
  - ACPI_PCC=y
  - X86_AMD_PSTATE=m
  - Memory Management options
  - ANON_VMA_NAME=y
  - Networking support
  - NET_9P_FD=m
  - File systems
  - CACHEFILES_ERROR_INJECTION=n
  - UNICODE_UTF8_DATA=y
  - Kernel hacking
  - NET_DEV_REFCNT_TRACKER=n
  - NET_NS_REFCNT_TRACKER=n
  - PAGE_TABLE_CHECK=y
  - PAGE_TABLE_CHECK_ENFORCED=n
  - FTRACE_SORT_STARTUP_TEST=n
  - TEST_REF_TRACKER=n
  - TEST_SIPHASH=n
  - Generic Driver Options
  - DEVTMPFS_SAFE=n
  - Network device support
  - NET_VENDOR_ENGLEDER=y
  - TSNEP=m
  - TSNEP_SELFTESTS=n
  - ICE_HWTS=y
  - NET_VENDOR_VERTEXCOM=y
  - MSE102X=m
  - MCTP_SERIAL=m
  - IWLMEI=m
  - WWAN_DEBUGFS=n
  - Hardware Monitoring support
  - SENSORS_NZXT_SMART2=m
  - SENSORS_DELTA_AHE50DC_FAN=m
  - SENSORS_IR38064_REGULATOR=y
  - SENSORS_MP5023=m
  - SENSORS_INA238=m
  - SENSORS_ASUS_WMI=m
  - SENSORS_ASUS_WMI_EC=m
  - Voltage and Current Regulator Support
  - REGULATOR_MAX20086=m
  - REGULATOR_TPS68470=m
  - Graphics support
  - TINYDRM_ILI9163=n
  - Sound card support
  - SND_HDA_SCODEC_CS35L41_I2C=m
  - SND_HDA_SCODEC_CS35L41_SPI=m
  - SND_SOC_INTEL_SOF_NAU8825_MACH=m
  - SND_SOC_SOF_AMD_TOPLEVEL=m
  - SND_SOC_SOF_AMD_RENOIR=m
  - SND_SOC_AK4375=n
  - SND_SOC_TLV320ADC3XXX=n
  - X86 Platform Specific Device Drivers
  - YOGABOOK_WMI=m
  - ASUS_TF103C_DOCK=m
  - INTEL_VSEC=m
  - X86_ANDROID_TABLETS=m
  - SIEMENS_SIMATIC_IPC=m
  - SIEMENS_SIMATIC_IPC_WDT=m
  - Common Clock Framework
  - COMMON_CLK_TPS68470=n
  - COMMON_CLK_LAN966X=n
  - Industrial I/O support
  - TI_ADS8344=n
  - TI_ADS8688=n
  - TI_ADS124S08=n
  - AD74413R=n
  - AD3552R=n
  - AD7293=n
  - MAX5821=n
  - ADMV8818=n
  - ADMV1013=n
  - Misc drivers
  - GNSS_USB=m
  - SERIAL_8250_PERICOM=y
  - GPIO_SIM=m
  - CHARGER_MAX77976=m
  - VIDEO_OV5693=m
  - HID_LETSKETCH=m
  - LEDS_SIEMENS_SIMATIC_IPC=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - DRM_RCAR_USE_LVDS=n
  - DRM_RCAR_MIPI_DSI=n
  - DRM_PANEL_BOE_BF060Y8M_AJ0=n
  - DRM_PANEL_JDI_R63452=n
  - DRM_PANEL_NOVATEK_NT35950=n
  - DRM_PANEL_SONY_TULIP_TRULY_NT35521=n
  - VIDEO_MAX96712=m
  - PHY_FSL_IMX8M_PCIE=m
  - x86_64
  - SLS=y
  - i386
  - PHY_LAN966X_SERDES=m
  - ppc64 / ppc64le
  - KVM_BOOK3S_HV_NESTED_PMU_WORKAROUND=n
  - SURFACE_PLATFORMS=n
  - s390x
  - SURFACE_PLATFORMS=n
  - CRYPTO_CHACHA_S390=m
  - riscv64
  - SOC_STARFIVE=y
  - RISCV_BOOT_SPINWAIT=y
  - PINCTRL_STARFIVE=m
  - SND_AMD_ACP_CONFIG=m
  - CLK_STARFIVE_JH7100=y
  - RESET_STARFIVE_JH7100=y
  - PHY_LAN966X_SERDES=m
- commit 8751a94
* Fri Jan 21 2022 jslaby@suse.cz
- Linux 5.16.2 (bsc#1012628).
- ALSA: hda/realtek: Re-order quirk entries for Lenovo
  (bsc#1012628).
- ALSA: hda/realtek: Add quirk for Legion Y9000X 2020
  (bsc#1012628).
- ALSA: hda/tegra: Fix Tegra194 HDA reset failure (bsc#1012628).
- ALSA: hda: ALC287: Add Lenovo IdeaPad Slim 9i 14ITL5 speaker
  quirk (bsc#1012628).
- ALSA: hda/realtek - Fix silent output on Gigabyte X570 Aorus
  Master after reboot from Windows (bsc#1012628).
- ALSA: hda/realtek: Use ALC285_FIXUP_HP_GPIO_LED on another HP
  laptop (bsc#1012628).
- ALSA: hda/realtek: Add speaker fixup for some Yoga 15ITL5
  devices (bsc#1012628).
- perf annotate: Avoid TUI crash when navigating in the annotation
  of recursive functions (bsc#1012628).
- firmware: qemu_fw_cfg: fix kobject leak in probe error path
  (bsc#1012628).
- firmware: qemu_fw_cfg: fix NULL-pointer deref on duplicate
  entries (bsc#1012628).
- firmware: qemu_fw_cfg: fix sysfs information leak (bsc#1012628).
- rtlwifi: rtl8192cu: Fix WARNING when calling local_irq_restore()
  with interrupts enabled (bsc#1012628).
- media: uvcvideo: fix division by zero at stream start
  (bsc#1012628).
- video: vga16fb: Only probe for EGA and VGA 16 color graphic
  cards (bsc#1012628).
- 9p: fix enodata when reading growing file (bsc#1012628).
- 9p: only copy valid iattrs in 9P2000.L setattr implementation
  (bsc#1012628).
- NFSD: Fix zero-length NFSv3 WRITEs (bsc#1012628).
- remoteproc: qcom: pas: Add missing power-domain "mxc" for CDSP
  (bsc#1012628).
- KVM: s390: Clarify SIGP orders versus STOP/RESTART
  (bsc#1012628).
- KVM: x86: don't print when fail to read/write pv eoi memory
  (bsc#1012628).
- KVM: x86: Register Processor Trace interrupt hook iff PT
  enabled in guest (bsc#1012628).
- KVM: x86: Register perf callbacks after calling vendor's
  hardware_setup() (bsc#1012628).
- perf: Protect perf_guest_cbs with RCU (bsc#1012628).
- vfs: fs_context: fix up param length parsing in
  legacy_parse_param (bsc#1012628).
- remoteproc: qcom: pil_info: Don't memcpy_toio more than is
  provided (bsc#1012628).
- orangefs: Fix the size of a memory allocation in
  orangefs_bufmap_alloc() (bsc#1012628).
- drm/amd/display: explicitly set is_dsc_supported to false
  before use (bsc#1012628).
- devtmpfs regression fix: reconfigure on each mount
  (bsc#1012628).
- commit 6fa29ec
* Thu Jan 20 2022 msuchanek@suse.de
- kernel-binary.spec: Do not use the default certificate path (bsc#1194943).
  Using the the default path is broken since Linux 5.17
- commit 68b36f0
* Wed Jan 19 2022 mkubecek@suse.cz
- series.conf: cleanup
- move mainline patches into sorted section:
  - patches.suse/mwifiex-Fix-skb_over_panic-in-mwifiex_usb_recv.patch
  - patches.suse/0001-usb-Add-Xen-pvUSB-protocol-description.patch
  - patches.suse/0002-usb-Introduce-Xen-pvUSB-frontend-xen-hcd.patch
- update upstream references and move into sorted section:
  - patches.suse/ALSA-usb-audio-Add-minimal-mute-notion-in-dB-mapping.patch
  - patches.suse/ALSA-usb-audio-Fix-dB-level-of-Bose-Revolve-SoundLin.patch
  - patches.suse/ALSA-usb-audio-Use-int-for-dB-map-values.patch
  No effect on expanded tree.
- commit 607f978
* Wed Jan 19 2022 mkubecek@suse.cz
- Refresh and reenable
  patches.suse/Bluetooth-Apply-initial-command-workaround-for-more-.patch.
- commit a7b7c0d
* Mon Jan 17 2022 jeffm@suse.com
- series.conf: Add sorted section header/footer
  Even though we don't carry many patches in the stable or master
  branches, having the sorted section header/footer allows the automated
  tools to work.
- commit 05f8150
* Sun Jan 16 2022 jslaby@suse.cz
- Linux 5.16.1 (bsc#1012628).
- workqueue: Fix unbind_workers() VS wq_worker_running() race
  (bsc#1012628).
- workqueue: Fix unbind_workers() VS wq_worker_sleeping() race
  (bsc#1012628).
- staging: r8188eu: switch the led off during deinit
  (bsc#1012628).
- bpf: Fix out of bounds access from invalid *_or_null type
  verification (bsc#1012628).
- Bluetooth: btusb: Add one more Bluetooth part for the Realtek
  RTL8852AE (bsc#1012628).
- Bluetooth: btusb: Fix application of sizeof to pointer
  (bsc#1012628).
- Bluetooth: btusb: fix memory leak in
  btusb_mtk_submit_wmt_recv_urb() (bsc#1012628).
- Bluetooth: btusb: enable Mediatek to support AOSP extension
  (bsc#1012628).
- Bluetooth: btusb: Add the new support IDs for WCN6855
  (bsc#1012628).
- Bluetooth: btusb: Add one more Bluetooth part for WCN6855
  (bsc#1012628).
- Bluetooth: btusb: Add two more Bluetooth parts for WCN6855
  (bsc#1012628).
- Bluetooth: btusb: Add support for Foxconn MT7922A (bsc#1012628).
- Bluetooth: btintel: Fix broken LED quirk for legacy ROM devices
  (bsc#1012628).
- Bluetooth: btusb: Add support for Foxconn QCA 0xe0d0
  (bsc#1012628).
- Bluetooth: bfusb: fix division by zero in send path
  (bsc#1012628).
- ARM: dts: exynos: Fix BCM4330 Bluetooth reset polarity in I9100
  (bsc#1012628).
- USB: core: Fix bug in resuming hub's handling of wakeup requests
  (bsc#1012628).
- USB: Fix "slab-out-of-bounds Write" bug in
  usb_hcd_poll_rh_status (bsc#1012628).
- ath11k: Fix buffer overflow when scanning with extraie
  (bsc#1012628).
- mmc: sdhci-pci: Add PCI ID for Intel ADL (bsc#1012628).
- Bluetooth: add quirk disabling LE Read Transmit Power
  (bsc#1012628).
- Bluetooth: btbcm: disable read tx power for some Macs with
  the T2 Security chip (bsc#1012628).
- Bluetooth: btbcm: disable read tx power for MacBook Air 8,1
  and 8,2 (bsc#1012628).
- veth: Do not record rx queue hint in veth_xmit (bsc#1012628).
- mfd: intel-lpss: Fix too early PM enablement in the ACPI
  - >probe() (bsc#1012628).
- mfd: intel-lpss-pci: Fix clock speed for 38a8 UART
  (bsc#1012628).
- can: gs_usb: fix use of uninitialized variable, detach device
  on reception of invalid USB data (bsc#1012628).
- can: isotp: convert struct tpcon::{idx,len} to unsigned int
  (bsc#1012628).
- can: gs_usb: gs_can_start_xmit(): zero-initialize
  hf->{flags,reserved} (bsc#1012628).
- random: fix data race on crng_node_pool (bsc#1012628).
- random: fix data race on crng init time (bsc#1012628).
- platform/x86/intel: hid: add quirk to support Surface Go 3
  (bsc#1012628).
- drm/i915: Avoid bitwise vs logical OR warning in
  snb_wm_latency_quirk() (bsc#1012628).
- staging: greybus: fix stack size warning with UBSAN
  (bsc#1012628).
- parisc: Fix pdc_toc_pim_11 and pdc_toc_pim_20 definitions
  (bsc#1012628).
  Disabled:
  patches.suse/Bluetooth-Apply-initial-command-workaround-for-more-.patch
  as it conflicts with 95655456e7ce. Asked in bsc#1193124.
- commit 13f032a
* Thu Jan 13 2022 tiwai@suse.de
- Refresh patches.suse/iwlwifi-module-firmware-ucode-fix.patch.
  Adapt the uapi version for the latest kernel-firmware-20220111.
- commit 2f088f6
* Thu Jan 13 2022 mkubecek@suse.cz
- Update patches.suse/vfs-add-super_operations-get_inode_dev
  Copy an updated version from SLE15-SP4 with one minor refresh.
- commit c02e2ab
* Thu Jan 13 2022 jgross@suse.com
- Refresh
  patches.suse/0001-usb-Add-Xen-pvUSB-protocol-description.patch.
- Refresh
  patches.suse/0002-usb-Introduce-Xen-pvUSB-frontend-xen-hcd.patch.
- commit 8950040
* Wed Jan 12 2022 mkubecek@suse.cz
- update patches metadata
- update upstream references
  - patches.suse/media-Revert-media-uvcvideo-Set-unique-vdev-name-bas.patch
  - patches.suse/mwifiex-Fix-skb_over_panic-in-mwifiex_usb_recv.patch
  - patches.suse/random-fix-crash-on-multiple-early-calls-to-add_bootloader_randomness.patch
- commit 949bbaa
* Mon Jan 10 2022 jslaby@suse.cz
- Refresh
  patches.suse/random-fix-crash-on-multiple-early-calls-to-add_bootloader_randomness.patch.
  * Update upstream status
  * Update to the latest (upstream) version
  * Move it within series to upstream-soon patches
- commit c4ca5fd
* Mon Jan 10 2022 mkubecek@suse.cz
- Update to 5.16 final
- refresh configs (headers only)
- commit b8251b4
* Fri Jan  7 2022 tiwai@suse.de
- rpm/kernel-binary.spec.in: Add Provides of kernel-preempt (jsc#SLE-18857)
  For smooth migration with the former kernel-preempt user, kernel-default
  provides kernel-preempt now when CONFIG_PREEMPT_DYNAMIC is defined.
- commit d292a81
* Fri Jan  7 2022 tiwai@suse.de
- Refresh BT workaround patch (bsc#1193124)
  Fix yet another broken device 8086:0aa7
- commit 163b552
* Mon Jan  3 2022 dmueller@suse.com
- Revert "config: disable BTRFS_ASSERT in default kernels"
  This was pushed without enough review, reverting.
- commit e86c2a0
* Mon Jan  3 2022 tiwai@suse.de
- media: Revert "media: uvcvideo: Set unique vdev name based in
  type" (bsc#1193255).
- commit b3f1eb0
* Mon Jan  3 2022 mkubecek@suse.cz
- Update to 5.16-rc8
- commit b59b474
* Fri Dec 31 2021 schwab@suse.de
- config: Enable CONFIG_CMA on riscv64
  Non-default dependent config changes:
- DMA_CMA=y
- commit c0aa71e
* Thu Dec 30 2021 dmueller@suse.com
- fix rpm build warning
  tumbleweed rpm is adding these warnings to the log:
  It's not recommended to have unversioned Obsoletes: Obsoletes:      microcode_ctl
- commit 3ba8941
* Mon Dec 27 2021 mkubecek@suse.cz
- Update to 5.16-rc7
- refresh
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
- refresh configs
- commit cce91fd
* Wed Dec 22 2021 dmueller@suse.com
- build initrd without systemd
  This reduces the size of the initrd by over 25%%, which
  improves startup time of the virtual machine by 0.5-0.6s on
  very fast machines, more on slower ones.
- commit ef4c569
* Wed Dec 22 2021 dmueller@suse.com
- config: disable BTRFS_ASSERT in default kernels
  BTRFS_ASSERT is marked as developer only option and hence
  shouldn't be enabled in the default kernel. we enable it
  in the debug flavor now.
  This improves performance of a fio randrw run by over 21%% and
  reduces code size by 25%%.
- commit 6567403
* Mon Dec 20 2021 dmueller@suse.com
- add kvmsmall flavor for aarch64
- commit 1775f8c
* Mon Dec 20 2021 mkubecek@suse.cz
- Update to 5.16-rc6
- refresh configs
- disable
  patches.suse/btrfs-use-the-new-VFS-super_block_dev.patch
  - needs an update after mainline commit 33fab972497a ("btrfs: fix double
    free of anon_dev after failure to create subvolume")
- commit ccebb20
* Mon Dec 20 2021 mkubecek@suse.cz
- config: enable and refresh arm architectures
- commit 487d839
* Fri Dec 17 2021 dmueller@suse.com
- kernel-obs-build: remove duplicated/unused parameters
  lbs=0 - this parameters is just giving "unused parameter" and it looks
  like I can not find any version that implemented this.
  rd.driver.pre=binfmt_misc is not needed when setup_obs is used, it
  alread loads the kernel module.
  quiet and panic=1 will now be also always added by OBS, so we don't have
  to set it here anymore.
- commit 972c692
* Thu Dec 16 2021 mbrugger@suse.com
- armv6hl: Update config files.
  Update config to v5.16-rc5
- commit fcea0c3
* Thu Dec 16 2021 mbrugger@suse.com
- armv7hl: Update config files.
  Update config to v5.16-rc3
- commit 36ef1bb
* Thu Dec 16 2021 mbrugger@suse.com
- arm64: Update config files.
  Update configs to v5.16-rc5
- commit 99d3870
* Tue Dec 14 2021 dmueller@suse.com
- Revert "- rpm/*build: use buildroot macro instead of env variable"
  buildroot macro is not being expanded inside a shell script. go
  back to the environment variable usage. This reverts parts of
  commit e2f60269b9330d7225b2547e057ef0859ccec155.
- commit fe85f96
* Tue Dec 14 2021 dmueller@suse.com
- kernel-obs-build: include the preferred kernel parameters
  Currently the Open Build Service hardcodes the kernel boot parameters
  globally. Recently functionality was added to control the parameters
  by the kernel-obs-build package, so make use of that. parameters here
  will overwrite what is used by OBS otherwise.
- commit a631240
* Mon Dec 13 2021 msuchanek@suse.de
- config: INPUT_EVBUG=n (bsc#1192974).
  Debug driver unsuitable for production, only enabled on ppc64.
- commit 4e0adba
* Mon Dec 13 2021 dmueller@suse.com
- kernel-obs-build: inform build service about virtio-serial
  Inform the build worker code that this kernel supports virtio-serial,
  which improves performance and relability of logging.
- commit 301a3a7
* Mon Dec 13 2021 dmueller@suse.com
- rpm/*.spec.in: use buildroot macro instead of env variable
  The RPM_BUILD_ROOT variable is considered deprecated over
  a buildroot macro. future proof the spec files.
- commit e2f6026
* Mon Dec 13 2021 mkubecek@suse.cz
- Update to 5.16-rc5
- commit c317c11
* Fri Dec 10 2021 tiwai@suse.de
- Update BT fix patch for regression with 8087:0026 device (bsc#1193124)
  Also corrected the references and patch description
- commit ee06149
* Thu Dec  9 2021 ohering@suse.de
- Disable hyperv_fb in favour of hyperv_drm (jsc#SLE-19733)
- commit f85f403
* Mon Dec  6 2021 mkubecek@suse.cz
- Update to 5.16-rc4
- eliminated 1 patch:
  - patches.suse/rtw89-update-partition-size-of-firmware-header-on-sk.patch
- commit d1dc164
* Thu Dec  2 2021 tiwai@suse.de
- Bluetooth: Apply initial command workaround for more Intel chips
  (bsc#83f2dafe2a62).
- commit 9c66401
* Thu Dec  2 2021 jslaby@suse.cz
- rpm/kernel-binary.spec.in: don't strip vmlinux again (bsc#1193306)
  After usrmerge, vmlinux file is not named vmlinux-<version>, but simply
  vmlinux. And this is not reflected in STRIP_KEEP_SYMTAB we set.
  So fix this by removing the dash...
- commit 83af88d
* Wed Dec  1 2021 tiwai@suse.de
- mwifiex: Fix skb_over_panic in mwifiex_usb_recv()
  (CVE-2021-43976 bsc#1192847).
- commit 62666c5
* Mon Nov 29 2021 mkubecek@suse.cz
- Update to 5.16-rc3
- refresh configs
- commit e8ae228
* Fri Nov 26 2021 msuchanek@suse.de
- constraints: Build aarch64 on recent ARMv8.1 builders.
  Request asimdrdm feature which is available only on recent ARMv8.1 CPUs.
  This should prevent scheduling the kernel on an older slower builder.
- commit 60fc53f
* Tue Nov 23 2021 msuchanek@suse.de
- kernel-source.spec: install-kernel-tools also required on 15.4
- commit 6cefb55
* Mon Nov 22 2021 mkubecek@suse.cz
- config: disable unprivileged BPF by default (jsc#SLE-22573)
  Backport of mainline commit 8a03e56b253e ("bpf: Disallow unprivileged bpf
  by default") only changes kconfig default, used e.g. for "make oldconfig"
  when the config option is missing, but does not update our kernel configs
  used for build. Update also these to make sure unprivileged BPF is really
  disabled by default.
  [ddiss: extend to all tumbleweed kernel configs]
- commit 61d2576
* Mon Nov 22 2021 mkubecek@suse.cz
- update to 5.16-rc2
- refresh
  - patches.suse/suse-hv-guest-os-id.patch
- update configs (restore values before 5.14-rc1)
  - PSTORE_ZONE=m
  - PSTORE_BLK=m
  - PSTORE_BLK_BLKDEV=""
  - PSTORE_BLK_KMSG_SIZE=64
  - PSTORE_BLK_MAX_REASON=2
  - MTD_PSTORE=m
- commit 696d453
* Tue Nov 16 2021 iivanov@suse.de
- random: fix crash on multiple early calls to add_bootloader_randomness() (bsc#1184924)
- commit e24ee9e
* Tue Nov 16 2021 tiwai@suse.de
- ALSA: usb-audio: Fix dB level of Bose Revolve+ SoundLink
  (bsc#1192375).
- ALSA: usb-audio: Add minimal-mute notion in dB mapping table
  (bsc#1192375).
- ALSA: usb-audio: Use int for dB map values (bsc#1192375).
- commit 7a21313
* Tue Nov 16 2021 tiwai@suse.de
- rtw89: update partition size of firmware header on skb->data
  (bsc#1188303).
- commit 4e4f5f9
* Tue Nov 16 2021 msuchanek@suse.de
- kernel-*-subpackage: Add dependency on kernel scriptlets (bsc#1192740).
- commit a133bf4
* Tue Nov 16 2021 tiwai@suse.de
- Drop downstream rtw89 fix patch, to be replaced with the upstream fix
- commit 9ba8358
* Mon Nov 15 2021 mkubecek@suse.cz
- Update to 5.16-rc1
- eliminated 26 patches (13 stable, 13 mainline)
  - patches.kernel.org/*
  - patches.suse/ALSA-usb-audio-Restrict-rates-for-the-shared-clocks.patch
  - patches.suse/Bluetooth-sco-Fix-lock_sock-blockage-by-memcpy_from_.patch
  - patches.suse/Input-i8042-Add-quirk-for-Fujitsu-Lifebook-T725.patch
  - patches.suse/arm64-dts-rockchip-Disable-CDN-DP-on-Pinebook-Pro.patch
  - patches.suse/rtw89-Fix-two-spelling-mistakes-in-debug-messages.patch
  - patches.suse/rtw89-Fix-variable-dereferenced-before-check-sta.patch
  - patches.suse/rtw89-Remove-redundant-check-of-ret-after-call-to-rt.patch
  - patches.suse/rtw89-add-Realtek-802.11ax-driver.patch
  - patches.suse/rtw89-fix-error-function-parameter.patch
  - patches.suse/rtw89-fix-return-value-check-in-rtw89_cam_send_sec_k.patch
  - patches.suse/rtw89-fix-return-value-in-hfc_pub_cfg_chk.patch
  - patches.suse/rtw89-remove-duplicate-register-definitions.patch
  - patches.suse/rtw89-remove-unneeded-semicolon.patch
- refresh
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/suse-hv-guest-os-id.patch
- disable ARM architectures (need config update)
- new config options
  - General setup
  - PREEMPT_DYNAMIC=y
  - Processor type and features
  - SCHED_CLUSTER=y
  - STRICT_SIGALTSTACK_SIZE=n
  - Networking support
  - NETFILTER_EGRESS=y
  - MCTP=y
  - File systems
  - EROFS_FS_ZIP_LZMA=y
  - Library routines
  - XZ_DEC_MICROLZMA=y
  - Kernel hacking
  - DEBUG_PREEMPT=n
  - PREEMPT_TRACER=n
  - SCSI device support
  - SCSI_UFS_HWMON=y
  - Network device support
  - AMT=m
  - NET_VENDOR_ASIX=y
  - SPI_AX88796C=m
  - SPI_AX88796C_COMPRESSION=y
  - ICE_SWITCHDEV=y
  - MT7921S=m
  - Character devices
  - RPMSG_TTY=m
  - CEC support
  - CEC_GPIO=m
  - CEC_PIN_ERROR_INJ=n
  - Multimedia support
  - VIDEO_HI846=m
  - VIDEO_OV13B10=m
  - Graphics support
  - DRM_DEBUG_MODESET_LOCK=n
  - DRM_I915_PXP=y
  - Sound card support
  - SND_SOC_AMD_VANGOGH_MACH=m
  - SND_SOC_AMD_ACP6x=m
  - SND_SOC_AMD_ACP_COMMON=m
  - SND_SOC_AMD_YC_MACH=m
  - SND_AMD_ASOC_RENOIR=m
  - SND_SOC_AMD_LEGACY_MACH=m
  - SND_SOC_AMD_SOF_MACH=m
  - SND_SOC_INTEL_SOF_ES8336_MACH=m
  - SND_SOC_CS35L41_SPI=m
  - SND_SOC_CS35L41_I2C=m
  - SND_SOC_MAX98520=m
  - SND_SOC_RT9120=m
  - SND_SOC_NAU8821=m
  - HID support
  - HID_XIAOMI=m
  - HID_NINTENDO=m
  - NINTENDO_FF=y
  - X86 Platform Specific Device Drivers
  - NVIDIA_WMI_EC_BACKLIGHT=m
  - INTEL_ISHTP_ECLITE=m
  - BARCO_P50_GPIO=m
  - Industrial I/O support
  - ADXL313_I2C=n
  - ADXL313_SPI=n
  - ADXL355_I2C=n
  - ADXL355_SPI=n
  - SCD4X=n
  - SENSEAIR_SUNRISE_CO2=n
  - ADRF6780=n
  - MAX31865=m
  - Misc devices
  - INTEL_MEI_PXP=m
  - KEYBOARD_CYPRESS_SF=m
  - SENSORS_MAX6620=m
  - HT16K33=n
  - ALIBABA_ENI_VDPA=m
  - MLXREG_LC=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - SPI_CADENCE_XSPI=m
  - DRM_PANEL_EDP=m
  - DRM_PANEL_SAMSUNG_S6D27A1=n
  - DRM_PANEL_SHARP_LS060T1SX01=n
  - i386
    SND_AUDIO_GRAPH_CARD2=n
    SND_TEST_COMPONENT=m
  - ppc64
  - IPMI_IPMB=m
  - s390x
  - COMMAND_LINE_SIZE=4096 (default)
  - riscv64
  - TIME_NS=y
  - VIRTUALIZATION=y
  - KVM=m
  - SND_AUDIO_GRAPH_CARD2=n
  - SND_TEST_COMPONENT=m
  - */debug
  - DRM_DEBUG_MODESET_LOCK=y
- commit 2e30d30
* Thu Nov 11 2021 msuchanek@suse.de
- Fix problem with missing installkernel on Tumbleweed.
- commit 2ed6686
* Thu Nov 11 2021 mkubecek@suse.cz
- config: refresh
- drop PROFILE_ALL_BRANCHES where not available any more
- commit d11f2e4
* Tue Nov  9 2021 tiwai@suse.de
- Update config files: set CONFIG_FORTIFY_SOURCE=y consistently (bsc#1192476)
- commit 3837451
* Mon Nov  8 2021 msuchanek@suse.de
- Update config files (bsc#1192456).
  CONFIG_IMA_TRUSTED_KEYRING=y
- commit 2251920
* Sun Nov  7 2021 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move to appropriate section
  - patches.suse/ALSA-usb-audio-Restrict-rates-for-the-shared-clocks.patch
- commit 651a971
* Sat Nov  6 2021 jslaby@suse.cz
- Linux 5.15.1 (bsc#1012628).
- sfc: Fix reading non-legacy supported link modes (bsc#1012628).
- Revert "xhci: Set HCD flag to defer primary roothub
  registration" (bsc#1012628).
- Revert "usb: core: hcd: Add support for deferring roothub
  registration" (bsc#1012628).
- drm/amdkfd: fix boot failure when iommu is disabled in Picasso
  (bsc#1012628).
- Revert "soc: imx: gpcv2: move reset assert after requesting
  domain power up" (bsc#1012628).
- ARM: 9120/1: Revert "amba: make use of -1 IRQs warn"
  (bsc#1012628).
- Revert "wcn36xx: Disable bmps when encryption is disabled"
  (bsc#1012628).
- drm/amdgpu: revert "Add autodump debugfs node for gpu reset v8"
  (bsc#1012628).
- drm/amd/display: Revert "Directly retrain link from debugfs"
  (bsc#1012628).
- Revert "drm/i915/gt: Propagate change in error status to
  children on unhold" (bsc#1012628).
- ALSA: usb-audio: Add quirk for Audient iD14 (bsc#1012628).
- commit 7ecebb2
* Fri Nov  5 2021 mkubecek@suse.cz
- update patch metadata
- update upstream reference
  - patches.suse/arm64-dts-rockchip-Disable-CDN-DP-on-Pinebook-Pro.patch
- commit aa05ab3
* Fri Nov  5 2021 mkubecek@suse.cz
- series.conf: cleanup
- move to the section for short lived patches:
  - patches.suse/rtw89-Fix-crash-by-loading-compressed-firmware-file.patch
- commit 1fb2e08
* Fri Nov  5 2021 tiwai@suse.de
- rtw89: Fix crash by loading compressed firmware file
  (bsc#1188303).
- commit 42e1103
* Wed Nov  3 2021 mkubecek@suse.cz
- supported-flag: consolidate a bit more
  patches.suse/revert-modpost-remove-get_next_text-and-make-grab-release_-file-s.patch
  is a partial revert of mainline commit 75893572d453 ("modpost: remove
  get_next_text() and make {grab,release_}file static"); it restores function
  get_next_line() which was removed in mainline but we still need it.
  As the function is static and only used in code built only with
  CONFIG_SUSE_KERNEL_SUPPORTED enabled, compiler issues a warning when
  building with CONFIG_SUSE_KERNEL_SUPPORTED disabled. Merge the patch into
  patches.suse/add-suse-supported-flag.patch and move the function into
  an #ifdef CONFIG_SUSE_KERNEL_SUPPORTED block.
  The only effect on expanded tree is moving get_next_line() lower so that it
  is only compiled when CONFIG_SUSE_KERNEL_SUPPORTED=n.
- commit 0c612fa
* Wed Nov  3 2021 tiwai@suse.de
- Input: i8042 - Add quirk for Fujitsu Lifebook T725
  (bsc#1191980).
- commit 44f2754
* Wed Nov  3 2021 mkubecek@suse.cz
- update patch metadata
- update upstream references:
  - patches.suse/Bluetooth-sco-Fix-lock_sock-blockage-by-memcpy_from_.patch
  - patches.suse/media-firewire-firedtv-avc-fix-a-buffer-overflow-in-.patch
  - patches.suse/rtw89-Fix-two-spelling-mistakes-in-debug-messages.patch
  - patches.suse/rtw89-Fix-variable-dereferenced-before-check-sta.patch
  - patches.suse/rtw89-Remove-redundant-check-of-ret-after-call-to-rt.patch
  - patches.suse/rtw89-add-Realtek-802.11ax-driver.patch
  - patches.suse/rtw89-fix-error-function-parameter.patch
  - patches.suse/rtw89-fix-return-value-check-in-rtw89_cam_send_sec_k.patch
  - patches.suse/rtw89-fix-return-value-in-hfc_pub_cfg_chk.patch
  - patches.suse/rtw89-remove-duplicate-register-definitions.patch
  - patches.suse/rtw89-remove-unneeded-semicolon.patch
- commit 2e35b89
* Mon Nov  1 2021 mcgrof@suse.com
- Drop patches where were added for ustat()
  glibc doesn't expose this system call anymore, and so no point in
  carrying this delta. LTP does test for this but the test uses its
  own headers instead of libc for it. It is not worth carrying this
  delta for a deprecated call.
  This patch set was tested with kernel-ci and found no new regressions
  with btrfs.
- Delete
  patches.suse/btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch.
- Delete patches.suse/btrfs-use-the-new-VFS-super_block_dev.patch.
  (Cherry picked from commit ea7c7f6bd63bd560c95f994b1aff269fa53bfc8d)
- commit 5210262
* Mon Nov  1 2021 tiwai@suse.de
- Refresh patches.suse/iwlwifi-module-firmware-ucode-fix.patch (boo#1191417)
  There is one model that contains *-66.ucode.  Add the exception.
- commit f0d7a09
* Mon Nov  1 2021 mkubecek@suse.cz
- Update to 5.15 final
- refresh configs
  - drop CONFIG_RESET_PISTACHIO
- commit 2ab31e7
* Mon Nov  1 2021 mkubecek@suse.cz
- config: update and enable armv6hl
  Update armv6hl configs to 5.15-rc7 and enable them. Where possible, values
  are taken from armv7hl, the rest is guesswork based on values of similar
  config options.
- commit 22c5286
* Mon Nov  1 2021 mkubecek@suse.cz
- config: update and enable armv7hl
  Update armv7hl configs to 5.15-rc7 and enable them. Where possible, values
  are taken from arm64, the rest is guesswork based on values of similar
  config options.
- commit 3b362e7
* Mon Nov  1 2021 mkubecek@suse.cz
- config: update and enable arm64
  Update arm64 configs to 5.15-rc7 and enable them. Where possible, values
  are taken from x86_64, the rest is guesswork based on values of similar
  config options.
- commit 482d5b4
* Fri Oct 29 2021 tiwai@suse.de
- rtw89: Fix variable dereferenced before check 'sta'
  (bsc#1191321).
- rtw89: fix return value in hfc_pub_cfg_chk (bsc#1191321).
- rtw89: remove duplicate register definitions (bsc#1191321).
- rtw89: fix error function parameter (bsc#1191321).
- rtw89: remove unneeded semicolon (bsc#1191321).
- rtw89: fix return value check in rtw89_cam_send_sec_key_cmd()
  (bsc#1191321).
- rtw89: Remove redundant check of ret after call to
  rtw89_mac_enable_bb_rf (bsc#1191321).
- rtw89: Fix two spelling mistakes in debug messages
  (bsc#1191321).
- commit 719bb03
* Thu Oct 28 2021 ykaukab@suse.de
- config: arm64: enable dpaa2 restool support
  References: bsc#1191190
- commit c86f145
* Mon Oct 25 2021 mkubecek@suse.cz
- Update to 5.15-rc7
- commit 89a05b7
* Wed Oct 20 2021 jack@suse.cz
- Update tags in patches.suse/readahead-request-tunables.patch (VM
  Performance, bsc#548529 bsc#1189955).
- commit b531271
* Wed Oct 20 2021 tiwai@suse.de
- media: firewire: firedtv-avc: fix a buffer overflow in
  avc_ca_pmt() (CVE-2021-3542 bsc#1184673).
- commit 45f5ddd
* Wed Oct 20 2021 msuchanek@suse.de
- kernel-binary.spec: Bump dwarves requirement to 1.22.
  1.22 is finally released, and it is required for functionality.
- commit c88d345
* Tue Oct 19 2021 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: move to zstd for the initrd
  Newer distros have capability to decompress zstd, which
  provides a 2-5%% better compression ratio at very similar
  cpu overhead. Plus this tests the zstd codepaths now as well.
- commit 3d53a5b
* Tue Oct 19 2021 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: reduce initrd functionality
  For building in OBS, we always build inside a virtual machine
  that gets a new, freshly created scratch filesystem image. So
  we do not need to handle fscks because that ain't gonna happen,
  as well as not we do not need to handle microcode update in the
  initrd as these only can be run on the host system anyway. We
  can also strip and hardlink as an additional optimisation that
  should not significantly hurt.
- commit c72c6fc
* Mon Oct 18 2021 tiwai@suse.de
- Update upstream commit id for rtw89 patch (bsc#1191321)
- commit 9587a7b
* Mon Oct 18 2021 mkubecek@suse.cz
- Update to 5.15-rc6
- refresh configs
  - drop SIMPLE_PM_BUS
- commit b7fe390
* Wed Oct 13 2021 msuchanek@suse.de
- kernel-spec-macros: Since rpm 4.17 %%verbose is unusable (bsc#1191229).
  The semantic changed in an incompatible way so invoking the macro now
  causes a build failure.
- commit 3e55f55
* Mon Oct 11 2021 mbrugger@suse.com
- rtw89: add Realtek 802.11ax driver (bsc#1191321).
- commit 40c7cf3
* Mon Oct 11 2021 tiwai@suse.de
- Enable CONFIG_RTW88_DEBUG and CONFIG_RTW89_DEBUG on debug flavors (bsc#1191321)
- commit d98701e
* Mon Oct 11 2021 mkubecek@suse.cz
- Update to 5.15-rc5
- update configs
  - FIRMWARE_MEMMAP=y (ppc64, ppc64le, s390x)
  - FW_CFG_SYSFS=m (ppc64)
  - FB_SIMPLE=n (s390x)
- commit f616781
* Fri Oct  8 2021 tiwai@suse.de
- iwlwifi: Fix MODULE_FIRMWARE() for non-existing ucode version
  (boo#1191417).
- commit b3fa747
* Tue Oct  5 2021 ludwig.nussel@suse.de
- rpm: use _rpmmacrodir (boo#1191384)
- commit e350c14
* Mon Oct  4 2021 mkubecek@suse.cz
- Update to 5.15-rc4
- commit 01d91cd
* Fri Oct  1 2021 tiwai@suse.de
- ALSA: usb-audio: Restrict rates for the shared clocks
  (bsc#1190418).
- commit ffe0c6a
* Thu Sep 30 2021 mbrugger@suse.com
- arm64: Update config files. (bsc#1185927)
  Set PINCTRL_ZYNQMP as build-in.
- commit 94782db
* Mon Sep 27 2021 trenn@suse.com
- Those are all really old, some of them might have been fixed via BIOS enhancements:
- Delete patches.suse/acpi_thermal_passive_blacklist.patch. (bsc#1189969)
- Delete
  patches.suse/acpi_thinkpad_introduce_acpi_root_table_boot_param.patch. (bsc#1189968)
- Delete patches.suse/perf_timechart_fix_zero_timestamps.patch. (bsc#1189958)
- Delete patches.suse/pstore_disable_efi_backend_by_default.patch. (bsc#1189961)
- Delete
  patches.suse/x86-apic-force-bigsmp-apic-on-IBM-EXA3-4.patch. (bsc#1189956)
- commit c421931
* Mon Sep 27 2021 msuchanek@suse.de
- kernel-binary.spec: Do not sign kernel when no key provided
  (bsc#1187167).
- commit 6c24533
* Sun Sep 26 2021 mkubecek@suse.cz
- Update to 5.15-rc3
- eliminated 3 patches:
  - patches.rpmify/scripts-sorttable-riscv-fix-undelcred-identifier-EM_.patch
  - patches.suse/posix-cpu-timers-Fix-spuriously-armed-0-value-itimer.patch
  - patches.suse/nvmem-nintendo-otp-add-dependency-on-CONFIG_HAS_IOME.patch
    (still meaningful in upstream but no longer needed four our configs)
- refresh configs
  - drop NVMEM_NINTENDO_OTP
  - i386: drop XEN_PCIDEV_FRONTEND and SWIOTLB_XEN
- commit e48f187
* Sat Sep 25 2021 msuchanek@suse.de
- rpm/config.sh: Compress modules with zstd (jsc#SLE-21256).
- commit 66843b7
* Wed Sep 22 2021 msuchanek@suse.de
- kernel-binary.spec: suse-kernel-rpm-scriptlets required for uninstall as
  well.
  Fixes: e98096d5cf85 ("rpm: Abolish scritplet templating (bsc#1189841).")
- commit e082fbf
* Mon Sep 20 2021 mkubecek@suse.cz
- Update to 5.15-rc2
- eliminated 2 patches
  - patches.suse/memblock-introduce-saner-memblock_free_ptr-interface.patch
  - patches.suse/tools-bootconfig-define-memblock_free_ptr-to-fix-build-error.patch
- update configs
  - ARCH_NR_GPIO (1024 on x86_64, 512 on i386)
  - drop WARN_DYNAMIC_STACK on s390x
- commit 05c92eb
* Fri Sep 17 2021 msuchanek@suse.de
- kernel-binary.spec: Check for no kernel signing certificates.
  Also remove unused variable.
- commit bdc323e
* Fri Sep 17 2021 msuchanek@suse.de
- Revert "rpm/kernel-binary.spec: Use only non-empty certificates."
  This reverts commit 30360abfb58aec2c9ee7b6a27edebe875c90029d.
- commit 413e05b
* Fri Sep 17 2021 mkubecek@suse.cz
- nvmem: nintendo-otp: add dependency on CONFIG_HAS_IOMEM
  (202108250657.h5CWR7Xf-lkp@intel.com).
  Fix s390x/zfcpdump build.
- refresh configs (s390x/zfcpdump: NVMEM_NINTENDO_OTP=n)
- commit 68ad835
* Fri Sep 17 2021 msuchanek@suse.de
- rpm/kernel-binary.spec: Use only non-empty certificates.
- commit 30360ab
* Thu Sep 16 2021 jslaby@suse.cz
- posix-cpu-timers: Fix spuriously armed 0-value itimer (timer
  breakage).
- commit 2b37340
* Wed Sep 15 2021 vbabka@suse.cz
- tools/bootconfig: Define memblock_free_ptr() to fix build error
  (Build fix for tools.).
- commit 890a28b
* Wed Sep 15 2021 mkubecek@suse.cz
- scripts/sorttable: riscv: fix undelcred identifier 'EM_RISCV'
  error (e8965b25-f15b-c7b4-748c-d207dda9c8e8@i2se.com).
  Fix build on systems with glibc-devel < 2.24.
- commit 62f1dd0
* Wed Sep 15 2021 mkubecek@suse.cz
- config: disable ZERO_CALL_USED_REGS
  This was enable due to a misunderstanding, I thought it was a workaround
  for a recent CPU vulnerability. Now it rather seems to be just another
  hardening with questionable gain and measurable performance impact.
- commit b09844e
* Wed Sep 15 2021 vbabka@suse.cz
- memblock: introduce saner 'memblock_free_ptr()' interface
  (Fixes memory corruption on boot in 5.15-rc1).
- commit 4311d55
* Wed Sep 15 2021 vbabka@suse.cz
- config: disable CONFIG_SYSFB_SIMPLEFB
  The new option in 5.15 is a rename from CONFIG_X86_SYSFB which we had disabled
  due to bsc#855821. Moreover, enabling CONFIG_SYSFB_SIMPLEFB caused regression
  on my UEFI desktop - no printk output on screen between grub's loading of
  kernel and initrd, and a gpu modesetting driver taking over.
- commit 69dc36e
* Mon Sep 13 2021 rgoldwyn@suse.com
- Delete patches.suse/apparmor-compatibility-with-v2.x-net.patch (bsc#118997)
  Apparmor upgraded to v3.x
- commit a1d1731
* Mon Sep 13 2021 mkubecek@suse.cz
- Update to 5.15-rc1
- eliminated 36 patches (27 stable, 9 mainline)
  - patches.kernel.org/*
  - patches.suse/Bluetooth-avoid-circular-locks-in-sco_sock_connect.patch
  - patches.suse/Bluetooth-btusb-Add-support-for-Foxconn-Mediatek-Chi.patch
  - patches.suse/Bluetooth-btusb-Add-support-for-IMC-Networks-Mediate.patch
  - patches.suse/Bluetooth-schedule-SCO-timeouts-with-delayed_work.patch
  - patches.suse/Bluetooth-switch-to-lock_sock-in-SCO.patch
  - patches.suse/HID-usbhid-Simplify-code-in-hid_submit_ctrl.patch
  - patches.suse/crypto-ecc-handle-unaligned-input-buffer-in-ecc_swap.patch
  - patches.suse/memcg-enable-accounting-of-ipc-resources.patch
  - patches.suse/watchdog-Fix-NULL-pointer-dereference-when-releasing.patch
- refresh
  - patches.suse/add-suse-supported-flag.patch
  - patches.suse/btrfs-use-the-new-VFS-super_block_dev.patch
  - patches.suse/suse-hv-guest-os-id.patch
- disable ARM architectures (need config update)
- new config options
  - General setup
  - CONFIG_WERROR=n
  - CONFIG_PRINTK_INDEX=y
  - Processor type and features
  - CONFIG_PERF_EVENTS_AMD_UNCORE=m
  - Firmware Drivers
  - CONFIG_SYSFB_SIMPLEFB=y
  - Memory Management options
  - CONFIG_DAMON=n
  - Networking support
  - CONFIG_IPV6_IOAM6_LWTUNNEL=n
  - CONFIG_MCTP=m
  - File systems
  - CONFIG_F2FS_IOSTAT=y
  - CONFIG_NTFS3_FS=m
  - CONFIG_NTFS3_64BIT_CLUSTER=n
  - CONFIG_NTFS3_LZX_XPRESS=y
  - CONFIG_NTFS3_FS_POSIX_ACL=y
  - CONFIG_SMB_SERVER=m
  - CONFIG_SMB_SERVER_SMBDIRECT=n
  - CONFIG_SMB_SERVER_CHECK_CAP_NET_ADMIN=y
  - CONFIG_SMB_SERVER_KERBEROS5=y
  - Security options
  - CONFIG_ZERO_CALL_USED_REGS=y
  - Cryptographic API
  - CONFIG_CRYPTO_SM4_AESNI_AVX_X86_64=m
  - CONFIG_CRYPTO_SM4_AESNI_AVX2_X86_64=m
  - CONFIG_MODULE_SIG_KEY_TYPE_RSA=y
  - CONFIG_MODULE_SIG_KEY_TYPE_ECDSA=n
  - Kernel hacking
  - CONFIG_FAIL_SUNRPC=n
  - SCSI device support
  - CONFIG_SCSI_UFS_HPB=y
  - CONFIG_SCSI_UFS_FAULT_INJECTION=n
  - Network device support
  - CONFIG_NET_VENDOR_LITEX=y
  - CONFIG_MAXLINEAR_GPHY=m
  - CONFIG_MHI_WWAN_MBIM=m
  - Power management
  - CONFIG_CHARGER_CROS_PCHG=m
  - CONFIG_SENSORS_AQUACOMPUTER_D5NEXT=m
  - CONFIG_SENSORS_SBRMI=m
  - CONFIG_REGULATOR_RTQ2134=m
  - CONFIG_REGULATOR_RTQ6752=m
  - Graphics support
  - CONFIG_DRM_VMWGFX_MKSSTATS=n
  - CONFIG_DRM_PANEL_WIDECHIPS_WS2401=n
  - Sound card support
  - CONFIG_SND_HDA_CODEC_CS8409=m
  - CONFIG_SND_SOC_AMD_ACP5x=m
  - CONFIG_SND_SOC_ICS43432=n
  - CONFIG_SND_SOC_SDW_MOCKUP=m
  - DMA Engine support
  - CONFIG_INTEL_IDXD_COMPAT=y
  - CONFIG_AMD_PTDMA=m
  - X86 Platform Specific Device Drivers
  - CONFIG_MERAKI_MX100=m
  - CONFIG_INTEL_SAR_INT1092=m
  - IOMMU Hardware Support
  - CONFIG_IOMMU_DEFAULT_DMA_STRICT=n
  - CONFIG_IOMMU_DEFAULT_DMA_LAZY=n
  - Industrial I/O support
  - CONFIG_SENSIRION_SGP40=n
  - CONFIG_AD5110=n
  - Misc devices
  - CONFIG_I2C_VIRTIO=m
  - CONFIG_GPIO_VIRTIO=m
  - CONFIG_DMABUF_SYSFS_STATS=n
  - CONFIG_VDPA_USER=m
  - CONFIG_NVMEM_NINTENDO_OTP=m
  - OF dependent (i386, ppc64/ppc64le, riscv64)
  - HI6421V600_IRQ=m
  - LITEX_LITEETH=m
  - MFD_RSMU_I2C=n
  - MFD_RSMU_SPI=n
  - VIDEO_IMX335=m
  - VIDEO_IMX412=m
  - VIDEO_OV9282=m
  - DRM_PANEL_INNOLUX_EJ030NA=n
  - DRM_PANEL_SAMSUNG_ATNA33XC20=n
  - DRM_PANEL_SAMSUNG_DB7430=n
  - COMMON_CLK_XLNX_CLKWZRD=m
  - DMA_RESTRICTED_POOL=n
  - i386
  - CS89x0_ISA=n
  - ppc64
  - DEBUG_WX=n
  - PTDUMP_DEBUGFS=n
  - s390x
  - KCSAN=n
  - KFENCE=y (=n in zfcpdump)
  - KFENCE_STATIC_KEYS=y
  - KFENCE_SAMPLE_INTERVAL=0
  - KFENCE_NUM_OBJECTS=255
  - KFENCE_STRESS_TEST_FAULTS=0
  - riscv64
  - POWER_RESET_TPS65086=y
  - DRM_PANEL_ILITEK_ILI9341=n
- commit 8787773
* Mon Sep 13 2021 martin.wilck@suse.com
- fixup "rpm: support gz and zst compression methods" once more
  (bsc#1190428, bsc#1190358)
  Fixes: 3b8c4d9bcc24 ("rpm: support gz and zst compression methods")
  Fixes: 23510fce36ec ("fixup "rpm: support gz and zst compression methods"")
- commit 165378a
* Sun Sep 12 2021 martin.wilck@suse.com
- fixup "rpm: support gz and zst compression methods" once more
  Fixes: 3b8c4d9bcc24 ("rpm: support gz and zst compression methods")
  Fixes: 23510fce36ec ("fixup "rpm: support gz and zst compression methods"")
- commit 34e68f4
* Sun Sep 12 2021 jeffm@suse.com
- Avoid double printing SUSE specific flags in mod->taint (bsc#1190413).
- commit 3b944fc
* Sun Sep 12 2021 martin.wilck@suse.com
- fixup "rpm: support gz and zst compression methods"
  Fixes: 3b8c4d9bcc24 ("rpm: support gz and zst compression methods")
- commit 23510fc
* Fri Sep 10 2021 msuchanek@suse.de
- kernel-cert-subpackage: Fix certificate location in scriptlets
  (bsc#1189841).
  Fixes: d9a1357edd73 ("rpm: Define $certs as rpm macro (bsc#1189841).")
- commit 8684de8
* Fri Sep 10 2021 msuchanek@suse.de
- kernel-binary.spec.in Stop templating the scriptlets for subpackages
  (bsc#1190358).
  The script part for base package case is completely separate from the
  part for subpackages. Remove the part for subpackages from the base
  package script and use the KMP scripts for subpackages instead.
- commit 5d1f677
* Fri Sep 10 2021 msuchanek@suse.de
- kernel-binary.spec: Do not fail silently when KMP is empty
  (bsc#1190358).
  Copy the code from kernel-module-subpackage that deals with empty KMPs.
- commit d7d2e6e
* Fri Sep 10 2021 ohering@suse.de
- Document suse-hv-guest-os-id.patch (bsc#814005, bsc#1189965).
- commit 6205661
* Thu Sep  9 2021 rgoldwyn@suse.com
- Delete 0001-apparmor-fix-unnecessary-creation-of-net-compat.patch
  (bsc#1189978)
  Compat patch no longer required since userspace is upgraded to v3.x
- commit c28bbe5
* Wed Sep  8 2021 jeffm@suse.com
- supported-flag: consolidate separate patches into one
  The history of the five supported flag patches can be found in the commit
  log.  This commit unifies them and reverts the removal of get_next_line
  from mainline to allow supported() to repeatedly scan the file in memory
  without modifying it.  I looked into using tsearch() to handle the
  lookups and it turns out that it's no faster than just scanning the file
  repeatedly in memory.
- commit d3dcd16
* Wed Sep  8 2021 jeffm@suse.com
- Delete patches.suse/setuid-dumpable-wrongdir (bsc#1189957).
- commit 762368d
* Wed Sep  8 2021 tiwai@suse.de
- Bluetooth: schedule SCO timeouts with delayed_work
  (CVE-2021-3640 bsc#1188172).
- Refresh patches.suse/Bluetooth-switch-to-lock_sock-in-SCO.patch.
- commit 2605fb9
* Wed Sep  8 2021 jslaby@suse.cz
- rpm/kernel-source.spec.in: do some more for vanilla_only
  Make sure:
  * sources are NOT executable
  * env is not used as interpreter
  * timestamps are correct
  We do all this for normal kernel builds, but not for vanilla_only
  kernels (linux-next and vanilla).
- commit b41e4fd
* Wed Sep  8 2021 jslaby@suse.cz
- Linux 5.14.2 (bsc#1012628).
- ext4: fix race writing to an inline_data file while its xattrs
  are changing (bsc#1012628).
- ext4: fix e2fsprogs checksum failure for mounted filesystem
  (bsc#1012628).
- xtensa: fix kconfig unmet dependency warning for
  HAVE_FUTEX_CMPXCHG (bsc#1012628).
- USB: serial: pl2303: fix GL type detection (bsc#1012628).
- USB: serial: cp210x: fix control-characters error handling
  (bsc#1012628).
- USB: serial: cp210x: fix flow-control error handling
  (bsc#1012628).
- ALSA: hda/realtek: Quirk for HP Spectre x360 14 amp setup
  (bsc#1012628).
- ALSA: usb-audio: Fix regression on Sony WALKMAN NW-A45 DAC
  (bsc#1012628).
- ALSA: hda/realtek: Workaround for conflicting SSID on ASUS
  ROG Strix G17 (bsc#1012628).
- ALSA: pcm: fix divide error in snd_pcm_lib_ioctl (bsc#1012628).
- ALSA: usb-audio: Work around for XRUN with low latency playback
  (bsc#1012628).
- media: stkwebcam: fix memory leak in stk_camera_probe
  (bsc#1012628).
- commit b155faa
* Tue Sep  7 2021 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move to appropriate section:
  - patches.suse/crypto-ecc-handle-unaligned-input-buffer-in-ecc_swap.patch
- commit 1eedbb8
* Tue Sep  7 2021 mbrugger@suse.com
- crypto: ecc - handle unaligned input buffer in ecc_swap_digits
  (bsc#1188327).
- commit f7925a4
* Tue Sep  7 2021 hare@suse.de
- Refresh patches.suse/scsi-retry-alua-transition-in-progress.
- Delete patches.suse/megaraid-mbox-fix-SG_IO.
- commit d1e442c
* Mon Sep  6 2021 mkoutny@suse.com
- memcg: enable accounting of ipc resources (bsc#1190115
  CVE-2021-3759).
- commit 9193235
* Mon Sep  6 2021 msuchanek@suse.de
- rpm: Fold kernel-devel and kernel-source scriptlets into spec files
  (bsc#1189841).
  These are unchanged since 2011 when they were introduced. No need to
  track them separately.
- commit 692d38b
* Mon Sep  6 2021 msuchanek@suse.de
- rpm: Abolish image suffix (bsc#1189841).
  This is used only with vanilla kernel which is not supported in any way.
  The only effect is has is that the image and initrd symlinks are created
  with this suffix.
  These symlinks are not used except on s390 where the unsuffixed symlinks
  are used by zipl.
  There is no reason why a vanilla kernel could not be used with zipl as
  well as it's quite unexpected to not be able to boot when only a vanilla
  kernel is installed.
  Finally we now have a backup zipl kernel so if the vanilla kernel is
  indeed unsuitable the backup kernel can be used.
- commit e2f37db
* Mon Sep  6 2021 msuchanek@suse.de
- kernel-binary.spec: Define $image as rpm macro (bsc#1189841).
- commit e602b0f
* Mon Sep  6 2021 msuchanek@suse.de
- rpm: Define $certs as rpm macro (bsc#1189841).
  Also pass around only the shortened hash rather than full filename.
  As has been discussed in bsc#1124431 comment 51
  https://bugzilla.suse.com/show_bug.cgi?id=1124431#c51 the placement of
  the certificates is an API which cannot be changed unless we can ensure
  that no two kernels that use different certificate location can be built
  with the same certificate.
- commit d9a1357
* Sat Sep  4 2021 jslaby@suse.cz
- watchdog: Fix NULL pointer dereference when releasing cdev
  (bsc#1190093).
- Update config files.
  We can enable the option after this fix again.
- commit 65109d0
* Sat Sep  4 2021 jslaby@suse.cz
- Linux 5.14.1 (bsc#1012628).
- Bluetooth: btusb: check conditions before enabling USB ALT 3
  for WBS (bsc#1012628).
- net: dsa: mt7530: fix VLAN traffic leaks again (bsc#1012628).
- btrfs: fix NULL pointer dereference when deleting device by
  invalid id (bsc#1012628).
- Revert "floppy: reintroduce O_NDELAY fix" (bsc#1012628).
- fscrypt: add fscrypt_symlink_getattr() for computing st_size
  (bsc#1012628).
- ext4: report correct st_size for encrypted symlinks
  (bsc#1012628).
- f2fs: report correct st_size for encrypted symlinks
  (bsc#1012628).
- ubifs: report correct st_size for encrypted symlinks
  (bsc#1012628).
- net: don't unconditionally copy_from_user a struct ifreq for
  socket ioctls (bsc#1012628).
- audit: move put_tree() to avoid trim_trees refcount underflow
  and UAF (bsc#1012628).
- commit 1059c60
* Fri Sep  3 2021 mkubecek@suse.cz
- update patches metadata
- update upstream references:
  - patches.suse/Bluetooth-avoid-circular-locks-in-sco_sock_connect.patch
  - patches.suse/Bluetooth-btusb-Add-support-for-Foxconn-Mediatek-Chi.patch
  - patches.suse/Bluetooth-btusb-Add-support-for-IMC-Networks-Mediate.patch
  - patches.suse/Bluetooth-switch-to-lock_sock-in-SCO.patch
- commit c2e3f15
* Fri Sep  3 2021 mkubecek@suse.cz
- HID: usbhid: Simplify code in hid_submit_ctrl()
  (<cover.1630658591.git.mkubecek@suse.cz>).
- HID: usbhid: Fix warning caused by 0-length input reports
  (<cover.1630658591.git.mkubecek@suse.cz>).
- HID: usbhid: Fix flood of "control queue full" messages
  (<cover.1630658591.git.mkubecek@suse.cz>).
- commit 4552165
* Fri Sep  3 2021 mkubecek@suse.cz
- Delete patches.suse/hid-fix-length-inconsistency.patch.
  To be replaced by a cherry pick of corresponding upstream commits.
- commit ba7e2a2
* Thu Sep  2 2021 mkubecek@suse.cz
- Delete patches.suse/Revert-netfilter-conntrack-remove-helper-hook-again.patch (bsc#1189964)
  The regression addressed by this revert was fixed properly by mainline
  commit ee04805ff54a ("netfilter: conntrack: make conntrack userspace
  helpers work again") in 5.7.
- commit 775ed38
* Thu Sep  2 2021 mkubecek@suse.cz
- series.conf: cleanup
  Move queued patches to "almost mainline" section.
  No effect on expanded tree.
- commit e91bb9d
* Thu Sep  2 2021 jslaby@suse.cz
- vt_kdsetmode: extend console locking (bsc#1190025
  CVE-2021-3753).
- commit 18d6ea3
* Thu Sep  2 2021 jslaby@suse.cz
- Update config files. Disable CONFIG_WATCHDOG_HRTIMER_PRETIMEOUT
  (bsc#1190093)
- commit 55bd270
* Wed Sep  1 2021 tiwai@suse.de
- Bluetooth: sco: Fix lock_sock() blockage by memcpy_from_msg()
  (CVE-2021-3640 bsc#1188172).
- commit b9d15a3
* Tue Aug 31 2021 lduncan@suse.com
- Delete
  patches.suse/uapi-add-a-compatibility-layer-between-linux-uio-h-and-glibc (bsc#1189959).
  No longer needed, since it's upstream now.
- commit b1aeba4
* Tue Aug 31 2021 msuchanek@suse.de
- rpm: Abolish scritplet templating (bsc#1189841).
  Outsource kernel-binary and KMP scriptlets to suse-module-tools.
  This allows fixing bugs in the scriptlets as well as defining initrd
  regeneration policy independent of the kernel packages.
- commit e98096d
* Tue Aug 31 2021 mbrugger@suse.com
- arm64: Update config files. (bsc#1189922)
  Enable ISP1760_DUAL_ROLE
- commit c265161
* Tue Aug 31 2021 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Use kmod-zstd provide.
  This makes it possible to use kmod with ZSTD support on non-Tumbleweed.
- commit 357f09a
* Mon Aug 30 2021 ludwig.nussel@suse.de
- rpm/kernel-binary.spec.in: avoid conflicting suse-release
  suse-release has arbitrary values in staging, we can't use it for
  dependencies. The filesystem one has to be enough (boo#1184804).
- commit 56f2cba
* Mon Aug 30 2021 mkubecek@suse.cz
- Update to 5.14 final
- refresh configs
- commit d419f63
* Mon Aug 30 2021 mkubecek@suse.cz
- config: update and enable armv6hl
  New config option values copied from arvm7hl.
- commit 7224850
* Mon Aug 30 2021 mkubecek@suse.cz
- config: update and enable armv7hl
  New config option values copied from arm64 except:
  - PCI_IXP4XX=n (does not allow module build)
  - MTD_NAND_PL35X=m
  - IPMI_KCS_BMC_CDEV_IPMI=m
  - IPMI_KCS_BMC_SERIO=m
  - MSC313E_WATCHDOG=m
  - REGULATOR_MT6359=m
  - REGULATOR_RT5033=m
  - ARM_GT_INITIAL_PRESCALER_VAL=2 (default)
  - INTEL_QEP=m
- commit 2df785b
* Fri Aug 27 2021 ludwig.nussel@suse.de
- rpm: fix kmp install path
- commit 22ec560
* Thu Aug 26 2021 ludwig.nussel@suse.de
- post.sh: detect /usr mountpoint too
- commit c7b3d74
* Mon Aug 23 2021 jeffm@suse.com
- config: re-modularize CRYPTO_{CTS,ECB,XTS} on arm* (bsc#1189034).
  Now that FS_ENCRYPTION_ALGS is modular, the crypto modules it utilizes
  can be modular as well.  CRYPTO_AES and CRYPTO_CBC are used by
  ENCRYPTED_KEYS and must remain built-in.  CRYPTO_SHA512 and CRYPTO_HMAC
  are used by module signature validation and must also remain built-in.
- commit dbb9dbc
* Mon Aug 23 2021 jeffm@suse.com
- config: re-modularize CRYPTO_{GCM,GHASH,GF128MUL} on arm* (bsc#1189033).
  These modules were selected as built-in due to Kconfig changes between
  4.14-rc3 and 5.8-rc1 selecting them if BIG_KEYS was enabled.  They can
  be built as modules again now.
- commit bb04225
* Mon Aug 23 2021 martin.wilck@suse.com
- kernel-binary.spec.in: make sure zstd is supported by kmod if used
- commit f36412b
* Mon Aug 23 2021 martin.wilck@suse.com
- kernel-binary.spec.in: add zstd to BuildRequires if used
- commit aa61dba
* Mon Aug 23 2021 mkubecek@suse.cz
- hid: fix length inconsistency
  (20210816130059.3yxtdvu2r7wo4uu3@lion.mk-sys.cz).
- commit 61596f4
* Mon Aug 23 2021 mkubecek@suse.cz
- config: refresh vanilla configs
  Vanilla configs also need to include DEBUG_INFO_BTF_MODULES even if the
  value does not differ from base config.
- commit f317ebc
* Mon Aug 23 2021 jslaby@suse.cz
- Update config files. (arm & epaper drivers and other old graphics)
  Propagate recent epaper drivers and other old graphics changes to arms.
- commit dda8a0c
* Mon Aug 23 2021 jslaby@suse.cz
- Update config files. (arm & CONFIG_GAMEPORT)
  Propagate recent CONFIG_GAMEPORT changes to arms.
- commit dc92f5f
* Mon Aug 23 2021 jslaby@suse.cz
- Update config files. (arm & CONFIG_BT_MSFTEXT)
  Propagate recent CONFIG_BT_MSFTEXT changes to arms.
- commit 408b13b
* Mon Aug 23 2021 jslaby@suse.cz
- Update config files. (arm & ATALK)
  Propagate recent ATALK changes to arms.
- commit 32afa86
* Mon Aug 23 2021 jslaby@suse.cz
- Update config files. (arm & EXT4_FS)
  Propagate recent EXT4_FS changes to arms.
- commit dbd131f
* Mon Aug 23 2021 mkubecek@suse.cz
- Update to 5.14-rc7
- eliminated 3 patches:
  - patches.suse/mmc-sdhci-iproc-cap-min-clock-frequency-on-bcm2711.patch
  - patches.suse/mmc-sdhci-iproc-set-sdhci_quirk_cap_clock_base_broken-on-bcm2711.patch
  - patches.suse/crypto-drbg-select-SHA512.patch
- refresh configs
  - DYNAMIC_FTRACE_WITH_ARGS=y (x86_64 only)
- commit 3e03413
* Sun Aug 22 2021 jeffm@suse.com
- config: enable CONFIG_NO_HZ_FULL where supported (bsc#1189692).
- commit 2ac990d
* Sun Aug 22 2021 jeffm@suse.com
- config: enable CONFIG_MAXSMP (bsc#1189691).
- commit 6a73ec9
* Sat Aug 21 2021 jeffm@suse.com
- config: disable CONFIG_SOUNDWIRE_QCOM on x86 (bsc#1189686).
- commit 3b1df20
* Fri Aug 20 2021 jeffm@suse.com
- config: disable CONFIG_MD_MULTIPATH (bsc#1189678).
  First-class multipath on Linux has used dm-multipath for ages.
- commit c61d1ca
* Fri Aug 20 2021 jeffm@suse.com
- config: disable CONFIG_PM_AUTOSLEEP and CONFIG_PM_WAKELOCKS (bsc#1189677).
- commit 1864e4e
* Fri Aug 20 2021 jeffm@suse.com
- config: disable CONFIG_ISDN on arm* (bsc#1189675).
  Without CONFIG_ISDN, we no longer need to carry:
- patches.suse/misdn-add-support-for-group-membership-check.
- config: disable CONFIG_ISDN (bsc#1189675).
  Without CONFIG_ISDN, we no longer need to carry:
- patches.suse/misdn-add-support-for-group-membership-check.
- commit 310ae3e
* Fri Aug 20 2021 jeffm@suse.com
- config: enable CONFIG_PRINTK_CALLER on arm* (bsc#1189674).
- config: enable CONFIG_PRINTK_CALLER (bsc#1189674).
- commit 0ba49b0
* Fri Aug 20 2021 afaerber@suse.com
- config: arm64: Update to 5.14-rc6
- commit 1a6db50
* Fri Aug 20 2021 martin.wilck@suse.com
- rpm: support gz and zst compression methods
  Extend commit 18fcdff43a00 ("rpm: support compressed modules") for
  compression methods other than xz.
- commit 3b8c4d9
* Fri Aug 20 2021 tiwai@suse.de
- Update config files: make pinctrl-cherryview built-in (bsc#1189447)
  Otherwise some devices aren't properly intiailized.
- commit 3bc441a
* Wed Aug 18 2021 tiwai@suse.de
- Bluetooth: switch to lock_sock in SCO (CVE-2021-3640
  bsc#1188172).
- Bluetooth: avoid circular locks in sco_sock_connect
  (CVE-2021-3640 bsc#1188172).
- commit 9562b07
* Tue Aug 17 2021 tiwai@suse.de
- Bluetooth: btusb: Add support for Foxconn Mediatek Chip
  (bsc#1188064).
- Bluetooth: btusb: Add support for IMC Networks Mediatek Chip
  (bsc#1188064).
- commit 3cfd9ab
* Mon Aug 16 2021 msuchanek@suse.de
- kernel-binary.spec: Require dwarves for kernel-binary-devel when BTF is
  enabled (jsc#SLE-17288).
  About the pahole version: v1.18 should be bare mnimum, v1.22 should be
  fully functional, for now we ship git snapshot with fixes on top of
  v1.21.
- commit 8ba3382
* Mon Aug 16 2021 mkubecek@suse.cz
- Update to 5.14-rc6
- refresh configs
  - drop MQ_IOSCHED_DEADLINE_CGROUP
- commit 17c8c26
* Wed Aug 11 2021 msuchanek@suse.de
- README: Modernize build instructions.
- commit 8cc5c28
* Wed Aug 11 2021 jslaby@suse.cz
- rpm/kernel-obs-build.spec.in: make builds reproducible (bsc#1189305)
- commit 7f9ade7
* Tue Aug 10 2021 ykaukab@suse.de
- config: arm64: enable audio support for Nvidia Tegra SOCs
- commit 9983afb
* Mon Aug  9 2021 jeffm@suse.com
- crypto: drbg - select SHA512 (bsc#1189034).
  config: CRYPTO_SHA512 is built-in again.
- commit 80170a0
* Mon Aug  9 2021 ludwig.nussel@suse.de
- Fix filesystem requirement and suse-release requires
  Reduce filesystem conflict to anything less than 16 to allow pulling the
  change into the next major stable version.
  Don't require suse-release as that's not technically required. Conflict
  with a too old one instead.
- commit 913f755
* Mon Aug  9 2021 mkubecek@suse.cz
- Update to 5.14-rc5
- update configs
  - PHYS_RAM_BASE_FIXED=n (riscv64 only, follow upstream revert)
- commit 1838496
* Thu Aug  5 2021 jslaby@suse.cz
- rpm/kernel-source.rpmlintrc: ignore new include/config files
  In 5.13, since 0e0345b77ac4, config files have no longer .h suffix.
  Adapt the zero-length check.
  Based on Martin Liska's change.
- commit b6f021b
* Wed Aug  4 2021 jeffm@suse.com
- config: make CONFIG_INTEL_PMC_CORE modular (bsc#1189072).
  When this option was introduced, it was a boolean.  Since then it's
  been changed to a tristate and can be made modular again.
- config: config: disable epaper drivers and other old graphics (bsc#1189116).
- config: disable CONFIG_GAMEPORT (bsc#1189115).
  The last SoundBlaster card to use a Game Port shipped in 2001.  Devices
  that connect via Game Port can still be used with a USB adapter, which
  doesn't use the GAMEPORT driver.
- config: enable CONFIG_BT_MSFTEXT (bsc#1189113).
- config: disable CONFIG_ATALK (bsc#1189112).
  This disables support for native AppleTalk which Apple stopped
  supporting in 2009.  AppleTalk over IP is implemented using the netatalk
  package.
- config: enable CONFIG_CMA on x86_64 (bsc#1189109).
  CMA was enabled in SLE15-SP3 via jsc#SLE-17227.  One difference is that
  v5.10-rc1 (b7176c261cd) upstream added the ability to allocate areas for
  each NUMA node, which changed some of the defaults.
  The default number of areas (19) is used here.
- commit 1c88b51
* Wed Aug  4 2021 jeffm@suse.com
- config: enable CONFIG_EFI_RCI2_TABLE (bsc#1189108).
- config: disable X86_X32 (bsc#1189069).
  This feature requires a userspace rebuild to use the X32 ABI and that
  hasn't happened.  If that support is eventually added, we can re-enable.
- commit 6fe54e8
* Tue Aug  3 2021 jeffm@jeffm.io
- config: re-modularize CRYPTO_{CTS,ECB,HMAC,SHA512,XTS} (bsc#1189034).
  Now that FS_ENCRYPTION_ALGS is modular, the crypto modules it utilizes
  can be modular as well.  CRYPTO_AES and CRYPTO_CBC are used by
  ENCRYPTED_KEYS and must remain built-in.
- commit 5f8b914
* Tue Aug  3 2021 jeffm@jeffm.io
- config: re-modularize CRYPTO_{GCM,GHASH,GF128MUL} (bsc#1189033).
  These modules were selected as built-in due to Kconfig changes between
  4.14-rc3 and 5.8-rc1 selecting them if BIG_KEYS was enabled.  They can
  be built as modules again now.
- commit fa0c287
* Tue Aug  3 2021 jeffm@jeffm.io
- config: re-modularize ext4 (bsc#1189032).
  ext2/3/4 hasn't been a default file system for SLE or openSUSE in many
  years.  There is little reason to continue to keep it as a built-in.
- commit f41d666
* Tue Aug  3 2021 mbrugger@suse.com
- arm64: Update config files. (bsc#1188702)
- commit a293b6e
* Mon Aug  2 2021 mkubecek@suse.cz
- Update to 5.14-rc4
- refresh configs (cosmetic only)
- commit 025a97d
* Wed Jul 28 2021 mkubecek@suse.cz
- use 3.0 SPDX identifier in rpm License tags
  As requested by Maintenance, change rpm License tags from "GPL-2.0"
  (SPDX 2.0) to "GPL-2.0-only" (SPDX 3.0) so that their scripts do not have
  to adjust the tags with each maintenance update submission.
- commit f888e0b
* Mon Jul 26 2021 mkubecek@suse.cz
- Update to 5.14-rc3
- eliminated 1 patch:
  - patches.suse/seq_file-disallow-extremely-large-seq-buffer-allocat.patch
- update configs
  - SND_SOC_SSM2518=n (x86 and riscv64)
  - drop SND_SOC_ZX_AUD96P22
- commit ee7a475
* Wed Jul 21 2021 mkubecek@suse.cz
- seq_file: disallow extremely large seq buffer allocations
  (CVE-2021-33909 bsc#1188062).
- commit 060b3df
* Sun Jul 18 2021 mkubecek@suse.cz
- Update to 5.14-rc2
- update configs
  - NCSI_OEM_CMD_KEEP_PHY=y
  - EDAC_IGEN6=m (x86_64 only)
- commit 1d63327
* Sun Jul 18 2021 mkubecek@suse.cz
- series.conf: cleanup
- move submitted patch to "almost mainline" section:
  - patches.suse/arm64-dts-rockchip-Disable-CDN-DP-on-Pinebook-Pro.patch
- commit e96fd76
* Fri Jul 16 2021 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Do not install usrmerged kernel on Leap
  (boo#1184804).
- commit 5b51131
* Thu Jul 15 2021 mbrugger@suse.com
- arm64: dts: rockchip: Disable CDN DP on Pinebook Pro
  (bsc#1188234).
- commit 73020a9
* Mon Jul 12 2021 mkubecek@suse.cz
- Update to 5.14-rc1
- eliminated 13 patches (3 stable, 9 mainline, 1 obsolete SUSE)
  - patches.kernel.org/5.13.1-001-Revert-KVM-x86-mmu-Drop-kvm_mmu_extended_role..patch
  - patches.kernel.org/5.13.1-002-mm-page_alloc-correct-return-value-of-populate.patch
  - patches.kernel.org/5.13.1-003-Linux-5.13.1.patch
  - patches.rpmify/scripts-mkmakefile-honor-second-argument.patch
  - patches.suse/ACPI-PM-s2idle-Add-missing-LPS0-functions-for-AMD.patch
  - patches.suse/ACPI-processor-idle-Fix-up-C-state-latency-if-not-or.patch
  - patches.suse/Bluetooth-btqca-Don-t-modify-firmware-contents-in-pl.patch
  - patches.suse/Input-elants_i2c-Fix-NULL-dereference-at-probing.patch
  - patches.suse/brcmfmac-Add-clm_blob-firmware-files-to-modinfo.patch
  - patches.suse/brcmfmac-Delete-second-brcm-folder-hierarchy.patch
  - patches.suse/crypto-ccp-Annotate-SEV-Firmware-file-names.patch
  - patches.suse/pinctrl-bcm2835-accept-fewer-than-expected-irqs.patch
  - patches.suse/proc-Avoid-mixing-integer-types-in-mem_rw.patch
- refresh
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/dm-table-switch-to-readonly
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/kernel-add-release-status-to-kernel-build.patch
  - patches.suse/supported-flag
- disable ARM architectures (need config update)
- new config options
  - General setup
  - SCHED_CORE=y
  - Power management and ACPI options
  - ACPI_PRMT=y
  - TPS68470_PMIC_OPREGION=y
  - Block layer
  - BLK_CGROUP_FC_APPID=y
  - BLK_CGROUP_IOPRIO=y
  - Networking support
  - NETFILTER_NETLINK_HOOK=m
  - File systems
  - HUGETLB_PAGE_FREE_VMEMMAP_DEFAULT_ON=n
  - Security options
  - IMA_DISABLE_HTABLE=n
  - Kernel hacking
  - STACKTRACE_BUILD_ID=y
  - DEBUG_FORCE_FUNCTION_ALIGN_64B=n
  - OSNOISE_TRACER=y
  - TIMERLAT_TRACER=y
  - TEST_SCANF=n
  - TEST_CLOCKSOURCE_WATCHDOG=n
  - PCI support
  - CXL_ACPI=m
  - CXL_PMEM=m
  - SCSI device support
  - SCSI_MPI3MR=m
  - SCSI_EFCT=m
  - Network device support
  - DWMAC_LOONGSON=m
  - MEDIATEK_GE_PHY=m
  - MOTORCOMM_PHY=m
  - WWAN_HWSIM=m
  - RPMSG_WWAN_CTRL=m
  - IOSM=m
  - PHY_CAN_TRANSCEIVER=m
  - INFINIBAND_IRDMA=m
  - Hardware Monitoring support
  - SENSORS_DPS920AB=m
  - SENSORS_MP2888=m
  - SENSORS_PIM4328=m
  - SENSORS_SHT4x=m
  - Voltage and Current Regulator Support
  - REGULATOR_MAX8893=m
  - REGULATOR_RT6160=m
  - REGULATOR_RT6245=m
  - REGULATOR_RT4831=m
  - Graphics support
  - HSA_AMD_SVM=y
  - DRM_SIMPLEDRM=m
  - DRM_HYPERV=m
  - FB_SSD1307=m
  - BACKLIGHT_RT4831=m
  - Sound card support
  - SND_SOC_INTEL_SOF_CS42L42_MACH=m
  - SND_SOC_TFA989X=n
  - SND_SOC_WCD938X_SDW=n
  - X86 Platform Specific Device Drivers
  - DELL_WMI_PRIVACY=y
  - WIRELESS_HOTKEY=m
  - THINKPAD_LMI=m
  - X86_PLATFORM_DRIVERS_INTEL=y
  - INTEL_SKL_INT3472=m
  - Common Clock Framework
  - ICST=n
  - CLK_SP810=n
  - LMK04832=m
  - IOMMU Hardware Support
  - VIRTIO_IOMMU=m
  - Industrial I/O support
  - FXLS8962AF_I2C=n
  - FXLS8962AF_SPI=n
  - SCA3300=n
  - TI_TSC2046=n
  - SPS30_I2C=n
  - SPS30_SERIAL=n
  - IIO_ST_LSM9DS0=n
  - TSL2591=n
  - TMP117=n
  - Misc devices
  - MTD_MCHP48L640=n
  - JOYSTICK_QWIIC=m
  - XILLYUSB=m
  - GPIO_TPS68470=n
  - BATTERY_RT5033=m
  - WATCHDOG_HRTIMER_PRETIMEOUT=y
  - MFD_RT4831=m
  - VIDEO_IMX208=m
  - LEDS_LT3593=m
  - RESET_MCHP_SPARX5=n
  - OF dependent (i386, ppc64 / ppc64le, riscv64)
  - MFD_QCOM_PM8008=n
  - DRM_ITE_IT66121=n
  - DRM_TI_SN65DSI83=n
  - i386
  - DRM_CROS_EC_ANX7688=n
  - ppc64 / ppc64le
  - STRICT_MODULE_RWX=y
  - PPC_RFI_SRR_DEBUG=n
  - ppc64
  - PS3_VERBOSE_RESULT=n
  - s390x
  - SPARX5_SWITCH=m
  - RESET_TI_SYSCON=n
  - riscv64
  - PHYS_RAM_BASE=0x80000000 (default)
  - VMAP_STACK=y
  - TRANSPARENT_HUGEPAGE=y
  - READ_ONLY_THP_FOR_FS=y
  - SND_SOC_RK817=n
  - SND_SOC_RT5640=m
  - POLARFIRE_SOC_MAILBOX=m
  - DEV_DAX=m
  - STACK_HASH_ORDER=20 (default)
  - KFENCE=y
  - KFENCE_STATIC_KEYS=y
  - KFENCE_SAMPLE_INTERVAL=0 (other archs, see bsc#1185565)
  - KFENCE_NUM_OBJECTS=255 (default)
  - KFENCE_STRESS_TEST_FAULTS=0 (default)
- commit 34fe32a
* Sun Jul 11 2021 schwab@suse.de
- config: riscv64: enable DRM_I2C_NXP_TDA998X
  This also selects SND_SOC_HDMI_CODEC, SND_PCM_ELD, SND_PCM_IEC958.
- commit d56d022
* Sun Jul 11 2021 schwab@suse.de
- config: riscv64: enable MFD_TPS65086
  Also enable the related drivers GPIO_TPS65086 and REGULATOR_TPS65086.
- commit ce26f32
* Fri Jul  9 2021 mbrugger@suse.com
- arm64: Update config files. (bsc#1187589)
  Enable PL330 DMA controller.
- commit b6bd6f5
* Fri Jul  9 2021 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Remove zdebug define used only once.
- commit 85a9fc2
* Thu Jul  8 2021 msuchanek@suse.de
- Update config files (boo#1187824).
  CRYPTO_FIPS=y
  CRYPTO_MANAGER_DISABLE_TESTS=n
- commit c81d16b
* Thu Jul  8 2021 msuchanek@suse.de
- kernel-binary.spec: Exctract s390 decompression code (jsc#SLE-17042).
- commit 7f97df2
* Thu Jul  8 2021 msuchanek@suse.de
- rpm/config.sh: Build on s390.
- commit 641dff8
* Thu Jul  8 2021 msuchanek@suse.de
- kernel-binary.spec: Fix up usrmerge for non-modular kernels.
- commit d718cd9
* Thu Jul  8 2021 jslaby@suse.cz
- Linux 5.13.1 (bsc#1012628).
- Revert "KVM: x86/mmu: Drop kvm_mmu_extended_role.cr4_la57 hack"
  (bsc#1012628).
- commit bfd7864
* Wed Jul  7 2021 schwab@suse.de
- config: riscv64: enable MFD_DA9063
  Also enable the related drivers DA9063_WATCHDOG, REGULATOR_DA9063,
  RTC_DRV_DA9063.
- commit 40fb687
* Mon Jul  5 2021 mkubecek@suse.cz
- update upstream references
- update upstream references of patches added in 5.14 merge window:
  - patches.suse/pinctrl-bcm2835-accept-fewer-than-expected-irqs.patch
  - patches.suse/proc-Avoid-mixing-integer-types-in-mem_rw.patch
- commit 9510801
* Thu Jul  1 2021 msuchanek@suse.de
- kernel-binary.spec: Remove obsolete and wrong comment
  mkmakefile is repleced by echo on newer kernel
- commit d9209e7
* Thu Jul  1 2021 mkubecek@suse.cz
- update upstream references
- update upstream references of patches added in 5.14 merge window:
  - patches.suse/ACPI-PM-s2idle-Add-missing-LPS0-functions-for-AMD.patch
  - patches.suse/ACPI-processor-idle-Fix-up-C-state-latency-if-not-or.patch
  - patches.suse/Bluetooth-btqca-Don-t-modify-firmware-contents-in-pl.patch
  - patches.suse/brcmfmac-Add-clm_blob-firmware-files-to-modinfo.patch
  - patches.suse/brcmfmac-Delete-second-brcm-folder-hierarchy.patch
  - patches.suse/crypto-ccp-Annotate-SEV-Firmware-file-names.patch
- commit f094788
* Thu Jul  1 2021 ptesarik@suse.cz
- Set CONFIG_SCSI_SNIC_DEBUG_FS=y (bsc#1158776 comment 19).
- commit d8e1777
* Thu Jul  1 2021 ptesarik@suse.cz
- Set CONFIG_BLK_SED_OPAL=y on arm64 (bsc#1158776 comment 16).
- commit 59a8e8d
* Thu Jul  1 2021 ptesarik@suse.cz
- Set CONFIG_SATA_ZPODD=y on arm64 (bsc#1158776 comment 14).
- commit aad226c
* Thu Jul  1 2021 ptesarik@suse.cz
- Disable MANDATORY_FILE_LOCKING on arm and arm64 (bsc#1158776 comment 12).
- commit b10530c
* Thu Jul  1 2021 ptesarik@suse.cz
- Disable 842 compression on arm64 (bsc#1158776 comment 11).
- commit 41a7837
* Thu Jul  1 2021 ptesarik@suse.cz
- Set CONFIG_USB_CHAOSKEY=m on arm64 (bsc#1158776 comment 9).
- commit e652a59
* Thu Jul  1 2021 ptesarik@suse.cz
- Set CONFIG_INET_DIAG_DESTROY=y on arm64 (bsc#1158776 comment 7).
- commit 1a13a0b
* Thu Jul  1 2021 ptesarik@suse.cz
- Set CONFIG_SLAB_FREELIST_RANDOM=y on arm64 (bsc#1158776 comment 6).
- commit 75baa7c
* Thu Jul  1 2021 ptesarik@suse.cz
- Disable CONFIG_PCCARD on arm64 (bsc#1158776 comment 2).
- commit 1c1f5ad
* Thu Jul  1 2021 jslaby@suse.cz
- mm/page_alloc: Correct return value of populated elements if
  bulk array is populated (bsc#1187901).
- commit b48104a
* Mon Jun 28 2021 jslaby@suse.cz
- ACPI: PM: s2idle: Add missing LPS0 functions for AMD
  (bsc#1185840).
- ACPI: processor idle: Fix up C-state latency if not ordered
  (bsc#1185840).
- Bluetooth: btqca: Don't modify firmware contents in-place
  (bsc#1187472).
- Input: elants_i2c - Fix NULL dereference at probing
  (bsc#1186454).
- mmc: sdhci-iproc: Cap min clock frequency on BCM2711
  (bsc#1176576).
- mmc: sdhci-iproc: Set SDHCI_QUIRK_CAP_CLOCK_BASE_BROKEN on
  BCM2711 (bsc#1176576).
- pinctrl: bcm2835: Accept fewer than expected IRQs (bsc#1181942).
- Refresh
  patches.suse/proc-Avoid-mixing-integer-types-in-mem_rw.patch.
  Port post-5.13 patches from the stable branch.
  Note that patches.suse/proc-Avoid-mixing-integer-types-in-mem_rw.patch
  is in the -mmotm tree, so that the updated upstream info (esp. the SHA)
  is subject to change.
- commit bd5babc
* Mon Jun 28 2021 mkubecek@suse.cz
- Update to 5.13 final
- refresh configs
  - update headers
  - armv7hl: drop GPIO_TQMX86
- commit 54fc53e
* Fri Jun 25 2021 msuchanek@suse.de
- Revert "Update config files (bsc#1187167)" (bsc#1187711).
  The key is needed. When a random key is generaeted it is a problem with
  OBS repository setup. OBS should provide a signing key.
- commit 9839b4a
* Wed Jun 23 2021 schwab@suse.de
- Add dtb-microchip
- commit c797107
* Mon Jun 21 2021 mkubecek@suse.cz
- Update to 5.13-rc7
- eliminate 1 patch
  - patches.suse/0001-x86-ioremap-Map-efi_mem_reserve-memory-as-encrypted-.patch
- refresh configs
- commit d808585
* Thu Jun 17 2021 ludwig.nussel@suse.de
- UsrMerge the kernel (boo#1184804)
- Move files in /boot to modules dir
  The file names in /boot are included as %%ghost links. The %%post script
  creates symlinks for the kernel, sysctl.conf and System.map in
  /boot for compatibility. Some tools require adjustments before we
  can drop those links. If boot is a separate partition, a copy is
  used instead of a link.
  The logic for /boot/vmlinuz and /boot/initrd doesn't change with
  this patch.
- Use /usr/lib/modules as module dir when usermerge is active in the
  target distro.
- commit 6f5ed04
* Wed Jun 16 2021 mbrugger@suse.com
- Refresh
  patches.suse/brcmfmac-Add-clm_blob-firmware-files-to-modinfo.patch.
- Refresh
  patches.suse/brcmfmac-Delete-second-brcm-folder-hierarchy.patch.
- commit b5a438c
* Wed Jun 16 2021 tiwai@suse.de
- Update config files: CONFIG_SND_HDA_INTEL=m for armv7hl, too (bsc#1187334)
  It's used by openQA.
- commit e752118
* Wed Jun 16 2021 msuchanek@suse.de
- kernel-binary.spec.in: Regenerate makefile when not using mkmakefile.
- commit 6b30fe5
* Mon Jun 14 2021 tiwai@suse.de
- rpm/kernel-binary.spec.in: Fix handling of +arch marker (bsc#1186672)
  The previous commit made a module wrongly into Module.optional.
  Although it didn't influence on the end result, better to fix it.
  Also, add a comment to explain the markers briefly.
- commit 8f79742
* Mon Jun 14 2021 schwab@suse.de
- config: riscv64: enable STMMAC_PLATFORM
  This also makes DWMAC_DWC_QOS_ETH, DWMAC_GENERIC, DWMAC_INTEL_PLAT visible
  which are all enabled.
- commit a7c9025
* Mon Jun 14 2021 mkubecek@suse.cz
- Update to 5.13-rc6
- commit e91bc34
* Mon Jun 14 2021 mkubecek@suse.cz
- update patch metadata
- update upstream references and move into more appropriate section
  patches.suse/0001-x86-ioremap-Map-efi_mem_reserve-memory-as-encrypted-.patch
- commit 716a407
* Fri Jun 11 2021 tiwai@suse.de
- Add arch-dependent support markers in supported.conf (bsc#1186672)
  We may need to put some modules as supported only on specific archs.
  This extends the supported.conf syntax to allow to put +arch additionally
  after the unsupported marker, then it'll be conditionally supported on
  that arch.
- commit 8cbdb41
* Fri Jun 11 2021 bwiedemann@suse.de
- Create Symbols.list and ipa-clones.list determistically
  without this patch, filesystem readdir order would influence
  order of entries in these files.
  This patch was done while working on reproducible builds for SLE.
- commit a898b6d
* Fri Jun 11 2021 tiwai@suse.de
- Update config files (bsc#1187167)
  Set empty to CONFIG_MODULE_SIG_KEY for reproducible builds
- commit f27e6f9
* Thu Jun 10 2021 martin.wilck@suse.com
- kernel-binary.spec.in: Add Supplements: for -extra package on Leap
  kernel-$flavor-extra should supplement kernel-$flavor on Leap, like
  it does on SLED, and like the kernel-$flavor-optional package does.
- commit c60d87f
* Tue Jun  8 2021 jroedel@suse.de
- x86/ioremap: Map efi_mem_reserve() memory as encrypted for SEV (bsc#1186884).
- commit c7fb36b
* Mon Jun  7 2021 mbrugger@suse.com
- brcmfmac: Add clm_blob firmware files to modinfo (bsc#1186857).
- commit a0fa2f0
* Mon Jun  7 2021 mkubecek@suse.cz
- Update to 5.13-rc5
- update configs
  - HID_SEMITEK=m
- commit 6828450
* Mon Jun  7 2021 mkubecek@suse.cz
- series.conf: cleanup
  Move submitted patch to "almost mainline" section.
- commit 9f593b6
* Fri Jun  4 2021 mbrugger@suse.com
- brcmfmac: Delete second brcm folder hierarchy (bsc#1186857).
- commit 4011d8b
* Thu Jun  3 2021 msuchanek@suse.de
- Refresh config files.
  Align across architectures:
  BPFILTER_UMH=m
- commit 39d2f9c
* Thu Jun  3 2021 afaerber@suse.com
- config: armv7hl: Update to 5.13-rc4
- commit f762975
* Thu Jun  3 2021 afaerber@suse.com
- config: armv6hl: Update to 5.13-rc4
- commit e26370d
* Thu Jun  3 2021 afaerber@suse.com
- config: arm64: Update to 5.13-rc4
- commit 22709d7
* Thu Jun  3 2021 msuchanek@suse.de
- kernel-binary.spec.in: build-id check requires elfutils.
- commit 01569b3
* Wed Jun  2 2021 msuchanek@suse.de
- kernel-binary.spec: Only use mkmakefile when it exists
  Linux 5.13 no longer has a mkmakefile script
- commit b453c7b
* Tue Jun  1 2021 msuchanek@suse.de
- kernel-doc: Use Sphinx3.
  Sphinx2 is about to be removed from Factory.
- commit e26bc4f
* Mon May 31 2021 mkubecek@suse.cz
- Update to 5.13-rc4
- eliminate 3 patches
  - patches.suse/bpf-Fix-alu32-const-subreg-bound-tracking-on-bitwise.patch
  - patches.suse/bpf-Prevent-writable-memory-mapping-of-read-only-rin.patch
  - patches.suse/bpf-ringbuf-Deny-reserve-of-buffers-larger-than-ring.patch
- update configs
  - BPF_UNPRIV_DEFAULT_OFF=n (backward compatible)
  - MEMTEST=y (riscv64 only, enabled on most architectures)
- commit 25beba1
* Mon May 24 2021 mkubecek@suse.cz
- Update to 5.13-rc3
- eliminated 3 patches
  patches.rpmify/kbuild-dummy-tools-adjust-to-stricter-stackprotector.patch
  patches.suse/ipc-mqueue-msg-sem-Avoid-relying-on-a-stack-reference.patch
- commit 2d296e7
* Wed May 19 2021 jslaby@suse.cz
- Refresh
  patches.suse/crypto-ccp-Annotate-SEV-Firmware-file-names.patch.
  Update upstream status.
- commit 698115b
* Mon May 17 2021 varad.gautam@suse.com
- ipc/mqueue, msg, sem: Avoid relying on a stack reference past
  its expiry (bsc#1185988).
- commit 3e71e40
* Mon May 17 2021 mkubecek@suse.cz
- Update to 5.13-rc2
- commit 977da2f
* Sat May 15 2021 mkubecek@suse.cz
- kbuild: dummy-tools: adjust to stricter stackprotector check.
  Fix i386 builds after recent changes of stackprotector feature check and
  restore stackprotector related config options.
- commit 9c7db9a
* Wed May 12 2021 glin@suse.com
- bpf: Prevent writable memory-mapping of read-only ringbuf pages
  (bsc#1185640 CVE-2021-3489).
- bpf, ringbuf: Deny reserve of buffers larger than ringbuf
  (bsc#1185640 CVE-2021-3489).
- bpf: Fix alu32 const subreg bound tracking on bitwise operations
  (bsc#1185641 CVE-2021-3490).
- commit 1f475c8
* Wed May 12 2021 glin@suse.com
- scripts/git_sort/git_sort.py: add bpf git repo
- commit 65979e3
* Tue May 11 2021 ddiss@suse.de
- proc: Avoid mixing integer types in mem_rw() (CVE-2021-3491
  bsc#1185642).
- io_uring: truncate lengths larger than MAX_RW_COUNT on provide
  buffers (CVE-2021-3491 bsc#1185642).
- io_uring: fix overflows checks in provide buffers (CVE-2021-3491
  bsc#1185642).
- commit 079e747
* Mon May 10 2021 dmueller@suse.com
- Add dtb-apple (bsc#1185845)
- commit 405d0ae
* Mon May 10 2021 mkubecek@suse.cz
- Update to 5.13-rc1
- eliminated 34 patches (22 stable, 12 other)
  - patches.kernel.org/*
  - patches.suse/clk-bcm-rpi-release-firmware-handle-on-unbind.patch
  - patches.suse/dt-bindings-pwm-add-binding-for-rpi-firmware-pwm-bus.patch
  - patches.suse/firmware-raspberrypi-introduce-devm_rpi_firmware_get.patch
  - patches.suse/firmware-raspberrypi-keep-count-of-all-consumers.patch
  - patches.suse/gpio-raspberrypi-exp-release-firmware-handle-on-unbind.patch
  - patches.suse/input-raspberrypi-ts-release-firmware-handle-when-not-needed.patch
  - patches.suse/media-dvb-usb-Fix-memory-leak-at-error-in-dvb_usb_de.patch
  - patches.suse/media-dvb-usb-Fix-use-after-free-access.patch
  - patches.suse/pwm-add-raspberry-pi-firmware-based-pwm-bus.patch
  - patches.suse/reset-raspberrypi-release-firmware-handle-on-unbind.patch
  - patches.suse/soc-bcm-raspberrypi-power-release-firmware-handle-on-unbind.patch
  - patches.suse/vchiq-release-firmware-handle-on-unbind.patch
- disable ARM architectures (need config update)
- refresh
  - patches.rpmify/powerpc-64-BE-option-to-use-ELFv2-ABI-for-big-endian.patch
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/supported-flag
  - patches.suse/supported-flag-modverdir
  - patches.suse/vfs-add-super_operations-get_inode_dev
- config refresh (no longer available as module)
  - PVPANIC (m -> y)
  - NFS_V4_2_SSC_HELPER (m -> y)
- new config options
  - General setup
  - CGROUP_MISC=y
  - Virtualization
  - X86_SGX_KVM=y
  - General architecture-dependent options
  - RANDOMIZE_KSTACK_OFFSET_DEFAULT=y
  - Enable loadable module support
  - MODULE_COMPRESS_NONE=y
  - MODULE_COMPRESS_GZIP=n
  - MODULE_COMPRESS_XZ=n
  - MODULE_COMPRESS_ZSTD=n
  - MODPROBE_PATH="/sbin/modprobe"
  - Networking support
  - NF_LOG_SYSLOG=m
  - NETFILTER_XTABLES_COMPAT=y
  - PCPU_DEV_REFCNT=y
  - CAN_ETAS_ES58X=m
  - BT_AOSPEXT=y
  - BT_VIRTIO=m
  - File systems
  - NETFS_SUPPORT=m
  - NETFS_STATS=y
  - Security options
  - SECURITY_LANDLOCK=y
  - Cryptographic API
  - CRYPTO_ECDSA=y
  - SYSTEM_REVOCATION_LIST=y
  - SYSTEM_REVOCATION_KEYS=""
  - Kernel hacking
  - VMLINUX_MAP=y
  - TEST_DIV64=n
  - Virtualiation drivers
  - PVPANIC=y
  - PVPANIC_MMIO=m
  - PVPANIC_PCI=m
  - VDPA_SIM_BLOCK=m
  - VP_VDPA=m
  - Network device support
  - NET_DSA_MICROCHIP_KSZ8863_SMI=m
  - NET_VENDOR_MICROSOFT=y
  - MICROSOFT_MANA=m
  - MLX5_TC_SAMPLE=y
  - MARVELL_88X2222_PHY=m
  - NXP_C45_TJA11XX_PHY=m
  - WWAN=y
  - WWAN_CORE=m
  - MHI_WWAN_CTRL=m
  - Input device support
  - TOUCHSCREEN_HYCON_HY46XX=m
  - TOUCHSCREEN_ILITEK=m
  - TOUCHSCREEN_MSG2638=m
  - INPUT_IQS626A=m
  - Power supply class support
  - BATTERY_GOLDFISH=m
  - BATTERY_SURFACE=m
  - CHARGER_SURFACE=m
  - Hardware Monitoring support
  - SENSORS_NZXT_KRAKEN2=m
  - SENSORS_BPA_RS600=m
  - SENSORS_FSP_3Y=m
  - SENSORS_IR36021=m
  - SENSORS_MAX15301=m
  - SENSORS_STPDDC60=m
  - Graphics support
  - DRM_AMD_SECURE_DISPLAY=y
  - DRM_I915_REQUEST_TIMEOUT=20000
  - DRM_GUD=m
  - Sound card support
  - SND_SOC_FSL_RPMSG=n
  - SND_SOC_TLV320AIC3X_I2C=n
  - SND_SOC_TLV320AIC3X_SPI=n
  - SND_VIRTIO=m
  - HID support
  - HID_FT260=m
  - SURFACE_KBD=m
  - SURFACE_HID=m
  - X86 Platform Specific Device Drivers
  - GIGABYTE_WMI=m
  - ADV_SWBUTTON=m
  - Microsoft Surface Platform-Specific Device Drivers
  - SURFACE_AGGREGATOR_REGISTRY=m
  - SURFACE_DTX=m
  - SURFACE_PLATFORM_PROFILE=m
  - Industrial I/O support
  - BMI088_ACCEL=n
  - TI_ADS131E08=n
  - CROS_EC_MKBP_PROXIMITY=n
  - Misc devices
  - DW_XDATA_PCIE=m
  - I2C_CP2615=m
  - SPI_ALTERA_CORE=m
  - SPI_ALTERA_DFL=m
  - INTEL_TCC_COOLING=m
  - MFD_ATC260X_I2C=n
  - RTC_DRV_GOLDFISH=m
  - INTEL_IDXD_PERFMON=y
  - UIO_DFL=m
  - OF dependent (i386, ppc64 / ppc64le, riscv64)
  - MFD_NTXEC=n
  - MFD_ROHM_BD957XMUF=n
  - DRM_CHIPONE_ICN6211=n
  - DRM_LONTIUM_LT8912B=n
  - LEDS_RT4505=m
  - i386
  - MODULE_SIG_ALL=n
  - MODULE_SIG_SHA256=y
  - SND_SOC_RT1316_SDW=n
  - SND_SOC_RT711_SDCA_SDW=n
  - SND_SOC_RT715_SDCA_SDW=n
  - LEDS_LGM=m
  - MODULE_SIG_KEY="certs/signing_key.pem"
  - ppc64 / ppc64le
  - TIME_NS=y
  - STRICT_KERNEL_RWX=y
  - CMA_SYSFS=n
  - FSL_DPAA2_SWITCH=m
  - FSL_ENETC_IERB=m
  - DEBUG_RODATA_TEST=n
  - DEBUG_VM_PGTABLE=n
  - s390x
  - CMA_SYSFS=n
  - NET_DSA=n
  - CIO_INJECT=n
  - riscv64
  - SOC_MICROCHIP_POLARFIRE=y
  - RISCV_ERRATA_ALTERNATIVE=y
  - ERRATA_SIFIVE_CIP_453=y
  - ERRATA_SIFIVE_CIP_1200=y
  - KEXEC=y
  - CRASH_DUMP=y
  - PHYS_RAM_BASE_FIXED=n
  - XIP_KERNEL=n
  - STRICT_MODULE_RWX=y
  - PCIE_FU740
  - PROC_VMCORE=y
  - PROC_VMCORE_DEVICE_DUMP=y
  - FORTIFY_SOURCE=y
- commit 0ba08a9
* Fri May  7 2021 jslaby@suse.cz
- Linux 5.12.2 (bsc#1012628).
- perf/core: Fix unconditional security_locked_down() call
  (bsc#1012628).
- platform/x86: thinkpad_acpi: Correct thermal sensor allocation
  (bsc#1012628).
- USB: Add reset-resume quirk for WD19's Realtek Hub
  (bsc#1012628).
- USB: Add LPM quirk for Lenovo ThinkPad USB-C Dock Gen2 Ethernet
  (bsc#1012628).
- ALSA: usb-audio: Fix implicit sync clearance at stopping stream
  (bsc#1012628).
- ALSA: usb-audio: Add MIDI quirk for Vox ToneLab EX
  (bsc#1012628).
- ovl: allow upperdir inside lowerdir (bsc#1012628).
- ovl: fix leaked dentry (bsc#1012628).
- net: qrtr: Avoid potential use after free in MHI send
  (bsc#1012628).
- bpf: Fix leakage of uninitialized bpf stack under speculation
  (bsc#1012628).
- bpf: Fix masking negation logic upon negative dst register
  (bsc#1012628).
- drm/i915: Disable runtime power management during shutdown
  (bsc#1012628).
- net: usb: ax88179_178a: initialize local variables before use
  (bsc#1012628).
- netfilter: conntrack: Make global sysctls readonly in non-init
  netns (bsc#1012628).
- mips: Do not include hi and lo in clobber list for R6
  (bsc#1012628).
- commit 85a2a31
* Thu May  6 2021 msuchanek@suse.de
- kernel-docs.spec.in: Build using an utf-8 locale.
  Sphinx cannot handle UTF-8 input in non-UTF-8 locale.
- commit 0db6da1
* Thu May  6 2021 mkubecek@suse.cz
- config: disable kfence by default (bsc#1185565)
  Apperently the overhead of kfence is not as negligible as the help text
  seemed to promise so that it seems more appropriate to disable kfence by
  default by setting CONFIG_KFENCE_SAMPLE_INTERVAL to 0. Anyone who wants to
  enable it can still do so using the kfence.sample_interval command line
  parameter.
- commit 5d73dc7
* Wed May  5 2021 msuchanek@suse.de
- rpm/kernel-docs.spec.in: Add amscls as required for build.
  [  781s] ! LaTeX Error: File `amsthm.sty' not found.
- commit 1fd6a67
* Wed May  5 2021 msuchanek@suse.de
- Fix vanilla ppc64 build.
- commit f1085cb
* Wed May  5 2021 mkubecek@suse.cz
- rpm: drop /usr/bin/env in interpreter specification
  OBS checks don't like /usr/bin/env in script interpreter lines but upstream
  developers tend to use it. A proper solution would be fixing the depedency
  extraction and drop the OBS check error but that's unlikely to happen so
  that we have to work around the problem on our side and rewrite the
  interpreter lines in scripts before collecting files for packages instead.
- commit 45c5c1a
* Tue May  4 2021 mbrugger@suse.com
- supported.conf: add USB Typec to installer (bsc#1184867)
- commit 17b53f0
* Tue May  4 2021 dwagner@suse.de
- scripts/git_sort/git_sort.py: Update nvme repositories
- commit e849c44
* Sun May  2 2021 jslaby@suse.cz
- Linux 5.12.1 (bsc#1012628).
- mei: me: add Alder Lake P device id (bsc#1012628).
- cfg80211: fix locking in netlink owner interface destruction
  (bsc#1012628).
- iwlwifi: Fix softirq/hardirq disabling in
  iwl_pcie_gen2_enqueue_hcmd() (bsc#1012628).
- USB: CDC-ACM: fix poison/unpoison imbalance (bsc#1012628).
- net: hso: fix NULL-deref on disconnect regression (bsc#1012628).
- commit 9f237a4
* Sat May  1 2021 msuchanek@suse.de
- powerpc/64: BE option to use ELFv2 ABI for big endian kernels
  (BTFIDS vmlinux FAILED unresolved symbol vfs_truncate).
  Update config files.
- commit 17ebdf1
* Fri Apr 30 2021 schwab@suse.de
- rpm/constraints.in: bump disk space to 45GB on riscv64
- commit f8b883f
* Thu Apr 29 2021 tiwai@suse.de
- Update config files: fix armv7hl/lpae config (bsc#1152773)
  CONFIG_OABI_COMPAT was left enabled mistakenly on lpae flavor, which
  resulted in the disablement of CONFIG_SECCOMP_FILTER.  Fix those.
  CONFIG_OABI_COMPAT -> disabled
  CONFIG_SECCOMP_FILTER=y
  CONFIG_HAVE_ARCH_SECCOMP_FILTER=y
  Also corrected the following with the update:
  CONFIG_HAVE_ARCH_AUDITSYSCALL=y
  CONFIG_AUDITSYSCALL=y
  CONFIG_FPE_NWFPE -> removed
  CONFIG_FPE_NWFPE_XP -> removed
  CONFIG_FPE_FASTFPE -> removed
- commit 644711e
* Wed Apr 28 2021 jslaby@suse.cz
- rpm/constraints.in: remove aarch64 disk size exception
  obs://Kernel:stable/kernel-default/ARM/aarch64 currrently fails:
  installing package kernel-default-livepatch-devel-5.12.0-3.1.g6208a83.aarch64 needs 3MB more space on the / filesystem
  The stats say:
  Maximal used disk space: 31799 Mbyte
  By default, we require 35G. For aarch64 we had an exception to lower
  this limit to 30G there. Drop this exception as it is obviously no
  longer valid.
- commit ee00b50
* Mon Apr 26 2021 mkubecek@suse.cz
- series.conf: cleanup
- fix Patch-mainline tag and move to "almost mainline" section:
  patches.suse/crypto-ccp-Annotate-SEV-Firmware-file-names.patch
- commit 3a48ed8
* Mon Apr 26 2021 jroedel@suse.de
- crypto: ccp: Annotate SEV Firmware file names (bsc#1185282).
- commit 66154b6
* Sun Apr 25 2021 mkubecek@suse.cz
- Update to 5.12 final
- refresh configs (headers only)
- commit 9683115
* Sun Apr 25 2021 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Require new enough pahole.
  pahole 1.21 is required for building line-next BTF
- commit 8df1aaa
* Fri Apr 23 2021 martin.wilck@suse.com
- rpm/macros.kernel-source: fix KMP failure in %%install (bsc#1185244)
- commit 52805ed
* Thu Apr 22 2021 msuchanek@suse.de
- rpm/kernel-obs-build.spec.in: Include essiv with dm-crypt (boo#1183063).
  Previously essiv was part of dm-crypt but now it is separate.
  Include the module in kernel-obs-build when available.
  Fixes: 7cf5b9e26d87 ("rpm/kernel-obs-build.spec.in: add dm-crypt for building with cryptsetup")
- commit fe15b78
* Thu Apr 22 2021 tiwai@suse.de
- Revert "rpm/kernel-binary.spec.in: Fix dependency of kernel-*-devel package (bsc#1184514)"
  This turned out to be a bad idea: the kernel-$flavor-devel package
  must be usable without kernel-$flavor, e.g. at the build of a KMP.
  And this change brought superfluous installation of kernel-preempt
  when a system had kernel-syms (bsc#1185113).
- commit d771304
* Wed Apr 21 2021 jslaby@suse.cz
- rpm/check-for-config-changes: add AS_HAS_* to ignores
  arch/arm64/Kconfig defines a lot of these. So far our current compilers
  seem to support them all. But it can quickly change with SLE later.
- commit a4d8194
* Mon Apr 19 2021 mkubecek@suse.cz
- Update to 5.12-rc8
- refresh configs
- commit a71cb9a
* Wed Apr 14 2021 jslaby@suse.cz
- rpm/check-for-config-changes: remove stale comment
  It is stale since 8ab393bf905a committed in 2005 :).
- commit c9f9f5a
* Tue Apr 13 2021 tiwai@suse.de
- rpm/mkspec: Use tilde instead of dot for version string with rc (bsc#1184650)
- commit f37613f
* Mon Apr 12 2021 tiwai@suse.de
- rpm/kernel-binary.spec.in: Fix dependency of kernel-*-devel package (bsc#1184514)
  The devel package requires the kernel binary package itself for building
  modules externally.
- commit 794be7b
* Mon Apr 12 2021 mkubecek@suse.cz
- Update to 5.12-rc7
- commit bd61ada
* Fri Apr  9 2021 msuchanek@suse.de
- Add obsolete_rebuilds_subpackage (boo#1172073 bsc#1191731).
- commit f037781
* Fri Apr  9 2021 msuchanek@suse.de
- rpm/check-for-config-changes: Also ignore AS_VERSION added in 5.12.
- commit bd64cb2
* Fri Apr  9 2021 msuchanek@suse.de
- post.sh: Return an error when module update fails (bsc#1047233 bsc#1184388).
- commit 18f65df
* Wed Apr  7 2021 dmueller@suse.com
- config.conf: reenable armv6/armv7 configs
  (all modules, otherwise same settings like arm64)
- commit d115d63
* Wed Apr  7 2021 dmueller@suse.com
- arm64: add debug config with KASAN enabled (bsc#1183716)
- commit b68cba9
* Tue Apr  6 2021 dmueller@suse.com
- arm64: enable and update config for 5.12
- commit 0a5586c
* Mon Apr  5 2021 mkubecek@suse.cz
- Update to 5.12-rc6
- commit b5f88e6
* Mon Mar 29 2021 mkubecek@suse.cz
- Update to 5.12-rc5
- refresh configs
  - XEN_BALLOON_MEMORY_HOTPLUG_LIMIT renamed to XEN_MEMORY_HOTPLUG_LIMIT (x86_64)
- commit 5fe2d5c
* Fri Mar 26 2021 tiwai@suse.de
- Update config files: disable CONFIG_SND_HDA_INTEL_HDMI_SILENT_STREAM (bsc#1184019)
- commit d848134
* Mon Mar 22 2021 mkubecek@suse.cz
- Update to 5.12-rc4
- update configs
  - VFIO=n (s390x/zfcpdump only)
  - drop SND_SOC_SIRF_AUDIO_CODEC (removed)
  - drop ADI_AXI_ADC (x86_64, depends on OF now)
- commit 094141b
* Mon Mar 22 2021 mkubecek@suse.cz
- config: disable obsolete crypto algorithms (bsc#1180928)
- CONFIG_CRYPTO_USER_API_ENABLE_OBSOLETE y->n
  - drop CRYPTO_ANUBIS
  - drop CRYPTO_ARC4
  - drop CRYPTO_KHAZAD
  - drop CRYPTO_SEED
  - drop CRYPTO_TEA
- commit 1c5c406
* Tue Mar 16 2021 tiwai@suse.de
- Update config files: enable CONFIG_BMP280=m for x86 (bsc#1183198)
- commit e29c84f
* Mon Mar 15 2021 mkubecek@suse.cz
- Update to 5.12-rc3
- eliminated 3 patches
  - patches.rpmify/kbuild-dummy-tools-adjust-to-scripts-cc-version.sh.patch
  - patches.rpmify/kbuild-dummy-tools-fix-inverted-tests-for-gcc.patch
  - patches.rpmify/kbuild-dummy-tools-support-MPROFILE_KERNEL-checks-fo.patch
- update configs
  - COMPILE_TEST=n (s390x)
  - TMPFS_INODE64=y (s390x)
- commit 89b1f10
* Sun Mar 14 2021 mkubecek@suse.cz
- config: update with dummy toolchain
- new config options:
  - GCC_PLUGINS=y
  - GCC_PLUGIN_CYC_COMPLEXITY is not set
  - GCC_PLUGIN_LATENT_ENTROPY is not set
  - GCC_PLUGIN_RANDSTRUCT is not set
  - GCC_PLUGIN_STRUCTLEAK_USER is not set
  - GCC_PLUGIN_STRUCTLEAK_BYREF is not set
  - GCC_PLUGIN_STRUCTLEAK_BYREF_ALL is not set
- commit 6e44961
* Fri Mar 12 2021 tiwai@suse.de
- Refresh media fixes to the upstreamed version (bsc#1181104)
  Refreshed:
  patches.suse/media-dvb-usb-Fix-memory-leak-at-error-in-dvb_usb_de.patch
  patches.suse/media-dvb-usb-Fix-use-after-free-access.patch
- commit 101728a
* Wed Mar 10 2021 jslaby@suse.cz
- rpm/check-for-config-changes: comment on the list
  To explain what it actually is.
- commit e94bacf
* Wed Mar 10 2021 jslaby@suse.cz
- rpm/check-for-config-changes: define ignores more strictly
  * search for whole words, so make wildcards explicit
  * use ' for quoting
  * prepend CONFIG_ dynamically, so it need not be in the list
- commit f61e954
* Wed Mar 10 2021 jslaby@suse.cz
- rpm/check-for-config-changes: sort the ignores
  They are growing so to make them searchable by humans.
- commit 67c6b55
* Wed Mar 10 2021 jslaby@suse.cz
- rpm/check-for-config-changes: add -mrecord-mcount ignore
  Added by 3b15cdc15956 (tracing: move function tracer options to Kconfig)
  upstream.
- commit 018b013
* Wed Mar 10 2021 jslaby@suse.cz
- kbuild: dummy-tools: adjust to scripts/cc-version.sh
  (bsc#1181862).
- commit cfbfafc
* Tue Mar  9 2021 msuchanek@suse.de
- Delete patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch.
  Should not be needed anymore with dummy-tools.
- commit 41fc82c
* Mon Mar  8 2021 jslaby@suse.cz
- kbuild: dummy-tools, support MPROFILE_KERNEL checks for ppc
  (bsc#1181862).
- commit c4424c2
* Sun Mar  7 2021 mkubecek@suse.cz
- Update to 5.12-rc2
- eliminated 1 patch
  - patches.suse/swap-fix-swapfile-read-write-offset.patch
- update configs
  - KVM_XEN=n (x86)
  - SND_SOC_SOF_MERRIFIELD=m (i386)
- commit d9388fc
* Fri Mar  5 2021 dmueller@suse.com
- ARMv6/v7: Update config files. (bsc#1183009)
  enable CONFIG_ARM_MODULE_PLTS to fix module loading issues
- commit 501199e
* Fri Mar  5 2021 jslaby@suse.cz
- rpm/check-for-config-changes: declare sed args as an array
  So that we can reuse it in both seds.
  This also introduces IGNORED_CONFIGS_RE array which can be easily
  extended.
- commit a1976d2
* Thu Mar  4 2021 jslaby@suse.cz
- rpm/check-for-config-changes: ignore more configs
  Specifially, these:
  * CONFIG_CC_HAS_*
  * CONFIG_CC_HAVE_*
  * CONFIG_CC_CAN_*
  * CONFIG_HAVE_[A-Z]*_COMPILER
  * CONFIG_TOOLS_SUPPORT_*
  are compiler specific too. This will allow us to use super configs
  using kernel's dummy-tools.
- commit d12dcbd
* Thu Mar  4 2021 mkubecek@suse.cz
- swap: fix swapfile read/write offset.
- commit bdb065a
* Wed Mar  3 2021 yousaf.kaukab@suse.com
- config: arm64: sync xgmac-mdio config with SLE
- commit 29472ca
* Wed Mar  3 2021 yousaf.kaukab@suse.com
- config: arm64: sync coresight configs with SLE
- commit 914c23b
* Wed Mar  3 2021 jslaby@suse.cz
- kbuild: dummy-tools, fix inverted tests for gcc (bsc#1181862).
- commit ddbefa3
* Tue Mar  2 2021 dmueller@suse.com
- Remove zte device tree builds
  The zte vendor directory has been dropped in 5.12.rc1 via this change:
  commit 89d4f98ae90d95716009bb89823118a8cfbb94dd
  Author: Arnd Bergmann <arnd@arndb.de>
  Date:   Mon Jan 18 14:06:09 2021 +0100
- commit 6811d6c
* Mon Mar  1 2021 mkubecek@suse.cz
- Update to 5.12-rc1
- eliminated 30 patches (26 stable, 4 other)
  - patches.kernel.org/*
  - patches.suse/drm-bail-out-of-nouveau_channel_new-if-channel-init-.patch
  - patches.suse/floppy-reintroduce-O_NDELAY-fix.patch
  - patches.suse/media-uvcvideo-Accept-invalid-bFormatIndex-and-bFram.patch
  - patches.suse/nvmem-add-driver-to-expose-reserved-memory-as-nvmem.patch
- disable ARM architectures (need config update)
- refresh
  - patches.rpmify/Add-ksym-provides-tool.patch
  - patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch
  - patches.suse/acpi_thermal_passive_blacklist.patch
  - patches.suse/btrfs-use-the-new-VFS-super_block_dev.patch
  - patches.suse/supported-flag
  - patches.suse/supported-flag-modverdir
  - patches.suse/supported-flag-wildcards
  - patches.suse/vfs-add-super_operations-get_inode_dev
- new config options
  - Power management and ACPI options
  - CONFIG_ACPI_FPDT=y
  - General architecture-dependent options
  - CONFIG_LTO_NONE=y
  - Enable loadable module support
  - CONFIG_TRIM_UNUSED_KSYMS=n
  - Networking support
  - CONFIG_IP_VS_TWOS=m
  - CONFIG_NET_DSA_TAG_XRS700X=m
  - CONFIG_NFC_VIRTUAL_NCI=m
  - Library routines
  - CONFIG_STACK_HASH_ORDER=20
  - Kernel hacking
  - CONFIG_DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT=n
  - CONFIG_KFENCE=y
  - CONFIG_KFENCE_STATIC_KEYS=y
  - CONFIG_KFENCE_SAMPLE_INTERVAL=100
  - CONFIG_KFENCE_NUM_OBJECTS=255
  - CONFIG_KFENCE_STRESS_TEST_FAULTS=0
  - CONFIG_DEBUG_IRQFLAGS=n
  - PCI support
  - CONFIG_PCI_EPF_NTB=m
  - CONFIG_CXL_BUS=m
  - CONFIG_CXL_MEM=m
  - CONFIG_CXL_MEM_RAW_COMMANDS=n
  - Network device support
  - CONFIG_NET_DSA_XRS700X_I2C=m
  - CONFIG_NET_DSA_XRS700X_MDIO=m
  - CONFIG_MLX5_SF=y
  - CONFIG_XILINX_EMACLITE=n
  - CONFIG_MT7921E=m
  - Power management
  - CONFIG_CHARGER_LTC4162L=m
  - CONFIG_CHARGER_BQ256XX=m
  - CONFIG_SENSORS_AHT10=m
  - CONFIG_SENSORS_TPS23861=m
  - CONFIG_REGULATOR_MT6315=m
  - Multimedia support
  - CONFIG_CIO2_BRIDGE=y
  - CONFIG_VIDEO_OV5648=m
  - CONFIG_VIDEO_OV8865=m
  - CONFIG_VIDEO_RDACM21=m
  - Sound card support
  - CONFIG_SND_JACK_INJECTION_DEBUG=n
  - CONFIG_SND_INTEL_BYT_PREFER_SOF=y
  - CONFIG_SND_SOC_RT5659=m
  - CONFIG_SND_SOC_LPASS_RX_MACRO=n
  - CONFIG_SND_SOC_LPASS_TX_MACRO=n
  - HID support
  - CONFIG_HID_PLAYSTATION=m
  - CONFIG_PLAYSTATION_FF=y
  - CONFIG_I2C_HID_ACPI=m
  - USB support
  - CONFIG_USB_CDNS_SUPPORT=m
  - CONFIG_USB_CDNSP_PCI=m
  - CONFIG_USB_CDNSP_GADGET=y
  - CONFIG_USB_CDNSP_HOST=y
  - CONFIG_USB_SERIAL_XR=m
  - LED Support
  - CONFIG_LEDS_TRIGGER_TTY=m
  - CONFIG_LEDS_BLINK=y
  - Microsoft Surface Platform-Specific Device Drivers
  - CONFIG_SURFACE_HOTPLUG=m
  - CONFIG_SURFACE_ACPI_NOTIFY=m
  - CONFIG_SURFACE_AGGREGATOR=m
  - CONFIG_SURFACE_AGGREGATOR_CDEV=m
  - CONFIG_SURFACE_AGGREGATOR_BUS=y
  - CONFIG_SURFACE_AGGREGATOR_ERROR_INJECTION=n
  - Industrial I/O support
  - CONFIG_AD5766=n
  - CONFIG_YAMAHA_YAS530=n
  - CONFIG_HID_SENSOR_CUSTOM_INTEL_HINGE=n
  - Generic powercap sysfs driver
  - CONFIG_DTPM=y
  - CONFIG_DTPM_CPU=y
  - Misc devices
  - CONFIG_BCM_VK=m
  - CONFIG_BCM_VK_TTY=y
  - CONFIG_TCG_TIS_I2C_CR50=m
  - CONFIG_SVC_I3C_MASTER=m
  - CONFIG_MMC_CRYPTO=y
  - CONFIG_INTEL_LDMA=y
  - CONFIG_DMABUF_DEBUG=n
  - CONFIG_ACRN_HSM=m
  - CONFIG_FPGA_DFL_EMIF=m
  - CONFIG_NTB_EPF=m
  - CONFIG_FPGA_DFL_NIOS_INTEL_PAC_N3000=m
  - x86
  - CONFIG_X86_PLATFORM_DRIVERS_DELL=y
  - OF dependent drivers (i386, ppc64/ppc64le, riscv64)
  - PCIE_MICROCHIP_HOST=y
  - VIDEO_IMX334=m
  - DRM_PANEL_DSI_CM=n
  - DRM_PANEL_KHADAS_TS050=n
  - I2C_HID_OF=m
  - I2C_HID_OF_GOODIX=m
  - COMMON_CLK_AXI_CLKGEN=m
  - i386
  - NET_DSA_MV88E6XXX_PTP=y
  - SPI_CADENCE_QUADSPI=m
  - LEDS_BLINK_LGM=m
  - s390x
  - TIME_NS=y
  - DEBUG_ENTRY=n
  - riscv64
  - NUMA=y
  - NODES_SHIFT=2
  - SPARSEMEM_VMEMMAP=y
  - DEFERRED_STRUCT_PAGE_INIT=y
  - LEDS_BLINK_LGM=m
  - KGDB_HONOUR_BLOCKLIST=y
  - FAIL_FUNCTION=n
  - KPROBES_SANITY_TEST=n
  - NUMA_BALANCING=y
  - NUMA_BALANCING_DEFAULT_ENABLED=y
- commit 42fc050
* Mon Mar  1 2021 mkubecek@suse.cz
- rpm/kernel-source.spec.in: temporary workaround for a build failure
  Upstream c6x architecture removal left a dangling link behind which
  triggers openSUSE post-build check in kernel-source, failing
  kernel-source build.
  A fix deleting the danglink link has been submitted but it did not make
  it into 5.12-rc1. Unfortunately we cannot add it as a patch as patch
  utility does not handle symlink removal. Add a temporary band-aid which
  deletes all dangling symlinks after unpacking the kernel source tarball.
  [jslaby] It's not that temporary as we are dragging this for quite some
  time in master. The reason is that this can happen any time again, so
  let's have this in packaging instead.
- rpm/kernel-source.spec.in: temporary workaround for a build failure
  Upstream c6x architecture removal left a dangling link behind which
  triggers openSUSE post-build check in kernel-source, failing
  kernel-source build.
  A fix deleting the danglink link has been submitted but it did not make
  it into 5.12-rc1. Unfortunately we cannot add it as a patch as patch
  utility does not handle symlink removal. Add a temporary band-aid which
  deletes all dangling symlinks after unpacking the kernel source tarball.
- commit 52a1ad7
* Sun Feb 28 2021 schwab@suse.de
- config: riscv64: enable EFI_STUB for vanilla
- commit 40f74b3
* Fri Feb 26 2021 jslaby@suse.cz
- Linux 5.11.2 (bsc#1012628).
- KVM: Use kvm_pfn_t for local PFN variable in
  hva_to_pfn_remapped() (bsc#1012628).
- mm: provide a saner PTE walking API for modules (bsc#1012628).
- KVM: do not assume PTE is writable after follow_pfn
  (bsc#1012628).
- KVM: x86: Zap the oldest MMU pages, not the newest
  (bsc#1012628).
- hwmon: (dell-smm) Add XPS 15 L502X to fan control blacklist
  (bsc#1012628).
- arm64: tegra: Add power-domain for Tegra210 HDA (bsc#1012628).
- Bluetooth: btusb: Some Qualcomm Bluetooth adapters stop working
  (bsc#1012628).
- ntfs: check for valid standard information attribute
  (bsc#1012628).
- usb: quirks: add quirk to start video capture on ELMO L-12F
  document camera reliable (bsc#1012628).
- USB: quirks: sort quirk entries (bsc#1012628).
- HID: make arrays usage and value to be the same (bsc#1012628).
- bpf: Fix truncation handling for mod32 dst reg wrt zero
  (bsc#1012628).
- commit 6fd6105
* Fri Feb 26 2021 mkubecek@suse.cz
- config: refresh
- fix misspelled USB gadget debugging options
- commit 20be8e3
* Wed Feb 24 2021 oneukum@suse.com
- Update config files. Update config files. Enable USB_GADGET(jsc#SLE-14042)
- supported.conf:
  After discussion what the feature request implied, it was
  decided that gadget mode is also needed on x86_64
- commit 4adcbc0
* Wed Feb 24 2021 msuchanek@suse.de
- macros.kernel-source: Use spec_install_pre for certificate installation (boo#1182672).
  Since rpm 4.16 files installed during build phase are lost.
- commit d0b887e
* Wed Feb 24 2021 mkubecek@suse.cz
- update mainline references
- update mainline references:
  patches.suse/drm-bail-out-of-nouveau_channel_new-if-channel-init-.patch
  patches.suse/floppy-reintroduce-O_NDELAY-fix.patch
  patches.suse/media-uvcvideo-Accept-invalid-bFormatIndex-and-bFram.patch
- commit 4eacbc9
* Tue Feb 23 2021 jslaby@suse.cz
- Linux 5.11.1 (bsc#1012628).
- Xen/x86: don't bail early from clear_foreign_p2m_mapping()
  (bsc#1012628).
- Xen/x86: also check kernel mapping in set_foreign_p2m_mapping()
  (bsc#1012628).
- Xen/gntdev: correct dev_bus_addr handling in
  gntdev_map_grant_pages() (bsc#1012628).
- Xen/gntdev: correct error checking in gntdev_map_grant_pages()
  (bsc#1012628).
- xen/arm: don't ignore return errors from set_phys_to_machine
  (bsc#1012628).
- xen-blkback: don't "handle" error by BUG() (bsc#1012628).
- xen-netback: don't "handle" error by BUG() (bsc#1012628).
- xen-scsiback: don't "handle" error by BUG() (bsc#1012628).
- xen-blkback: fix error handling in xen_blkbk_map()
  (bsc#1012628).
- tty: protect tty_write from odd low-level tty disciplines
  (bsc#1012628).
- Bluetooth: btusb: Always fallback to alt 1 for WBS
  (bsc#1012628).
- commit 3652ea1
* Mon Feb 22 2021 mbrugger@suse.com
- arm: Update config files.
  Set CONFIG_WATCHDOG_SYSFS to true (bsc#1182560)
- commit 702d1a3
* Mon Feb 22 2021 msuchanek@suse.de
- rpm/kernel-subpackage-build: Workaround broken bot
  (https://github.com/openSUSE/openSUSE-release-tools/issues/2439)
- commit b74d860
* Wed Feb 17 2021 nsaenzjulienne@suse.de
- Update config files: Set reset-raspberrypi as builtin (bsc#1180336)
  This driver is needed in order to boot through USB. Ideally the kernel
  module should be selected by dracut, but it's not. So make it builtin
  until the relevant dracut fixes are available.
- commit 8186eab
* Tue Feb 16 2021 mkubecek@suse.cz
- series.conf: cleanup
- move patches on the way to mainline into respective section
  patches.suse/drm-bail-out-of-nouveau_channel_new-if-channel-init-.patch
  patches.suse/media-uvcvideo-Accept-invalid-bFormatIndex-and-bFram.patch
  patches.suse/media-dvb-usb-Fix-memory-leak-at-error-in-dvb_usb_de.patch
  patches.suse/media-dvb-usb-Fix-use-after-free-access.patch
  patches.suse/media-pwc-Use-correct-device-for-DMA.patch
- commit 8309a4e
* Mon Feb 15 2021 msuchanek@suse.de
- kernel-binary.spec: Add back initrd and image symlink ghosts to
  filelist (bsc#1182140).
  Fixes: 76a9256314c3 ("rpm/kernel-{source,binary}.spec: do not include ghost symlinks (boo#1179082).")
- commit 606c9d1
* Mon Feb 15 2021 tiwai@suse.de
- rpm/post.sh: Avoid purge-kernel for the first installed kernel (bsc#1180058)
- commit c29e77d
* Mon Feb 15 2021 jslaby@suse.cz
- Refresh
  patches.suse/drm-bail-out-of-nouveau_channel_new-if-channel-init-.patch.
- Refresh
  patches.suse/media-uvcvideo-Accept-invalid-bFormatIndex-and-bFram.patch.
  Update upstream status.
- commit 1916d9d
* Mon Feb 15 2021 mkubecek@suse.cz
- Update to 5.11 final
- refresh configs
- commit 253d8c6
* Fri Feb 12 2021 tiwai@suse.de
- Update config files: enable CONFIG_SERIAL_DEV_CTRL_TTYPORT on x86 (bsc#1182035)
  For supporting MS Surface devices. This required CONFIG_SERIAL_DEV_BUS
  to be built-in. Also this allowed CONFIG_BT_HCIUART_BCM=y as well.
- commit 52688e6
* Fri Feb 12 2021 tiwai@suse.de
- media: pwc: Use correct device for DMA (bsc#1181133).
- commit 721eebd
* Fri Feb 12 2021 nsaenzjulienne@suse.de
- Update config files: armv7hl: Set ledtrig-default-on as builtin (bsc#1182128)
- commit fa9dd94
* Thu Feb 11 2021 nsaenzjulienne@suse.de
- Update config files: Set ledtrig-default-on as builtin (bsc#1182128)
- commit 7800832
* Thu Feb 11 2021 oneukum@suse.com
- Update config files. Enable DWC3 on x86_64
  DWC3 is now needed on x86_64, too, with the added benefit
  of making x86_64 and ARM64 closer (jsc#SLE-14042)
- commit ad4ea5b
* Mon Feb  8 2021 matwey.kornilov@gmail.com
- config: arm64: Use y for CLK_RK3399
  This is to fix booting on RK3399 systems (JeOS-rockpi4)
  When compiled as 'm' there are lots of errors related to clk and no host mmc
  controler initialized.
- commit 3295207
* Mon Feb  8 2021 mkubecek@suse.cz
- Update to 5.11-rc7
- refresh configs
- commit 68cabb0
* Wed Feb  3 2021 tiwai@suse.de
- rpm/kernel-binary.spec.in: Correct Supplements in optional subpkg (jsc#SLE-11796)
  The product string was changed from openSUSE to Leap.
- commit 3cb7943
* Mon Feb  1 2021 mkubecek@suse.cz
- Update to 5.11-rc6
- eliminated 1 patch
  - patches.suse/iwlwifi-dbg-Don-t-touch-the-tlv-data.patch
- refresh
  - patches.suse/acpi_thermal_passive_blacklist.patch
- update configs
  - LEDS_RT8515=m
- commit 8d79a70
* Sat Jan 30 2021 afaerber@suse.com
- config: arm64: Enable Arm SP805 hardware watchdog (boo#1181607)
  The Ten64 board with NXP LS1088A SoC is documented to have Arm SP805 based
  watchdogs, so let's enable the driver for it.
- commit 616a505
* Fri Jan 29 2021 mkubecek@suse.cz
- series.conf: cleanup
- move to "almost mainline" section:
  patches.suse/floppy-reintroduce-O_NDELAY-fix.patch
- commit 26dd464
* Thu Jan 28 2021 mgorman@suse.de
- series.conf: Move performance-related tuning parameters to separate section
  This is in preparation for syncing between SLE-specific tunable changes and
  the master tunings.
- commit 1019feb
* Thu Jan 28 2021 msuchanek@suse.de
- floppy: reintroduce O_NDELAY fix (boo#1181018).
- commit d1b21a6
* Mon Jan 25 2021 mkubecek@suse.cz
- Update to 5.11-rc5
- eliminated 3 patches
  - patches.suse/fs-cachefs-Drop-superfluous-readpages-aops-NULL-chec.patch
  - patches.suse/irq-export-irq_check_status_bit-symbol.patch
  - patches.suse/x86-xen-fix-nopvspin-build-error.patch
- refresh configs
- commit 1a51baa
* Thu Jan 21 2021 tiwai@suse.de
- media: dvb-usb: Fix use-after-free access (bsc#1181104).
- media: dvb-usb: Fix memory leak at error in
  dvb_usb_device_init() (bsc#1181104).
- commit 8c718c9
* Wed Jan 20 2021 msuchanek@suse.de
- Exclude Symbols.list again.
  Removing the exclude builds vanilla/linux-next builds.
  Fixes: 55877625c800 ("kernel-binary.spec.in: Package the obj_install_dir as explicit filelist.")
- commit a1728f2
* Mon Jan 18 2021 mkubecek@suse.cz
- update patch metadata
- update upstream reference:
  patches.suse/iwlwifi-dbg-Don-t-touch-the-tlv-data.patch
- commit e7f6170
* Mon Jan 18 2021 mkubecek@suse.cz
- x86/xen: fix 'nopvspin' build error.
  (fix x86_64/debug and i586/debug builds)
- commit 813e08e
* Mon Jan 18 2021 mkubecek@suse.cz
- Update to 5.11-rc4
- update configs
  - KPROBE_EVENTS_ON_NOTRACE=n (new on arm*, ppc64)
- commit 41414a9
* Thu Jan 14 2021 dmueller@suse.com
- arm*: config: Disable CONFIG_CRYPTO_USER_API_ENABLE_OBSOLETE (bsc#1180928)
  We don't need those deprecated ciphers to be enabled, as nothing
  should be using them
- commit 936fdc1
* Wed Jan 13 2021 nsaenzjulienne@suse.de
- nvmem: Add driver to expose reserved memory as nvmem (jsc#SLE-SLE-16616).
- Update config files: Enable nvmem-rmem as module on arm64 & armv7+lpae, disable it otherwise
  This is needed early to get boot-loader configuration working on RPi4;
  an essential feature.
- commit 33196a7
* Wed Jan 13 2021 nsaenzjulienne@suse.de
- Update config files: Enable i2c_mux_pinctrl (jsc#SLE-15318)
- commit 2cdf5df
* Mon Jan 11 2021 mkubecek@suse.cz
- Update to 5.11-rc3
- update configs
  - NULL_TTY=m
  - AQTION=m (also on other architectures than x86_64 and arm64)
- commit 840b25f
* Sat Jan  9 2021 mbrugger@suse.com
- regulator: mt6323: Add OF match table (bsc#1180731).
- regulator: mt6358: Add OF match table (bsc#1180731).
- regulator: mt6360: Add OF match table (bsc#1180731).
- commit b8fd94e
* Fri Jan  8 2021 tiwai@suse.de
- drm: bail out of nouveau_channel_new if channel init fails
  (CVE-2020-25639 bsc#1176846).
- commit c1cbbd6
* Thu Jan  7 2021 mkubecek@suse.cz
- irq: export irq_check_status_bit symbol.
  Fix aarch64 builds.
- commit 74f9771
* Thu Jan  7 2021 mkubecek@suse.cz
- config: refresh arm configs
- now available: DEBUG_INFO_BTF_MODULES=y
- commit e9c4359
* Thu Jan  7 2021 mkubecek@suse.cz
- iwlwifi: dbg: Don't touch the tlv data (bsc#1180344).
- commit cba8ab9
* Wed Jan  6 2021 dmueller@suse.com
- config.conf: Reenable armv6hl/armv7hl/arm64
- Update config files:
  * Settings copied from x86_64 update
  * arm specific options are =m except if debug or test, =y otherwise
- commit 1fc3034
* Mon Jan  4 2021 mkubecek@suse.cz
- Update to 5.11-rc2
- commit b4a462c
* Mon Dec 28 2020 mkubecek@suse.cz
- Update to 5.11-rc1
- eliminated 63 patches (61 stable, 2 other)
  - patches.kernel.org/*
  - patches.suse/clk-bcm-dvp-add-module_device_table.patch
  - patches.suse/drm-amdgpu-only-set-DP-subconnector-type-on-DP-and-e.patch
- disable ARM architectures (need config update)
- refresh
  - patches.suse/btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch
  - patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
    (renamed to patches.suse/btrfs-use-the-new-VFS-super_block_dev.patch
    to ease frequent refreshes)
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  - patches.suse/supported-flag
- new config options:
  - Processor type and features
  - CONFIG_XEN_PVHVM_GUEST=y
  - CONFIG_X86_SGX=n
  - General architecture-dependent options
  - CONFIG_SECCOMP_CACHE_DEBUG=n
  - Memory Management options
  - CONFIG_GUP_TEST=n
  - Networking support
  - CONFIG_NFT_REJECT_NETDEV=n
  - CONFIG_BRIDGE_CFM=n
  - CONFIG_NET_DSA_TAG_HELLCREEK=n
  - CONFIG_CAN_M_CAN_PCI=n
  - CONFIG_NFC_S3FWRN82_UART=n
  - File systems
  - CONFIG_PSTORE_DEFAULT_KMSG_BYTES=10240
  - CONFIG_CIFS_SWN_UPCALL=n
  - Cryptographic API
  - CONFIG_CRYPTO_DEV_QAT_4XXX=n
  - Library routines
  - CONFIG_DMA_MAP_BENCHMARK=n
  - Kernel hacking
  - CONFIG_DEBUG_KMAP_LOCAL_FORCE_MAP=n
  - CONFIG_FTRACE_RECORD_RECURSION=n
  - CONFIG_RING_BUFFER_VALIDATE_TIME_DELTAS=n
  - Memory Technology Device (MTD) support
  - CONFIG_MTD_NAND_ECC_SW_HAMMING=y
  - CONFIG_MTD_SPI_NOR_SWP_DISABLE=n
  - CONFIG_MTD_SPI_NOR_SWP_DISABLE_ON_VOLATILE=y
  - CONFIG_MTD_SPI_NOR_SWP_KEEP=n
  - Block devices
  - CONFIG_DM_MULTIPATH_IOA=n
  - CONFIG_ZRAM_DEF_COMP_LZORLE=y
  - Network device support
  - CONFIG_MHI_NET=n
  - CONFIG_NET_DSA_HIRSCHMANN_HELLCREEK=n
  - CONFIG_USB_RTL8153_ECM=m
  - Input device support
  - CONFIG_INPUT_DA7280_HAPTICS=n
  - CONFIG_AMD_SFH_HID=n
  - Pin controllers
  - CONFIG_PINCTRL_ALDERLAKE=n
  - CONFIG_PINCTRL_ELKHARTLAKE=n
  - CONFIG_PINCTRL_LAKEFIELD=n
  - Hardware Monitoring support
  - CONFIG_SENSORS_CORSAIR_PSU=n
  - CONFIG_SENSORS_LTC2992=n
  - CONFIG_SENSORS_MAX127=n
  - CONFIG_SENSORS_PM6764TR=n
  - CONFIG_SENSORS_Q54SJ108A2=n
  - CONFIG_SENSORS_SBTSI=n
  - Multimedia support
  - CONFIG_VIDEO_OV02A10=n
  - CONFIG_VIDEO_OV9734=n
  - CONFIG_VIDEO_CCS=n
  - Sound card support
  - CONFIG_SND_SOC_ADI=n
  - CONFIG_SND_SOC_FSL_XCVR=n
  - CONFIG_SND_SOC_SOF_BAYTRAIL_SUPPORT=n
  - CONFIG_SND_SOC_SOF_ALDERLAKE_SUPPORT=n
  - CONFIG_SND_SOC_ADAU1372_I2C=n
  - CONFIG_SND_SOC_ADAU1372_SPI=n
  - CONFIG_SND_SOC_PCM5102A=n
  - CONFIG_SND_SOC_SIMPLE_MUX=n
  - CONFIG_SND_SOC_NAU8315=n
  - CONFIG_SND_SOC_LPASS_WSA_MACRO=n
  - CONFIG_SND_SOC_LPASS_VA_MACRO=n
  - CONFIG_SND_SOC_ADI_AXI_I2S=m
  - CONFIG_SND_SOC_ADI_AXI_SPDIF=m
  - X86 Platform Specific Device Drivers
  - CONFIG_UV_SYSFS=n
  - CONFIG_AMD_PMC=n
  - CONFIG_DELL_WMI_SYSMAN=n
  - CONFIG_INTEL_PMT_CLASS=n
  - CONFIG_INTEL_PMT_TELEMETRY=n
  - CONFIG_INTEL_PMT_CRASHLOG=n
  - Misc drivers
  - CONFIG_MHI_BUS_PCI_GENERIC=n
  - CONFIG_SERIAL_BCM63XX=n
  - CONFIG_MIPI_I3C_HCI=n
  - CONFIG_PTP_1588_CLOCK_OCP=n
  - CONFIG_MFD_INTEL_PMT=n
  - CONFIG_EDAC_IGEN6=n
  - CONFIG_INTEL_IDXD_SVM=n
  - CONFIG_LCD2S=n
  - CONFIG_VDPA_SIM_NET=n
  - CONFIG_EXTCON_USBC_TUSB320=n
  - CONFIG_PWM_DWC=n
  - CONFIG_USB4_DMA_TEST=n
  - CONFIG_SURFACE_PLATFORMS=y
  - CONFIG_SURFACE_GPE=n
  - OF dependent drivers (i386, ppc64/ppc64le, riscv64)
  - MTD_NAND_INTEL_LGM=m
  - PINCTRL_MICROCHIP_SGPIO=n
  - REGULATOR_DA9121=m
  - REGULATOR_PF8X00=m
  - DRM_PANEL_ABT_Y030XX067A=n
  - DRM_PANEL_NOVATEK_NT36672A=n
  - DRM_PANEL_SAMSUNG_SOFEF00=n
  - DRM_PANEL_TDO_TL070WSH30=n
  - DRM_LONTIUM_LT9611UXC=n
  - DRM_ANALOGIX_ANX7625=n
  - RTC_DRV_GOLDFISH=m
  - LITEX_SOC_CONTROLLER=n
  - PWM_ATMEL_TCB=m
  - i386
  - PWM_INTEL_LGM=m
  - DEBUG_KMAP_LOCAL=n
  - s390x
  - DEBUG_USER_ASCE=n
  - riscv64
  - IRQ_TIME_ACCOUNTING
  - POWER_RESET_REGULATOR=y
- commit acbbbf7
* Mon Dec 28 2020 mkubecek@suse.cz
- rpm: drop /usr/bin/env in interpreter specification
  OBS checks don't like /usr/bin/env in script interpreter lines but upstream
  developers tend to use it. A proper solution would be fixing the depedency
  extraction and drop the OBS check error but that's unlikely to happen so
  that we have to work around the problem on our side and rewrite the
  interpreter lines in scripts before collecting files for packages instead.
- commit 0ec5324
* Sun Dec 27 2020 tiwai@suse.de
- media: uvcvideo: Accept invalid bFormatIndex and bFrameIndex
  values (bsc#1180117).
- commit 8684dfe
* Sat Dec 26 2020 jslaby@suse.cz
- Linux 5.10.3 (bsc#1012628).
- md: fix a warning caused by a race between concurrent
  md_ioctl()s (bsc#1012628).
- nl80211: validate key indexes for cfg80211_registered_device
  (bsc#1012628).
- crypto: af_alg - avoid undefined behavior accessing salg_name
  (bsc#1012628).
- media: msi2500: assign SPI bus number dynamically (bsc#1012628).
- fs: quota: fix array-index-out-of-bounds bug by passing correct
  argument to vfs_cleanup_quota_inode() (bsc#1012628).
- quota: Sanity-check quota file headers on load (bsc#1012628).
- Bluetooth: Fix slab-out-of-bounds read in
  hci_le_direct_adv_report_evt() (bsc#1012628).
- f2fs: prevent creating duplicate encrypted filenames
  (bsc#1012628).
- ext4: prevent creating duplicate encrypted filenames
  (bsc#1012628).
- ubifs: prevent creating duplicate encrypted filenames
  (bsc#1012628).
- fscrypt: add fscrypt_is_nokey_name() (bsc#1012628).
- fscrypt: remove kernel-internal constants from UAPI header
  (bsc#1012628).
- serial_core: Check for port state when tty is in error state
  (bsc#1012628).
- HID: i2c-hid: add Vero K147 to descriptor override
  (bsc#1012628).
- scsi: megaraid_sas: Check user-provided offsets (bsc#1012628).
- f2fs: init dirty_secmap incorrectly (bsc#1012628).
- f2fs: fix to seek incorrect data offset in inline data file
  (bsc#1012628).
- coresight: etm4x: Handle TRCVIPCSSCTLR accesses (bsc#1012628).
- coresight: etm4x: Fix accesses to TRCPROCSELR (bsc#1012628).
- coresight: etm4x: Fix accesses to TRCCIDCTLR1 (bsc#1012628).
- coresight: etm4x: Fix accesses to TRCVMIDCTLR1 (bsc#1012628).
- coresight: etm4x: Skip setting LPOVERRIDE bit for qcom,
  skip-power-up (bsc#1012628).
- coresight: etb10: Fix possible NULL ptr dereference in
  etb_enable_perf() (bsc#1012628).
- coresight: tmc-etr: Fix barrier packet insertion for perf buffer
  (bsc#1012628).
- coresight: tmc-etr: Check if page is valid before dma_map_page()
  (bsc#1012628).
- coresight: tmc-etf: Fix NULL ptr dereference in
  tmc_enable_etf_sink_perf() (bsc#1012628).
- ARM: dts: exynos: fix USB 3.0 pins supply being turned off on
  Odroid XU (bsc#1012628).
- ARM: dts: exynos: fix USB 3.0 VBUS control and over-current
  pins on Exynos5410 (bsc#1012628).
- ARM: dts: exynos: fix roles of USB 3.0 ports on Odroid XU
  (bsc#1012628).
- usb: chipidea: ci_hdrc_imx: Pass DISABLE_DEVICE_STREAMING flag
  to imx6ul (bsc#1012628).
- USB: gadget: f_rndis: fix bitrate for SuperSpeed and above
  (bsc#1012628).
- usb: gadget: f_fs: Re-use SS descriptors for SuperSpeedPlus
  (bsc#1012628).
- USB: gadget: f_midi: setup SuperSpeed Plus descriptors
  (bsc#1012628).
- USB: gadget: f_acm: add support for SuperSpeed Plus
  (bsc#1012628).
- USB: serial: option: add interface-number sanity check to flag
  handling (bsc#1012628).
- usb: mtu3: fix memory corruption in mtu3_debugfs_regset()
  (bsc#1012628).
- soc/tegra: fuse: Fix index bug in get_process_id (bsc#1012628).
- exfat: Avoid allocating upcase table using kcalloc()
  (bsc#1012628).
- x86/split-lock: Avoid returning with interrupts enabled
  (bsc#1012628).
- net: ipconfig: Avoid spurious blank lines in boot log
  (bsc#1012628).
- commit 246b3e0
* Thu Dec 24 2020 nsaenzjulienne@suse.de
- reset: raspberrypi: Don't reset USB if already up (bsc#1180336).
- commit cbfc03c
* Tue Dec 22 2020 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference and move to "almost mainline" section:
  patches.suse/clk-bcm-dvp-add-module_device_table.patch
- commit 24deb54
* Mon Dec 21 2020 mkubecek@suse.cz
- config: refresh
- drop USB_SISUSBVGA_CON (no longer accessible)
- commit c403c88
* Mon Dec 21 2020 jslaby@suse.cz
- Linux 5.10.2 (bsc#1012628).
- serial: 8250_omap: Avoid FIFO corruption caused by MDR1 access
  (bsc#1012628).
- ALSA: pcm: oss: Fix potential out-of-bounds shift (bsc#1012628).
- USB: sisusbvga: Make console support depend on BROKEN
  (bsc#1012628).
- USB: UAS: introduce a quirk to set no_write_same (bsc#1012628).
- xhci-pci: Allow host runtime PM as default for Intel Maple
  Ridge xHCI (bsc#1012628).
- xhci-pci: Allow host runtime PM as default for Intel Alpine
  Ridge LP (bsc#1012628).
- usb: xhci: Set quirk for XHCI_SG_TRB_CACHE_SIZE_QUIRK
  (bsc#1012628).
- xhci: Give USB2 ports time to enter U3 in bus suspend
  (bsc#1012628).
- ALSA: usb-audio: Fix control 'access overflow' errors from chmap
  (bsc#1012628).
- ALSA: usb-audio: Fix potential out-of-bounds shift
  (bsc#1012628).
- USB: add RESET_RESUME quirk for Snapscan 1212 (bsc#1012628).
- USB: dummy-hcd: Fix uninitialized array use in init()
  (bsc#1012628).
- USB: legotower: fix logical error in recent commit
  (bsc#1012628).
- ktest.pl: Fix the logic for truncating the size of the log
  file for email (bsc#1012628).
- ktest.pl: If size of log is too big to email, email error
  message (bsc#1012628).
- ptrace: Prevent kernel-infoleak in ptrace_get_syscall_info()
  (bsc#1012628).
- commit 0c7d1c1
* Mon Dec 21 2020 nsaenzjulienne@suse.de
- clk: bcm: dvp: Add MODULE_DEVICE_TABLE() (bsc#1180260).
- commit fa7a177
* Fri Dec 18 2020 tiwai@suse.de
- drm/amdgpu: only set DP subconnector type on DP and eDP
  connectors (bsc#1180227).
- commit 74c3250
* Tue Dec 15 2020 mkubecek@suse.cz
- Linux 5.10.1 (bsc#1012628).
- Revert "dm raid: fix discard limits for raid1 and raid10"
  (bsc#1012628).
- Revert "md: change mddev 'chunk_sectors' from int to unsigned"
  (bsc#1012628).
- commit bc79fb6
* Mon Dec 14 2020 guillaume.gardet@arm.com
- lpae: disable CONFIG_QCOM_PIL_INFO to fix build on armv7
- commit 0c08c2e
* Mon Dec 14 2020 mkubecek@suse.cz
- Update to 5.10 final
- eliminated 1 patch
  - patches.suse/revert-mm-filemap-add-static-for-function-__add_to_p.patch
- update configs
  - NFS_V4_2_READ_PLUS=n (recommended default, unsafe feature)
- commit ff9060b
* Sun Dec 13 2020 dmueller@suse.com
- config.conf: Reenable armv6hl/armv7hl/arm64
- Update config files:
  * Settings copied from x86_64 update
  * arm specific options are =m except if debug or test, =y otherwise
- commit cc424ba
* Thu Dec 10 2020 ohering@suse.de
- config: disable IP_PNP
  The kernel IP autoconfiguration can only be used in practice when driver of
  the network device to be configured is also built into vmlinux. As we build
  all network device drivers as modules, there is no point keeping IP_PNP
  enabled.
- commit 7e286c2
* Thu Dec 10 2020 mkubecek@suse.cz
- config: refresh
- only update CC_VERSION_TEXT after gcc update
- commit 012c071
* Thu Dec 10 2020 mgorman@suse.de
- Update config files to disable CONFIG_DEBUG_SECTION_MISMATCH (bsc#1177403)
- commit d24bd37
* Tue Dec  8 2020 mkubecek@suse.cz
- revert "mm/filemap: add static for
  function __add_to_page_cache_locked"
  (http://lkml.kernel.org/r/20201207081556.pwxmhgdxayzbofpi@lion.mk-sys.cz).
- fix build on ppc64, ppc64le and riscv64
- commit 9688120
* Mon Dec  7 2020 mkubecek@suse.cz
- Update to 5.10-rc7
- refresh
  - patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch
- refresh configs
- commit baa1207
* Tue Dec  1 2020 msuchanek@suse.de
- rpm/kernel-{source,binary}.spec: do not include ghost symlinks
  (boo#1179082).
- commit 76a9256
* Mon Nov 30 2020 ohering@suse.de
- scripts/lib/SUSE/MyBS.pm: properly close prjconf Macros: section
- commit 965157e
* Mon Nov 30 2020 tiwai@suse.de
- Update config files: make CONFIG_SOUNDWIRE=m (bsc#1179201)
  Also turned it off for unrelated platforms
- commit a60b1c2
* Mon Nov 30 2020 mkubecek@suse.cz
- Update to 5.10-rc6
- eliminated 1 patch
  - patches.suse/btrfs-qgroup-don-t-commit-transaction-when-we-have-a.patch
- refresh configs
  - headers only (Factory updated gcc and binutils)
- commit 248e2b4
* Thu Nov 26 2020 nsaenzjulienne@suse.de
- dt-bindings: pwm: Add binding for RPi firmware PWM bus
  (jsc#SLE-16543).
- staging: vchiq: Release firmware handle on unbind
  (jsc#SLE-16543).
- soc: bcm: raspberrypi-power: Release firmware handle on unbind
  (jsc#SLE-16543).
- reset: raspberrypi: Release firmware handle on unbind
  (jsc#SLE-16543).
-  - pwm: Add Raspberry Pi Firmware based PWM bus (jsc#SLE-16543).
  - Update configs: Enable pwm driver on arm64
  - supported.conf: Enable pwm driver
- input: raspberrypi-ts: Release firmware handle when not needed
  (jsc#SLE-16543).
- gpio: raspberrypi-exp: Release firmware handle on unbind
  (jsc#SLE-16543).
- firmware: raspberrypi: Keep count of all consumers
  (jsc#SLE-16543).
- firmware: raspberrypi: Introduce devm_rpi_firmware_get()
  (jsc#SLE-16543).
- clk: bcm: rpi: Release firmware handle on unbind
  (jsc#SLE-16543).
- commit bdec34d
* Tue Nov 24 2020 jslaby@suse.cz
- Update config files (bsc#1179102).
  Set AMIGA_PARTITION=y wherever AFFS_FS=m. The AMIGA_PARTITION's Kconfig
  help suggests: default y if (AMIGA || AFFS_FS=y). And we enable Amiga FS
  in some configs, but don't enable support for Amiga partitions. That is
  a bit pointless. So fix this.
- commit 00f1e2b
* Mon Nov 23 2020 jslaby@suse.cz
- rpm/kernel-binary.spec.in: use grep -E instead of egrep (bsc#1179045)
  egrep is only a deprecated bash wrapper for "grep -E". So use the latter
  instead.
- commit 63d7072
* Mon Nov 23 2020 jslaby@suse.cz
- kernel-{binary,source}.spec.in: do not create loop symlinks (bsc#1179082)
- commit adf56a8
* Mon Nov 23 2020 jslaby@suse.cz
- rpm/kernel-binary.spec.in: avoid using more barewords (bsc#1179014)
  %%split_extra still contained two.
- commit d9b4c40
* Mon Nov 23 2020 mkubecek@suse.cz
- Update to 5.10-rc5
- refresh configs
  - DMA_VIRT_OPS and dependecies dropped on i386
- commit 8ebabda
* Fri Nov 20 2020 msuchanek@suse.de
- kernel-source.spec: Fix build with rpm 4.16 (boo#1179015).
  RPM_BUILD_ROOT is cleared before %%%%install. Do the unpack into
  RPM_BUILD_ROOT in %%%%install
- commit 13bd533
* Fri Nov 20 2020 jslaby@suse.cz
- rpm/kernel-binary.spec.in: avoid using barewords (bsc#1179014)
  Author: Dominique Leuenberger <dimstar@opensuse.org>
- commit 21f8205
* Fri Nov 20 2020 jslaby@suse.cz
- rpm/mkspec: do not build kernel-obs-build on x86_32
  We want to use 64bit kernel due to various bugs (bsc#1178762 to name
  one).
  There is:
  ExportFilter: ^kernel-obs-build.*\.x86_64.rpm$ . i586
  in Factory's prjconf now. No other actively maintained distro (i.e.
  merging packaging branch) builds a x86_32 kernel, hence pushing to
  packaging directly.
- commit 8099b4b
* Wed Nov 18 2020 jslaby@suse.cz
- btrfs: qgroup: don't commit transaction when we already hold
  the handle (bsc#1178634).
  Update upstream status and take the upstream version.
- commit 5d64ed9
* Mon Nov 16 2020 mkubecek@suse.cz
- Update to 5.10-rc4
- commit ea0f69f
* Thu Nov 12 2020 jslaby@suse.cz
- btrfs: qgroup: don't commit transaction when we have already
  hold a transaction handler (bsc#1178634).
- commit 646ed4a
* Tue Nov 10 2020 dmueller@suse.com
- ARM64: Enable CONFIG_ARM64_SW_TTBR0_PAN
  This can help prevent use-after-free bugs becoming an exploitable
  privilege escalation by ensuring that magic values (such as LIST_POISON)
  will always fault when dereferenced
- commit 5a3f5b3
* Mon Nov  9 2020 mkubecek@suse.cz
- Update to 5.10-rc3
- eliminated 1 patch
  - patches.suse/tty-make-FONTX-ioctl-use-the-tty-pointer-they-were-a.patch
- refresh configs
  - update headers after Factory binutils update
  - drop options no longer available
- commit e72caa5
* Wed Nov  4 2020 jslaby@suse.cz
- tty: make FONTX ioctl use the tty pointer they were actually
  passed (bsc#1178123 CVE-2020-25668).
- commit 3b8edfa
* Wed Nov  4 2020 tiwai@suse.de
- Updated Copyright line in rpm templates with SUSE LLC
- commit 39a1fcf
* Wed Nov  4 2020 tiwai@suse.de
- rpm/kernel-obs-build.spec.in: Add -q option to modprobe calls (bsc#1178401)
- commit 33ded45
* Tue Nov  3 2020 tiwai@suse.de
- rpm/kernel-binary.spec.in: Fix compressed module handling for in-tree KMP (jsc#SLE-10886)
  The in-tree KMP that is built with SLE kernels have a different scriptlet
  that is embedded in kernel-binary.spec.in rather than *.sh files.
- commit e32ee2c
* Mon Nov  2 2020 mkubecek@suse.cz
- Update to 5.10-rc2
- eliminated 5 patches
  - patches.rpmify/s390-correct-__bootdata-__bootdata_preserved-macros.patch
  - patches.suse/drm-amd-display-Don-t-invoke-kgdb_breakpoint-uncondi.patch
  - patches.suse/drm-amd-display-Fix-kernel-panic-by-dal_gpio_open-er.patch
  - patches.suse/vt_ioctl-fix-GIO_UNIMAP-regression.patch
  - patches.suse/x86-unwind-orc-Fix-inactive-tasks-with-stack-pointer.patch
- refresh configs
  - CPU_FREQ_DEFAULT_GOV_ONDEMAND -> CPU_FREQ_DEFAULT_GOV_SCHEDUTIL (x86)
  - Intel MIC drivers dropped
- commit a51c4bb
* Thu Oct 29 2020 jslaby@suse.cz
- Refresh patches.suse/vt_ioctl-fix-GIO_UNIMAP-regression.patch.
- Refresh
  patches.suse/x86-unwind-orc-Fix-inactive-tasks-with-stack-pointer.patch.
  Update upstream statuses.
- commit 91029f0
* Thu Oct 29 2020 tiwai@suse.de
- rpm/kernel-module-subpackage: make Group tag optional (bsc#1163592)
- commit 552ec97
* Mon Oct 26 2020 mkubecek@suse.cz
- s390: correct __bootdata / __bootdata_preserved macros
  (http://lkml.kernel.org/r/20201026104811.22ta4pby2chmz4pv@lion.mk-sys.cz).
- commit e4bed42
* Mon Oct 26 2020 jslaby@suse.cz
- vt_ioctl: fix GIO_UNIMAP regression (5.9 GIO_UNIMAP regression).
- commit 8b38830
* Mon Oct 26 2020 mkubecek@suse.cz
- Update to 5.10-rc1
- eliminated 17 patches (16 stable, 1 other)
  - patches.kernel.org/*
  - patches.suse/coresight-fix-offset-by-one-error-in-counting-ports.patch
- disable ARM architectures (need config update)
- refresh
  - patches.suse/apparmor-compatibility-with-v2.x-net.patch
  - patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
  - patches.suse/btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch
  - patches.suse/readahead-request-tunables.patch
- new config options:
  - General setup
  - CONFIG_BPF_PRELOAD=n
  - Power management and ACPI options
  - CONFIG_ACPI_DPTF=y
  - CONFIG_DPTF_PCH_FIVR=m
  - General architecture-dependent options
  - CONFIG_STATIC_CALL_SELFTEST=n
  - Networking support
  - CONFIG_XFRM_USER_COMPAT=m
  - CONFIG_CAN_ISOTP=m
  - CONFIG_CAN_MCP251XFD=m
  - CONFIG_CAN_MCP251XFD_SANITY=n
  - File systems
  - CONFIG_XFS_SUPPORT_V4=y
  - CONFIG_FUSE_DAX=y
  - CONFIG_NFSD_V4_2_INTER_SSC=y
  - Cryptographic API
  - CONFIG_CRYPTO_SM2=m
  - CONFIG_CRYPTO_USER_API_RNG_CAVP=n
  - CONFIG_CRYPTO_USER_API_ENABLE_OBSOLETE=y
  - Library routines
  - CONFIG_FONT_6x8=y
  - Kernel hacking
  - CONFIG_KGDB_HONOUR_BLOCKLIST=y
  - CONFIG_SCF_TORTURE_TEST=n
  - CONFIG_CSD_LOCK_WAIT_DEBUG=n
  - CONFIG_RCU_SCALE_TEST=m
  - CONFIG_FAULT_INJECTION_USERCOPY=n
  - CONFIG_TEST_FREE_PAGES=n
  - PCI support
  - CONFIG_PCIE_BUS_TUNE_OFF=n
  - CONFIG_PCIE_BUS_DEFAULT=y
  - CONFIG_PCIE_BUS_SAFE=n
  - CONFIG_PCIE_BUS_PERFORMANCE=n
  - CONFIG_PCIE_BUS_PEER2PEER=n
  - Network device support
  - CONFIG_NET_DSA_MSCC_SEVILLE=m
  - CONFIG_CHELSIO_INLINE_CRYPTO=y
  - CONFIG_PRESTERA=m
  - CONFIG_PRESTERA_PCI=m
  - CONFIG_ATH11K=m
  - CONFIG_ATH11K_PCI=m
  - CONFIG_ATH11K_DEBUG=n
  - CONFIG_ATH11K_DEBUGFS=n
  - CONFIG_ATH11K_TRACING=n
  - CONFIG_USB_LGM_PHY=m
  - CONFIG_PHY_INTEL_LGM_EMMC=m
  - Input device support
  - CONFIG_JOYSTICK_ADC=m
  - CONFIG_TOUCHSCREEN_ZINITIX=m
  - CONFIG_RMI4_F3A=y
  - CONFIG_HID_VIVALDI=m
  - Character devices
  - CONFIG_HW_RANDOM_XIPHERA=m
  - GPIO Support
  - CONFIG_GPIO_CDEV=y
  - CONFIG_GPIO_CDEV_V1=y
  - Power management
  - CONFIG_CHARGER_BQ25980=m
  - CONFIG_SENSORS_MR75203=m
  - CONFIG_SENSORS_ADM1266=m
  - CONFIG_SENSORS_MP2975=m
  - ACPI INT340X thermal drivers
  - CONFIG_REGULATOR_RASPBERRYPI_TOUCHSCREEN_ATTINY=m
  - CONFIG_REGULATOR_RT4801=m
  - CONFIG_REGULATOR_RTMV20=m
  - Multifunction device drivers
  - CONFIG_MFD_SL28CPLD=n
  - CONFIG_MFD_INTEL_M10_BMC=n
  - Graphics support
  - CONFIG_DRM_AMD_DC_SI=y
  - CONFIG_BACKLIGHT_KTD253=m
  - CONFIG_VIDEO_ZORAN=m
  - CONFIG_VIDEO_ZORAN_DC30=m
  - CONFIG_VIDEO_ZORAN_ZR36060=m
  - CONFIG_VIDEO_ZORAN_BUZ=m
  - CONFIG_VIDEO_ZORAN_DC10=m
  - CONFIG_VIDEO_ZORAN_LML33=m
  - CONFIG_VIDEO_ZORAN_LML33R10=m
  - CONFIG_VIDEO_ZORAN_AVS6EYES=m
  - Sound card support
  - CONFIG_SND_SOC_INTEL_CATPT=m
  - CONFIG_SND_SOC_SOF_BROADWELL_SUPPORT=y
  - CONFIG_SND_SOC_SOF_INTEL_SOUNDWIRE_LINK=y
  - CONFIG_SND_SOC_INTEL_SOUNDWIRE_SOF_MACH=m
  - CONFIG_SND_SOC_CS4234=n
  - CONFIG_SND_SOC_TAS2764=n
  - CONFIG_SOUNDWIRE_QCOM=m
  - USB support
  - CONFIG_USB_FEW_INIT_RETRIES=n
  - CONFIG_TYPEC_TCPCI_MAXIM=m
  - CONFIG_TYPEC_STUSB160X=m
  - CONFIG_USB4_DEBUGFS_WRITE=n
  - Virtualization
  - CONFIG_NITRO_ENCLAVES=m
  - Industrial I/O support
  - CONFIG_IIO_BUFFER_DMA=m
  - CONFIG_IIO_BUFFER_DMAENGINE=m
  - CONFIG_ADXRS290=n
  - CONFIG_HDC2010=n
  - CONFIG_AS73211=n
  - Misc drivers
  - CONFIG_MHI_BUS_DEBUG=y
  - CONFIG_INTEL_MEI_VIRTIO=m
  - CONFIG_RTC_DRV_RV3032=m
  - CONFIG_LEDS_LP50XX=m
  - CONFIG_SPMI_HISI3670=n
  - CONFIG_MST_IRQ=y
  - OF dependent drivers (i386, ppc64/ppc64le, riscv64)
  - HISI_HIKEY_USB=m
  - DRM_PANEL_MANTIX_MLAF057WE51=n
  - DRM_PANEL_SAMSUNG_S6E63M0_SPI=n
  - DRM_PANEL_SAMSUNG_S6E63M0_DSI=n
  - DRM_LONTIUM_LT9611=n
  - DRM_TOSHIBA_TC358762=n
  - DRM_TOSHIBA_TC358775=n
  - DRM_CDNS_MHDP8546=n
  - MFD_HI6421_SPMI=m
  - REGULATOR_HI6421V600=m
  - i386
  - DRM_PANEL_SAMSUNG_S6E63M0_SPI=m
  - DRM_PANEL_SAMSUNG_S6E63M0_DSI=m
  - PHY_INTEL_LGM_COMBO=y
  - ppc64 / ppc64le
  - PPC_RTAS_FILTER=y
  - I2C_SLAVE_TESTUNIT=n
  - s390x
  - PCS_XPCS=m
  - VFIO_PCI_ZDEV=y
  - ZCRYPT_DEBUG=n
  - DEBUG_WX=n
  - PTDUMP_DEBUGFS=n
  - riscv64
  - EFI=y
  - FIRMWARE_MEMMAP=y
  - GOOGLE_FIRMWARE=n
  - EFI_VARS_PSTORE=m
  - EFI_VARS_PSTORE_DEFAULT_DISABLE=n
  - EFI_BOOTLOADER_CONTROL=m
  - EFI_CAPSULE_LOADER=m
  - EFI_TEST=n
  - RESET_ATTACK_MITIGATION=n
  - EFI_DISABLE_PCI_DMA=n
  - FB_EFI=y
  - MMC_DW=m
  - MMC_DW_PLTFM=m
  - MMC_DW_BLUEFIELD=m
  - MMC_DW_EXYNOS=m
  - MMC_DW_HI3798CV200=m
  - MMC_DW_K3=m
  - MMC_DW_PCI=m
  - RTC_DRV_EFI=m
  - EFIVAR_FS=m
- commit 3c50825
* Sun Oct 25 2020 mkubecek@suse.cz
- kernel-binary.spec.in: pack scripts/module.lds into kernel-$flavor-devel
  Since mainline commit 596b0474d3d9 ("kbuild: preprocess module linker
  script") in 5.10-rc1, scripts/module.lds linker script is needed to build
  out of tree modules. Add it into kernel-$flavor-devel subpackage.
- commit fe37c16
* Fri Oct 23 2020 tiwai@suse.de
- drm/amd/display: Don't invoke kgdb_breakpoint() unconditionally
  (bsc#1177973).
- drm/amd/display: Fix kernel panic by dal_gpio_open() error
  (bsc#1177973).
- commit 3f21462
* Mon Oct 19 2020 tiwai@suse.de
- rpm/split-modules: Avoid errors even if Module.* are not present
- commit 752fbc6
* Sun Oct 18 2020 mkubecek@suse.cz
- series.conf: cleanup
- move to "almost mainline" section:
  patches.suse/coresight-fix-offset-by-one-error-in-counting-ports.patch
- commit 8e0635b
* Sun Oct 18 2020 jslaby@suse.cz
- Refresh
  patches.suse/coresight-fix-offset-by-one-error-in-counting-ports.patch.
  Update upstream status.
- commit 7b40cc9
* Sun Oct 18 2020 jslaby@suse.cz
- Linux 5.9.1 (bsc#1012628).
- Bluetooth: MGMT: Fix not checking if BT_HS is enabled
  (bsc#1012628).
- media: usbtv: Fix refcounting mixup (bsc#1012628).
- USB: serial: option: add Cellient MPL200 card (bsc#1012628).
- USB: serial: option: Add Telit FT980-KS composition
  (bsc#1012628).
- staging: comedi: check validity of wMaxPacketSize of usb
  endpoints found (bsc#1012628).
- USB: serial: pl2303: add device-id for HP GC device
  (bsc#1012628).
- USB: serial: ftdi_sio: add support for FreeCalypso JTAG+UART
  adapters (bsc#1012628).
- vt_ioctl: make VT_RESIZEX behave like VT_RESIZE (bsc#1012628).
- reiserfs: Initialize inode keys properly (bsc#1012628).
- reiserfs: Fix oops during mount (bsc#1012628).
- Revert "drm/amdgpu: Fix NULL dereference in dpm sysfs handlers"
  (bsc#1012628).
- crypto: bcm - Verify GCM/CCM key length in setkey (bsc#1012628).
- crypto: qat - check cipher length for aead AES-CBC-HMAC-SHA
  (bsc#1012628).
- commit b7f511b
* Fri Oct 16 2020 mkubecek@suse.cz
- update patches metadata
- update upstream references:
  patches.suse/Bluetooth-A2MP-Fix-not-initializing-all-members.patch
  patches.suse/Bluetooth-L2CAP-Fix-calling-sk_filter-on-non-socket-.patch
- commit b1f22f7
* Thu Oct 15 2020 jslaby@suse.cz
- x86/unwind/orc: Fix inactive tasks with stack pointer in %%sp
  on GCC 10 compiled kernels (bsc#1176907).
- commit f522fd5
* Thu Oct 15 2020 jslaby@suse.cz
- Bluetooth: L2CAP: Fix calling sk_filter on non-socket based
  channel (bsc#1177724 CVE-2020-12351).
- commit a96bf01
* Thu Oct 15 2020 tiwai@suse.de
- Bluetooth: A2MP: Fix not initializing all members
  (CVE-2020-12352 bsc#1177725).
- commit 74ef4a4
* Wed Oct 14 2020 tiwai@suse.de
- Update config files: CONFIG_PINCTRL_AMD=y for fixing dependency (bsc#1177049)
- commit 233d0fc
* Tue Oct 13 2020 tiwai@suse.de
- Add the support for kernel-FLAVOR-optional subpackage (jsc#SLE-11796)
  This change allows to create kernel-*-optional subpackage containing
  the modules that are not shipped on SLE but only on Leap.  Those
  modules are marked in the new "-!optional" marker in supported.conf.
  Flip split_optional definition in kernel-binaries.spec.in for the
  branch that needs the splitting.
- commit 1fa25f8
* Mon Oct 12 2020 mkubecek@suse.cz
- Update to 5.9 final
- eliminated 1 patch
  - patches.suse/bpf-Fix-unresolved-symbol-build-error-with-resolve_b.patch
- update configs
  - MLX5_VDPA=y, MLX5_VDPA_NET=m
  - restore FB_ARMCLCD (y on armv6hl and armv7hl, n on arm64)
- commit 11733e1
* Fri Oct  9 2020 mkubecek@suse.cz
- config: disable DEBUG_INFO_BTF in s390x/zfcpdump
  Even if the build has been fixed, there is little use for BTF debug
  information in kernel-zfcpdump so disable it there.
- commit e7595e7
* Thu Oct  8 2020 msuchanek@suse.de
- kernel-binary.spec.in: Exclude .config.old from kernel-devel
  - use tar excludes for .kernel-binary.spec.buildenv
- commit 939a79b
* Wed Oct  7 2020 msuchanek@suse.de
- kernel-binary.spec.in: Package the obj_install_dir as explicit filelist.
- commit 5587762
* Mon Oct  5 2020 afaerber@suse.com
- rpm/mkspec-dtb: Update for 5.9
  arch/arm64/boot/dts/al subdir has been renamed to amazon.
- commit e450c4d
* Mon Oct  5 2020 afaerber@suse.com
- config: armv7hl: Update to 5.9-rc8
- commit 2a6c374
* Mon Oct  5 2020 afaerber@suse.com
- config: armv6hl: Update to 5.9-rc8
- commit 52c5e56
* Mon Oct  5 2020 afaerber@suse.com
- config: arm64: Update to 5.9-rc8
- commit bbcb0ce
* Mon Oct  5 2020 mkubecek@suse.cz
- Update to 5.9-rc8
- commit f75a311
* Sun Oct  4 2020 mkubecek@suse.cz
- bpf: Fix "unresolved symbol" build error with resolve_btfids
  (http://lkml.kernel.org/r/20200929101737.3ufw36bngkmzppqk@lion.mk-sys.cz).
  Fixes s390x/zfcpdump build failure.
- commit c27d6ab
* Fri Oct  2 2020 mkubecek@suse.cz
- config: disable SECURITY_SELINUX_DISABLE also in arm*/* (bsc#1176923)
  The arm configs (both 64-bit and 32-bit) are currently disabled so that
  they cannot be updated the usual way. Apply the changes manually.
- commit a1b15af
* Fri Oct  2 2020 mkubecek@suse.cz
- config: disable SECURITY_SELINUX_DISABLE (bsc#1176923)
- commit 9702a5f
* Wed Sep 30 2020 ohering@suse.de
- rpm/constraints.in: recognize also kernel-source-azure (bsc#1176732)
- commit 7214bbe
* Mon Sep 28 2020 mkubecek@suse.cz
- Update to 5.9-rc7
- eliminated 1 patch
  - patches.suse/dax-Fix-compilation-for-CONFIG_DAX-CONFIG_FS_DAX.patch
- commit a5f5f07
* Tue Sep 22 2020 msuchanek@suse.de
- kernel-syms.spec.in: Also use bz compression (boo#1175882).
- commit ecaf78d
* Tue Sep 22 2020 mkubecek@suse.cz
- dax: Fix compilation for CONFIG_DAX && !CONFIG_FS_DAX
  (http://lkml.kernel.org/r/20200921010359.GO3027113@arch-chirva.localdomain).
- commit 289d4e9
* Mon Sep 21 2020 tiwai@suse.de
- Update config files: turn off CONFIG_SND_CTL_VALIDATION again (bsc#1176200)
  This causes errors on ASoC SOF driver.
- commit 4985410
* Mon Sep 21 2020 mkubecek@suse.cz
- Update to 5.9-rc6
- refresh configs
  - drop VGACON_SOFT_SCROLLBACK and related
- commit bf46e69
* Mon Sep 21 2020 glin@suse.com
- rpm/kernel-cert-subpackage: add CA check on key enrollment (bsc#1173115)
  To avoid the unnecessary key enrollment, when enrolling the signing key
  of the kernel package, "--ca-check" is added to mokutil so that mokutil
  will ignore the request if the CA of the signing key already exists in
  MokList or UEFI db.
  Since the macro, %%_suse_kernel_module_subpackage, is only defined in a
  kernel module package (KMP), it's used to determine whether the %%post
  script is running in a kernel package, or a kernel module package.
- commit b15c9bf
* Fri Sep 18 2020 glin@suse.com
- rpm/macros.kernel-source: pass -c proerly in kernel module package (bsc#1176698)
  The "-c" option wasn't passed down to %%_kernel_module_package so the
  ueficert subpackage wasn't generated even if the certificate is
  specified in the spec file.
- commit 34808fb
* Mon Sep 14 2020 mkubecek@suse.cz
- Update to 5.9-rc5
- eliminated 2 patches
  patches.suse/drm-virtio-fix-unblank.patch
  patches.suse/firmware_loader-fix-memory-leak-for-paged-buffer.patch
- commit e921ea1
* Tue Sep  8 2020 mbenes@suse.cz
- rpm/kernel-binary.spec.in: pack .ipa-clones files for live patching
  When -fdump-ipa-clones option is enabled, GCC reports about its cloning
  operation during IPA optimizations. We use the information for live
  patches preparation, because it is crucial to know if and how functions
  are optimized.
  Currently, we create the needed .ipa-clones dump files manually. It is
  unnecessary, because the files may be created automatically during our
  kernel build. Prepare for the step and provide the resulting files in
  - livepatch-devel package.
- commit 98e5a9d
* Mon Sep  7 2020 msuchanek@suse.de
- rpm/kernel-source.spec.in: Also use bz compression (boo#1175882).
- commit 375ec84
* Mon Sep  7 2020 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Also sign ppc64 kernels (jsc#SLE-15857
  jsc#SLE-13618).
- commit 971fc3d
* Mon Sep  7 2020 yousaf.kaukab@suse.com
- coresight: fix offset by one error in counting ports
  (bsc#1175054).
- commit 1169fee
* Mon Sep  7 2020 tiwai@suse.de
- Update config files: add CONFIG_GCOV_KENREL=n
  Define this explicitly as kbuild bot still uses gcc9 for testing
- commit 0dcb9bb
* Mon Sep  7 2020 tiwai@suse.de
- Update config files: enable a few missing Intel SOF and SST ASoC entries (bsc#1176200)
- commit 074fdcf
* Mon Sep  7 2020 mkubecek@suse.cz
- Update to 5.9-rc4
- eliminated 1 patch
  - patches.suse/net-packet-fix-overflow-in-tpacket_rcv.patch
- update configs
  - new config option:
  - XEN_UNPOPULATED_ALLOC=y (x86_64 only)
- commit 2817e6d
* Fri Sep  4 2020 mkubecek@suse.cz
- net/packet: fix overflow in tpacket_rcv (CVE-2020-14386
  bsc#1176069).
- commit 2fb5c5e
* Mon Aug 31 2020 mkubecek@suse.cz
- Update to 5.9-rc3
- eliminated 1 patch
  - patches.suse/Revert-HID-usbhid-do-not-sleep-when-opening-device.patch
- update configs
  - new config option:
  - PPC_PROT_SAO_LPAR=n (ppc64 and ppc64le)
- commit 3cc13d8
* Sun Aug 30 2020 mkubecek@suse.cz
- series.conf: whitespace cleanup
- commit efc1fed
* Fri Aug 28 2020 msuchanek@suse.de
- obsolete_kmp: provide newer version than the obsoleted one
  (boo#1170232).
- commit c5ecb27
* Fri Aug 28 2020 tiwai@suse.de
- fs/cachefiles: Drop superfluous readpages aops NULL check
  (bsc#1175245).
- commit e4cd10b
* Thu Aug 27 2020 mkubecek@suse.cz
- Update upstream reference:
  patches.suse/Revert-HID-usbhid-do-not-sleep-when-opening-device.patch.
- commit 993f7ee
* Wed Aug 26 2020 alnovak@suse.cz
- Mark the kernel properly released.
  There perhaps was a typo, when SUSE_KERNEL_RELEASED missed the trailing
  "D" - this leads to our kernels being marked as "Unreleased kernel".
  SUSE_KERNEL_RELEASED is defined in rpm/kernel-binary.spec.in.
  To fix that, it should be enough to switch from SUSE_KERNEL_RELEASE to
  SUSE_KERNEL_RELEASED.
- commit 4daffd2
* Mon Aug 24 2020 mkubecek@suse.cz
- Revert "HID: usbhid: do not sleep when opening device".
- commit 4229f31
* Mon Aug 24 2020 wqu@suse.com
- Refresh
  patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch.
- commit 31073f8
* Mon Aug 24 2020 mkubecek@suse.cz
- Update to 5.9-rc2
- eliminated 1 patch
  - patches.suse/squashfs-avoid-bio_alloc-failure-with-1Mbyte-blocks.patch
- refresh configs
- commit 7bec2d7
* Sun Aug 23 2020 mkubecek@suse.cz
- series.conf: cleanup
  Move an "almost mainline" patch to "almost mainline" section.
- commit 4e4b6b0
* Thu Aug 20 2020 jslaby@suse.cz
- drm/virtio: fix unblank (make virtio gpu work again).
- commit 42af09b
* Wed Aug 19 2020 nstange@suse.de
- rpm/kernel-binary.spec.in: restrict livepatch metapackage to default flavor
  It has been reported that the kernel-*-livepatch metapackage got
  erroneously enabled for SLE15-SP3's new -preempt flavor, leading to a
  unresolvable dependency to a non-existing kernel-livepatch-x.y.z-preempt
  package.
  As SLE12 and SLE12-SP1 have run out of livepatching support, the need to
  build said metapackage for the -xen flavor is gone and the only remaining
  flavor for which they're still wanted is -default.
  Restrict the build of the kernel-*-livepatch metapackage to the -default
  flavor.
- commit 58949f3
* Wed Aug 19 2020 tiwai@suse.de
- squashfs: avoid bio_alloc() failure with 1Mbyte blocks
  (bsc#1175308).
- commit 8f3c2bf
* Tue Aug 18 2020 mkubecek@suse.cz
- config: restore PHYLIB=m in */vanilla
  As the PHYLIB/ETHTOOL_NETLINK dependency fix is now in 5.9-rc1 tarball,
  we can apply the changes from commit 4756d9edf730 ("config: restore
  PHYLIB=m") also to vanilla configs.
- commit 4d4447f
* Tue Aug 18 2020 mkubecek@suse.cz
- Update to 5.9-rc1
- eliminated 50 patches (39 stable, 11 other)
- disable ARM architectures (need config update)
- disable (needs update)
  - patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
- refresh
  - patches.rpmify/Add-ksym-provides-tool.patch
  - patches.suse/acpi_thermal_passive_blacklist.patch
  - patches.suse/add-product-identifying-information-to-vmcoreinfo.patch
  - patches.suse/apparmor-compatibility-with-v2.x-net.patch
  - patches.suse/b43-missing-firmware-info.patch
  - patches.suse/dm-mpath-no-partitions-feature
  - patches.suse/vfs-add-super_operations-get_inode_dev
- new config options:
  - General setup
  - KERNEL_ZSTD=n
  - RD_ZSTD=y
  - File systems
  - FS_ENCRYPTION_INLINE_CRYPT=y
  - TMPFS_INODE64=y
  - Kernel hacking
  - DEBUG_FORCE_FUNCTION_ALIGN_32B=n
  - DEBUG_FS_ALLOW_ALL=y
  - DEBUG_FS_DISALLOW_MOUNT=n
  - DEBUG_FS_ALLOW_NONE=n
  - RCU_REF_SCALE_TEST=n
  - TEST_FPU=n
  - PCI support
  - PCI_J721E_HOST=n
  - PCI_J721E_EP=n
  - Storage
  - NVME_TARGET_PASSTHRU=n
  - SCSI_UFS_CRYPTO=y
  - BCACHE_ASYNC_REGISTRATION=y
  - Network device support
  - MLX5_IPSEC=y
  - MT7663S=m
  - WLAN_VENDOR_MICROCHIP=y
  - RTW88_8821CE=m
  - Character devices
  - HW_RANDOM_BA431=m
  - SERIAL_IMX_EARLYCON=n
  - Power management
  - CHARGER_BQ2515X=m
  - SENSORS_CORSAIR_CPRO=m
  - THERMAL_NETLINK=y
  - REGULATOR_PCA9450=m
  - REGULATOR_QCOM_USB_VBUS=m
  - REGULATOR_QCOM_LABIBB=m
  - REGULATOR_FAN53880=m
  - REGULATOR_SY8827N=m
  - Multimedia support
  - VIDEO_RDACM20=m
  - VIDEO_DW9768=m
  - VIDEO_MAX9286=m
  - Graphics support
  - DRM_AMD_DC_DCN3_0=y
  - NOUVEAU_DEBUG_PUSH=n
  - DRM_PANEL_SITRONIX_ST7703=n
  - Sound card support
  - SND_HDA_INTEL_HDMI_SILENT_STREAM=y
  - SND_SOC_MAX98373_SDW=m
  - USB support
  - USB_OTG_PRODUCTLIST=n
  - USB_OTG_DISABLE_EXTERNAL_HUB=n
  - X86 Platform Specific Device Drivers
  - INTEL_ATOMISP2_LED=m
  - Industrial I/O support
  - SCD30_CORE=n
  - INV_ICM42600_I2C=n
  - INV_ICM42600_SPI=n
  - Misc drivers
  - SPI_LANTIQ_SSC=n
  - PINCTRL_EMMITSBURG=m
  - GPIO_PCA9570=m
  - IR_TOY=m
  - CEC_CH7322=m
  - LEDS_CLASS_MULTICOLOR=m
  - XILINX_ZYNQMP_DPDMA=m
  - MLX5_VDPA=n
  - CLK_HSDK=n
  - i386
  - REGULATOR_CROS_EC=m
  - ppc
  - PPC_QUEUED_SPINLOCKS=y
  - s390x
  - BPF_KPROBE_OVERRIDE=n
  - FAIL_FUNCTION=n
  - riscv64
  - NO_HZ_IDLE=y
  - VIRT_CPU_ACCOUNTING_GEN=y
  - JUMP_LABEL=y
  - STATIC_KEYS_SELFTEST=n
  - STACKPROTECTOR=y
  - STACKPROTECTOR_STRONG=y
  - SND_SOC_MAX98373_I2C=m
  - DEBUG_KMEMLEAK=n
  - DEBUG_VM_PGTABLE=n
  - PROVE_LOCKING=n
  - LOCK_STAT=n
  - DEBUG_WW_MUTEX_SLOWPATH=n
  - DEBUG_LOCK_ALLOC=n
  - KCOV=n
  - CONTEXT_TRACKING_FORCE=n
- commit 6a30651
* Mon Aug 17 2020 tiwai@suse.de
- firmware_loader: fix memory leak for paged buffer (bsc#1175367).
- commit 996bcd6
* Fri Aug 14 2020 jslaby@suse.cz
- r8169: add support for RTL8125B (bsc#1174875).
- r8169: rename RTL8125 to RTL8125A (bsc#1174875).
- commit d6761b2
* Wed Aug 12 2020 duwe@suse.de
- rpm/modules.fips:
  * add ecdh_generic (boo#1173813)
- commit 42f38df
* Wed Aug 12 2020 jslaby@suse.cz
- Update config files (bsc#1174058).
  Enable GENERIC_IRQ_DEBUGFS.
  This (automatically) sets GENERIC_IRQ_INJECTION=y on some platforms and
  aligns them with x86.
- commit 7e5ee01
* Wed Aug 12 2020 jslaby@suse.cz
- Linux 5.8.1 (bnc#1012628).
- scsi: ufs: Fix and simplify setup_xfer_req variant operation
  (bnc#1012628).
- USB: serial: qcserial: add EM7305 QDL product ID (bnc#1012628).
- USB: iowarrior: fix up report size handling for some devices
  (bnc#1012628).
- usb: xhci: define IDs for various ASMedia host controllers
  (bnc#1012628).
- usb: xhci: Fix ASMedia ASM1142 DMA addressing (bnc#1012628).
- Revert "ALSA: hda: call runtime_allow() for all hda controllers"
  (bnc#1012628).
- ALSA: hda/realtek: Add alc269/alc662 pin-tables for Loongson-3
  laptops (bnc#1012628).
- ALSA: hda/ca0132 - Add new quirk ID for Recon3D (bnc#1012628).
- ALSA: hda/ca0132 - Fix ZxR Headphone gain control get value
  (bnc#1012628).
- ALSA: hda/ca0132 - Fix AE-5 microphone selection commands
  (bnc#1012628).
- ALSA: seq: oss: Serialize ioctls (bnc#1012628).
- staging: android: ashmem: Fix lockdep warning for write
  operation (bnc#1012628).
- staging: rtl8712: handle firmware load failure (bnc#1012628).
- Staging: rtl8188eu: rtw_mlme: Fix uninitialized variable
  authmode (bnc#1012628).
- Bluetooth: Fix slab-out-of-bounds read in
  hci_extended_inquiry_result_evt() (bnc#1012628).
- Bluetooth: Prevent out-of-bounds read in
  hci_inquiry_result_evt() (bnc#1012628).
- Bluetooth: Prevent out-of-bounds read in
  hci_inquiry_result_with_rssi_evt() (bnc#1012628).
- omapfb: dss: Fix max fclk divider for omap36xx (bnc#1012628).
- binder: Prevent context manager from incrementing ref 0
  (bnc#1012628).
- Smack: fix use-after-free in smk_write_relabel_self()
  (bnc#1012628).
- scripts: add dummy report mode to add_namespace.cocci
  (bnc#1012628).
- lkdtm/heap: Avoid edge and middle of slabs (bnc#1012628).
- mtd: properly check all write ioctls for permissions
  (bnc#1012628).
- leds: wm831x-status: fix use-after-free on unbind (bnc#1012628).
- leds: lm36274: fix use-after-free on unbind (bnc#1012628).
- leds: da903x: fix use-after-free on unbind (bnc#1012628).
- leds: lm3533: fix use-after-free on unbind (bnc#1012628).
- leds: 88pm860x: fix use-after-free on unbind (bnc#1012628).
- gpio: max77620: Fix missing release of interrupt (bnc#1012628).
- xattr: break delegations in {set,remove}xattr (bnc#1012628).
- Revert "powerpc/kasan: Fix shadow pages allocation failure"
  (bnc#1012628).
- powerpc/kasan: Fix shadow pages allocation failure
  (bnc#1012628).
- PCI: tegra: Revert tegra124 raw_violation_fixup (bnc#1012628).
- ima: move APPRAISE_BOOTPARAM dependency on ARCH_POLICY to
  runtime (bnc#1012628).
- random32: move the pseudo-random 32-bit definitions to prandom.h
  (bnc#1012628).
- random: random.h should include archrandom.h, not the other
  way around (bnc#1012628).
- arm64: kaslr: Use standard early random function (bnc#1012628).
- commit 7303946
* Mon Aug 10 2020 tiwai@suse.de
- ALSA: usb-audio: fix overeager device match for MacroSilicon
  MS2109 (bsc#1174625).
- commit e0b3a44
* Sun Aug  9 2020 mkubecek@suse.cz
- config: refresh
- only headers update (gcc 10.1.1 -> 10.2.1)
- commit 2efb7ba
* Tue Aug  4 2020 nsaenzjulienne@suse.de
- clk: bcm2835: Do not use prediv with bcm2711's PLLs
  (bsc#1174865).
- commit bb9b402
* Mon Aug  3 2020 afaerber@suse.com
- config: armv7hl: Update to 5.8
- commit ede84e7
* Mon Aug  3 2020 afaerber@suse.com
- config: armv6hl: Update to 5.8
- commit ecdaa95
* Mon Aug  3 2020 schwab@suse.de
- config: refresh riscv64/default
- commit d1aeef8
* Mon Aug  3 2020 jslaby@suse.cz
- Fix for missing check in vgacon scrollback handling (bsc#1174205
  CVE-2020-14331).
  Update to the latest findings/submission.
- commit e91a540
* Mon Aug  3 2020 mkubecek@suse.cz
- Update to 5.8 final
- refresh configs (headers only)
- commit c02ba5f
* Tue Jul 28 2020 acho@suse.com
- Bluetooth: Disconnect if E0 is used for Level 4 (bsc#1171988
  CVE-2020-10135).
- commit 86181ec
* Tue Jul 28 2020 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: Enable overlayfs
  Overlayfs is needed for podman or docker builds when no more specific
  driver can be used (like lvm or btrfs). As the default build fs is ext4
  currently, we need overlayfs kernel modules to be available.
- commit 29474aa
* Tue Jul 28 2020 jslaby@suse.cz
- vgacon: fix out of bounds write to the scrollback buffer
  (bsc#1174205 CVE-2020-14331).
- commit e8f8dc4
* Mon Jul 27 2020 mkubecek@suse.cz
- Update to 5.8-rc7
- eliminated 2 patches
- commit 786d3ff
* Tue Jul 21 2020 mkubecek@suse.cz
- sched: Fix race against ptrace_freeze_trace() (bsc#1174345).
- commit 007dcf0
* Mon Jul 20 2020 mkubecek@suse.cz
- Update to 5.8-rc6
- eliminated 2 patches
- refresh config files
- commit 25ae237
* Fri Jul 17 2020 mkubecek@suse.cz
- config: restore PHYLIB=m
  This essentially reverts kernel-source commit fcc47b444be6 ("config:
  enable PHYLIB=y and ETHTOOL_NETLINK=y") which responded to upstream
  change not allowing ETHTOOL_NETLINK=y with PHYLIB=m. There are two
  exceptions:
  - vanilla flavors keep PHYLIB=y as patches fixing the dependency are
    not applied to */vanilla (will be fixed with 5.9-rc1 update)
  - we preserve ETHTOOL_NETLINK=y which was previously lost in 5.8-rc1
    update
- commit 4756d9e
* Fri Jul 17 2020 mkubecek@suse.cz
- net: ethtool: Remove PHYLIB direct dependency
  (http://lkml.kernel.org/r/0353ce74-ffc6-4d40-bf0f-d2a7ad640b30@gmail.com).
- net: phy: Register ethtool PHY operations
  (http://lkml.kernel.org/r/0353ce74-ffc6-4d40-bf0f-d2a7ad640b30@gmail.com).
- net: ethtool: Introduce ethtool_phy_ops
  (http://lkml.kernel.org/r/0353ce74-ffc6-4d40-bf0f-d2a7ad640b30@gmail.com).
- commit bcc2825
* Fri Jul 17 2020 mkubecek@suse.cz
- bpf: Use dedicated bpf_trace_printk event instead of
  trace_printk().
- commit a2c9fc2
* Wed Jul 15 2020 mbrugger@suse.com
- brcmfmac: Transform compatible string for FW loading
  (bsc#1169771).
- commit 0f57628
* Tue Jul 14 2020 afaerber@suse.com
- config: arm64: Update to 5.8-rc5
- commit b4e494e
* Mon Jul 13 2020 mkubecek@suse.cz
- Update to 5.8-rc5
- refresh riscv64 configs
- commit 9f5e5ef
* Fri Jul 10 2020 mkubecek@suse.cz
- sched: Fix loadavg accounting race
  (http://lkml.kernel.org/r/20200702171548.GA11813@codemonkey.org.uk).
- commit 2cd7849
* Mon Jul  6 2020 mkubecek@suse.cz
- x86/entry/32: Fix XEN_PV build dependency
  (https://lkml.kernel.org/r/20200706084155.ndltt24ipognh67e@lion.mk-sys.cz).
- commit 006adcb
* Mon Jul  6 2020 mkubecek@suse.cz
- Update to 5.8-rc4
- eliminated 1 patch
- refresh
  patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch
- commit 6584126
* Thu Jul  2 2020 mkubecek@suse.cz
- rpm/kernel-binary.spec.in: do not run klp-symbols for configs with no modules
  Starting with 5.8-rc1, s390x/zfcpdump builds fail because rpm/klp-symbols
  script does not find .tmp_versions directory. This is missing because
  s390x/zfcpdump is built without modules (CONFIG_MODULES disabled).
  As livepatching cannot work without modules, the cleanest solution is
  setting %%klp_symbols to 0 if CONFIG_MODULES is disabled. (We cannot simply
  add another condition to the place where %%klp_symbols is set as it can be
  already set to 1 from prjconf.)
- commit a048c4b
* Thu Jul  2 2020 mkubecek@suse.cz
- Revert "rpm/kernel-binary.spec.in: do not run klp-symbols for configs with no modules"
  This reverts commit b5e55f7584b89b6e17d91451bc47c5c0f732e730.
  This approach doesn't work correctly if %%klp_symbols is set to 1 in
  prjconf and correct solution is simpler.
- commit 708b64e
* Thu Jul  2 2020 mkubecek@suse.cz
- config: refresh riscv64/default
- commit 6b56aca
* Wed Jul  1 2020 rgoldwyn@suse.com
- Re-enable F2FS (boo#1173546)
  Since the changes of blacklisting landed)boo#1109665), we can re-enable
  F2FS for opensuse kernels. For SLE, it will land in
  kernel-default-extra
- commit 33443b2
* Wed Jul  1 2020 mkubecek@suse.cz
- Update
  patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch.
- we faked also CC_CAN_LINK_STATIC temporarily to work around the
  bpfilter_umh build breakage but that is no longer needed so we no longer
  need to pretend we can do static linkage on build
- refresh config files to reflect the change
- commit c06a44f
* Wed Jul  1 2020 mkubecek@suse.cz
- bpfilter: allow to build bpfilter_umh
  as a module without static library
  (http://lkml.kernel.org/r/20200608115628.osizkpo76cgn2ci7@lion.mk-sys.cz).
- Delete
  patches.rpmify/bpfilter-only-build-bpfilter_umh-as-static-when-BPFI.patch.
  Replace temporary version of the build fix with upstream submitted patch.
- commit 75906a0
* Wed Jul  1 2020 mkubecek@suse.cz
- rpm/kernel-binary.spec.in: do not run klp-symbols for configs with no modules
  Starting with 5.8-rc1, s390x/zfcpdump builds fail because rpm/klp-symbols
  script does not find .tmp_versions directory. This is missing because
  s390x/zfcpdump is built without modules (CONFIG_MODULES disabled).
  As livepatching cannot work without modules, the cleanest solution is not
  setting %%klp_symbols if CONFIG_MODULES is disabled. To implement that, we
  need to move the block where %%klp_symbols is defined after the place where
  we set macros for config options.
- commit b5e55f7
* Wed Jul  1 2020 mkubecek@suse.cz
- Revert "fs: Do not check if there is
  a fsnotify watcher on pseudo inodes"
  (http://lkml.kernel.org/r/7b4aa1e985007c6d582fffe5e8435f8153e28e0f.camel@redhat.com).
- commit 45231d0
* Mon Jun 29 2020 mkubecek@suse.cz
- Update to 5.8-rc3
- eliminated 2 patches
- refresh
  patches.suse/suse-hv-guest-os-id.patch
- update configs
  - EFI_CUSTOM_SSDT_OVERLAYS=y
- commit 162848a
* Tue Jun 23 2020 jslaby@suse.cz
- Refresh
  patches.suse/iwl-fix-crash-in-iwl_dbg_tlv_alloc_trigger.patch.
- Refresh
  patches.suse/syscalls-fix-offset-type-of-ksys_ftruncate.patch.
  Update upstream status.
- commit b8c3da5
* Mon Jun 22 2020 mkubecek@suse.cz
- Update to 5.8-rc2
- refresh configs
- commit f76a148
* Thu Jun 18 2020 jeyu@suse.de
- panic: do not print uninitialized taint_flags (bsc#1172814).
- commit ed3a673
* Wed Jun 17 2020 duwe@suse.de
- rpm/modules.fips:
  * add aes-ce-ccm and des3_ede-x86_64 (boo#173030)
  * add aes_ti and aes_neon_bs (boo#1172956)
- commit 08a1655
* Tue Jun 16 2020 jslaby@suse.cz
- efi/tpm: Verify event log header before parsing (bnc#1165773).
- commit 1964d31
* Tue Jun 16 2020 jslaby@suse.cz
- Update
  patches.suse/iwl-fix-crash-in-iwl_dbg_tlv_alloc_trigger.patch
  (bsc#1172905).
  Add a bsc as a reference.
- commit 9706e22
* Mon Jun 15 2020 mkubecek@suse.cz
- config: disable BPFILTER_UMH on i386
  It does not build currently.
- commit 72fbe18
* Mon Jun 15 2020 mkubecek@suse.cz
- config: enable PHYLIB=y and ETHTOOL_NETLINK=y
  As an unfortunate side effect of ethtool cable diagnostic support,
  ETHTOOL_NETLINK now depends on PHYLIB and the dependency is implemented in
  a way making "make oldconfig" drops ETHTOOL_NETLINK if PHYLIB=m.
  Until this issue is resolved in upstream, set PHYLIB=y so that
  ETHTOOL_NETLINK can be enabled again.
- commit fcc47b4
* Mon Jun 15 2020 mkubecek@suse.cz
- rpm: drop execute permissions on source files
  Sometimes a source file with execute permission appears in upstream
  repository and makes it into our kernel-source packages. This is caught by
  OBS build checks and may even result in build failures.
  Sanitize the source tree by removing execute permissions from all C source
  and header files.
- commit 771e293
* Mon Jun 15 2020 mkubecek@suse.cz
- Update to 5.8-rc1
- eliminated 48 patches (40 stable, 8 other)
- disable ARM architectures (need config update)
- refresh
  patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch
  patches.suse/apparmor-compatibility-with-v2.x-net.patch
  patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
  patches.suse/dm-mpath-leastpending-path-update
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  patches.suse/pstore_disable_efi_backend_by_default.patch
  patches.suse/readahead-request-tunables.patch
  patches.suse/supported-flag
  patches.suse/supported-flag-external
  patches.suse/supported-flag-modverdir
  patches.suse/suse-hv-guest-os-id.patch
- fix build with BPFILTER_UMH=m
  patches.rpmify/bpfilter-only-build-bpfilter_umh-as-static-when-BPFI.patch
- new config options:
  - General setup
  - CONFIG_DEFAULT_INIT=""
  - CONFIG_WATCH_QUEUE=y
  - Power management and ACPI options
  - CONFIG_HIBERNATION_SNAPSHOT_DEV=y
  - Enable the block layer
  - CONFIG_BLK_INLINE_ENCRYPTION=y
  - CONFIG_BLK_INLINE_ENCRYPTION_FALLBACK=y
  - CONFIG_BLK_DEV_RNBD_CLIENT=m
  - CONFIG_BLK_DEV_RNBD_SERVER=m
  - Memory Management options
  - CONFIG_ZSMALLOC_PGTABLE_MAPPING=n
  - Networking support
  - CONFIG_INET6_ESPINTCP=y
  - CONFIG_BRIDGE_MRP=y
  - CONFIG_NET_ACT_GATE=m
  - CONFIG_QRTR=m
  - CONFIG_QRTR_SMD=m
  - CONFIG_QRTR_TUN=m
  - CONFIG_QRTR_MHI=m
  - CONFIG_BT_MSFTEXT=n
  - File systems
  - CONFIG_PSTORE_BLK=m
  - Library routines
  - CONFIG_PRIME_NUMBERS=n
  - CONFIG_DEBUG_INFO_COMPRESSED=n
  - CONFIG_DEBUG_VM_PGTABLE=n
  - CONFIG_HIST_TRIGGERS_DEBUG=n
  - CONFIG_TEST_BITOPS=n
  - CONFIG_TEST_HMM=n
  - Multiple devices driver support (RAID and LVM)
  - CONFIG_BCACHE_ASYNC_REGISTRAION=n
  - CONFIG_DM_EBS=m
  - CONFIG_DM_MULTIPATH_HST=m
  - Network device support
  - CONFIG_NET_DSA_SJA1105_VL=y
  - CONFIG_MLX5_CLS_ACT=y
  - CONFIG_BCM54140_PHY=m
  - CONFIG_MT7663U=m
  - CONFIG_MT7915E=m
  - CONFIG_RTW88_8723DE=m
  - Input device support
  - CONFIG_TOUCHSCREEN_CY8CTMA140=m
  - CONFIG_INPUT_IQS269A=m
  - Character devices
  - CONFIG_SERIAL_LANTIQ=m
  - Multifunction device drivers
  - CONFIG_MFD_MP2629=n
  - CONFIG_MFD_INTEL_PMC_BXT=m
  - CONFIG_INTEL_SOC_PMIC_MRFLD=m
  - CONFIG_INTEL_MRFLD_PWRBTN=m
  - CONFIG_EXTCON_INTEL_MRFLD=m
  - CONFIG_INTEL_MRFLD_ADC=n
  - CONFIG_MFD_INTEL_MSIC=n
  - CONFIG_MFD_MT6360=n
  - Multimedia support
  - CONFIG_MEDIA_SUPPORT_FILTER=y
  - CONFIG_MEDIA_PLATFORM_SUPPORT=n
  - CONFIG_MEDIA_TEST_SUPPORT=n
  - CONFIG_VIDEO_OV2740=m
  - CONFIG_INTEL_ATOMISP=y
  - CONFIG_VIDEO_ATOMISP=m
  - CONFIG_VIDEO_ATOMISP_ISP2401=y
  - CONFIG_VIDEO_ATOMISP_OV5693=m
  - CONFIG_VIDEO_ATOMISP_OV2722=m
  - CONFIG_VIDEO_ATOMISP_GC2235=m
  - CONFIG_VIDEO_ATOMISP_MSRLIST_HELPER=m
  - CONFIG_VIDEO_ATOMISP_MT9M114=m
  - CONFIG_VIDEO_ATOMISP_GC0310=m
  - CONFIG_VIDEO_ATOMISP_OV2680=m
  - CONFIG_VIDEO_ATOMISP_LM3554=m
  - CONFIG_CEC_CROS_EC=m
  - CONFIG_CEC_SECO=m
  - CONFIG_CEC_SECO_RC=n
  - Graphics support
  - CONFIG_DRM_I915_FENCE_TIMEOUT=10000
  - Sound card support
  - CONFIG_SND_SOC_AMD_RENOIR=m
  - CONFIG_SND_SOC_AMD_RENOIR_MACH=m
  - CONFIG_SND_SOC_INTEL_SOF_WM8804_MACH=m
  - CONFIG_SND_SOC_INTEL_EHL_RT5660_MACH=m
  - CONFIG_SND_SOC_MAX98390=m
  - CONFIG_SND_SOC_ZL38060=n
  - USB support
  - CONFIG_USB_XHCI_PCI_RENESAS=m
  - InfiniBand support
  - CONFIG_INFINIBAND_RTRS_CLIENT=m
  - CONFIG_INFINIBAND_RTRS_SERVER=m
  - Virtio drivers
  - CONFIG_VIRTIO_MEM=m
  - X86 Platform Specific Device Drivers
  - CONFIG_INTEL_WMI_SBL_FW_UPDATE=m
  - CONFIG_INTEL_SCU_PCI=y
  - CONFIG_INTEL_SCU_PLATFORM=m
  - CONFIG_INTEL_MID_POWER_BUTTON=m
  - CONFIG_INTEL_SCU_IPC_UTIL=m
  - Industrial I/O support
  - CONFIG_AD9467=n
  - CONFIG_ADI_AXI_ADC=n
  - CONFIG_MAX1241=n
  - CONFIG_ATLAS_EZO_SENSOR=n
  - CONFIG_ADIS16475=n
  - CONFIG_SX9310=n
  - CONFIG_VCNL3020=n
  - Misc drivers
  - CONFIG_MTD_NAND_ARASAN=m
  - CONFIG_MTD_PSTORE=m
  - CONFIG_INTERCONNECT=n
  - CONFIG_SPI_AMD=n
  - CONFIG_PINCTRL_JASPERLAKE=m
  - CONFIG_GPIO_PCA953X_IRQ=y
  - CONFIG_GPIO_AGGREGATOR=m
  - CONFIG_BATTERY_CW2015=m
  - CONFIG_CHARGER_BD99954=m
  - CONFIG_SENSORS_AMD_ENERGY=m
  - CONFIG_SENSORS_MAX16601=m
  - ACPI INT340X thermal drivers
  - CONFIG_REGULATOR_MAX77826=m
  - CONFIG_LEDS_SGM3140=m
  - CONFIG_PWM_IQS620A=m
  - i386 / ppc64 / ppc64le
  - MDIO_IPQ4019=m
  - HW_RANDOM_CCTRNG=n
  - MFD_GATEWORKS_GSC=m
  - DRM_PANEL_ASUS_Z00T_TM5P5_NT35596=n
  - DRM_PANEL_LEADTEK_LTK050H3146W=n
  - DRM_PANEL_VISIONOX_RM69299=n
  - DRM_CHRONTEL_CH7033=n
  - DRM_NWL_MIPI_DSI=n
  - LEDS_AW2013=m
  - CLK_LGM_CGU=y
  - PHY_CADENCE_SALVO=m
  - PHY_INTEL_COMBO=y
  - PHY_OCELOT_SERDES=m
  - MTD_PHYSMAP_VERSATILE=y
  - MTD_PHYSMAP_GEMINI=y
  - MDIO_IPQ8064=m
  - SERIAL_8250_ASPEED_VUART=n
  - GPIO_LOGICVC=n
  - GPIO_SAMA5D2_PIOBU=n
  - GPIO_SYSCON=n
  - SENSORS_GSC=m
  - DRM_PANEL_ARM_VERSATILE=n
  - LEDS_SYSCON=y
- commit 8874901
* Fri Jun 12 2020 bp@suse.de
- x86/speculation: PR_SPEC_FORCE_DISABLE enforcement for indirect
  branches (bsc#1172783 CVE-2020-10768).
- commit 3bb02b8
* Fri Jun 12 2020 bp@suse.de
- x86/speculation: Prevent rogue cross-process SSBD shutdown
  (bsc#1172781 CVE-2020-10766).
- commit 765c970
* Fri Jun 12 2020 jslaby@suse.cz
- iwl: fix crash in iwl_dbg_tlv_alloc_trigger (iwlwifi crash).
- commit 6645a57
* Thu Jun 11 2020 bp@suse.de
- x86/speculation: Avoid force-disabling IBPB based on STIBP
  and enhanced IBRS (bsc#1172782 CVE-2020-10767).
- commit 5c5774f
* Thu Jun 11 2020 jslaby@suse.cz
- Linux 5.7.2 (bnc#1012628).
- uprobes: ensure that uprobe->offset and ->ref_ctr_offset are
  properly aligned (bnc#1012628).
- x86/speculation: Add Ivy Bridge to affected list (bnc#1012628).
- x86/speculation: Add SRBDS vulnerability and mitigation
  documentation (bnc#1012628).
- x86/speculation: Add Special Register Buffer Data Sampling
  (SRBDS) mitigation (bnc#1012628).
- x86/cpu: Add 'table' argument to cpu_matches() (bnc#1012628).
- x86/cpu: Add a steppings field to struct x86_cpu_id
  (bnc#1012628).
- nvmem: qfprom: remove incorrect write support (bnc#1012628).
- CDC-ACM: heed quirk also in error handling (bnc#1012628).
- staging: rtl8712: Fix IEEE80211_ADDBA_PARAM_BUF_SIZE_MASK
  (bnc#1012628).
- tty: hvc_console, fix crashes on parallel open/close
  (bnc#1012628).
- vt: keyboard: avoid signed integer overflow in k_ascii
  (bnc#1012628).
- serial: 8250: Enable 16550A variants by default on non-x86
  (bnc#1012628).
- usb: musb: jz4740: Prevent lockup when CONFIG_SMP is set
  (bnc#1012628).
- usb: musb: Fix runtime PM imbalance on error (bnc#1012628).
- usb: musb: start session in resume for host port (bnc#1012628).
- iio: adc: stm32-adc: fix a wrong error message when probing
  interrupts (bnc#1012628).
- iio:chemical:pms7003: Fix timestamp alignment and prevent data
  leak (bnc#1012628).
- iio: vcnl4000: Fix i2c swapped word reading (bnc#1012628).
- iio:chemical:sps30: Fix timestamp alignment (bnc#1012628).
- USB: serial: ch341: fix lockup of devices with limited prescaler
  (bnc#1012628).
- USB: serial: ch341: add basis for quirk detection (bnc#1012628).
- USB: serial: option: add Telit LE910C1-EUX compositions
  (bnc#1012628).
- USB: serial: usb_wwan: do not resubmit rx urb on fatal errors
  (bnc#1012628).
- USB: serial: qcserial: add DW5816e QDL support (bnc#1012628).
- commit 936fe4f
* Wed Jun 10 2020 jslaby@suse.cz
- syscalls: fix offset type of ksys_ftruncate (bsc#1172699).
- commit 8d4977c
* Tue Jun  9 2020 dmueller@suse.com
- armv7/ararch64: Update config files.
  Enable IOMMU_DEFAULT_PASSTHROUGH; per jsc#SLE-5568 this should be on by
  default, like on x86_64.
- commit bb34387
* Mon Jun  8 2020 jslaby@suse.cz
- Refresh
  patches.suse/jbd2-avoid-leaking-transaction-credits-when-unreserv.patch.
  Update upstream status.
- commit c3ae43f
* Mon Jun  8 2020 jslaby@suse.cz
- KVM: x86/mmu: Set mmio_value to '0' if reserved #PF can't be
  generated (bsc#1171904).
- KVM: x86: only do L1TF workaround on affected processors
  (bsc#1171904).
- commit 16721c7
* Mon Jun  8 2020 jslaby@suse.cz
- Linux 5.7.1 (bnc#1012628).
- airo: Fix read overflows sending packets (bnc#1012628).
- net: dsa: mt7530: set CPU port to fallback mode (bnc#1012628).
- media: staging: ipu3-imgu: Move alignment attribute to field
  (bnc#1012628).
- media: Revert "staging: imgu: Address a compiler warning on
  alignment" (bnc#1012628).
- mmc: fix compilation of user API (bnc#1012628).
- kernel/relay.c: handle alloc_percpu returning NULL in relay_open
  (bnc#1012628).
- crypto: api - Fix use-after-free and race in crypto_spawn_alg
  (bnc#1012628).
- mt76: mt76x02u: Add support for newer versions of the XBox
  One wifi adapter (bnc#1012628).
- p54usb: add AirVasT USB stick device-id (bnc#1012628).
- HID: i2c-hid: add Schneider SCL142ALM to descriptor override
  (bnc#1012628).
- HID: multitouch: enable multi-input as a quirk for some devices
  (bnc#1012628).
- HID: sony: Fix for broken buttons on DS3 USB dongles
  (bnc#1012628).
- mm: Fix mremap not considering huge pmd devmap (bnc#1012628).
- media: dvbdev: Fix tuner->demod media controller link
  (bnc#1012628).
- commit cc2f849
* Thu Jun  4 2020 mkubecek@suse.cz
- config: refresh with gcc10
  gcc10 is default in Tumbleweed now.
- commit 0b1e86b
* Wed Jun  3 2020 jslaby@suse.cz
- Revert "Update config files."
  This reverts commit 34be040b91701c047e592935bc2dbb46a3947a56. We now
  have a fix (previous commit) in place, so change the configuration back
  (bsc#1156053).
- commit f4546fe
* Wed Jun  3 2020 jslaby@suse.cz
- usercopy: mark dma-kmalloc caches as usercopy caches
  (bsc#1156053).
- commit d3b5ce7
* Tue Jun  2 2020 jslaby@suse.cz
- jbd2: avoid leaking transaction credits when unreserving handle
  (bnc#1169774).
- commit 8599ef4
* Tue Jun  2 2020 jslaby@suse.cz
- Refresh
  patches.suse/drm-nouveau-Fix-regression-by-audio-component-transition.patch.
  Update upstream status.
- commit 3000ce5
* Mon Jun  1 2020 mkubecek@suse.cz
- config: enable DEBUG_INFO_BTF
  This was disabled when the option was introduced in 5.2-rc1 but it turned
  out there are interesting use cases for having it enabled.
  Add pahole to build time dependencies as it is used to extracth the BTF
  data. Once we figure out how to make it conditional (only if DEBUG_INFO_BTF
  exists and is enabled), it should be done in packaging branch.
- commit 9ddab66
* Mon Jun  1 2020 mkubecek@suse.cz
- Updated to 5.7 final
- refresh configs
- commit 7cd0da5
* Tue May 26 2020 trenn@suse.com
- Update config files.
  Remove ACPI_PROCFS_POWER
  This should all be in sysfs nowadays. If this is in Tumbleweed for a while,
  a patch to totally remove this code will be sent mainline.
  Related to bsc#1160977
- commit 96731f2
* Tue May 26 2020 msuchanek@suse.de
- rpm/kernel-source.spec.in: Add obsolete_rebuilds (boo#1172073).
- commit 6524463
* Mon May 25 2020 mkubecek@suse.cz
- Update to 5.7-rc7
- refresh configs (ARCH_HAS_STRICT_KERNEL_RWX=n on ppc64/ppc64le)
- commit 67f7fb5
* Tue May 19 2020 afaerber@suse.com
- config: armv7hl: Update to 5.7-rc6
- commit 8e7f5b8
* Mon May 18 2020 mkubecek@suse.cz
- Update to 5.7-rc6
- eliminated 2 patches
- refresh configs
- commit 3603fcd
* Sun May 17 2020 afaerber@suse.com
- config: armv6hl: Update to 5.7-rc5
- commit 2a4b8c3
* Thu May 14 2020 msuchanek@suse.de
- rpm/check-for-config-changes: Ignore CONFIG_CC_VERSION_TEXT
- commit 8e6b05f
* Mon May 11 2020 mkubecek@suse.cz
- Update to 5.7-rc5
- refresh configs
- commit 298ea3d
* Thu May  7 2020 afaerber@suse.com
- config: arm64: Update to 5.7-rc4
- commit 47279b9
* Thu May  7 2020 jzerebecki@suse.com
- kernel-docs: Change Requires on python-Sphinx to earlier than version 3
  References: bsc#1166965
  From 3 on the internal API that the build system uses was rewritten in
  an incompatible way.
  See https://github.com/sphinx-doc/sphinx/issues/7421 and
  https://bugzilla.suse.com/show_bug.cgi?id=1166965#c16 for some details.
- commit cf60b5c
* Wed May  6 2020 jslaby@suse.cz
- ipc/util.c: sysvipc_find_ipc() incorrectly updates position
  index (bnc#1171211).
- commit 31ea4f6
* Mon May  4 2020 mkubecek@suse.cz
- Update to 5.7-rc4
- commit 9761f3e
* Thu Apr 30 2020 tiwai@suse.de
- drm/nouveau: Fix regression by audio component transition
  (bsc#1170951).
- commit 779158b
* Wed Apr 29 2020 ykaukab@suse.de
- config: arm64: enable coresight support
  Coresight is already enabled in armv7hl
- commit f6f465c
* Mon Apr 27 2020 mkubecek@suse.cz
- Update to 5.7-rc3
- eliminated 1 patch
- refresh configs
- commit 888b015
* Wed Apr 22 2020 mkubecek@suse.cz
- config.conf: fix order of i386 flavors
  Unlike on other architectures, i386/pae is the basic config and others,
  including i386/default are diffs against it. With i386/default listed
  first, it is also processed first by run_oldconfig.sh so that if there
  is a new config option, it is added to i386/default (as it's not present
  in i386/pae yet) even if the value is going to be the same as in
  i386/pae. To get stable result, one needs to run run_oldconfig.sh twice.
  Swat the two entries so that i386/pae is updated first and i386/default
  is created as a diff against already updated i386/pae.
- commit f047e04
* Tue Apr 21 2020 schwab@suse.de
- config: riscv64: enable left out config options
  Enable some config options to reduce difference with x86 config
- commit ffb4ebb
* Tue Apr 21 2020 mkubecek@suse.cz
- series.conf: cleanup
- fix Patch-mainline and move to more appropriate place:
  patches.suse/s390-export-symbols-for-crash-kmp.patch
- commit d3c6449
* Mon Apr 20 2020 tiwai@suse.de
- Update config files: revert CONFIG_SND_HDA_PREALLOC_SIZE changes (bsc#1169471)
- commit 438882a
* Mon Apr 20 2020 mkubecek@suse.cz
- config: enable PCIE_EDR (bsc#1169263)
  (x86 only)
- commit e781722
* Mon Apr 20 2020 mkubecek@suse.cz
- Update to 5.7-rc2
- eliminated 2 patches
- commit 487485c
* Mon Apr 20 2020 mbrugger@suse.com
- armv7hl: Update config files.
  Build MediaTek watchdog as built-in.
- commit dfe578b
* Wed Apr 15 2020 msuchanek@suse.de
- rpm/check-for-config-changes: Ignore CONFIG_LD_VERSION
- commit e60242e
* Tue Apr 14 2020 schwab@suse.de
- Add config files for riscv64
- commit b85c09e
* Mon Apr 13 2020 mkubecek@suse.cz
- Update to 5.7-rc1
- eliminated 70 patches (66 stable, 4 other)
- disable ARM architectures (need config update)
- refresh
  - patches.suse/supported-flag
  - patches.suse/supported-flag-external
  - patches.suse/supported-flag-modverdir
  - patches.suse/vfs-add-super_operations-get_inode_dev
  - patches.suse/acpi_thinkpad_introduce_acpi_root_table_boot_param.patch
  - patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
- fix s390x build:
  patches.suse/tty-sysrq-Export-sysrq_mask.patch
- new config options:
- General setup
  - CONFIG_SCHED_THERMAL_PRESSURE=y
  - CONFIG_BPF_LSM=y
- Power management and ACPI options
  - CONFIG_ACPI_TINY_POWER_BUTTON=m
  - CONFIG_ACPI_TINY_POWER_BUTTON_SIGNAL=38
- Memory Management options
  - CONFIG_ZSWAP_COMPRESSOR_DEFAULT_LZO=y
  - CONFIG_ZSWAP_ZPOOL_DEFAULT_ZBUD=y
  - CONFIG_ZSWAP_DEFAULT_ON=n
- Networking support
  - CONFIG_IPV6_RPL_LWTUNNEL=y
- File systems
  - CONFIG_EXFAT_FS=m
  - CONFIG_EXFAT_DEFAULT_IOCHARSET="utf8"
- Cryptographic API
  - CONFIG_CHELSIO_TLS_DEVICE=y
- Kernel hacking
  - CONFIG_MAGIC_SYSRQ_SERIAL_SEQUENCE=""
  - CONFIG_TEST_LOCKUP=n
  - CONFIG_TEST_MIN_HEAP=n
- PCI
  - CONFIG_PCIE_EDR=n
- Network device drivers
  - CONFIG_BAREUDP=m
  - CONFIG_MLX5_TC_CT=y
  - CONFIG_DWMAC_INTEL=m
  - CONFIG_MDIO_MVUSB=m
  - CONFIG_BCM84881_PHY=m
  - PHY_CADENCE_TORRENT=m (i386, ppc64(le))
- PTP clock support
  - CONFIG_PTP_1588_CLOCK_IDT82P33=m
  - CONFIG_PTP_1588_CLOCK_VMW=m
- Graphics
  - CONFIG_DRM_I915_MAX_REQUEST_BUSYWAIT=8000
  - CONFIG_TINYDRM_ILI9486=n
  - DRM_PANEL_BOE_TV101WUM_NL6=n
  - DRM_PANEL_ELIDA_KD35T133=n
  - DRM_PANEL_FEIXIN_K101_IM2BA02=n
  - DRM_PANEL_NOVATEK_NT35510=n
  - DRM_PANEL_SAMSUNG_S6E88A0_AMS452EF01=n
  - DRM_DISPLAY_CONNECTOR=n
  - DRM_PARADE_PS8640=n
  - DRM_SIMPLE_BRIDGE=n
  - DRM_TOSHIBA_TC358768=n
  - DRM_TI_TPD12S015=n
- Sound
  - CONFIG_SND_SOC_AMD_RV_RT5682_MACH=m
  - CONFIG_SND_BCM63XX_I2S_WHISTLER=n
  - CONFIG_SND_SOC_INTEL_SOF_PCM512x_MACH=m
  - CONFIG_SND_SOC_SOF_DEBUG_PROBES=n
  - CONFIG_SND_SOC_RT5682_SDW=n
  - CONFIG_SND_SOC_TLV320ADCX140=n
- Input
  - CONFIG_HID_GLORIOUS=m
  - CONFIG_HID_MCP2221=m
  - CONFIG_KEYBOARD_IQS62X=m
- USB
  - CONFIG_APPLE_MFI_FASTCHARGE=m
  - CONFIG_TYPEC_MUX_INTEL_PMC=m
- Virtio drivers
  - CONFIG_VIRTIO_VDPA=m
  - CONFIG_VDPA_MENU=y
  - CONFIG_VDPA_SIM=m
  - CONFIG_IFCVF=m
  - CONFIG_VHOST_MENU=y
  - CONFIG_VHOST_VDPA=m
- Platform drivers
  - CONFIG_SURFACE_3_POWER_OPREGION=m
  - CONFIG_CROS_EC_TYPEC=m
  - CONFIG_CROS_USBPD_NOTIFY=m
- Industrial I/O
  - CONFIG_HMC425=n
  - CONFIG_AD5770R=n
  - CONFIG_AL3010=n
  - CONFIG_GP2AP002=n
  - CONFIG_ICP10100=n
  - CONFIG_IQS621_ALS=n
  - CONFIG_IQS624_POS=n
  - CONFIG_IQS620AT_TEMP=n
- Misc drivers
  - CONFIG_MHI_BUS=m
  - CONFIG_UACCE=m
  - CONFIG_ATA_FORCE=y
  - CONFIG_SERIAL_SPRD=m
  - CONFIG_SPI_MUX=m
  - CONFIG_PINCTRL_DA9062=m
  - CONFIG_SENSORS_AXI_FAN_CONTROL=m
  - CONFIG_MFD_IQS62X=m
  - CONFIG_VIDEO_IMX219=m
  - CONFIG_MMC_HSQ=m
  - CONFIG_DMABUF_MOVE_NOTIFY=n
  - CONFIG_PWM_DEBUG=n
  - CONFIG_MUX_ADG792A=n
  - CONFIG_MUX_ADGS1408=n
  - CONFIG_MUX_GPIO=n
- i386
  - REGULATOR_MP541=m
  - REGULATOR_MP886X=m
- ppc64
  - PMU_SYSFS=y
  - FSL_ENETC=m
  - FSL_ENETC_VF=m
  - FSL_ENETC_PTP_CLOCK=m
  - FSL_ENETC_QOS=y
  - SPI_FSI=m
  - REGULATOR_MP5416=m
  - REGULATOR_MP886X=m
- s390x
  - XILINX_LL_TEMAC=m
  - MDIO_XPCS=m
  - QETH_OSN=y
  - QETH_OSX=y
- commit 84ddad4
* Sun Apr 12 2020 mkubecek@suse.cz
- constrants: fix malformed XML
  Closing tag of an element is "</foo>", not "<foo/>".
  Fixes: 8b37de2eb835 ("rpm/constraints.in: Increase memory for kernel-docs")
- commit 4a8ca28
* Thu Apr  9 2020 jslaby@suse.cz
- efi/x86: Fix the deletion of variables in mixed mode
  (bnc#1167933).
- commit 47f4c16
* Thu Apr  9 2020 jslaby@suse.cz
- efi/x86: Don't remap text<->rodata gap read-only for mixed mode
  (bnc#1168645).
- commit fd9c360
* Thu Apr  9 2020 mgorman@suse.de
- Update config files to disable CONFIG_TRACE_IRQFLAGS (bsc#1169078).
- commit d379575
* Thu Apr  9 2020 msuchanek@suse.de
- rpm/constraints.in: Increase memory for kernel-docs
  References: https://build.opensuse.org/request/show/792664
- commit 8b37de2
* Thu Apr  9 2020 neilb@suse.de
- cachefiles: fix corruption of 'ret' (boo#1168841).
- commit 0a79cdc
* Wed Apr  8 2020 jslaby@suse.cz
- Linux 5.6.3 (bnc#1012628).
- ipv4: fix a RCU-list lock in fib_triestat_seq_show
  (bnc#1012628).
- net: dsa: ksz: Select KSZ protocol tag (bnc#1012628).
- net, ip_tunnel: fix interface lookup with no key (bnc#1012628).
- sctp: fix possibly using a bad saddr with a given dst
  (bnc#1012628).
- sctp: fix refcount bug in sctp_wfree (bnc#1012628).
- net: macb: Fix handling of fixed-link node (bnc#1012628).
- net: fix fraglist segmentation reference count leak
  (bnc#1012628).
- udp: initialize is_flist with 0 in udp_gro_receive
  (bnc#1012628).
- padata: fix uninitialized return value in padata_replace()
  (bnc#1012628).
- brcmfmac: abort and release host after error (bnc#1012628).
- XArray: Fix xa_find_next for large multi-index entries
  (bnc#1012628).
- drm/bridge: analogix-anx6345: Avoid duplicate -supply suffix
  (bnc#1012628).
- misc: rtsx: set correct pcr_ops for rts522A (bnc#1012628).
- misc: pci_endpoint_test: Fix to support > 10 pci-endpoint-test
  devices (bnc#1012628).
- misc: pci_endpoint_test: Avoid using module parameter to
  determine irqtype (bnc#1012628).
- PCI: sysfs: Revert "rescan" file renames (bnc#1012628).
- coresight: do not use the BIT() macro in the UAPI header
  (bnc#1012628).
- mei: me: add cedar fork device ids (bnc#1012628).
- nvmem: release the write-protect pin (bnc#1012628).
- nvmem: check for NULL reg_read and reg_write before
  dereferencing (bnc#1012628).
- nvmem: sprd: Fix the block lock operation (bnc#1012628).
- extcon: axp288: Add wakeup support (bnc#1012628).
- power: supply: axp288_charger: Add special handling for HP
  Pavilion x2 10 (bnc#1012628).
- Revert "ALSA: uapi: Drop asound.h inclusion from asoc.h"
  (bnc#1012628).
- Revert "dm: always call blk_queue_split() in dm_process_bio()"
  (bnc#1012628).
- ALSA: hda/ca0132 - Add Recon3Di quirk to handle integrated
  sound on EVGA X99 Classified motherboard (bnc#1012628).
- soc: mediatek: knows_txdone needs to be set in Mediatek CMDQ
  helper (bnc#1012628).
- perf python: Fix clang detection to strip out options passed
  in $CC (bnc#1012628).
- mm: mempolicy: require at least one nodeid for MPOL_PREFERRED
  (bnc#1012628).
- commit 97c6e99
* Tue Apr  7 2020 msuchanek@suse.de
- s390x: zfcpdump: disable CONFIG_RELOCATABLE (bsc#1168847).
- commit c824449
* Tue Apr  7 2020 mgorman@suse.de
- Update config files to disable CONFIG_UCLAMP_TASK (bsc#1168888).
- commit 025835f
* Mon Apr  6 2020 jslaby@suse.cz
- net/bpfilter: remove superfluous testing message (bnc#1168664).
- commit 7d8cfa8
* Fri Apr  3 2020 msuchanek@suse.de
- Delete patches.rpmify/powerpc-Blacklist-GCC-5.4-6.1-and-6.2.patch.
- commit daf9f5a
* Fri Apr  3 2020 yousaf.kaukab@suse.com
- config: arm64: enable cpufreq driver for Jetson Nano and Jetson TX1
- commit 3187813
* Thu Apr  2 2020 tiwai@suse.de
- drm/i915/display: Fix mode private_flags comparison at
  atomic_check (bsc#1168383).
- commit a83dd8f
* Thu Apr  2 2020 jslaby@suse.cz
- bpf: update jmp32 test cases to fix range bound deduction
  (bnc#1012628).
- serial: sprd: Fix a dereference warning (bnc#1012628).
- vt: selection, introduce vc_is_sel (bnc#1012628).
- vt: ioctl, switch VT_IS_IN_USE and VT_BUSY to inlines
  (bnc#1012628).
- vt: switch vt_dont_switch to bool (bnc#1012628).
- vt: vt_ioctl: remove unnecessary console allocation checks
  (bnc#1012628).
- vt: vt_ioctl: fix VT_DISALLOCATE freeing in-use virtual console
  (bnc#1012628).
- vt: vt_ioctl: fix use-after-free in vt_in_use() (bnc#1012628).
- platform/x86: pmc_atom: Add Lex 2I385SW to critclk_systems
  DMI table (bnc#1012628).
- Linux 5.6.2 (bnc#1012628).
- commit 8dfb75b
* Wed Apr  1 2020 jslaby@suse.cz
- Linux 5.6.1 (bnc#1012628).
- media: v4l2-core: fix a use-after-free bug of sd->devnode
  (bnc#1012628).
- media: xirlink_cit: add missing descriptor sanity checks
  (bnc#1012628).
- media: stv06xx: add missing descriptor sanity checks
  (bnc#1012628).
- media: dib0700: fix rc endpoint lookup (bnc#1012628).
- media: ov519: add missing endpoint sanity checks (bnc#1012628).
- libfs: fix infoleak in simple_attr_read() (bnc#1012628).
- ahci: Add Intel Comet Lake H RAID PCI ID (bnc#1012628).
- staging: wfx: annotate nested gc_list vs tx queue locking
  (bnc#1012628).
- staging: wfx: fix init/remove vs IRQ race (bnc#1012628).
- staging: wfx: add proper "compatible" string (bnc#1012628).
- staging: wlan-ng: fix use-after-free Read in
  hfa384x_usbin_callback (bnc#1012628).
- staging: wlan-ng: fix ODEBUG bug in prism2sta_disconnect_usb
  (bnc#1012628).
- staging: rtl8188eu: Add ASUS USB-N10 Nano B1 to device table
  (bnc#1012628).
- staging: kpc2000: prevent underflow in cpld_reconfigure()
  (bnc#1012628).
- media: usbtv: fix control-message timeouts (bnc#1012628).
- media: flexcop-usb: fix endpoint sanity check (bnc#1012628).
- usb: musb: fix crash with highmen PIO and usbmon (bnc#1012628).
- USB: serial: io_edgeport: fix slab-out-of-bounds read in
  edge_interrupt_callback (bnc#1012628).
- USB: cdc-acm: restore capability check order (bnc#1012628).
- USB: serial: option: add Wistron Neweb D19Q1 (bnc#1012628).
- USB: serial: option: add BroadMobi BM806U (bnc#1012628).
- USB: serial: option: add support for ASKEY WWHC050
  (bnc#1012628).
- bpf: Undo incorrect __reg_bound_offset32 handling (bnc#1012628).
- commit 1675c56
* Wed Apr  1 2020 jslaby@suse.cz
- Refresh
  patches.suse/media-go7007-Fix-URB-type-for-interrupt-handling.patch.
  Update upstream status.
- commit 96043ad
* Wed Apr  1 2020 jslaby@suse.cz
- Refresh
  patches.suse/mac80211-fix-authentication-with-iwlwifi-mvm.patch.
  Update upstream status -- merged.
- commit 26b6c02
* Mon Mar 30 2020 jslaby@suse.cz
- Refresh
  patches.suse/media-go7007-Fix-URB-type-for-interrupt-handling.patch.
  Update upstream status.
- commit 46fab61
* Mon Mar 30 2020 mkubecek@suse.cz
- mac80211: fix authentication with iwlwifi/mvm
  (https://lkml.kernel.org/r/20200329.212136.273575061630425724.davem@davemloft.net).
- commit 5032681
* Mon Mar 30 2020 mkubecek@suse.cz
- Revert "sign also s390x kernel images (bsc#1163524)"
  This reverts commit b38b61155f0a2c3ebca06d4bb0c2e11a19a87f1f.
  The pesign-obs-integration changes needed for s390x image signing are
  still missing in Factory so that this change breaks s390x builds.
- commit 9544af9
* Mon Mar 30 2020 mkubecek@suse.cz
- Update to 5.6 final
- refresh configs
- commit da616f7
* Mon Mar 23 2020 mkubecek@suse.cz
- Update to 5.6-rc7
- refresh
  patches.suse/supported-flag
- refresh config files:
  - CC_HAS_INT128=n on 32-bit architectures (was =y on i386)
- commit 0801cd7
* Thu Mar 19 2020 yousaf.kaukab@suse.com
- config: arm64: enable CONFIG_MTD_PHYSMAP_OF
  Get rid of CONFIG_MTD_PHYSMAP_COMPAT and enable CONFIG_MTD_PHYSMAP_OF.
  Compat maps of zero length (CONFIG_MTD_PHYSMAP_LEN=0x0) doesn't make
  sense and driver initialization is bound to fail. So use device-tree
  based initialization.
- commit 2205109
* Mon Mar 16 2020 mkubecek@suse.cz
- Update to 5.6-rc6
- refresh config files
- commit 5c2f002
* Fri Mar 13 2020 nsaenzjulienne@suse.de
- mmc: sdhci: iproc: Add custom set_power() callback for bcm2711
  (bsc#1165954).
- mmc: sdhci: Introduce sdhci_set_power_and_bus_voltage()
  (bsc#1165954).
- commit 43f25fe
* Fri Mar 13 2020 nsaenzjulienne@suse.de
- Delete patches.suse/linux-log2-h-add-roundup-rounddown_pow_two64-family-of-functions.patch.
  The patch was initially introduced to support RPi4's PCIe controller.
  The now available upstream driver isn't using this roundup
  functionality.
- commit ea370a5
* Thu Mar 12 2020 tiwai@suse.de
- Update config files: disable CONFIG_OABI_COMPAT for 32bit Arm (bsc#1165462)
  It enables CONFIG_SECCOMP_FILTER.
- commit e9e55d0
* Thu Mar 12 2020 tiwai@suse.de
- Update config files: enable CONFIG_EROFS_FS_ZIP=y
  Requested for supporting EROFS compressed files:
  https://lists.opensuse.org/opensuse-kernel/2020-02/msg00007.html
- commit 37ad336
* Mon Mar  9 2020 jeyu@suse.de
- rpm/kabi.pl: account for namespace field being moved last
  Upstream is moving the namespace field in Module.symvers last in order to
  preserve backwards compatibility with kmod tools (depmod, etc). Fix the kabi.pl
  script to expect the namespace field last. Since split() ignores trailing empty
  fields and delimeters, switch to using tr to count how many fields/tabs are in
  a line. Also, in load_symvers(), pass LIMIT of -1 to split() so it does not
  strip trailing empty fields, as namespace is an optional field.
- commit a3bb253
* Mon Mar  9 2020 mkubecek@suse.cz
- Update to 5.6-rc5
- new config options:
  - BACKLIGHT_LED=m
- commit ff29e08
* Wed Mar  4 2020 jeffm@suse.com
- config: re-enable NLS_ISO8859_1 for kvmsmall
  The EFI partition wants NLS_ISO8859_1 and will fail to mount without it.
- commit b981821
* Mon Mar  2 2020 mkubecek@suse.cz
- Update to 5.6-rc4
- eliminated 3 patches
- new config options:
  - KVM_WERROR=n (x86)
- commit 8a04afc
* Wed Feb 26 2020 msuchanek@suse.de
- rpm/package-descriptions: garbege collection
  remove old ARM and Xen flavors.
- commit bda0360
* Wed Feb 26 2020 mhocko@suse.com
- Created new preempt kernel flavor (jsc#SLE-11309)
  Configs are cloned from the respective $arch/default configs. All
  changed configs appart from CONFIG_PREEMPT->y are a result of
  dependencies, namely many lock/unlock primitives are no longer
  inlined in the preempt kernel. TREE_RCU has been also changed to
  PREEMPT_RCU which is the default implementation for PREEMPT kernel.
- commit f994874
* Tue Feb 25 2020 meissner@suse.de
- sign also s390x kernel images (bsc#1163524)
- commit fd52e6c
* Tue Feb 25 2020 jroedel@suse.de
- KVM: nVMX: Check IO instruction VM-exit conditions
  (CVE-2020-2732 bsc#1163971).
- KVM: nVMX: Refactor IO bitmap checks into helper function
  (CVE-2020-2732 bsc#1163971).
- KVM: nVMX: Don't emulate instructions in guest mode
  (CVE-2020-2732 bsc#1163971).
- commit 9a155f2
* Mon Feb 24 2020 msuchanek@suse.de
- Enable CONFIG_BLK_DEV_SR_VENDOR (boo#1164632).
- commit 5a0f1b6
* Mon Feb 24 2020 mkubecek@suse.cz
- Update to 5.6-rc3
- eliminated 3 patches
- commit 8f8ffe7
* Fri Feb 21 2020 mkubecek@suse.cz
- config: fix config options added with 5.5-rc1
  Due to a mistake on my side, some config options introduced in 5.5-rc1 got
  different values than the commit message claimed (and, more important, than
  intended). Thanks to Jean Delvare for catching this.
- restored config option values:
  - BACKLIGHT_QCOM_WLED=m
  - BYTCRC_PMIC_OPREGION=y
  - CAIF_DRIVERS=y
  - CHTCRC_PMIC_OPREGION=y
  - CRYPTO_BLAKE2S=m
  - CRYPTO_CURVE25519=m
  - CRYPTO_DEV_AMLOGIC_GXL=m
  - DP83869_PHY=m
  - DRM_AMD_DC_HDCP=y
  - NET_DSA_MSCC_FELIX=m
  - NET_DSA_TAG_OCELOT=m
  - NFC_PN532_UART=m
  - PINCTRL_EQUILIBRIUM=m
  - PINCTRL_TIGERLAKE=m
  - PTP_1588_CLOCK_IDTCM=m
  - SENSORS_BEL_PFE=m
  - SENSORS_LTC2947_I2C=m
  - SENSORS_LTC2947_SPI=m
  - SENSORS_TMP513=m
  - SF_PDMA=m
  - SYSTEM76_ACPI=m
  - TCG_TIS_SPI_CR50=y
  - TYPEC_HD3SS3220=m
  - VIDEO_HI556=m
  - VIDEO_IMX290=m
  - W1_SLAVE_DS2430=m
  - WFX=m
- new config options visible after the changes above:
  - CAIF_TTY=m
  - CAIF_SPI_SLAVE=m
  - CAIF_SPI_SYNC=n
  - CAIF_HSI=m
  - CAIF_VIRTIO=m
  - CRYPTO_DEV_AMLOGIC_GXL_DEBUG=n
- commit db2e01e
* Fri Feb 21 2020 jslaby@suse.cz
- Update config files (bnc#1163396).
  Disable CONFIG_RESET_ATTACK_MITIGATION as we don't have the userspace
  part and it causes problems during reboot. The config description
  states:
  This should only be enabled when userland is configured to clear the
  MemoryOverwriteRequest flag on clean shutdown after secrets have been
  evicted, since otherwise it will trigger even on clean reboots.
- commit e8bf686
* Wed Feb 19 2020 jslaby@suse.cz
- Update config files (bnc#1161832).
  Disable CONFIG_MODULE_SIG on i386. We don't run pesign on i386 builds,
  hence the modules are not signed at all. This results in module
  verification failures and warnings.
  CONFIG_SECURITY_LOCKDOWN_LSM depends on (selects) CONFIG_MODULE_SIG, so
  we have to disable it too. But it makes no sense to lockdown without
  module signature anyway.
- commit 621a9b6
* Tue Feb 18 2020 msuchanek@suse.de
- Delete patches.rpmify/powerpc-boot-Fix-missing-crc32poly.h-when-building-w.patch.
- commit 3083c73
* Mon Feb 17 2020 jslaby@suse.cz
- vt: selection, close sel_buffer race (bnc#1162928
  CVE-2020-8648).
- vt: selection, handle pending signals in paste_selection
  (bnc#1162928 CVE-2020-8648).
- commit 6252d6b
* Mon Feb 17 2020 mkubecek@suse.cz
- Update to 5.6-rc2
- refresh configs (drop LIBXBC)
- commit 327abc9
* Mon Feb 17 2020 mkubecek@suse.cz
- ethtool: fix application of verbose no_mask bitset.
- commit 7b26eb4
* Thu Feb 13 2020 tiwai@suse.de
- Update config files: enable CONFIG_FW_CFG_SYSFS for arm64 (bsc#1163521)
- commit 865d99b
* Wed Feb 12 2020 jdelvare@suse.de
- Update config files: CONFIG_NVME_HWMON=y
  When the config files were updated for kernel v5.5, the commit
  message claimed CONFIG_NVME_HWMON was to be enabled, however the
  configuration files themselves had the option disabled. We definitely
  want hardware monitoring enabled on NVME devices, so fix the
  configuration files to match the original intent.
- commit 30b1016
* Tue Feb 11 2020 afaerber@suse.com
- config: armv7hl: Update to 5.6-rc1
- commit b09045a
* Tue Feb 11 2020 afaerber@suse.com
- config: armv6hl: Update to 5.6-rc1
- commit e68a306
* Tue Feb 11 2020 afaerber@suse.com
- config: arm64: Update to 5.6-rc1
- commit 0ae2ac2
* Mon Feb 10 2020 tiwai@suse.de
- media: go7007: Fix URB type for interrupt handling
  (bsc#1162583).
- commit 23d5616
* Mon Feb 10 2020 mkubecek@suse.cz
- Update to 5.6-rc1
- eliminated 95 patches (70 stable, 25 other)
- disable ARM architectures (need config update)
- refresh
  - patches.rpmify/Add-ksym-provides-tool.patch
  - patches.suse/acpi_thermal_passive_blacklist.patch
- new config options :
  - General setup
  - TIME_NS=y
  - BOOT_CONFIG=y
  - Firmware Drivers
  - EFI_DISABLE_PCI_DMA=n
  - Networking core
  - INET_ESPINTCP=y
  - MPTCP=y
  - MPTCP_IPV6=y
  - MPTCP_HMAC_TEST=n
  - NET_DSA_TAG_AR9331=m
  - NET_SCH_FQ_PIE=m
  - NET_SCH_ETS=m
  - VSOCKETS_LOOPBACK=m
  - ETHTOOL_NETLINK=y
  - WIREGUARD=m
  - WIREGUARD_DEBUG=n
  - File systems
  - ZONEFS_FS=m
  - VBOXSF_FS=m
  - NFS_DISABLE_UDP_SUPPORT=n
  - NFSD_V4_2_INTER_SSC=y
  - Security options
  - SECURITY_SELINUX_SIDTAB_HASH_BITS=9
  - SECURITY_SELINUX_SID2STR_CACHE_SIZE=256
  - TEE=m
  - AMDTEE=m
  - Kernel hacking
  - PTDUMP_DEBUGFS=n
  - BOOTTIME_TRACING=y
  - SYNTH_EVENT_GEN_TEST=n
  - KPROBE_EVENT_GEN_TEST=n
  - Networking drivers
  - NET_DSA_AR9331=m
  - NET_DSA_VITESSE_VSC73XX_SPI=m
  - NET_DSA_VITESSE_VSC73XX_PLATFORM=m
  - PHY_INTEL_EMMC=m
  - Hardware Monitoring support
  - SENSORS_ADM1177=m
  - SENSORS_DRIVETEMP=m
  - SENSORS_MAX31730=m
  - SENSORS_MAX20730=m
  - SENSORS_XDPE122=m
  - Sound
  - SND_CTL_VALIDATION=n
  - SND_SOC_INTEL_USER_FRIENDLY_LONG_NAMES=n
  - SND_SOC_INTEL_BDW_RT5650_MACH=m
  - SND_SOC_INTEL_SOF_DA7219_MAX98373_MACH=m
  - SND_SOC_RT1308_SDW=n
  - SND_SOC_RT700_SDW=n
  - SND_SOC_RT711_SDW=n
  - SND_SOC_RT715_SDW=n
  - SND_SOC_WSA881X=n
  - SND_SOC_MT6660=n
  - Graphics
  - DRM_PANEL_BOE_HIMAX8279D=n
  - DRM_PANEL_LEADTEK_LTK500HD1829=n
  - DRM_PANEL_SONY_ACX424AKP=n
  - DRM_PANEL_XINPENG_XPP055C272=n
  - DRM_LVDS_CODEC=m
  - DRM_ANALOGIX_ANX6345=n
  - Industrial I/O support
  - BMA400=n
  - AD7091R5=n
  - LTC2496=n
  - DLHL60D=n
  - PING=n
  - USB
  - USB4_NET=m
  - USB4=m
  - Misc drivers
  - SERIAL_8250_16550A_VARIANTS=n
  - PINCTRL_LYNXPOINT=m
  - INTEL_IDXD=m
  - PLX_DMA=m
  - QCOM_CPR=m
  - REGULATOR_MP8859=m
  - MFD_ROHM_BD71828=n
  - MEDIA_CEC_RC=y
  - NVMEM_SPMI_SDAM=m
  - DMABUF_HEAPS=n
  - RESET_BRCMSTB_RESCAL=n
  - INTEL_IOMMU_SCALABLE_MODE_DEFAULT_ON=n
  - GPIO_SIFIVE=n
  - x86
  - INTEL_UNCORE_FREQ_CONTROL=m
  - i386
  - PCIE_INTEL_GW=n
  - CPU_FREQ_THERMAL=y
  - CPU_IDLE_THERMAL=y
  - MICROCHIP_PIT64B=y
  - RESET_INTEL_GW=n
  - powerpc
  - STRICT_KERNEL_RWX=y
  - CPU_FREQ_THERMAL=y
  - MICROCHIP_PIT64B=y
  - RESET_INTEL_GW=n
  - DEBUG_RODATA_TEST=n
  - QUICC_ENGINE=y
  - QE_GPIO=y
  - FSL_PQ_MDIO=m
  - FSL_XGMAC_MDIO=m
  - GIANFAR=m
  - SERIAL_QE=m
  - PTP_1588_CLOCK_QORIQ=m
  - USB_FHCI_HCD=m
  - FHCI_DEBUG=n
  - s390x
  - ZLIB_DFLTCC=y
  - KPROBE_EVENTS_ON_NOTRACE=n
- commit 00fe0a9
* Fri Feb  7 2020 ykaukab@suse.de
- config.conf: enable armv6 and armv7 configs
- commit d355d69
* Thu Feb  6 2020 chrubis@suse.cz
- rpm/kernel-binary.spec.in: Replace Novell with SUSE
- commit 8719d69
* Wed Feb  5 2020 mkubecek@suse.cz
- series.conf: cleanup
- update upstream reference (in mainline now) and move to "almost mainline" section:
  patches.suse/btrfs-do-not-zero-f_bavail-if-we-have-available-spac.patch
- commit d386a7a
* Wed Feb  5 2020 jslaby@suse.cz
- Linux 5.5.2 (bnc#1012628).
- vfs: fix do_last() regression (bnc#1012628).
- cifs: fix soft mounts hanging in the reconnect code
  (bnc#1012628).
- x86/resctrl: Fix a deadlock due to inaccurate reference
  (bnc#1012628).
- x86/resctrl: Fix use-after-free when deleting resource groups
  (bnc#1012628).
- x86/resctrl: Fix use-after-free due to inaccurate refcount of
  rdtgroup (bnc#1012628).
- KVM: PPC: Book3S PR: Fix -Werror=return-type build failure
  (bnc#1012628).
- gfs2: Another gfs2_find_jhead fix (bnc#1012628).
- lib/test_bitmap: correct test data offsets for 32-bit
  (bnc#1012628).
- perf c2c: Fix return type for histogram sorting comparision
  functions (bnc#1012628).
- PM / devfreq: Add new name attribute for sysfs (bnc#1012628).
- tools lib: Fix builds when glibc contains strlcpy()
  (bnc#1012628).
- arm64: kbuild: remove compressed images on 'make ARCH=arm64
  (dist)clean' (bnc#1012628).
- mm/mempolicy.c: fix out of bounds write in mpol_parse_str()
  (bnc#1012628).
- reiserfs: Fix memory leak of journal device string
  (bnc#1012628).
- media: digitv: don't continue if remote control state can't
  be read (bnc#1012628).
- media: af9005: uninitialized variable printked (bnc#1012628).
- media: vp7045: do not read uninitialized values if usb transfer
  fails (bnc#1012628).
- media: gspca: zero usb_buf (bnc#1012628).
- media: dvb-usb/dvb-usb-urb.c: initialize actlen to 0
  (bnc#1012628).
- tomoyo: Use atomic_t for statistics counter (bnc#1012628).
- ttyprintk: fix a potential deadlock in interrupt context issue
  (bnc#1012628).
- Bluetooth: Fix race condition in hci_release_sock()
  (bnc#1012628).
- cgroup: Prevent double killing of css when enabling threaded
  cgroup (bnc#1012628).
- commit c2619d7
* Tue Feb  4 2020 duwe@suse.de
- rpm/modules.fips: add keywrap (bsc#1160561)
- commit 719d9e1
* Tue Feb  4 2020 jslaby@suse.cz
- btrfs: do not zero f_bavail if we have available space
  (bnc#1162471).
- commit efe8ca5
* Mon Feb  3 2020 dsterba@suse.com
- btrfs: do not zero f_bavail if we have available space (bsc#1162471)
- commit edaa5de
* Mon Feb  3 2020 mkubecek@suse.cz
- series.conf: cleanup
- update upstream references and move into "almost mainline" section:
  patches.suse/0001-x86-kvm-Be-careful-not-to-clear-KVM_VCPU_FLUSH_TLB-b.patch
  patches.suse/0002-x86-kvm-Introduce-kvm_-un-map_gfn.patch
  patches.suse/0003-x86-kvm-Cache-gfn-to-pfn-translation.patch
  patches.suse/0004-x86-KVM-Make-sure-KVM_VCPU_FLUSH_TLB-flag-is-not-mis.patch
  patches.suse/0005-x86-KVM-Clean-up-host-s-steal-time-structure.patch
  patches.suse/pci-brcmstb-add-broadcom-stb-pcie-host-controller-driver.patch
  patches.suse/pci-brcmstb-add-msi-capability.patch
- move into "almost mainline" section
  patches.suse/ASoC-SOF-Introduce-state-machine-for-FW-boot.patch
- commit 9b0f74c
* Sat Feb  1 2020 jslaby@suse.cz
- Linux 5.5.1 (bnc#1012628).
- power/supply: ingenic-battery: Don't change scale if there's
  only one (bnc#1012628).
- Revert "um: Enable CONFIG_CONSTRUCTORS" (bnc#1012628).
- KVM: arm64: Write arch.mdcr_el2 changes since last vcpu_load
  on VHE (bnc#1012628).
- crypto: pcrypt - Fix user-after-free on module unload
  (bnc#1012628).
- crypto: caam - do not reset pointer size from MCFGR register
  (bnc#1012628).
- crypto: vmx - reject xts inputs that are too short
  (bnc#1012628).
- crypto: af_alg - Use bh_lock_sock in sk_destruct (bnc#1012628).
- rsi: fix non-atomic allocation in completion handler
  (bnc#1012628).
- rsi: fix memory leak on failed URB submission (bnc#1012628).
- rsi: fix use-after-free on probe errors (bnc#1012628).
- rsi: fix use-after-free on failed probe and unbind
  (bnc#1012628).
- rxrpc: Fix use-after-free in rxrpc_receive_data() (bnc#1012628).
- net: include struct nhmsg size in nh nlmsg size (bnc#1012628).
- mlxsw: minimal: Fix an error handling path in
  'mlxsw_m_port_create()' (bnc#1012628).
- udp: segment looped gso packets correctly (bnc#1012628).
- net: socionext: fix xdp_result initialization in
  netsec_process_rx (bnc#1012628).
- net: socionext: fix possible user-after-free in
  netsec_process_rx (bnc#1012628).
- net_sched: walk through all child classes in tc_bind_tclass()
  (bnc#1012628).
- net_sched: fix ops->bind_class() implementations (bnc#1012628).
- net_sched: ematch: reject invalid TCF_EM_SIMPLE (bnc#1012628).
- mvneta driver disallow XDP program on hardware buffer management
  (bnc#1012628).
- zd1211rw: fix storage endpoint lookup (bnc#1012628).
- rtl8xxxu: fix interface sanity check (bnc#1012628).
- brcmfmac: fix interface sanity check (bnc#1012628).
- ath9k: fix storage endpoint lookup (bnc#1012628).
- cifs: Fix memory allocation in __smb2_handle_cancelled_cmd()
  (bnc#1012628).
- cifs: set correct max-buffer-size for smb2_ioctl_init()
  (bnc#1012628).
- CIFS: Fix task struct use-after-free on reconnect (bnc#1012628).
- crypto: chelsio - fix writing tfm flags to wrong place
  (bnc#1012628).
- driver core: Fix test_async_driver_probe if NUMA is disabled
  (bnc#1012628).
- iio: st_gyro: Correct data for LSM9DS0 gyro (bnc#1012628).
- iio: adc: stm32-dfsdm: fix single conversion (bnc#1012628).
- mei: me: add jasper point DID (bnc#1012628).
- mei: me: add comet point (lake) H device ids (bnc#1012628).
- mei: hdcp: bind only with i915 on the same PCH (bnc#1012628).
- binder: fix log spam for existing debugfs file creation
  (bnc#1012628).
- component: do not dereference opaque pointer in debugfs
  (bnc#1012628).
- debugfs: Return -EPERM when locked down (bnc#1012628).
- serial: imx: fix a race condition in receive path (bnc#1012628).
- serial: 8250_bcm2835aux: Fix line mismatch on driver unbind
  (bnc#1012628).
- staging: vt6656: Fix false Tx excessive retries reporting
  (bnc#1012628).
- staging: vt6656: use NULLFUCTION stack on mac80211
  (bnc#1012628).
- staging: vt6656: correct packet types for CTS protect, mode
  (bnc#1012628).
- staging: wlan-ng: ensure error return is actually returned
  (bnc#1012628).
- staging: most: net: fix buffer overflow (bnc#1012628).
- usb: typec: fusb302: fix "op-sink-microwatt" default that was
  in mW (bnc#1012628).
- usb: typec: wcove: fix "op-sink-microwatt" default that was
  in mW (bnc#1012628).
- usb: dwc3: turn off VBUS when leaving host mode (bnc#1012628).
- USB: serial: ir-usb: fix IrLAP framing (bnc#1012628).
- USB: serial: ir-usb: fix link-speed handling (bnc#1012628).
- USB: serial: ir-usb: add missing endpoint sanity check
  (bnc#1012628).
- usb: host: xhci-tegra: set MODULE_FIRMWARE for tegra186
  (bnc#1012628).
- usb: dwc3: pci: add ID for the Intel Comet Lake -V variant
  (bnc#1012628).
- rsi_91x_usb: fix interface sanity check (bnc#1012628).
- orinoco_usb: fix interface sanity check (bnc#1012628).
- Bluetooth: btusb: fix non-atomic allocation in completion
  handler (bnc#1012628).
- commit d3e7b7d
* Fri Jan 31 2020 yousaf.kaukab@suse.com
- config: armv7lpae: Update to 5.5
- commit 74459b2
* Fri Jan 31 2020 yousaf.kaukab@suse.com
- config: armv7hl: Update to 5.5
- commit ae8d01e
* Fri Jan 31 2020 yousaf.kaukab@suse.com
- config: armv6hl: Update to 5.5
- commit edbc4d9
* Fri Jan 31 2020 jroedel@suse.de
- x86/KVM: Clean up host's steal time structure (bcs#1161154,
  CVE-2019-3016).
- x86/KVM: Make sure KVM_VCPU_FLUSH_TLB flag is not missed
  (bcs#1161154, CVE-2019-3016).
- x86/kvm: Cache gfn to pfn translation (bcs#1161154,
  CVE-2019-3016).
- x86/kvm: Introduce kvm_(un)map_gfn() (bcs#1161154,
  CVE-2019-3016).
- x86/kvm: Be careful not to clear KVM_VCPU_FLUSH_TLB bit
  (bcs#1161154, CVE-2019-3016).
- commit 77cf1f3
* Thu Jan 30 2020 mkubecek@suse.cz
- update upstream references
- update upstream status (in mainline now):
  patches.suse/ALSA-hda-Apply-aligned-MMIO-access-only-conditionall.patch
  patches.suse/hwrng-iproc-rng200-add-support-for-bcm2711.patch
- commit f202425
* Thu Jan 30 2020 mkubecek@suse.cz
- update upstream reference
- update upstream status (in mainline now):
  patches.suse/ASoC-SOF-Introduce-state-machine-for-FW-boot.patch
- commit 86483c3
* Wed Jan 29 2020 tiwai@suse.de
- Update patch tag for upstreamed rtw88 patch
- commit 1507410
* Mon Jan 27 2020 tiwai@suse.de
- ASoC: SOF: core: release resources on errors in probe_continue
  (bsc#1161246).
- ASoC: SOF: core: free trace on errors (bsc#1161246).
- ASoC: SOF: Introduce state machine for FW boot (bsc#1161246).
- commit ef0a514
* Mon Jan 27 2020 jeyu@suse.de
- rpm/kabi.pl: support new (>=5.4) Module.symvers format (new symbol namespace field)
- commit eecbd97
* Mon Jan 27 2020 mkubecek@suse.cz
- Update to 5.5 final
- refresh configs
- commit 002fd1a
* Fri Jan 24 2020 mkubecek@suse.cz
- config: refresh
  Only update headers.
- commit 7193c66
* Wed Jan 22 2020 afaerber@suse.com
- config: arm64: Update to 5.5-rc7
- commit 4e17086
* Tue Jan 21 2020 tiwai@suse.de
- Update config files: Update config files: adjust Intel ASoC audio items (bsc#1161463)
  Adjust the Kconfigs for Intel ASoC SOF/SST drivers more appropriately.
  Disable unrecommended items:
  CONFIG_SND_SOC_INTEL_SKYLAKE_HDAUDIO_CODEC=n
  CONFIG_SND_SST_ATOM_HIFI2_PLATFORM_PCI=n
  CONFIG_SND_SOC_SOF_MERRIFIELD_SUPPORT=n
  CONFIG_SND_SOC_INTEL_BYT_CHT_NOCODEC_MACH=n
  Enable the other ones:
  CONFIG_SND_SOC_INTEL_SKL_RT286_MACH=m
  CONFIG_SND_SOC_INTEL_SKL_NAU88L25_SSM4567_MACH=m
  CONFIG_SND_SOC_INTEL_SKL_NAU88L25_MAX98357A_MACH=m
  CONFIG_SND_SOC_INTEL_BXT_DA7219_MAX98357A_MACH=m
  CONFIG_SND_SOC_INTEL_BXT_RT298_MACH=m
  CONFIG_SND_SOC_INTEL_GLK_DA7219_MAX98357A_MACH=m
  CONFIG_SND_SOC_INTEL_SOF_CML_RT1011_RT5682_MACH=m
- commit 1da7ef3
* Mon Jan 20 2020 msuchanek@suse.de
- kernel-binary.spec.in: do not recommend firmware for kvmsmall and azure
  flavor (boo#1161360).
- commit dbe7b27
* Mon Jan 20 2020 msuchanek@suse.de
- config/x86_64/kvmsmall: Enable UINPUT (boo#1161305).
- commit 930edd3
* Mon Jan 20 2020 tiwai@suse.de
- ALSA: hda: Apply aligned MMIO access only conditionally
  (bsc#1161152).
- commit e1a66d4
* Mon Jan 20 2020 mkubecek@suse.cz
- Update to 5.5-rc7
- commit 3dbb847
* Wed Jan 15 2020 tiwai@suse.de
- rtw88: fix potential NULL skb access in TX ISR (bsc#1160730).
- commit f123aae
* Tue Jan 14 2020 tiwai@suse.de
- Update config files: enable forgotten configs for SOF (bsc#1160819)
  The configs have been forgotten to be enabled:
  CONFIG_SND_SOC_SOF_HDA_COMMON_HDMI_CODEC=y
  CONFIG_SND_SOC_SOF_JASPERLAKE_SUPPORT=y
  CONFIG_SND_SOC_SOF_JASPERLAKE=m
- commit c542b01
* Mon Jan 13 2020 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Do not obsolete KMPs (boo#1126512).
- commit da578e6
* Mon Jan 13 2020 mkubecek@suse.cz
- Update to 5.5-rc6
- commit 6dccaaf
* Fri Jan 10 2020 nsaenzjulienne@suse.de
- supported.conf: Enable mdio-bcm-unimac (bsc#1160310)
  Needed in order for Raspberry Pi 4's ethernet port to work.
- commit b949d3b
* Thu Jan  9 2020 mkubecek@suse.cz
- supported.conf: sort
  Fix order of entries in supported.conf file.
- commit 581d935
* Wed Jan  8 2020 nsaenzjulienne@suse.de
- supported.conf: enable Raspberry Pi cpufreq driver (bsc#1160461).
  These drivers are required in order to enable CPU frequency scaling on
  the Raspberry Pi family of boards.
- commit 224f041
* Wed Jan  8 2020 tiwai@suse.de
- rpm/kernel-docs.spec.in: pass PYTHON=python3 to fix build error (bsc#1160435)
- commit 9b5299f
* Wed Jan  8 2020 mkubecek@suse.cz
- config: fix pstore default compression options on 32-bit ARM
  Previous commit did not update arvm7hl and armv6hl configs properly and
  run_oldconfig.sh did not catch it as these architectures are disabled at
  the moment.
- commit 21dc79d
* Tue Jan  7 2020 msuchanek@suse.de
- Make lzo the default pstore compression method (bsc#1159986).
  Pstore has compression enabled, pstore is built-in, pstore default
  compression is deflate, deflate is modular -> pstore initialization
  fails on boot. Switch default compression to lzo which is built-in and
  the only built-in method on SLE15.
- commit 52fe949
* Mon Jan  6 2020 mkubecek@suse.cz
- Update to 5.5-rc5
- commit 288dac0
* Fri Jan  3 2020 jslaby@suse.cz
- Update config files.
  Turn off CONFIG_HARDENED_USERCOPY as it causes issues on s390
  (bnc#1156053). Until this gets resolved upstream...
- commit 34be040
* Mon Dec 30 2019 mkubecek@suse.cz
- Update to 5.5-rc4
- refresh
  patches.suse/vfs-add-super_operations-get_inode_dev
- commit 7e31c5e
* Sun Dec 29 2019 mkubecek@suse.cz
- config: refresh
  Refresh with a new gcc version.
- commit 2d3adcc
* Sat Dec 28 2019 mbrugger@suse.com
- arm64: Add Allwinner crypto modules to config
  Enabel SUN4I and SUN8I based HW crypto blocks.
- commit b496619
* Mon Dec 23 2019 mkubecek@suse.cz
- Update to 5.5-rc3
- refresh configs
- commit acd0797
* Thu Dec 19 2019 mkubecek@suse.cz
- rpm/kernel-subpackage-spec: fix kernel-default-base build
  There were some issues with recent changes to subpackage dependencies handling:
- a typo in %%kernel_base_conflicts macro name
- copy/pasted "Recommends:" instead of "Provides:", "Obsoletes:" and
  "Conflicts:
- missing escaping of backslashes in macro expansions
  Fixes: f3b74b0ae86b ("rpm/kernel-subpackage-spec: Unify dependency handling.")
  Fixes: 3fd22e219f77 ("rpm/kernel-subpackage-spec: Fix empty Recommends tag (bsc#1143959)")
- commit 762fd66
* Wed Dec 18 2019 msuchanek@suse.de
- rpm/kernel-subpackage-spec: Unify dependency handling.
- commit f3b74b0
* Tue Dec 17 2019 jslaby@suse.cz
- rpm/config.sh: set COMPRESS_VMLINUX to xz (bnc#1155921)
- commit 7fe1f4a
* Mon Dec 16 2019 tiwai@suse.de
- rpm/kernel-subpackage-spec: Fix empty Recommends tag (bsc#1143959)
- commit 3fd22e2
* Mon Dec 16 2019 mkubecek@suse.cz
- Update to 5.5-rc2
- update configs
  - CRYPTO_BLAKE2B=m
- commit 5d7acaa
* Thu Dec 12 2019 nsaenzjulienne@suse.de
- hwrng: iproc-rng200 - Add support for BCM2711 (jsc#SLE-7772).
- commit 9e9a23d
* Mon Dec  9 2019 mkubecek@suse.cz
- Update to 5.5-rc1
- eliminated 175 patches (114 stable, 61 other)
- ARM configs need update
- refresh
  patches.suse/0001-usb-Add-Xen-pvUSB-protocol-description.patch
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  patches.suse/linux-log2-h-add-roundup-rounddown_pow_two64-family-of-functions.patch
  patches.suse/setuid-dumpable-wrongdir
  patches.suse/supported-flag
  patches.suse/supported-flag-external
- new config options:
  - Processor type and features
  - X86_IOPL_IOPERM=y
  - X86_UMIP=y
  - Power management
  - BYTCRC_PMIC_OPREGION=y
  - CHTCRC_PMIC_OPREGION=y
  - Networking
  - TLS_TOE=n
  - TIPC_CRYPTO=y
  - NET_DSA_TAG_OCELOT=m
  - NFC_PN532_UART=m
  - Cryptographic API
  - CRYPTO_CURVE25519=m
  - CRYPTO_CURVE25519_X86=m
  - CRYPTO_BLAKE2B=m
  - CRYPTO_BLAKE2S=m
  - CRYPTO_BLAKE2S_X86=m
  - CRYPTO_LIB_BLAKE2S=m
  - CRYPTO_LIB_CHACHA=m
  - CRYPTO_LIB_CURVE25519=m
  - CRYPTO_LIB_POLY1305=m
  - CRYPTO_LIB_CHACHA20POLY1305=m
  - CRYPTO_DEV_AMLOGIC_GXL=m
  - Kernel hacking
  - SYMBOLIC_ERRNAME=y
  - TRACE_EVENT_INJECT=n
  - KUNIT=n
  - Kernel Testing and Coverage
  - HYPERV_TESTING=n
  - Networking drivers
  - CAIF_DRIVERS=y
  - NET_DSA_MSCC_FELIX=m
  - DP83869_PHY=m
  - Hardware Monitoring
  - SENSORS_LTC2947_I2C=m
  - SENSORS_LTC2947_SPI=m
  - SENSORS_BEL_PFE=m
  - SENSORS_TMP513=m
  - Multimedia
  - VIDEO_HI556=m
  - VIDEO_IMX290=m
  - Graphics
  - DRM_DEBUG_DP_MST_TOPOLOGY_REFS=n
  - DRM_AMD_DC_HDCP=y
  - DRM_I915_HEARTBEAT_INTERVAL=2500
  - DRM_I915_PREEMPT_TIMEOUT=640
  - DRM_I915_SPIN_REQUEST=5
  - DRM_I915_STOP_TIMEOUT=100
  - DRM_I915_TIMESLICE_DURATION=1
  - BACKLIGHT_QCOM_WLED=m
  - FB_TFT=n
  - Sound
  - SND_SOC_INTEL_GLK_DA7219_MAX98357A_MACH=m
  - SND_SOC_INTEL_SOF_CML_RT1011_RT5682_MACH=m
  - SND_SOC_SOF_DEVELOPER_SUPPORT=n
  - SND_SOC_SOF_JASPERLAKE_SUPPORT=y
  - SND_SOC_SOF_HDA_COMMON_HDMI_CODEC=y
  - SND_SOC_ADAU7118_HW=n
  - SND_SOC_ADAU7118_I2C=n
  - SND_SOC_TAS2562=n
  - SND_SOC_TAS2770=n
  - USB
  - TYPEC_HD3SS3220=m
  - Industrial I/O
  - AD7292=n
  - FXOS8700_I2C=n
  - FXOS8700_SPI=n
  - ADUX1020=n
  - VEML6030=n
  - LTC2983=n
  - Misc drivers
  - EFI_SOFT_RESERVE=y
  - FW_CACHE=y
  - TCG_TIS_SPI_CR50=y
  - PTP_1588_CLOCK_IDTCM=m
  - PINCTRL_TIGERLAKE=m
  - PINCTRL_EQUILIBRIUM=m
  - W1_SLAVE_DS2430=m
  - SF_PDMA=m
  - NVME_HWMON=y
  - WFX=m
  - SYSTEM76_ACPI=m
  - CROS_EC_SENSORHUB=m
  - DEV_DAX_HMEM=m
  - ppc64(le):
  - PPC_UV=n
  - */debug:
  - TRACE_EVENT_INJECT=y
  - x86_64/debug:
  - HYPERV_TESTING=y
- commit 6af0b1c
* Thu Dec  5 2019 nsaenzjulienne@suse.de
- supported.conf: Support Broadcom's Genet Ethernet driver (bsc#158563)
- commit 5e42d26
* Thu Dec  5 2019 jslaby@suse.cz
- Linux 5.4.2 (bnc#1012628).
- platform/x86: hp-wmi: Fix ACPI errors caused by passing 0 as
  input size (bnc#1012628).
- platform/x86: hp-wmi: Fix ACPI errors caused by too small buffer
  (bnc#1012628).
- HID: core: check whether Usage Page item is after Usage ID items
  (bnc#1012628).
- crypto: talitos - Fix build error by selecting LIB_DES
  (bnc#1012628).
- Revert "jffs2: Fix possible null-pointer dereferences in
  jffs2_add_frag_to_fragtree()" (bnc#1012628).
- ext4: add more paranoia checking in ext4_expand_extra_isize
  handling (bnc#1012628).
- r8169: fix resume on cable plug-in (bnc#1012628).
- r8169: fix jumbo configuration for RTL8168evl (bnc#1012628).
- selftests: pmtu: use -oneline for ip route list cache
  (bnc#1012628).
- tipc: fix link name length check (bnc#1012628).
- selftests: bpf: correct perror strings (bnc#1012628).
- selftests: bpf: test_sockmap: handle file creation failures
  gracefully (bnc#1012628).
- net/tls: use sg_next() to walk sg entries (bnc#1012628).
- net/tls: remove the dead inplace_crypto code (bnc#1012628).
- selftests/tls: add a test for fragmented messages (bnc#1012628).
- net: skmsg: fix TLS 1.3 crash with full sk_msg (bnc#1012628).
- net/tls: free the record on encryption error (bnc#1012628).
- net/tls: take into account that bpf_exec_tx_verdict() may free
  the record (bnc#1012628).
- openvswitch: remove another BUG_ON() (bnc#1012628).
- openvswitch: drop unneeded BUG_ON() in ovs_flow_cmd_build_info()
  (bnc#1012628).
- sctp: cache netns in sctp_ep_common (bnc#1012628).
- slip: Fix use-after-free Read in slip_open (bnc#1012628).
- sctp: Fix memory leak in sctp_sf_do_5_2_4_dupcook (bnc#1012628).
- openvswitch: fix flow command message size (bnc#1012628).
- net: sched: fix `tc -s class show` no bstats on class with
  nolock subqueues (bnc#1012628).
- net: psample: fix skb_over_panic (bnc#1012628).
- net: macb: add missed tasklet_kill (bnc#1012628).
- net: dsa: sja1105: fix sja1105_parse_rgmii_delays()
  (bnc#1012628).
- mdio_bus: don't use managed reset-controller (bnc#1012628).
- macvlan: schedule bc_work even if error (bnc#1012628).
- gve: Fix the queue page list allocated pages count
  (bnc#1012628).
- x86/fpu: Don't cache access to fpu_fpregs_owner_ctx
  (bnc#1012628).
- thunderbolt: Power cycle the router if NVM authentication fails
  (bnc#1012628).
- mei: me: add comet point V device id (bnc#1012628).
- mei: bus: prefix device names on bus with the bus name
  (bnc#1012628).
- USB: serial: ftdi_sio: add device IDs for U-Blox C099-F9P
  (bnc#1012628).
- staging: rtl8723bs: Add 024c:0525 to the list of SDIO device-ids
  (bnc#1012628).
- staging: rtl8723bs: Drop ACPI device ids (bnc#1012628).
- staging: rtl8192e: fix potential use after free (bnc#1012628).
- staging: wilc1000: fix illegal memory access in
  wilc_parse_join_bss_param() (bnc#1012628).
- usb: dwc2: use a longer core rest timeout in dwc2_core_reset()
  (bnc#1012628).
- driver core: platform: use the correct callback type for
  bus_find_device (bnc#1012628).
- crypto: inside-secure - Fix stability issue with Macchiatobin
  (bnc#1012628).
- net: disallow ancillary data for __sys_{send,recv}msg_file()
  (bnc#1012628).
- net: separate out the msghdr copy from ___sys_{send,recv}msg()
  (bnc#1012628).
- io_uring: async workers should inherit the user creds
  (bnc#1012628).
- commit 9df353f
* Wed Dec  4 2019 nsaenzjulienne@suse.de
- supported.conf: support gpio-regulator used by Raspberry Pi 4
  (bsc#1158451)
- commit d0225c2
* Tue Dec  3 2019 mbrugger@suse.com
- arm64: Update config files.
  Bump CONFIG_NODES_SHIFT from 2 to 6
- commit 476eb27
* Tue Dec  3 2019 tiwai@suse.de
- rpm/kernel-subpackage-spec: Exclude kernel-firmware recommends (bsc#1143959)
  For reducing the dependency on kernel-firmware in sub packages
- commit d950271
* Fri Nov 29 2019 msuchanek@suse.de
- Update config files.
  ppc64 is lats architecture without PRINTK_TIME. Align with the rest.
- commit f46c056
* Fri Nov 29 2019 jslaby@suse.cz
- blacklist.conf: add one invalid commit
- commit 4c2d405
* Fri Nov 29 2019 jslaby@suse.cz
- Linux 5.4.1 (bnc#1012628).
- Bluetooth: Fix invalid-free in bcsp_close() (bnc#1012628).
- ath9k_hw: fix uninitialized variable data (bnc#1012628).
- ath10k: Fix HOST capability QMI incompatibility (bnc#1012628).
- ath10k: restore QCA9880-AR1A (v1) detection (bnc#1012628).
- Revert "Bluetooth: hci_ll: set operational frequency earlier"
  (bnc#1012628).
- Revert "dm crypt: use WQ_HIGHPRI for the IO and crypt
  workqueues" (bnc#1012628).
- md/raid10: prevent access of uninitialized resync_pages offset
  (bnc#1012628).
- x86/insn: Fix awk regexp warnings (bnc#1012628).
- x86/speculation: Fix incorrect MDS/TAA mitigation status
  (bnc#1012628).
- x86/speculation: Fix redundant MDS mitigation message
  (bnc#1012628).
- nbd: prevent memory leak (bnc#1012628).
- x86/stackframe/32: Repair 32-bit Xen PV (bnc#1012628).
- x86/xen/32: Make xen_iret_crit_fixup() independent of frame
  layout (bnc#1012628).
- x86/xen/32: Simplify ring check in xen_iret_crit_fixup()
  (bnc#1012628).
- x86/doublefault/32: Fix stack canaries in the double fault
  handler (bnc#1012628).
- x86/pti/32: Size initial_page_table correctly (bnc#1012628).
- x86/cpu_entry_area: Add guard page for entry stack on 32bit
  (bnc#1012628).
- x86/entry/32: Fix IRET exception (bnc#1012628).
- x86/entry/32: Use %%ss segment where required (bnc#1012628).
- x86/entry/32: Move FIXUP_FRAME after pushing %%fs in SAVE_ALL
  (bnc#1012628).
- x86/entry/32: Unwind the ESPFIX stack earlier on exception entry
  (bnc#1012628).
- x86/entry/32: Fix NMI vs ESPFIX (bnc#1012628).
- selftests/x86/mov_ss_trap: Fix the SYSENTER test (bnc#1012628).
- selftests/x86/sigreturn/32: Invalidate DS and ES when abusing
  the kernel (bnc#1012628).
- x86/pti/32: Calculate the various PTI cpu_entry_area sizes
  correctly, make the CPU_ENTRY_AREA_PAGES assert precise
  (bnc#1012628).
- x86/entry/32: Fix FIXUP_ESPFIX_STACK with user CR3
  (bnc#1012628).
- futex: Prevent robust futex exit race (bnc#1012628).
- ALSA: usb-audio: Fix NULL dereference at parsing BADD
  (bnc#1012628).
- ALSA: usb-audio: Fix Scarlett 6i6 Gen 2 port data (bnc#1012628).
- media: vivid: Set vid_cap_streaming and vid_out_streaming to
  true (bnc#1012628).
- media: vivid: Fix wrong locking that causes race conditions
  on streaming stop (bnc#1012628).
- media: usbvision: Fix invalid accesses after device disconnect
  (bnc#1012628).
- media: usbvision: Fix races among open, close, and disconnect
  (bnc#1012628).
- cpufreq: Add NULL checks to show() and store() methods of
  cpufreq (bnc#1012628).
- futex: Move futex exit handling into futex code (bnc#1012628).
- futex: Replace PF_EXITPIDONE with a state (bnc#1012628).
- exit/exec: Seperate mm_release() (bnc#1012628).
- futex: Split futex_mm_release() for exit/exec (bnc#1012628).
- futex: Set task::futex_state to DEAD right after handling
  futex exit (bnc#1012628).
- futex: Mark the begin of futex exit explicitly (bnc#1012628).
- futex: Sanitize exit state handling (bnc#1012628).
- futex: Provide state handling for exec() as well (bnc#1012628).
- futex: Add mutex around futex exit (bnc#1012628).
- futex: Provide distinct return value when owner is exiting
  (bnc#1012628).
- futex: Prevent exit livelock (bnc#1012628).
- media: uvcvideo: Fix error path in control parsing failure
  (bnc#1012628).
- media: b2c2-flexcop-usb: add sanity checking (bnc#1012628).
- media: cxusb: detect cxusb_ctrl_msg error in query
  (bnc#1012628).
- media: imon: invalid dereference in imon_touch_event
  (bnc#1012628).
- media: mceusb: fix out of bounds read in MCE receiver buffer
  (bnc#1012628).
- ALSA: hda - Disable audio component for legacy Nvidia HDMI
  codecs (bnc#1012628).
- USBIP: add config dependency for SGL_ALLOC (bnc#1012628).
- usbip: tools: fix fd leakage in the function of
  read_attr_usbip_status (bnc#1012628).
- usbip: Fix uninitialized symbol 'nents' in
  stub_recv_cmd_submit() (bnc#1012628).
- usb-serial: cp201x: support Mark-10 digital force gauge
  (bnc#1012628).
- USB: chaoskey: fix error case of a timeout (bnc#1012628).
- appledisplay: fix error handling in the scheduled work
  (bnc#1012628).
- USB: serial: mos7840: add USB ID to support Moxa UPort 2210
  (bnc#1012628).
- USB: serial: mos7720: fix remote wakeup (bnc#1012628).
- USB: serial: mos7840: fix remote wakeup (bnc#1012628).
- USB: serial: option: add support for DW5821e with eSIM support
  (bnc#1012628).
- USB: serial: option: add support for Foxconn T77W968 LTE modules
  (bnc#1012628).
- staging: comedi: usbduxfast: usbduxfast_ai_cmdtest rounding
  error (bnc#1012628).
- powerpc/book3s64: Fix link stack flush on context switch
  (bnc#1012628).
- KVM: PPC: Book3S HV: Flush link stack on guest exit to host
  kernel (bnc#1012628).
- commit 694287b
* Fri Nov 29 2019 ptesarik@suse.cz
- Update config files (bsc#1158055 LTC#182629).
- commit 632b250
* Thu Nov 28 2019 mkubecek@suse.cz
- series.conf: cleanup
- update mainline reference:
  patches.suse/net-bcmgenet-Add-BCM2711-support.patch
  patches.suse/net-bcmgenet-Add-RGMII_RXID-support.patch
  patches.suse/net-bcmgenet-Add-a-shutdown-callback.patch
  patches.suse/net-bcmgenet-Avoid-touching-non-existent-interrupt.patch
  patches.suse/net-bcmgenet-Fix-error-handling-on-IRQ-retrieval.patch
  patches.suse/net-bcmgenet-Generate-a-random-MAC-if-none-is-valid.patch
  patches.suse/net-bcmgenet-Refactor-register-access-in-bcmgenet_mi.patch
- commit fd0f02f
* Wed Nov 27 2019 nsaenzjulienne@suse.de
- PCI: brcmstb: add MSI capability (jsc#SLE-7772).
- PCI: brcmstb: add Broadcom STB PCIe host controller driver
  (jsc#SLE-7772).
- supported.conf: Add pcie-brcmstb
- Update config files: build pcie-brcmstb as module
- linux/log2.h: Add roundup/rounddown_pow_two64() family of
  functions (jsc#SLE-7772).
- dma-mapping: treat dev->bus_dma_mask as a DMA limit
  (jsc#SLE-7772).
- dma-direct: exclude dma_direct_map_resource from the min_low_pfn
  check (jsc#SLE-7772).
- dma-direct: avoid a forward declaration for phys_to_dma
  (jsc#SLE-7772).
- dma-direct: unify the dma_capable definitions (jsc#SLE-7772).
- x86/PCI: sta2x11: use default DMA address translation
  (jsc#SLE-7772).
- dma-direct: check for overflows on 32 bit DMA addresses
  (jsc#SLE-7772).
- of: Make of_dma_get_range() work on bus nodes (jsc#SLE-7772).
- of/address: Fix of_pci_range_parser_one translation of DMA
  addresses (jsc#SLE-7772).
- of/address: Translate 'dma-ranges' for parent nodes missing
  'dma-ranges' (jsc#SLE-7772).
- of: Factor out #{addr,size}-cells parsing (jsc#SLE-7772).
- of: address: Follow DMA parent for "dma-coherent"
  (jsc#SLE-7772).
- of/address: Introduce of_get_next_dma_parent() helper
  (jsc#SLE-7772).
- PCI: rcar: Use inbound resources for setup (jsc#SLE-7772).
- PCI: iproc: Use inbound resources for setup (jsc#SLE-7772).
- PCI: xgene: Use inbound resources for setup (jsc#SLE-7772).
- PCI: v3-semi: Use inbound resources for setup (jsc#SLE-7772).
- PCI: ftpci100: Use inbound resources for setup (jsc#SLE-7772).
- PCI: of: Add inbound resource parsing to helpers (jsc#SLE-7772).
- PCI: versatile: Enable COMPILE_TEST (jsc#SLE-7772).
- PCI: versatile: Remove usage of PHYS_OFFSET (jsc#SLE-7772).
- PCI: versatile: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: xilinx-nwl: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: xilinx: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: xgene: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: v3-semi: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: rockchip: Drop storing driver private outbound resource
  data (jsc#SLE-7772).
- PCI: rockchip: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: mobiveil: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: mediatek: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: iproc: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: faraday: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: dwc: Use pci_parse_request_of_pci_ranges() (jsc#SLE-7772).
- PCI: altera: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: aardvark: Use pci_parse_request_of_pci_ranges()
  (jsc#SLE-7772).
- PCI: Export pci_parse_request_of_pci_ranges() (jsc#SLE-7772).
- resource: Add a resource_list_first_type helper (jsc#SLE-7772).
- commit 1c7ba00
* Tue Nov 26 2019 mbrugger@suse.com
- net: bcmgenet: Add RGMII_RXID support (jsc#SLE-7772).
- net: bcmgenet: Refactor register access in bcmgenet_mii_config (jsc#SLE-7772).
- net: bcmgenet: Fix error handling on IRQ retrieval (jsc#SLE-7772).
- net: bcmgenet: Avoid touching non-existent interrupt (jsc#SLE-7772).
- net: bcmgenet: Add BCM2711 support (jsc#SLE-7772).
- net: bcmgenet: Add a shutdown callback (jsc#SLE-7772).
- net: bcmgenet: Generate a random MAC if none is valid (jsc#SLE-7772).
- commit 9d632e7
* Mon Nov 25 2019 jslaby@suse.cz
- Refresh patches.suse/net-ath10k-Fix-a-NULL-ptr-deref-bug.patch.
  Update upstream status.
- commit b33144f
* Mon Nov 25 2019 jslaby@suse.cz
- drm/amdgpu: Add DC feature mask to disable fractional pwm
  (bsc#1154010).
- ata: make qc_prep return ata_completion_errors (bnc#1110252).
- ata: define AC_ERR_OK (bnc#1110252).
- ata: sata_mv, avoid trigerrable BUG_ON (bnc#1110252).
- libertas: fix a potential NULL pointer dereference
  (CVE-2019-16232,bsc#1150465).
- commit 42674e2
* Mon Nov 25 2019 jslaby@suse.cz
- mm: refresh ZONE_DMA and ZONE_DMA32 comments in 'enum zone_type'
  (jsc#SLE-7772).
  Port all non-upstream patches from stable to master.
- arm64: use both ZONE_DMA and ZONE_DMA32 (jsc#SLE-7772).
- Update config files.
  Config options taken from commit 4f2941cd44a2.
- arm64: rename variables used to calculate ZONE_DMA32's size
  (jsc#SLE-7772).
- arm64: mm: use arm64_dma_phys_limit instead of calling
  max_zone_dma_phys() (jsc#SLE-7772).
- arm64: dts: broadcom: Add reference to RPi 4 B (jsc#SLE-7772).
- ARM: dts: Add minimal Raspberry Pi 4 support (jsc#SLE-7772).
- ARM: bcm: Add support for BCM2711 SoC (jsc#SLE-7772).
- dt-bindings: arm: bcm2835: Add Raspberry Pi 4 to DT schema
  (jsc#SLE-7772).
- dt-bindings: arm: Convert BCM2835 board/soc bindings to
  json-schema (jsc#SLE-7772).
- ARM: dts: bcm283x: Move BCM2835/6/7 specific to
  bcm2835-common.dtsi (jsc#SLE-7772).
- ARM: dts: bcm283x: Remove brcm, bcm2835-pl011 compatible
  (jsc#SLE-7772).
- ARM: dts: bcm283x: Remove simple-bus from fixed clocks
  (jsc#SLE-7772).
- bluetooth: hci_bcm: Fix RTS handling during startup
  (jsc#SLE-7772).
- commit 19bad9e
* Mon Nov 25 2019 mkubecek@suse.cz
- Update to 5.4 final
- refresh configs (only update headers)
- commit 4c9cd0f
* Sun Nov 24 2019 mkubecek@suse.cz
- config: disable SECURITY_DMESG_RESTRICT (bsc#1157066)
  Enabling this option which restricts access to dmesg was not intentional
  and happened accidentally as part of a commit aiming to enable features
  which were enabled in SLE. We might restrict dmesg in the future if there
  is a consensus but for now the proper action is to revert this accidental
  change which only affected some architectures anyway.
- commit 5c1d459
* Thu Nov 21 2019 lpechacek@suse.com
- Add crypto modules required by tcrypt (FIPS)
  References: bsc#1153192
- commit 0bc5cd1
* Mon Nov 18 2019 mkubecek@suse.cz
- Update to 5.4-rc8
- refresh
  patches.suse/vfs-add-super_operations-get_inode_dev
- update configs
  - add X86_INTEL_TSX_MODE_OFF=y
  - drop VBOXSF_FS (driver dropped for now)
- commit 97aef18
* Thu Nov 14 2019 guillaume.gardet@arm.com
- arm64: Enable CONFIG_IR_GPIO_CIR (boo#1156748)
- commit 3f9623c
* Thu Nov 14 2019 mbrugger@suse.com
- arm64: Update config files.
  Enable HW_RANDOM_OMAP used by machiattobin (bsc#1156466).
- commit 1402755
* Mon Nov 11 2019 mkubecek@suse.cz
- Update to 5.4-rc7
- eliminated 1 patch
- new config option
  - VBOXSF_FS=m (x86 only)
- commit c59faac
* Wed Nov  6 2019 tiwai@suse.de
- rpm/kernel-source.spec.in: Fix dependency of kernel-devel (bsc#1154043)
- commit ceb9273
* Wed Nov  6 2019 afaerber@suse.com
- config: armv7hl: Update to 5.4-rc6
- commit be38a7b
* Wed Nov  6 2019 jslaby@suse.cz
- rpm/kernel-binary.spec.in: add COMPRESS_VMLINUX (bnc#1155921)
  Let COMPRESS_VMLINUX determine the compression used for vmlinux. By
  default (historically), it is gz.
- commit c8b2d9f
* Wed Nov  6 2019 mkubecek@suse.cz
- config: refresh armv6hl/vanilla
- commit 152052e
* Tue Nov  5 2019 afaerber@suse.com
- config: armv6hl: Update to 5.4-rc6
- commit e45bb5a
* Tue Nov  5 2019 mbrugger@suse.com
- rpm/mkspec-dtb: add mt76 based dtb package
- commit 8ff92d0
* Tue Nov  5 2019 jslaby@suse.cz
- stacktrace: Don't skip first entry on noncurrent tasks
  (bnc#1154866).
- commit 897b65b
* Mon Nov  4 2019 msuchanek@suse.de
- rpm/kernel-subpackage-spec: Mention debuginfo in the subpackage
  description (bsc#1149119).
- commit 525ec92
* Mon Nov  4 2019 mkubecek@suse.cz
- Update to 5.4-rc6
- eliminated 1 patch
- refresh configs
- commit 816e8ae
* Thu Oct 31 2019 afaerber@suse.de
- config: arm64: Re-enable default flavor, too
- commit c8cf7fe
* Wed Oct 30 2019 mkubecek@suse.cz
- config: refresh also arm64/vanilla
- commit a48c425
* Wed Oct 30 2019 mkubecek@suse.cz
- config: refresh
- commit cb090f9
* Wed Oct 30 2019 afaerber@suse.de
- config: arm64: Update to 5.4-rc5
- commit 22182c8
* Sun Oct 27 2019 mkubecek@suse.cz
- Update to 4.5-rc5
- New config option:
  - SND_SOC_SOF_HDA_ALWAYS_ENABLE_DMI_L1=n (x86 only)
- commit 13dfd5f
* Wed Oct 23 2019 mkubecek@suse.cz
- series.conf: cleanup
  Move two submitted wireless patches to "on the way to mainline" section.
  No effect on expanded tree.
- commit 21fb44d
* Tue Oct 22 2019 msuchanek@suse.de
- kernel-binary.spec.in: Fix build of non-modular kernels (boo#1154578).
- commit 7f1e881
* Tue Oct 22 2019 acho@suse.com
- rtlwifi: Fix potential overflow on P2P code (bsc#1154372
  CVE-2019-17666).
- commit 6257f3c
* Mon Oct 21 2019 msuchanek@suse.de
- kernel-binary.spec.in: Obsolete kgraft packages only when not building
  them.
- commit 25f7690
* Mon Oct 21 2019 msuchanek@suse.de
- kernel-subpackage-build: create zero size ghost for uncompressed vmlinux
  (bsc#1154354).
  It is not strictly necessary to uncompress it so maybe the ghost file
  can be 0 size in this case.
- commit 4bf73c8
* Mon Oct 21 2019 mkubecek@suse.cz
- Update to 5.4-rc4
- Eliminated 1 patch
- commit bdcace5
* Thu Oct 17 2019 acho@suse.com
- cfg80211: wext: avoid copying malformed SSIDs (bsc#1153158
  CVE-2019-17133).
- commit fd3ccf8
* Wed Oct 16 2019 mkubecek@suse.cz
- Update patches.suse/supported-flag references (add bsc#974406).
- commit df31cdf
* Wed Oct 16 2019 lpechacek@suse.com
- Squash module-Inform-user-when-loading-externally-supported.patch from
  SLE into supported-flag (bsc#974406).
- commit 3fd4e95
* Tue Oct 15 2019 jslaby@suse.cz
- Update config files.
  Disable CONFIG_RT_GROUP_SCHED again (bnc#950955 bnc#1153228).
- commit 53769fe
* Mon Oct 14 2019 mkubecek@suse.cz
- Update to 5.4-rc3
- Refresh configs
- commit 2309d7d
* Mon Oct  7 2019 mkubecek@suse.cz
- Update to 5.4-rc2
- Eliminated 2 patches
- Refresh config/i386/default
- commit 5b664b4
* Mon Oct  7 2019 mkubecek@suse.cz
- Delete
  patches.suse/module-swap-the-order-of-symbol.namespace.patch.
  This is not the patch fixing bogus modpost warnings when building
  out-of-tree modules. The patch supposed to fix them, when applied on its
  own, makes modpost segfault. So let's better live with the warnings until
  this is sorted in upstream.
- commit 5bf1873
* Sun Oct  6 2019 mkubecek@suse.cz
- module: swap the order of symbol.namespace.
  Fixes bogus modpost warnings when building out-of-tree modules.
- commit c3db450
* Fri Oct  4 2019 vbabka@suse.cz
- config: enable DEBUG_PAGEALLOC (jsc#PM-1168, bsc#1144653)
  Build with page allocation debugging (boot with debug_pagealloc=on to enable).
- commit ff41b2d
* Wed Oct  2 2019 mkubecek@suse.cz
- s390: mark __cpacf_query() as __always_inline.
  Fix s390x/zfcpdump build.
- commit 6fce476
* Tue Oct  1 2019 mkubecek@suse.cz
- config: refresh vanilla configs
  Configs for vanilla flavor also need a refresh.
- commit f67b42c
* Tue Oct  1 2019 mkubecek@suse.cz
- config: enable X86_5LEVEL (jsc#SLE-9308)
  Enable 5-level page tables (x86_64 architecture only).
- commit 4e52759
* Tue Oct  1 2019 mkubecek@suse.cz
- Update to 5.4-rc1
- Eliminated 23 patches (22 stable, 1 other)
- ARM configs need update
- Refresh
  patches.rpmify/scripts-mkmakefile-honor-second-argument.patch
  patches.suse/Revert-netfilter-conntrack-remove-helper-hook-again.patch
  patches.suse/btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  patches.suse/supported-flag
  patches.suse/supported-flag-external
  patches.suse/vfs-add-super_operations-get_inode_dev
- fix 32-bit builds:
  patches.rpmify/mlx5-avoid-64-bit-division-in-dr_icm_pool_mr_create.patch
- New config options:
  - General setup
  - UCLAMP_TASK_GROUP=n
  - MODULE_ALLOW_MISSING_NAMESPACE_IMPORTS=n
  - Power management and ACPI options
  - CPU_IDLE_GOV_HALTPOLL=y
  - HALTPOLL_CPUIDLE=m
  - Block layer
  - BLK_CGROUP_IOCOST=y
  - DM_CLONE=m
  - DM_VERITY_VERIFY_ROOTHASH_SIG=n
  - Memory Management
  - READ_ONLY_THP_FOR_FS=y
  - Networking
  - NET_TC_SKB_EXT=y
  - CAN_J1939=m
  - CAN_KVASER_PCIEFD=m
  - CAN_M_CAN_PLATFORM=m
  - CAN_M_CAN_TCAN4X5X=m
  - CAN_F81601=m
  - NET_DSA_MICROCHIP_KSZ9477_I2C=m
  - NET_DSA_MICROCHIP_KSZ8795=m
  - NET_DSA_MICROCHIP_KSZ8795_SPI=m
  - NET_DSA_SJA1105_TAS=y
  - MLX5_SW_STEERING=y
  - NET_VENDOR_PENSANDO=y
  - IONIC=m
  - ADIN_PHY=m
  - ATH9K_PCI_NO_EEPROM=m
  - Power management
  - SENSORS_AS370=m
  - SENSORS_INSPUR_IPSPS=m
  - REGULATOR_SY8824X=m
  - Graphics
  - DRM_AMD_DC_DCN2_1=y
  - DRM_GM12U320=m
  - Sound
  - SND_HDA_INTEL_DETECT_DMIC=y
  - SND_SOC_INTEL_CML_LP_DA7219_MAX98357A_MACH=m
  - SND_SOC_SOF_TIGERLAKE_SUPPORT=y
  - SND_SOC_SOF_ELKHARTLAKE_SUPPORT=y
  - SND_SOC_UDA1334=n
  - SND_SOC_SOF_OF=m
  - USB
  - USB_CONN_GPIO=m
  - USB_CDNS3=m
  - USB_CDNS3_HOST=y
  - USB_CDNS3_PCI_WRAP=m
  - Platform support
  - CROS_EC=m
  - CROS_EC_CHARDEV=m
  - CROS_EC_LIGHTBAR=m
  - CROS_EC_DEBUGFS=m
  - CROS_EC_SYSFS=m
  - CROS_EC_VBC=m
  - Industrial I/O
  - ADIS16460=n
  - NOA1305=n
  - MAX5432=n
  - Misc drivers
  - EFI_RCI2_TABLE=n
  - MTD_NAND_MXIC=m
  - JOYSTICK_FSIA6B=m
  - REMOTEPROC=n
  - SERIAL_FSL_LINFLEXUART=m
  - MFD_CROS_EC_DEV=m
  - W1_MASTER_SGI=m
  - W1_SLAVE_DS250X=m
  - VIDEO_OV5675=m
  - HID_CREATIVE_SB0540=m
  - DMABUF_SELFTESTS=n
  - MOXTET=n
  - File systems
  - FS_VERITY=y
  - FS_VERITY_DEBUG=n
  - FS_VERITY_BUILTIN_SIGNATURES=n
  - VIRTIO_FS=m
  - EXFAT_FS=m
  - EXFAT_DONT_MOUNT_VFAT=y
  - EXFAT_DISCARD=y
  - EXFAT_DELAYED_SYNC=n
  - EXFAT_KERNEL_DEBUG=n
  - EXFAT_DEBUG_MSG=n
  - EXFAT_DEFAULT_CODEPAGE=437
  - EXFAT_DEFAULT_IOCHARSET="utf8"
  - Security
  - SECURITY_LOCKDOWN_LSM=y
  - SECURITY_LOCKDOWN_LSM_EARLY=y
  - LOCK_DOWN_KERNEL_FORCE_NONE=y
  - IMA_DEFAULT_HASH_SHA512=n
  - IMA_APPRAISE_MODSIG=y
  - RANDOM_TRUST_BOOTLOADER=y
  - KEXEC_SIG=y
  - KEXEC_SIG_FORCE=n
  - KEXEC_BZIMAGE_VERIFY_SIG=y
  - Cryptographic API
  - CRYPTO_ESSIV=m
  - CRYPTO_DEV_CCP_DEBUGFS=n
  - CRYPTO_DEV_SAFEXCEL=m
  - PowerPC
  - PPC_SVM=y
  - OPAL_CORE=n
  - S/390
  - CRYPTO_SHA3_256_S390=m
  - CRYPTO_SHA3_512_S390=m
- commit 0599162
* Wed Sep 25 2019 fvogt@suse.com
- config: Enable dual-role modes for DWC on arm64 as well
- CONFIG_USB_DWC2_DUAL_ROLE=y and CONFIG_USB_DWC3_DUAL_ROLE=y
- Previously that was only enabled on armv6/armv7
- commit 4940602
* Tue Sep 24 2019 hare@suse.de
- Compile nvme.ko as module (bsc#1150846, bsc#1150850, bsc#1161889)
- commit 4caf1f7
* Sat Sep 21 2019 jslaby@suse.cz
- Linux 5.3.1 (bnc#1012628).
- media: technisat-usb2: break out of loop at end of buffer
  (bnc#1012628).
- floppy: fix usercopy direction (bnc#1012628).
- phy: qcom-qmp: Correct ready status, again (bnc#1012628).
- ovl: fix regression caused by overlapping layers detection
  (bnc#1012628).
- Revert "arm64: Remove unnecessary ISBs from set_{pte,pmd,pud}"
  (bnc#1012628).
- nl80211: Fix possible Spectre-v1 for CQM RSSI thresholds
  (bnc#1012628).
- tty/serial: atmel: reschedule TX after RX was started
  (bnc#1012628).
- serial: sprd: correct the wrong sequence of arguments
  (bnc#1012628).
- firmware: google: check if size is valid when decoding VPD data
  (bnc#1012628).
- Documentation: sphinx: Add missing comma to list of strings
  (bnc#1012628).
- KVM: coalesced_mmio: add bounds checking (bnc#1012628).
- net: stmmac: Hold rtnl lock in suspend/resume callbacks
  (bnc#1012628).
- net: dsa: Fix load order between DSA drivers and taggers
  (bnc#1012628).
- xen-netfront: do not assume sk_buff_head list is empty in
  error handling (bnc#1012628).
- udp: correct reuseport selection with connected sockets
  (bnc#1012628).
- net_sched: let qdisc_put() accept NULL pointer (bnc#1012628).
- net/sched: fix race between deactivation and dequeue for NOLOCK
  qdisc (bnc#1012628).
- ip6_gre: fix a dst leak in ip6erspan_tunnel_xmit (bnc#1012628).
- phy: renesas: rcar-gen3-usb2: Disable clearing VBUS in
  over-current (bnc#1012628).
- media: tm6000: double free if usb disconnect while streaming
  (bnc#1012628).
- USB: usbcore: Fix slab-out-of-bounds bug during device reset
  (bnc#1012628).
- commit f187578
* Wed Sep 18 2019 jroedel@suse.de
- Update config files.
  Disable CONFIG_ARM_SMMU_DISABLE_BYPASS_BY_DEFAULT. Not all drivers are
  ready for this yet, so enabling this config option causes regressions.
  See bsc#1150577 for an example.
- commit f759adc
* Mon Sep 16 2019 mkubecek@suse.cz
- Update to 5.3 final
- Eliminated 3 patches
- Refresh configs
  - NF_CONNTRACK_SLP is gone
- commit 6baef36
* Tue Sep 10 2019 mkubecek@suse.cz
- Delete patches.suse/netfilter-ip_conntrack_slp.patch (FATE#324143 jsc#SLE-8944 bsc#1127886).
  This veteran out of tree patch is no longer needed since the userspace
  conntrack helper (in conntrack-tools / conntrackd) has reached Factory.
- commit d6f0b71
* Tue Sep 10 2019 mkubecek@suse.cz
- Update and reenable
  patches.suse/Revert-netfilter-conntrack-remove-helper-hook-again.patch
  (FATE#324143 jsc#SLE-8944 bsc#1127886).
- commit 029452e
* Mon Sep  9 2019 mgorman@suse.de
- config: enable SLAB_FREELIST_HARDENED (bsc#1127808)
  Enable SLAB_FREELIST_HARDENED on all architectures. This obscures the
  free object pointer on a per-cache basis making it more difficult to
  locate kernel objects via exploits probing the cache metadata.
  This change was requested by the upstream openSUSE community to make
  the kernel more resistent to slab freelist attacks. Tests conducted
  by the kernel performance teams confirmed that the performance impact
  is detectable but negligible.
- commit 39e9013
* Mon Sep  9 2019 guillaume.gardet@arm.com
- rpm/constraints.in: lower disk space required for ARM
  With a requirement of 35GB, only 2 slow workers are usable for ARM.
  Current aarch64 build requires 27G and armv6/7 requires 14G.
  Set requirements respectively to 30GB and 20GB.
- commit f84c163
* Mon Sep  9 2019 mkubecek@suse.cz
- Update to 5.3-rc8
- refresh armv6hl configs (IXP4xx drivers no longer visible)
- commit 3dea797
* Mon Sep  9 2019 mkubecek@suse.cz
- config: enable STACKPROTECTOR_STRONG also on armv6hl
  Recently reenabled armv6hl architecture has STACKPROTECTOR_STRONG disabled,
  enable it here as well.
- commit 8c0677d
* Tue Sep  3 2019 mkubecek@suse.cz
- config: enable STACKPROTECTOR_STRONG (jsc#SLE-9120 bsc#1130365)
  Enable CONFIG_STACKPROTECTOR_STRONG on all architectures except s390x
  (where the feature is not available). This extends the number of functions
  which are protected by "stack canary" check to catch functions writing past
  their stack frame.
  This change was requested by SUSE security to make our kernels more
  resistant to some types of stack overflow attacks. Tests performed by
  kernel performance teams confirmed that performance impact is acceptable.
- commit 4c43fab
* Mon Sep  2 2019 mkubecek@suse.cz
- Update to 5.3-rc7
- Refresh configs
  - IXP4xx SoC drivers not visible
  - gcc 9.2.1
- commit 9bff5f9
* Sun Sep  1 2019 mkubecek@suse.cz
- config: armv7hl: Enable cadence watchdog
  CONFIG_CADENCE_WATCHDOG is required for Zynq-7000 based MIYR Zturn board.
- commit c4cbe5e
* Fri Aug 30 2019 dmueller@suse.com
- config.conf: Update ARMv6 config files
- commit c17167d
* Fri Aug 30 2019 dmueller@suse.com
- config.conf: Reenable ARMv7 config for Kernel 5.3
  All modules plus errata's enabled. Reused other
  values from x86_64 update.
- commit b1c627e
* Wed Aug 28 2019 tiwai@suse.de
- mwifiex: Fix three heap overflow at
  parsing element in cfg80211_ap_settings
  (CVE-2019-14814,bsc#1146512,CVE-2019-14815,bsc#1146514,CVE-2019-14816,bsc#1146516).
- commit 528fd68
* Wed Aug 28 2019 mkubecek@suse.cz
- supported.conf: mark more core networking modules supported
  Two more netfilter modules and one more *_diag should be supported too.
- commit bee2dd8
* Wed Aug 28 2019 mkubecek@suse.cz
- supported.conf: update status of some networking core modules
  This marks new networking modules which should be supported as such; it is
  mostly netfilter and traffic control modules which have been following the
  "support all of them" policy for some time.
- commit 65e1131
* Wed Aug 28 2019 mkubecek@suse.cz
- supported.conf: obsolete paths cleanup
  Update paths for existing modules which were moved, clean up duplicate
  entries and drop entries for modules which no longer exist (either not
  built any more or built into the image now).
- commit 3bb142a
* Tue Aug 27 2019 mkubecek@suse.cz
- rpm: raise required disk space for binary packages
  Current disk space constraints (10 GB on s390x, 25 GB on other
  architectures) no longer suffice for 5.3 kernel builds. The statistics
  show ~30 GB of disk consumption on x86_64 and ~11 GB on s390x so raise
  the constraints to 35 GB in general and 14 GB on s390x.
- commit 527cb66
* Mon Aug 26 2019 jgross@suse.com
- usb: Introduce Xen pvUSB frontend (xen hcd) (fate#315712).
- Update config files.
- usb: Add Xen pvUSB protocol description (fate#315712).
- commit b32b2bd
* Mon Aug 26 2019 tiwai@suse.de
- Update reference for ath6kl fix (CVE-2019-15290,bsc#1146543).
- commit b08d3d5
* Mon Aug 26 2019 tiwai@suse.de
- Fix a NULL-ptr-deref bug in ath6kl_usb_alloc_urb_from_pipe
  (CVE-2019-15098,bsc#1146378).
- Fix a NULL-ptr-deref bug in ath10k_usb_alloc_urb_from_pipe
  (CVE-2019-15099,bsc#1146368).
- commit 758e216
* Mon Aug 26 2019 bpoirier@suse.com
- Fix a double free bug in rsi_91x_deinit (bnc#1147116
  CVE-2019-15504).
- commit 8ae43d1
* Sun Aug 25 2019 mkubecek@suse.cz
- Update to 5.3-rc6
- commit 2831011
* Fri Aug 23 2019 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Fix kernel-livepatch description typo.
- commit 36acf91
* Thu Aug 22 2019 msuchanek@suse.de
- Pull packaging cleanup from mkubecek.
- Parametrize kgraft vs livepatch.
- commit 16f6816
* Thu Aug 22 2019 msuchanek@suse.de
- rpm/config.sh: Enable livepatch.
- commit e001776
* Thu Aug 22 2019 mkubecek@suse.cz
- config: update from SLE15-SP2
  In general, we want features and drivers from SLE also in openSUSE unless
  we have a good reason not to. Enable most config options which were
  disabled in master but enabled in SLE15-SP2 (inherited from SLE15-SP1).
- commit 769684a
* Wed Aug 21 2019 mkubecek@suse.cz
- series.conf: reorganize sections
  With ~40 patches in master branch, we have accumulated way too many
  sections in series.conf, some of them being very specific. While new SLE
  and Leap branches are going to have more patches, vast majority of them is
  going to end up in the sorted section (e.g. less than 1%% of SLE15-SP1
  patches are neither sorted nor stable baskports right now - and that
  includes quite a few which would actually belong into the sorted section
  but are left outside for historical reasons).
  After the reorganization, series.conf is ordered like this:
  - stable backports (patches.kernel.org/*)
  - tweaks applied to vanilla (patches.rpmify/*)
  - sorted section (not in master)
  - unsorted patches expected to get into mainline soon
  - permanent and longterm non-upstream patches
  - kabi hacks (not in master)
  This commit has no effect on expanded tree.
- commit 8ac1895
* Wed Aug 21 2019 mkubecek@suse.cz
- series.conf: cleanup
  Only whitespace and comments, no efect on expanded tree.
- commit bf21808
* Mon Aug 19 2019 bp@suse.de
- Update config files.
  As per https://jira.suse.com/browse/SLE-7041
  Factory first!
- commit 126cef1
* Mon Aug 19 2019 mkubecek@suse.cz
- Update to 5.3-rc5
- Refresh configs
  - RDMA_SIW available on i386 (=m)
  - clean up unavailable options
- commit cadbe00
* Sun Aug 18 2019 afaerber@suse.de
- config: arm64: Enable I2C_IMX (boo#1146026)
  Needed for Google Coral board.
- commit 8803b04
* Thu Aug 15 2019 msuchanek@suse.de
- Revert "Workaround gcc regression on ppc64 (bko#204125)."
  This reverts commit 8b84d1d46ff90146bb6ba5b760a54ddd87a1a680.
  Works for me 5.3-rc4-65-g329120423947
- commit d8f9e6c
* Mon Aug 12 2019 msuchanek@suse.de
- config.conf: syms should not depend on kernel-zfcpdump
  Kernel-zfcpdump is not modular so kernel-zfcpdump-devel does not make
  sense and is not built. kernel-syms cannot depend on it.
- commit 473ac28
* Mon Aug 12 2019 msuchanek@suse.de
- rpm/mkspec: Correct tarball URL for rc kernels.
- commit c4ef18d
* Sun Aug 11 2019 mkubecek@suse.cz
- Update to 5.3-rc4
- Refresh
  - patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
- commit 5402233
* Fri Aug  9 2019 msuchanek@suse.de
- rpm/config.sh: Enable building DTBs.
- commit 7de292a
* Fri Aug  9 2019 msuchanek@suse.de
- rpm/mkspec: Make building DTBs optional.
- commit 7c057c8
* Fri Aug  9 2019 mkubecek@suse.cz
- supported.conf: fix supported modules depending on unsupported on non-x86_64 architectures
  Some more "unsupported module needed by supported one" errors were reported
  on aarch64 and ppc64le.
- commit 6b609de
* Fri Aug  9 2019 mkubecek@suse.cz
- supported.conf: drop obsolete entry for hyperv_fb
  The module moved to a different directory, the obsolete entry causes
  file conflict betwen kernel-default and kernel-default-extra.
- commit 6b112e5
* Fri Aug  9 2019 msuchanek@suse.de
- rpm/modflist: Simplify compression support.
- commit fd135a6
* Fri Aug  9 2019 mkubecek@suse.cz
- supported.conf: close with respect to dependencies
  Modules which some supported module depends on must be supported as well.
  Also drop obsolete entries for rtsx_pci and rtsx_usb which were moved
  between 4.12 and 5.3.
- commit b781c36
* Fri Aug  9 2019 mkubecek@suse.cz
- rpm: support compressed modules
  Some of our scripts and scriptlets in rpm/ do not expect module files not
  ending with ".ko" which currently leads to failure in preuninstall
  scriptlet of cluster-md-kmp-default (and probably also other subpackages).
  Let those which could be run on compressed module files recognize ".ko.xz"
  in addition to ".ko".
- commit 18fcdff
* Fri Aug  9 2019 msuchanek@suse.de
- Bring back MODVERDIR to Makefile.modpost (bsc#1066369).
- commit 6cc69f5
* Fri Aug  9 2019 mkubecek@suse.cz
- supported.conf: sort again
  Make the order compatible with scripts/supported-conf-fixup (LC_ALL=C).
- commit 4a4b5dd
* Fri Aug  9 2019 msuchanek@suse.de
- supported.conf: Sort alphabetically, align comments.
- commit 5189766
* Fri Aug  9 2019 mkubecek@suse.cz
- supported.conf: drop extensions
  To make things more consistent, drop all ".ko" extensions.
- commit 398461b
* Fri Aug  9 2019 mkubecek@suse.cz
- Update patches.suse/supported-flag.
  Fix ReST table.
- commit 0692bf4
* Thu Aug  8 2019 msuchanek@suse.de
- Use upstream TAINT_AUX for TAINT_EXTERNAL_SUPPORT.
  Refresh patches.suse/supported-flag.
- commit a4999e0
* Thu Aug  8 2019 dmueller@suse.com
- rpm/kernel-obs-build.spec.in: add dm-crypt for building with cryptsetup
  Co-Authored-By: Adam Spiers <aspiers@suse.com>
- commit 7cf5b9e
* Thu Aug  8 2019 mkubecek@suse.cz
- supported.conf: add missing entries for all architectures
  As list of built modules depends on architecture, we must also add entries
  for modules which are not built (or do not even exist) on x86_64 but are
  built on other architectures (aarch64, ppc64le, s390x).
- commit 8f74082
* Thu Aug  8 2019 mkubecek@suse.cz
- supported.conf: add missing entries
  Add all modules currently built but not listed in supported.conf.
  Another update will be necessary once we replace configs inherited from
  master with true SLE15-SP2 configs. This is also why entries for modules
  not built are left in the file for now.
- commit 0f5033c
* Thu Aug  8 2019 mkubecek@suse.cz
- supported.conf: sort
  Also remove one commented out line.
- commit b539157
* Thu Aug  8 2019 mkubecek@suse.cz
- supported.conf: cleanup
  Remove duplicate and shadowed entries.
- commit 25e91ec
* Thu Aug  8 2019 mkubecek@suse.cz
- supported.conf: update from SLE15-SP1
  Differences from current SLE15-SP1 supported.conf:
  - f71808e_wdt and it87_wdt supported (jdelvare)
  - bpfilter marked +base (tiwai, bsc#1106751)
  - unified indentation
- commit 02162e4
* Wed Aug  7 2019 msuchanek@suse.de
- rpm/kernel-binary.spec.in: support partial rt debug config.
- commit af37821
* Wed Aug  7 2019 afaerber@suse.de
- config: arm64: Update to 5.3-rc3
- commit f1f49f3
* Wed Aug  7 2019 afaerber@suse.de
- config: Enable SENSORS_GPIO_FAN for all of Arm (boo#1144723)
  We already had it for armv6hl but were lacking it on arm64.
  Add it on armv7hl for consistency while at it.
- commit 607ebeb
* Mon Aug  5 2019 mkubecek@suse.cz
- Update to 5.3-rc3
- Eliminated 1 patch
- Refresh
  - patches.suse/supported-flag
  - patches.suse/supported-flag-external
- Refresh configs
- commit 571863b
* Fri Aug  2 2019 bwiedemann@suse.de
- kernel-binary: Drop .kernel-binary.spec.buildenv (boo#1154578).
  Without this patch,
  /usr/src/linux-@VERSION@-@RELEASE_SHORT@-obj/x86_64/vanilla/.kernel-binary.spec.buildenv
  contained rpm %%_smp_mflags in a line like
  export MAKE_ARGS=" --output-sync -j4"
  This made it hard to produce bit-identical builds.
- commit 789d131
* Thu Aug  1 2019 mkubecek@suse.cz
- config: refresh x86_64/default
  With HBMC_AM654 disabled, nothing selects MULTIPLEXER any more.
- commit 07a1a73
* Wed Jul 31 2019 jdelvare@suse.de
- Update config files: CONFIG_HBMC_AM654=n
  The TI AM654 is an ARM64 SoC, so disable the driver on all other
  architectures.
- commit 042f63f
* Tue Jul 30 2019 schwab@suse.de
- packaging: add support for riscv64
- commit c2885ea
* Sun Jul 28 2019 mkubecek@suse.cz
- Update to 5.3-rc2
- Eliminated 1 patch
  - patches.suse/dma-mapping-use-dma_get_mask-in-dma_addressing_limit.patch
- Refresh
  - patches.suse/netfilter-ip_conntrack_slp.patch
- Config changes
  - NF_TABLES_BRIDGE=m (was =y)
- commit fc5ebf3
* Sat Jul 27 2019 msuchanek@suse.de
- rpm/macros.kernel-source: KMPs should depend on kmod-compat to build.
  kmod-compat links are used in find-provides.ksyms, find-requires.ksyms,
  and find-supplements.ksyms in rpm-config-SUSE.
- commit f97ca49
* Sat Jul 27 2019 msuchanek@suse.de
- scripts/run_oldconfig.sh: Fix update-vanilla
  When CC is set we want to use it for native only. Cross-compilation
  still needs the crosscompilers.
- commit 3b9fcdb
* Wed Jul 24 2019 msuchanek@suse.de
- dma-mapping: use dma_get_mask in dma_addressing_limited
  (https://lore.kernel.org/lkml/cda1952f-0265-e055-a3ce-237c59069a3f@suse.com/T/#u).
- commit c584343
* Wed Jul 24 2019 msuchanek@suse.de
- scripts/arch-symbols: add missing link.
- commit ee7c635
* Tue Jul 23 2019 tiwai@suse.de
- rpm/config.sh: enable kernel module compression (bsc#1135854)
- commit b333e24
* Tue Jul 23 2019 tiwai@suse.de
- Add kernel module compression support (bsc#1135854)
  For enabling the kernel module compress, add the item COMPRESS_MODULES="xz"
  in config.sh, then mkspec will pass it to the spec file.
- commit cdf5806
* Tue Jul 23 2019 msuchanek@suse.de
- Workaround gcc regression on ppc64 (bko#204125).
- commit 8b84d1d
* Tue Jul 23 2019 msuchanek@suse.de
- config.conf: Add ppc64 kvmsmall config (bsc#1137361).
- Remove superfluous i2c drivers from ppc64 config
  - CONFIG_I2C_ALGOPCA=m
  - CONFIG_I2C_AMD8111=m
  - CONFIG_I2C_CBUS_GPIO=m
  - CONFIG_I2C_DESIGNWARE_CORE=y
  - CONFIG_I2C_DESIGNWARE_PLATFORM=y
  - CONFIG_I2C_DESIGNWARE_PCI=m
  - CONFIG_I2C_OCORES=m
  - CONFIG_I2C_PCA_PLATFORM=m
  Can't get rid of i2c in kvmsmall anyway but at least the DW i2c is gone.
- commit 3d0102c
* Tue Jul 23 2019 jeffm@suse.com
- config: enable PPPoE for kvmsmall (bsc#1133945).
- commit 39d218a
* Mon Jul 22 2019 jeffm@suse.com
- config: remove unnecessary drivers from kvmsmall
  The initial merge was incomplete and needed revisiting, which didn't really
  happen.  Since then, new options have been added and not removed from
  kvmsmall, leading to grow in size.
  This commit uses the following blacklist:
  _(BT|CHARGER|CHROMEOS|CROS|DVB|DW|EDAC|FPGA|GPIO|GNSS|HID|INFINIBAND|IR|JOYSTICK|LEDS|MFD|PINCTRL|REGULATOR|RTC|SENSORS|SND_SOC|STAGING|TOUCHSCREEN|VIDEO|XEN|XILINX)[_=]
  ... along with some manual removal of NET_VENDORs with no relevant drivers.
- commit e850d85
* Mon Jul 22 2019 mkubecek@suse.cz
- rpm/klp-symbols: update to work with kernel >= 5.3
  Since mainline commit b7dca6dd1e59 ("kbuild: create *.mod with full
  directory path and remove MODVERDIR") in v5.3-rc1, *.mod files are created
  in the build tree rather than in a single directory .tmp_versions
  ($MODVERDIR). They also do not provide path to the *.ko module file on
  their first line as the path is the same (except for the suffix).
  Update klp-symbols script to handle this new layout and format of *.mod
  files to fix build of 5.3-rc1 and newer kernel.
  Note: this is a quick band-aid to fix master branch build without risk of
  breaking any other branch. A more proper cleanup will follow.
- commit c32f8e7
* Mon Jul 22 2019 mkubecek@suse.cz
- Update to 5.3-rc1
- Eliminated 89 patches (83 stable, 6 other)
- ARM configs need update
- Refresh
  patches.suse/btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  patches.suse/netfilter-ip_conntrack_slp.patch
  patches.suse/rpm-kernel-config
  patches.suse/supported-flag
  patches.suse/vfs-add-super_operations-get_inode_dev
- replace patches.rpmify/BPF-UMH-do-not-detect-if-compiler-can-link-userspace.patch
  with patches.rpmify/Kconfig-make-CONFIG_CC_CAN_LINK-always-true.patch
- New config options:
  - General setup
  - HEADER_TEST=y
  - KERNEL_HEADER_TEST=y
  - PREEMPT_LL=n
  - UCLAMP_TASK=y
  - UCLAMP_BUCKETS_COUNT=5
  - Processor type and features
  - ACRN_GUEST=y
  - LEGACY_VSYSCALL_XONLY=y
  - IO Schedulers
  - BFQ_CGROUP_DEBUG=n (=y in */debug)
  - Networking
  - NFT_SYNPROXY=m
  - NFT_BRIDGE_META=m
  - NF_CONNTRACK_BRIDGE=m
  - NET_ACT_MPLS=m
  - NET_ACT_CTINFO=m
  - NET_ACT_CT=m
  - BT_HCIBTUSB_MTK=y
  - GVE=m
  - MLX5_FPGA_IPSEC=y
  - MLX5_FPGA_TLS=y
  - MLX5_TLS=y
  - STMMAC_SELFTESTS=n
  - XILINX_AXI_EMAC=m
  - SFP=m
  - NXP_TJA11XX_PHY=m
  - PHY_MIXEL_MIPI_DPHY=m
  - File systems
  - UBIFS_FS_ZSTD=y
  - SUNRPC_DISABLE_INSECURE_ENCTYPES=n
  - CEPH_FS_SECURITY_LABEL=y
  - Generic driver options
  - FW_LOADER_COMPRESS=y
  - Storage
  - SCSI_FDOMAIN_PCI=m
  - SCSI_FDOMAIN_ISA=n
  - PCMCIA_FDOMAIN=n
  - Input
  - KEYBOARD_APPLESPI=m
  - Power supply and hardware monitoring
  - POWER_SUPPLY_HWMON=y
  - CHARGER_WILCO=m
  - SENSORS_IRPS5401=m
  - SENSORS_PXE1610=m
  - REGULATOR_ARIZONA_LDO1=m
  - REGULATOR_ARIZONA_MICSUPP=m
  - REGULATOR_SLG51000=m
  - Multimedia
  - DVB_USB_CXUSB_ANALOG=y
  - VIDEO_TDA1997X=m
  - VIDEO_TLV320AIC23B=m
  - VIDEO_ADV7180=m
  - VIDEO_ADV7183=m
  - VIDEO_ADV7604=m
  - VIDEO_ADV7604_CEC=y
  - VIDEO_ADV7842=m
  - VIDEO_ADV7842_CEC=y
  - VIDEO_BT819=m
  - VIDEO_BT856=m
  - VIDEO_BT866=m
  - VIDEO_KS0127=m
  - VIDEO_ML86V7667=m
  - VIDEO_SAA7110=m
  - VIDEO_TC358743=m
  - VIDEO_TC358743_CEC=y
  - VIDEO_TVP514X=m
  - VIDEO_TVP7002=m
  - VIDEO_TW9910=m
  - VIDEO_VPX3220=m
  - VIDEO_SAA7185=m
  - VIDEO_ADV7170=m
  - VIDEO_ADV7175=m
  - VIDEO_ADV7343=m
  - VIDEO_ADV7393=m
  - VIDEO_ADV7511=m
  - VIDEO_ADV7511_CEC=y
  - VIDEO_AD9389B=m
  - VIDEO_AK881X=m
  - VIDEO_THS8200=m
  - VIDEO_IMX214=m
  - VIDEO_IMX258=m
  - VIDEO_IMX274=m
  - VIDEO_IMX319=m
  - VIDEO_IMX355=m
  - VIDEO_OV2659=m
  - VIDEO_OV2680=m
  - VIDEO_OV2685=m
  - VIDEO_OV5647=m
  - VIDEO_OV6650=m
  - VIDEO_OV5670=m
  - VIDEO_OV5695=m
  - VIDEO_OV7251=m
  - VIDEO_OV772X=m
  - VIDEO_OV7740=m
  - VIDEO_OV8856=m
  - VIDEO_OV9640=m
  - VIDEO_OV9650=m
  - VIDEO_OV13858=m
  - VIDEO_VS6624=m
  - VIDEO_MT9M001=m
  - VIDEO_MT9M032=m
  - VIDEO_MT9M111=m
  - VIDEO_MT9P031=m
  - VIDEO_MT9T001=m
  - VIDEO_MT9T112=m
  - VIDEO_MT9V032=m
  - VIDEO_MT9V111=m
  - VIDEO_SR030PC30=m
  - VIDEO_NOON010PC30=m
  - VIDEO_M5MOLS=m
  - VIDEO_RJ54N1=m
  - VIDEO_S5K6AA=m
  - VIDEO_S5K6A3=m
  - VIDEO_S5K4ECGX=m
  - VIDEO_S5K5BAF=m
  - VIDEO_SMIAPP=m
  - VIDEO_ET8EK8=m
  - VIDEO_S5C73M3=m
  - VIDEO_AD5820=m
  - VIDEO_AK7375=m
  - VIDEO_DW9714=m
  - VIDEO_DW9807_VCM=m
  - VIDEO_ADP1653=m
  - VIDEO_LM3560=m
  - VIDEO_LM3646=m
  - SDR_MAX2175=m
  - VIDEO_THS7303=m
  - VIDEO_I2C=m
  - VIDEO_ST_MIPID02=n
  - VIDEO_GS1662=m
  - DVB_S5H1432=m
  - DVB_DIB9000=m
  - DVB_CXD2880=m
  - DVB_MN88443X=m
  - DVB_LNBH29=m
  - DVB_LGS8GL5=m
  - Graphics
  - DRM_AMD_DC_DCN2_0=y
  - DRM_AMD_DC_DSC_SUPPORT=y
  - DRM_I915_FORCE_PROBE=""
  - DRM_I915_DEBUG_MMIO=n
  - DRM_I915_USERFAULT_AUTOSUSPEND=250
  - DRM_I915_SPIN_REQUEST=5
  - DRM_PANEL_OSD_OSD101T2587_53TS=m
  - DRM_PANEL_SAMSUNG_S6E63M0=m
  - Sound
  - SND_SOC_INTEL_CML_H=m
  - SND_SOC_INTEL_CML_LP=m
  - SND_SOC_INTEL_BYT_CHT_CX2072X_MACH=m
  - SND_SOC_SOF_COMETLAKE_LP_SUPPORT=y
  - SND_SOC_SOF_COMETLAKE_H_SUPPORT=y
  - SND_SOC_CX2072X=m
  - InfiniBand
  - RDMA_SIW=m
  - Platform specific drivers
  - XIAOMI_WMI=m
  - ACPI_CMPC=m
  - SAMSUNG_Q10=m
  - INTEL_SPEED_SELECT_INTERFACE=m
  - CROS_EC_ISHTP=m
  - WILCO_EC_EVENTS=m
  - WILCO_EC_TELEMETRY=m
  - Industrial I/O
  - XILINX_XADC=n
  - ADF4371=n
  - DPS310=n
  - LEDs
  - LEDS_SPI_BYTE=m
  - LEDS_TI_LMU_COMMON=m
  - LEDS_LM3697=m
  - LEDS_LM36274=m
  - Other drivers
  - MTD_HYPERBUS=m
  - HBMC_AM654=m
  - XILINX_SDFEC=n
  - GPIO_XILINX=m
  - WATCHDOG_OPEN_TIMEOUT=0
  - MFD_CS47L15=y
  - MFD_CS47L92=y
  - MFD_ROHM_BD70528=n
  - RTC_DRV_BD70528=m
  - DW_EDMA=m
  - DW_EDMA_PCIE=m
  - COMMON_CLK_SI5341=m
  - EXTCON_FSA9480=m
  - NTB_MSI=y
  - NTB_MSI_TEST=n
  - RAS_CEC_DEBUG=n
  - AL_FIC=n
  - Virtualization
  - VIRTIO_PMEM=m
  - Security options
  - KEYS_REQUEST_CACHE=y
  - Kernel hardening options
  - INIT_ON_ALLOC_DEFAULT_ON=n
  - INIT_ON_FREE_DEFAULT_ON=n
  - Cryptographic API
  - CRYPTO_XXHASH=n
  - CRYPTO_DEV_ATMEL_ECC=m
  - CRYPTO_DEV_ATMEL_SHA204A=m
  - Kernel hacking
  - HEADERS_INSTALL=n
  - REED_SOLOMON_TEST=n
  - TEST_BLACKHOLE_DEV=n
  - TEST_MEMINIT=n
- commit 0a6d0d9
* Sun Jul 21 2019 mkubecek@suse.cz
- Revert "netfilter: conntrack: remove helper hook again"
  (http://lkml.kernel.org/r/20190718092128.zbw4qappq6jsb4ja@breakpoint.cc).
- commit 8e9a006
* Sun Jul 21 2019 jslaby@suse.cz
- Linux 5.2.2 (bnc#1012628).
- x86/entry/32: Fix ENDPROC of common_spurious (bnc#1012628).
- crypto/NX: Set receive window credits to max number of CRBs
  in RxFIFO (bnc#1012628).
- crypto: talitos - fix hash on SEC1 (bnc#1012628).
- crypto: talitos - move struct talitos_edesc into talitos.h
  (bnc#1012628).
- s390/qdio: don't touch the dsci in tiqdio_add_input_queues()
  (bnc#1012628).
- s390/qdio: (re-)initialize tiqdio list entries (bnc#1012628).
- s390: fix stfle zero padding (bnc#1012628).
- s390/ipl: Fix detection of has_secure attribute (bnc#1012628).
- ARC: hide unused function unw_hdr_alloc (bnc#1012628).
- x86/irq: Seperate unused system vectors from spurious entry
  again (bnc#1012628).
- x86/irq: Handle spurious interrupt after shutdown gracefully
  (bnc#1012628).
- x86/ioapic: Implement irq_get_irqchip_state() callback
  (bnc#1012628).
- genirq: Add optional hardware synchronization for shutdown
  (bnc#1012628).
- genirq: Fix misleading synchronize_irq() documentation
  (bnc#1012628).
- genirq: Delay deactivation in free_irq() (bnc#1012628).
- firmware: improve LSM/IMA security behaviour (bnc#1012628).
- drivers: base: cacheinfo: Ensure cpu hotplug work is done
  before Intel RDT (bnc#1012628).
- nilfs2: do not use unexported cpu_to_le32()/le32_to_cpu()
  in uapi header (bnc#1012628).
- Input: synaptics - enable SMBUS on T480 thinkpad trackpad
  (bnc#1012628).
- e1000e: start network tx queue only when link is up
  (bnc#1012628).
- Revert "e1000e: fix cyclic resets at link up with active tx"
  (bnc#1012628).
- commit 93f0a54
* Tue Jul 16 2019 lpechacek@suse.com
- rpm/kernel-binary.spec.in: build kernel-*-kgraft only for default SLE kernel
  RT and Azure variants are excluded for the moment. (bsc#1141600)
- commit 620816f
* Sun Jul 14 2019 jslaby@suse.cz
- Linux 5.2.1 (bnc#1012628).
- staging: rtl8712: reduce stack usage, again (bnc#1012628).
- staging: bcm2835-camera: Handle empty EOS buffers whilst
  streaming (bnc#1012628).
- staging: bcm2835-camera: Remove check of the number of buffers
  supplied (bnc#1012628).
- staging: bcm2835-camera: Ensure all buffers are returned on
  disable (bnc#1012628).
- staging: bcm2835-camera: Replace spinlock protecting context_map
  with mutex (bnc#1012628).
- staging: fsl-dpaa2/ethsw: fix memory leak of switchdev_work
  (bnc#1012628).
- staging: vchiq: revert "switch to wait_for_completion_killable"
  (bnc#1012628).
- staging: vchiq: make wait events interruptible (bnc#1012628).
- staging: vchiq_2835_arm: revert "quit using custom
  down_interruptible()" (bnc#1012628).
- VMCI: Fix integer overflow in VMCI handle arrays (bnc#1012628).
- Revert "x86/build: Move _etext to actual end of .text"
  (bnc#1012628).
- carl9170: fix misuse of device driver API (bnc#1012628).
- coresight: tmc-etf: Do not call smp_processor_id from
  preemptible (bnc#1012628).
- coresight: tmc-etr: alloc_perf_buf: Do not call smp_processor_id
  from preemptible (bnc#1012628).
- coresight: tmc-etr: Do not call smp_processor_id() from
  preemptible (bnc#1012628).
- coresight: etb10: Do not call smp_processor_id from preemptible
  (bnc#1012628).
- coresight: Potential uninitialized variable in probe()
  (bnc#1012628).
- iio: adc: stm32-adc: add missing vdda-supply (bnc#1012628).
- binder: return errors from buffer copy functions (bnc#1012628).
- binder: fix memory leak in error path (bnc#1012628).
- lkdtm: support llvm-objcopy (bnc#1012628).
- HID: Add another Primax PIXART OEM mouse quirk (bnc#1012628).
- staging: mt7621-pci: fix PCIE_FTS_NUM_LO macro (bnc#1012628).
- staging: comedi: amplc_pci230: fix null pointer deref on
  interrupt (bnc#1012628).
- staging: bcm2835-camera: Restore return behavior of
  ctrl_set_bitrate() (bnc#1012628).
- staging: wilc1000: fix error path cleanup in
  wilc_wlan_initialize() (bnc#1012628).
- staging: comedi: dt282x: fix a null pointer deref on interrupt
  (bnc#1012628).
- p54: fix crash during initialization (bnc#1012628).
- drivers/usb/typec/tps6598x.c: fix 4CC cmd write (bnc#1012628).
- drivers/usb/typec/tps6598x.c: fix portinfo width (bnc#1012628).
- usb: renesas_usbhs: add a workaround for a race condition of
  workqueue (bnc#1012628).
- usb: dwc2: use a longer AHB idle timeout in dwc2_core_reset()
  (bnc#1012628).
- usb: gadget: ether: Fix race between gether_disconnect and
  rx_submit (bnc#1012628).
- usb: gadget: f_fs: data_len used before properly set
  (bnc#1012628).
- p54usb: Fix race between disconnect and firmware loading
  (bnc#1012628).
- Revert "serial: 8250: Don't service RX FIFO if interrupts are
  disabled" (bnc#1012628).
- USB: serial: option: add support for GosunCn ME3630 RNDIS mode
  (bnc#1012628).
- USB: serial: ftdi_sio: add ID for isodebug v1 (bnc#1012628).
- mwifiex: Don't abort on small, spec-compliant vendor IEs
  (bnc#1012628).
- Documentation/admin: Remove the vsyscall=native documentation
  (bnc#1012628).
- Documentation: Add section about CPU vulnerabilities for Spectre
  (bnc#1012628).
- x86/tls: Fix possible spectre-v1 in do_get_thread_area()
  (bnc#1012628).
- x86/ptrace: Fix possible spectre-v1 in ptrace_get_debugreg()
  (bnc#1012628).
- perf header: Assign proper ff->ph in
  perf_event__synthesize_features() (bnc#1012628).
- perf thread-stack: Fix thread stack return from kernel for
  kernel-only case (bnc#1012628).
- perf pmu: Fix uncore PMU alias list for ARM64 (bnc#1012628).
- perf intel-pt: Fix itrace defaults for perf script intel-pt
  documentation (bnc#1012628).
- perf auxtrace: Fix itrace defaults for perf script
  (bnc#1012628).
- perf intel-pt: Fix itrace defaults for perf script
  (bnc#1012628).
- block, bfq: NULL out the bic when it's no longer valid
  (bnc#1012628).
- block: fix .bi_size overflow (bnc#1012628).
- tpm: Fix TPM 1.2 Shutdown sequence to prevent future TPM
  operations (bnc#1012628).
- tpm: Actually fail on TPM errors during "get random"
  (bnc#1012628).
- ALSA: hda/realtek - Headphone Mic can't record after S3
  (bnc#1012628).
- ALSA: usb-audio: Fix parse of UAC2 Extension Units
  (bnc#1012628).
- media: stv0297: fix frequency range limit (bnc#1012628).
- udf: Fix incorrect final NOT_ALLOCATED (hole) extent length
  (bnc#1012628).
- fscrypt: don't set policy for a dead directory (bnc#1012628).
- crypto: talitos - rename alternative AEAD algos (bnc#1012628).
- crypto: lrw - use correct alignmask (bnc#1012628).
- commit 51ca500
* Thu Jul 11 2019 glin@suse.com
- net: bpfilter: print umh messages to /dev/kmsg (bsc#1140221).
- commit 139acc9
* Wed Jul 10 2019 jslaby@suse.cz
- rpm/kernel-binary.spec.in: handle modules.builtin.modinfo
  It was added in 5.2.
- commit eb88df3
* Tue Jul  9 2019 rgoldwyn@suse.com
- Disable CONFIG_OVERLAY_FS_REDIRECT_ALWAYS_FOLLOW in config (bsc#1140494)
- commit 8d950e4
* Tue Jul  9 2019 schwab@suse.de
- Build against openSUSE:Factory:RISCV for riscv64
- commit 74d6e96
* Mon Jul  8 2019 mkubecek@suse.cz
- Update to 5.2 final
- Eliminated 1 patch
- commit b36439f
* Sun Jul  7 2019 msuchanek@suse.de
- Refresh tpm: tpm_ibm_vtpm: Fix unallocated banks (boo#1139244).
- commit 99f9469
* Fri Jul  5 2019 tiwai@suse.de
- config: align CONFIG_PHYSICAL_START and CONFIG_PHYSICAL_ALIGN to default values
  As suggested in bsc#1067593, our kconfig keeps the old default values
  while the upstream took different (actually swapped) values for x86
  CONFIG_PHYSICAL_START and CONFIG_PHYSICAL_ALIGN.   Let's follow the
  upstream default now.
- commit baa2434
* Fri Jul  5 2019 mkubecek@suse.cz
- Rename patches.suse/[PATCH]_tpm:_fixes_uninitialized_allocated_banks_for_IBM_vtpm_driver
  to patches.suse/tpm-fixes-uninitialized-allocated-banks-for-IBM-vtpm-driver.patch
  Let's not risk some tool somewhere does not handle special characters correctly.
- commit 8a3fff9
* Thu Jul  4 2019 msuchanek@suse.de
- tpm: fixes uninitialized allocated banks for IBM vtpm driver
  (boo#1139244).
- Delete patches.suse/Revert-tpm-pass-an-array-of-tpm_extend_digest-struct.patch.
- commit 43ec0a5
* Wed Jul  3 2019 msuchanek@suse.de
- crypto: user - prevent operating on larval algorithms
  (bsc#1133401).
- Delete patches.suse/crypto-algapi-guard-against-uninitialized-spawn-list.patch.
- commit 90eea5d
* Wed Jul  3 2019 schwab@suse.de
- rpm/dtb.spec.in.in: don't make dtb directory inaccessible
  There is no reason to lock down the dtb directory for ordinary users.
- commit a69437a
* Wed Jul  3 2019 jslaby@suse.cz
- Update config files.
  Set CONFIG_SCSI_SCAN_ASYNC=y (bnc#1137686).
- commit a156b11
* Wed Jul  3 2019 mkubecek@suse.cz
- config: switch to SLUB allocator (Jira:PM-1158)
- new config options:
  - SLUB=y
  - SLUB_DEBUG=y
  - SLUB_MEMCG_SYSFS_ON=y
  - SLAB_FREELIST_HARDENED=n
  - SLUB_CPU_PARTIAL=y
  - SLUB_DEBUG_ON=n
  - SLUB_STATS=n
- commit 0ab8cfd
* Sun Jun 30 2019 mkubecek@suse.cz
- Update to 5.2-rc7
- Refresh configs
- commit 2d405cc
* Sun Jun 30 2019 msuchanek@suse.de
- Delete patches.rpmify/BPF-UMH-do-not-detect-if-compiler-can-link-userspace.patch.
  Obsoleted by the gcc9 cross-compilers with libc.
- commit 0e0679b
* Sun Jun 30 2019 msuchanek@suse.de
- Revert "tpm: pass an array of tpm_extend_digest structures to
  tpm_pcr_extend()" (boo#1139244).
- commit b09a129
* Fri Jun 28 2019 msuchanek@suse.de
- Refresh patches.suse/supported-flag.
  Supported kernel does not build with the patch in master so imported
  patch from SLE15.
- commit 10d9b2c
* Thu Jun 27 2019 msuchanek@suse.de
- Update config files
  - Add core options from SLE15 which are not enabled on master for no
  obvious reason
  - Add core option from x86 which are not enabled on non-x86 for no
  obvious reason
  - Enable fadump
  Changes:
  Scheduling:
    +CONFIG_CONTEXT_TRACKING=y
  - CONFIG_TICK_CPU_ACCOUNTING=y
    +CONFIG_VIRT_CPU_ACCOUNTING_GEN=y
    +CONFIG_VIRT_CPU_ACCOUNTING=y
    +CONFIG_IRQ_TIME_ACCOUNTING=y
    +CONFIG_TASKS_RCU=y
    +CONFIG_RT_GROUP_SCHED=y
  mm:
    +# CONFIG_TRANSPARENT_HUGEPAGE_ALWAYS is not set
    +CONFIG_TRANSPARENT_HUGEPAGE_MADVISE=y
    +CONFIG_FRONTSWAP=y
    +CONFIG_ZSWAP=y
  arc/ppc:
    +CONFIG_FA_DUMP=y
  fs:
    +CONFIG_9P_FSCACHE=y
  net:
    +CONFIG_TIPC=m
    +CONFIG_TIPC_DIAG=m
    +CONFIG_TIPC_MEDIA_UDP=y
  misc:
  - CONFIG_SERIAL_SIFIVE=m
    +CONFIG_SYSCTL_SYSCALL=y
  debug&test:
    +CONFIG_PAGE_EXTENSION=y
    +CONFIG_PAGE_OWNER=y
    +CONFIG_DEBUG_MISC=y
    +CONFIG_RCU_TRACE=y
    +CONFIG_KGDB_SERIAL_CONSOLE=y
    +CONFIG_SCOM_DEBUGFS=y
    +CONFIG_CRYPTO_TEST=m
    +CONFIG_RCU_TORTURE_TEST=m
    +CONFIG_TEST_FIRMWARE=m
    +CONFIG_TEST_LIVEPATCH=m
    +CONFIG_TEST_LKM=m
    +CONFIG_TEST_SYSCTL=m
    +CONFIG_TORTURE_TEST=m
- commit ce08519
* Mon Jun 24 2019 msuchanek@suse.de
- crypto: algapi - guard against uninitialized spawn list in
  crypto_remove_spawns (bsc#1133401).
- commit 543f67d
* Mon Jun 24 2019 tiwai@suse.de
- fonts: Prefer a bigger font for high resolution screens
  (bsc#1138496).
- fonts: Use BUILD_BUG_ON() for checking empty font table
  (bsc#1138496).
- fonts: Fix coding style (bsc#1138496).
- commit f99f70b
* Sun Jun 23 2019 mkubecek@suse.cz
- Update to 5.2-rc6
- Eliminated 5 patches
  - patches.suse/net-phy-rename-Asix-Electronics-PHY-driver.patch
  - patches.suse/tcp-limit-payload-size-of-sacked-skbs.patch
  - patches.suse/tcp-tcp_fragment-should-apply-sane-memory-limits.patch
  - patches.suse/tcp-add-tcp_min_snd_mss-sysctl.patch
  - patches.suse/tcp-enforce-tcp_min_snd_mss-in-tcp_mtu_probing.patch
- Refresh
  - patches.suse/apparmor-compatibility-with-v2.x-net.patch
- commit 75acedc
* Thu Jun 20 2019 msuchanek@suse.de
- kernel-binary: rpm does not support multiline condition
- commit aceae50
* Thu Jun 20 2019 msuchanek@suse.de
- kernel-binary: Use -c grep option in klp project detection.
- commit 5def2a2
* Thu Jun 20 2019 msuchanek@suse.de
- kernel-binary: fix missing \
- commit 8325214
* Wed Jun 19 2019 mkubecek@suse.cz
- config: refresh i386/default
- commit a562f5a
* Wed Jun 19 2019 jslaby@suse.cz
- Update config files.
  Enable SECURITY_YAMA to allow protection against ptrace attacks
  (bnc#1128245).
- commit f841e66
* Tue Jun 18 2019 jslaby@suse.cz
- Update config files.
  Set HARDENED_USERCOPY=y (bnc#1127808). This can be disabled on the
  commandline using hardened_usercopy=n.
- commit 3b85d22
* Tue Jun 18 2019 tiwai@suse.de
- config: enable CONFIG_FONT_TER16x32 for HiDPI monitors (boo#1138496)
- commit 073136d
* Mon Jun 17 2019 mkubecek@suse.cz
- tcp: enforce tcp_min_snd_mss in tcp_mtu_probing()
  (CVE-2019-11479 bsc#1137586).
- tcp: add tcp_min_snd_mss sysctl (CVE-2019-11479 bsc#1137586).
- tcp: tcp_fragment() should apply sane memory limits
  (CVE-2019-11478 bsc#1137586).
- tcp: limit payload size of sacked skbs (CVE-2019-11477
  bsc#1137586).
- commit ab45ff3
* Sun Jun 16 2019 mkubecek@suse.cz
- Update to 5.2-rc5
- Config changes:
  - Sound:
  - SND_SOC_SOF_NOCODEC_SUPPORT=n on x86, =y on ARM
  - Storage:
  - MQ_IOSCHED_DEADLINE m -> y on arm64
- commit b5857f8
* Thu Jun 13 2019 msuchanek@suse.de
- Build klp-symbols in kernel devel projects.
- commit ffd0ed9
* Thu Jun 13 2019 jdelvare@suse.de
- supported.conf: Enable it87_wdt and f71808e_wdt
  Both drivers are for watchdog devices included in Super-I/O chipsets
  which are popular on x86 PC mainboards. Code is clean and simple,
  so supporting them isn't a problem.
- commit b818771
* Mon Jun 10 2019 lduncan@suse.com
- scsi: mpt3sas_ctl: fix double-fetch bug in _ctl_ioctl_main()
  (bsc#1136922 cve-2019-12456).
- commit 42064d5
* Mon Jun 10 2019 mkubecek@suse.cz
- Update to 5.2-rc4
- Eliminated 1 patch
  - patches.rpmify/mlx5-avoid-64-bit-division.patch
- Refresh configs
  - IKHEADERS_PROC -> IKHEADERS
- commit c8bdb02
* Fri Jun  7 2019 mvedovati@suse.com
- rpm/post.sh: correct typo in err msg (bsc#1137625)
- commit 9fe85cc
* Thu Jun  6 2019 jslaby@suse.cz
- s390: drop meaningless 'targets' from tools Makefile (s390
  kmp build fix).
- commit b4eda05
* Wed Jun  5 2019 mvedovati@suse.com
- Enhance kvmsmall configuration (bsc#1137361)
  Add a minimal set of modules to  kvmsmall, to make this config usable
  to set up guest VMs interacting with the host.
- commit 34c4eab
* Wed Jun  5 2019 mkubecek@suse.cz
- config: refresh configs
  No functional change.
- commit cbc8b7e
* Tue Jun  4 2019 jslaby@suse.cz
- Update config files.
  Enable CRASH_DUMP and RELOCATABLE on ppc64le to be on par with the
  other archs and to allow for kdump (bnc#1135217).
- commit a6a9f0e
* Mon Jun  3 2019 mkubecek@suse.cz
- Update to 5.2-rc3
- Eliminated 1 patch
  - patches.suse/kvm-memunmap-also-needs-HAS_IOMEM.patch
- commit 038ee83
* Wed May 29 2019 mkubecek@suse.cz
- config: refresh vanilla configs
- commit cbe6c1c
* Wed May 29 2019 mkubecek@suse.cz
- reenable ARM architectures
- commit 194828b
* Wed May 29 2019 mkubecek@suse.cz
- refresh configs after Tumbleweed switch to gcc9 as default
- commit 3b7ae7e
* Wed May 29 2019 yousaf.kaukab@suse.com
- config: armv7hl: lpae: Update to v5.2.0-rc2
- commit 38ac345
* Wed May 29 2019 yousaf.kaukab@suse.com
- config: armv7hl: Update to v5.2.0-rc2
- commit 737b08e
* Wed May 29 2019 yousaf.kaukab@suse.com
- config: armv6hl: Update to v5.2.0-rc2
- commit c7bc712
* Tue May 28 2019 yousaf.kaukab@suse.com
- config: arm64: Update to v5.2.0-rc2
- commit 18d0586
* Mon May 27 2019 mkubecek@suse.cz
- Update to 5.2-rc2
- Eliminated 4 patches
  - patches.suse/dm-make-sure-to-obey-max_io_len_target_boundary.patch
  - patches.suse/kvm-make-kvm_vcpu_-un-map-dependency-on-CONFIG_HAS_I.patch
  - patches.suse/vfio_pci-Add-local-source-directory-as-include.patch
  - patches.suse/x86-kvm-pmu-Set-AMD-s-virt-PMU-version-to-1.patch
- add s390x/zfcpdump build fix
  - patches.suse/kvm-memunmap-also-needs-HAS_IOMEM.patch
- commit b02c459
* Wed May 22 2019 msuchanek@suse.de
- Delete patches.suse/Revert-Bluetooth-btusb-driver-to-enable-the-usb-wake.patch (boo#1130448).
  Should be fixed in 5.1-rc5
  commit 771acc7e4a6e5dba779cb1a7fd851a164bc81033
  Author: Brian Norris <briannorris@chromium.org>
  Date:   Tue Apr 9 11:49:17 2019 -0700
    Bluetooth: btusb: request wake pin with NOAUTOEN
- commit b225e5a
* Wed May 22 2019 jslaby@suse.cz
- dm: make sure to obey max_io_len_target_boundary (bnc#1135868).
- commit dbeb07c
* Mon May 20 2019 mkubecek@suse.cz
- kvm: make kvm_vcpu_(un)map dependency on CONFIG_HAS_IOMEM
  explicit.
  Fixes build of s390x/zfcpdump.
- commit b33dbfc
* Mon May 20 2019 mkubecek@suse.cz
- config: refresh vanilla configs
- commit 4c41263
* Mon May 20 2019 mkubecek@suse.cz
- net: phy: rename Asix Electronics PHY driver.
  Fix duplicate module name asix by renaming phy driver to ax88796b.
- Update config files.
- commit df18320
* Mon May 20 2019 mkubecek@suse.cz
- mlx5: avoid 64-bit division.
  Fix i386 build.
- commit 89c5a47
* Mon May 20 2019 mkubecek@suse.cz
- Update to 5.2-rc1
- Eliminated 106 patches (105 stable, 1 other)
- ARM configs need update
- Refresh
  patches.rpmify/scripts-mkmakefile-honor-second-argument.patch
  patches.suse/dm-mpath-leastpending-path-update
  patches.suse/supported-flag
  patches.suse/supported-flag-external
  patches.suse/vfs-add-super_operations-get_inode_dev
- New config options:
  - General setup
  - IKHEADERS_PROC=n
  - SHUFFLE_PAGE_ALLOCATOR=y
  - Security
  - SECURITY_TOMOYO_INSECURE_BUILTIN_SETTING=n
  - Filesystems
  - UNICODE=y
  - UNICODE_NORMALIZATION_SELFTEST=n
  - Crypto
  - CRYPTO_ECRDSA=m
  - Networking
  - BATMAN_ADV_SYSFS=y
  - BT_MTKSDIO=m
  - XILINX_LL_TEMAC=m
  - MT7615E=m
  - RTW88=m
  - RTW88_8822BE=y
  - RTW88_8822CE=y
  - RTW88_DEBUG=n
  - RTW88_DEBUGFS=n
  - INFINIBAND_EFA=m
  - Storage
  - DM_DUST=m
  - MTD drivers
  - MTD_RAW_NAND=m
  - MTD_NAND_ECC_SW_BCH=y
  - MTD_NAND_ECC_SW_HAMMING_SMC=n
  - Input
  - KEYBOARD_QT1050=m
  - TOUCHSCREEN_IQS5XX=m
  - INPUT_GPIO_VIBRA=n
  - INPUT_REGULATOR_HAPTIC=m
  - HID_MACALLY=m
  - HID_U2FZERO=m
  - INPUT_MAX77650_ONKEY=m
  - Serial
  - NULL_TTY=m
  - SERIAL_SIFIVE=m
  - Power management
  - CHARGER_MANAGER=y
  - CHARGER_LT3651=m
  - CHARGER_UCS1002=m
  - SENSORS_IR38064=m
  - SENSORS_ISL68137=m
  - SENSORS_LTC2978_REGULATOR=y
  - THERMAL_MMIO=m
  - MFD_MAX77650=m
  - MFD_STMFX=m
  - REGULATOR_DEBUG=n
  - REGULATOR_FIXED_VOLTAGE=m
  - REGULATOR_VIRTUAL_CONSUMER=m
  - REGULATOR_USERSPACE_CONSUMER=m
  - REGULATOR_88PG86X=m
  - REGULATOR_ACT8865=m
  - REGULATOR_AD5398=m
  - REGULATOR_AXP20X=m
  - REGULATOR_DA9062=m
  - REGULATOR_DA9210=m
  - REGULATOR_DA9211=m
  - REGULATOR_FAN53555=m
  - REGULATOR_GPIO=m
  - REGULATOR_ISL9305=m
  - REGULATOR_ISL6271A=m
  - REGULATOR_LM363X=m
  - REGULATOR_LP3971=m
  - REGULATOR_LP3972=m
  - REGULATOR_LP872X=m
  - REGULATOR_LP8755=m
  - REGULATOR_LTC3589=m
  - REGULATOR_LTC3676=m
  - REGULATOR_MAX1586=m
  - REGULATOR_MAX77650=m
  - REGULATOR_MAX8649=m
  - REGULATOR_MAX8660=m
  - REGULATOR_MAX8907=m
  - REGULATOR_MAX8952=m
  - REGULATOR_MAX8973=m
  - REGULATOR_MCP16502=m
  - REGULATOR_MT6311=m
  - REGULATOR_PFUZE100=m
  - REGULATOR_PV88060=m
  - REGULATOR_PV88080=m
  - REGULATOR_PV88090=m
  - REGULATOR_PWM=m
  - REGULATOR_QCOM_SPMI=m
  - REGULATOR_SY8106A=m
  - REGULATOR_TPS51632=m
  - REGULATOR_TPS62360=m
  - REGULATOR_TPS65023=m
  - REGULATOR_TPS6507X=m
  - REGULATOR_TPS65132=m
  - REGULATOR_TPS6524X=m
  - REGULATOR_VCTRL=m
  - CHARGER_MAX77650=m
  - Media
  - MEDIA_CONTROLLER_REQUEST_API=y
  - VIDEO_V4L2_SUBDEV_API=y
  - V4L2_FLASH_LED_CLASS=m
  - VIDEO_COBALT=n
  - VIDEO_IPU3_CIO2=m
  - VIDEO_CADENCE_CSI2RX=m
  - VIDEO_CADENCE_CSI2TX=m
  - VIDEO_MUX=m
  - VIDEO_XILINX=m
  - VIDEO_XILINX_TPG=m
  - VIDEO_VIMC=m
  - VIDEO_IPU3_IMGU=m
  - DRM
  - NOUVEAU_LEGACY_CTX_SUPPORT=n
  - DRM_PANEL_FEIYANG_FY07024DI26A30D=n
  - DRM_PANEL_ROCKTECH_JH057N00900=n
  - DRM_PANEL_RONBO_RB070D30=n
  - Sound
  - SND_SOC_FSL_AUDMIX=n
  - SND_SOC_SOF_TOPLEVEL=y
  - SND_SOC_SOF_PCI=m
  - SND_SOC_SOF_ACPI=m
  - SND_SOC_SOF_NOCODEC=n
  - SND_SOC_SOF_STRICT_ABI_CHECKS=n
  - SND_SOC_SOF_DEBUG=n
  - SND_SOC_SOF_INTEL_TOPLEVEL=y
  - SND_SOC_SOF_BAYTRAIL_SUPPORT=y
  - SND_SOC_SOF_BROADWELL_SUPPORT=y
  - SND_SOC_SOF_MERRIFIELD_SUPPORT=y
  - SND_SOC_SOF_APOLLOLAKE_SUPPORT=y
  - SND_SOC_SOF_GEMINILAKE_SUPPORT=y
  - SND_SOC_SOF_CANNONLAKE_SUPPORT=y
  - SND_SOC_SOF_COFFEELAKE_SUPPORT=y
  - SND_SOC_SOF_ICELAKE_SUPPORT=y
  - SND_SOC_SOF_HDA_LINK=y
  - SND_SOC_SOF_HDA_AUDIO_CODEC=y
  - SND_SOC_INTEL_SOF_RT5682_MACH=m
  - USB
  - TYPEC_NVIDIA_ALTMODE=m
  - LEDS
  - LEDS_LM3532=m
  - LEDS_REGULATOR=m
  - LEDS_MAX77650=m
  - Platform
  - CROS_EC_RPMSG=m
  - CROS_USBPD_LOGGER=m
  - CLK_SIFIVE=n
  - IXP4XX_QMGR=n
  - IXP4XX_NPE=m
  - IIO
  - CC10001_ADC=n
  - TI_ADS8344=n
  - FXAS21002C=n
  - MB1232=n
  - MAX31856=m
  - Misc drivers
  - I2C_AMD_MP2=m
  - PINCTRL_STMFX=n
  - FIELDBUS_DEV=n
  - KPC2000=n
  - NVMEM_SYSFS=y
  - COUNTER=n
  - GPIO_MAX77650=m
  - Library
  - PACKING=n
  - Debugging and testing
  - DEBUG_INFO_BTF=n
  - DEBUG_MISC=n
  - DEBUG_PLIST=n
  - TEST_STRSCPY=n
  - x86
  - ACPI_HMAT=y
  - INTEL_CHT_INT33FE=m
  - INTEL_ISH_FIRMWARE_DOWNLOADER=m
  - i386
  - MEMORY_HOTPLUG=y
  - MEMORY_HOTPLUG_DEFAULT_ONLINE=n
  - MEMORY_HOTREMOVE
  - XEN_BALLOON_MEMORY_HOTPLUG=y
  - XEN_BALLOON_MEMORY_HOTPLUG_LIMIT=4
  - DEV_DAX_KMEM=m
  - MEMORY_NOTIFIER_ERROR_INJECT=m
  - ACPI_HOTPLUG_MEMORY=y
  - ppc64 / ppc64le
  - PPC_KUEP=y
  - PPC_KUAP=y
  - PPC_KUAP_DEBUG=n
  - MTD_NAND_DENALI_PCI=m
  - MTD_NAND_CAFE=m
  - MTD_NAND_GPIO=m
  - MTD_NAND_PLATFORM=m
  - MTD_NAND_NANDSIM=m
  - MTD_NAND_RICOH=m
  - MTD_NAND_DISKONCHIP=m
  - MTD_NAND_DISKONCHIP_PROBE_ADVANCED=n
  - MTD_NAND_DISKONCHIP_BBTWRITE=n
  - INTEGRITY_PLATFORM_KEYRING=y
  - OPTIMIZE_INLINING=y
  - XMON_DEFAULT_RO_MODE=y
  - s390x
  - KEXEC_VERIFY_SIG=n
  - RELOCATABLE=y
  - RANDOMIZE_BASE=y
  - PROTECTED_VIRTUALIZATION_GUEST=y
  - LCD_CLASS_DEVICE=n
  - BACKLIGHT_CLASS_DEVICE=n
  - INTEGRITY_PLATFORM_KEYRING=y
  - OPTIMIZE_INLINING=n
- commit c8b1101
* Fri May 17 2019 jslaby@suse.cz
- Revert "selinux: do not report error on connect(AF_UNSPEC)"
  (git-fixes).
- Revert "Don't jump to compute_result state from check_result
  state" (git-fixes).
- commit 3d34296
* Fri May 17 2019 jslaby@suse.cz
- Linux 5.1.3 (bnc#1012628).
- f2fs: Fix use of number of devices (bnc#1012628).
- PCI: hv: Add pci_destroy_slot() in pci_devices_present_work(),
  if necessary (bnc#1012628).
- PCI: hv: Add hv_pci_remove_slots() when we unload the driver
  (bnc#1012628).
- PCI: hv: Fix a memory leak in hv_eject_device_work()
  (bnc#1012628).
- virtio_ring: Fix potential mem leak in
  virtqueue_add_indirect_packed (bnc#1012628).
- powerpc/booke64: set RI in default MSR (bnc#1012628).
- powerpc/powernv/idle: Restore IAMR after idle (bnc#1012628).
- powerpc/book3s/64: check for NULL pointer in pgd_alloc()
  (bnc#1012628).
- drivers/virt/fsl_hypervisor.c: prevent integer overflow in ioctl
  (bnc#1012628).
- drivers/virt/fsl_hypervisor.c: dereferencing error pointers
  in ioctl (bnc#1012628).
- isdn: bas_gigaset: use usb_fill_int_urb() properly
  (bnc#1012628).
- flow_dissector: disable preemption around BPF calls
  (bnc#1012628).
- net: phy: fix phy_validate_pause (bnc#1012628).
- tuntap: synchronize through tfiles array instead of
  tun->numqueues (bnc#1012628).
- tuntap: fix dividing by zero in ebpf queue selection
  (bnc#1012628).
- vrf: sit mtu should not be updated when vrf netdev is the link
  (bnc#1012628).
- vlan: disable SIOCSHWTSTAMP in container (bnc#1012628).
- tipc: fix hanging clients using poll with EPOLLOUT flag
  (bnc#1012628).
- selinux: do not report error on connect(AF_UNSPEC)
  (bnc#1012628).
- packet: Fix error path in packet_init (bnc#1012628).
- net: ucc_geth - fix Oops when changing number of buffers in
  the ring (bnc#1012628).
- net: seeq: fix crash caused by not set dev.parent (bnc#1012628).
- net: macb: Change interrupt and napi enable order in open
  (bnc#1012628).
- net: ethernet: stmmac: dwmac-sun8i: enable support of unicast
  filtering (bnc#1012628).
- net: dsa: Fix error cleanup path in dsa_init_module
  (bnc#1012628).
- ipv4: Fix raw socket lookup for local traffic (bnc#1012628).
- fib_rules: return 0 directly if an exactly same rule exists
  when NLM_F_EXCL not supplied (bnc#1012628).
- dpaa_eth: fix SG frame cleanup (bnc#1012628).
- bridge: Fix error path for kobject_init_and_add() (bnc#1012628).
- bonding: fix arp_validate toggling in active-backup mode
  (bnc#1012628).
- Don't jump to compute_result state from check_result state
  (bnc#1012628).
- rtlwifi: rtl8723ae: Fix missing break in switch statement
  (bnc#1012628).
- mwl8k: Fix rate_idx underflow (bnc#1012628).
- USB: serial: fix unthrottle races (bnc#1012628).
- virt: vbox: Sanity-check parameter types for hgcm-calls coming
  from userspace (bnc#1012628).
- kernfs: fix barrier usage in __kernfs_new_node() (bnc#1012628).
- i2c: core: ratelimit 'transfer when suspended' errors
  (bnc#1012628).
- selftests/seccomp: Handle namespace failures gracefully
  (bnc#1012628).
- hwmon: (occ) Fix extended status bits (bnc#1012628).
- hwmon: (pwm-fan) Disable PWM if fetching cooling data fails
  (bnc#1012628).
- platform/x86: dell-laptop: fix rfkill functionality
  (bnc#1012628).
- platform/x86: thinkpad_acpi: Disable Bluetooth for some machines
  (bnc#1012628).
- platform/x86: sony-laptop: Fix unintentional fall-through
  (bnc#1012628).
- commit 073196d
* Thu May 16 2019 mwilck@suse.com
- Update config files: disable CONFIG_IDE for ppc64/ppc64le (bsc#1135333)
- commit 012b7ed
* Wed May 15 2019 mkubecek@suse.cz
- x86/kvm/pmu: Set AMD's virt PMU version to 1
  (https://patchwork.kernel.org/patch/10936271/).
- commit d737fc7
* Tue May 14 2019 jslaby@suse.cz
- Linux 5.1.2 (bnc#1012628).
- x86/speculation/mds: Fix documentation typo (bnc#1012628).
- Documentation: Correct the possible MDS sysfs values
  (bnc#1012628).
- x86/mds: Add MDSUM variant to the MDS documentation
  (bnc#1012628).
- x86/speculation/mds: Add 'mitigations=' support for MDS
  (bnc#1012628).
- s390/speculation: Support 'mitigations=' cmdline option
  (bnc#1012628).
- powerpc/speculation: Support 'mitigations=' cmdline option
  (bnc#1012628).
- x86/speculation: Support 'mitigations=' cmdline option
  (bnc#1012628).
- cpu/speculation: Add 'mitigations=' cmdline option
  (bnc#1012628).
- x86/speculation/mds: Print SMT vulnerable on MSBDS with
  mitigations off (bnc#1012628).
- x86/speculation/mds: Fix comment (bnc#1012628).
- x86/speculation/mds: Add SMT warning message (bnc#1012628).
- x86/speculation: Move arch_smt_update() call to after mitigation
  decisions (bnc#1012628).
- x86/speculation/mds: Add mds=full,nosmt cmdline option
  (bnc#1012628).
- Documentation: Add MDS vulnerability documentation
  (bnc#1012628).
- Documentation: Move L1TF to separate directory (bnc#1012628).
- x86/speculation/mds: Add mitigation mode VMWERV (bnc#1012628).
- x86/speculation/mds: Add sysfs reporting for MDS (bnc#1012628).
- x86/speculation/mds: Add mitigation control for MDS
  (bnc#1012628).
- x86/speculation/mds: Conditionally clear CPU buffers on idle
  entry (bnc#1012628).
- x86/kvm/vmx: Add MDS protection when L1D Flush is not active
  (bnc#1012628).
- x86/speculation/mds: Clear CPU buffers on exit to user
  (bnc#1012628).
- x86/speculation/mds: Add mds_clear_cpu_buffers() (bnc#1012628).
- x86/kvm: Expose X86_FEATURE_MD_CLEAR to guests (bnc#1012628).
- x86/speculation/mds: Add BUG_MSBDS_ONLY (bnc#1012628).
- x86/speculation/mds: Add basic bug infrastructure for MDS
  (bnc#1012628).
- x86/speculation: Consolidate CPU whitelists (bnc#1012628).
- x86/msr-index: Cleanup bit defines (bnc#1012628).
- commit 5a8c05f
* Tue May 14 2019 mkubecek@suse.cz
- config: keep LSM empty in s390x/zfcpdump
  This config doesn't really build AppArmor and always had
  DEFAULT_SECURITY_DAC so it seems more consistent to keep LSM list empty.
- commit 3073856
* Tue May 14 2019 mkubecek@suse.cz
- config: enable AppArmor by default again (bsc#1134906)
  AppArmor used to be enabled in kernel by default by after the recent
  introduction of CONFIG_LSM, we disabled all LSM modules. Enable AppArmor
  again.
- commit 953db35
* Tue May 14 2019 mkubecek@suse.cz
- Update upstream reference:
  patches.suse/efifb-Omit-memory-map-check-on-legacy-boot.patch
- commit 133a780
* Sat May 11 2019 jslaby@suse.cz
- Linux 5.1.1 (bnc#1012628).
- arm64: futex: Bound number of LDXR/STXR loops in FUTEX_WAKE_OP
  (bnc#1012628).
- locking/futex: Allow low-level atomic operations to return
  - EAGAIN (bnc#1012628).
- i3c: Fix a shift wrap bug in i3c_bus_set_addr_slot_status()
  (bnc#1012628).
- ASoC: Intel: avoid Oops if DMA setup fails (bnc#1012628).
- UAS: fix alignment of scatter/gather segments (bnc#1012628).
- Bluetooth: hci_bcm: Fix empty regulator supplies for Intel Macs
  (bnc#1012628).
- Bluetooth: Fix not initializing L2CAP tx_credits (bnc#1012628).
- Bluetooth: Align minimum encryption key size for LE and BR/EDR
  connections (bnc#1012628).
- Bluetooth: hidp: fix buffer overflow (bnc#1012628).
- scsi: qla2xxx: Fix device staying in blocked state
  (bnc#1012628).
- scsi: qla2xxx: Set remote port devloss timeout to 0
  (bnc#1012628).
- scsi: qla2xxx: Fix incorrect region-size setting in optrom
  SYSFS routines (bnc#1012628).
- scsi: lpfc: change snprintf to scnprintf for possible overflow
  (bnc#1012628).
- soc: sunxi: Fix missing dependency on REGMAP_MMIO (bnc#1012628).
- ACPI / LPSS: Use acpi_lpss_* instead of acpi_subsys_* functions
  for hibernate (bnc#1012628).
- cpufreq: armada-37xx: fix frequency calculation for opp
  (bnc#1012628).
- iio: adc: qcom-spmi-adc5: Fix of-based module autoloading
  (bnc#1012628).
- intel_th: pci: Add Comet Lake support (bnc#1012628).
- genirq: Prevent use-after-free and work list corruption
  (bnc#1012628).
- usb-storage: Set virt_boundary_mask to avoid SG overflows
  (bnc#1012628).
- USB: cdc-acm: fix unthrottle races (bnc#1012628).
- USB: serial: f81232: fix interrupt worker not stop
  (bnc#1012628).
- usb: dwc3: Fix default lpm_nyet_threshold value (bnc#1012628).
- usb: dwc3: Allow building USB_DWC3_QCOM without EXTCON
  (bnc#1012628).
- staging: most: sound: pass correct device when creating a
  sound card (bnc#1012628).
- staging: most: cdev: fix chrdev_region leak in mod_exit
  (bnc#1012628).
- staging: wilc1000: Avoid GFP_KERNEL allocation from atomic
  context (bnc#1012628).
- staging: greybus: power_supply: fix prop-descriptor request size
  (bnc#1012628).
- ubsan: Fix nasty -Wbuiltin-declaration-mismatch GCC-9 warnings
  (bnc#1012628).
- Drivers: hv: vmbus: Remove the undesired put_cpu_ptr() in
  hv_synic_cleanup() (bnc#1012628).
- commit 8e0a089
* Thu May  9 2019 guillaume.gardet@free.fr
- Sign non-x86 kernels when possible (boo#1134303)
- commit bac621c
* Mon May  6 2019 mkubecek@suse.cz
- Update to 5.1 final
- Eliminated 1 patch
- New config options:
  - PCI:
  - PCIE_BW=n (recommended default)
- commit a974d8b
* Tue Apr 30 2019 mkubecek@suse.cz
- rdma: fix build errors on s390 and MIPS due to bad ZERO_PAGE use
  (http://lkml.kernel.org/r/20190429052136.GA21672@unicorn.suse.cz).
- Delete
  patches.suse/rdma-fix-argument-of-ZERO_PAGE-in-rdma_umap_fault.patch.
- commit a764394
* Mon Apr 29 2019 mkubecek@suse.cz
- Update to 5.1-rc7
- add patches.suse/rdma-fix-argument-of-ZERO_PAGE-in-rdma_umap_fault.patch
  (tentative s390x build fix)
- New config options:
  - ARM:
  - KEYBOARD_SNVS_PWRKEY=m
  - armv7hl:
  - FRAME_POINTER=y
  - UNWINDER_FRAME_POINTER=y
- commit 04c1966
* Sun Apr 21 2019 mkubecek@suse.cz
- Update to v5.1-rc6
- New config options:
  - IIO:
  - SENSIRION_SGP30=n
- commit ab97af0
* Tue Apr 16 2019 mkubecek@suse.cz
- series.conf: cleanup
  patches.suse/ext2-fsync-err was deleted in 2011 but its (commented out)
  line in series.conf was left behind.
- commit d2aebe3
* Mon Apr 15 2019 jkosina@suse.cz
- Delete
  patches.suse/0001-x86-speculation-Add-basic-IBRS-support-infrastructur.patch.
- Delete
  patches.suse/0002-x86-speculation-Add-inlines-to-control-Indirect-Bran.patch.
- Delete
  patches.suse/0003-x86-idle-Control-Indirect-Branch-Speculation-in-idle.patch.
- Delete
  patches.suse/0004-x86-enter-Create-macros-to-restrict-unrestrict-Indir.patch.
- Delete
  patches.suse/0005-x86-enter-Use-IBRS-on-syscall-and-interrupts.patch.
  Drop SUSE-specific IBRS-on-SKL implementation. Please refer to
  page 16 of [1]
  [1] https://software.intel.com/security-software-guidance/api-app/sites/default/files/Retpoline-A-Branch-Target-Injection-Mitigation.pdf
- commit 5e8da3a
* Mon Apr 15 2019 mkubecek@suse.cz
- Update to 5.1-rc5
- commit 2fd333d
* Thu Apr 11 2019 msuchanek@suse.de
- Do not provide kernel-default from kernel-default-base (boo#1132154, bsc#1106751).
- commit 0e54e61
* Thu Apr 11 2019 msuchanek@suse.de
- rpm/kernel-subpackage-spec: only provide firmware actually present in
  subpackage.
- commit 839debd
* Wed Apr 10 2019 msuchanek@suse.de
- kernel-subpackage-spec: Add dummy package to ensure subpackages are
  rebuilt with kernel update (bsc#1106751).
  In factory packages are not rebuilt automatically so a dependency is
  needed on the old kernel to get a rebuild with the new kernel. THe
  subpackage itself cannot depend on the kernel so add another empty
  pacakge that does depend on it.
- commit 6d14837
* Tue Apr  9 2019 jdelvare@suse.de
- Disable CONFIG_SERIO_OLPC_APSP on all but armv7
  This driver is only used by ARMv7-based OLPC laptops.
- commit 7b1b640
* Tue Apr  9 2019 jdelvare@suse.de
- Disable CONFIG_SENSORS_OCC_*
  These drivers are running on the BMC of PowerPC servers. The BMC runs
  OpenBMC and is not a target for SUSE distributions.
- commit a82eb87
* Mon Apr  8 2019 mkubecek@suse.cz
- config: disable DEVKMEM (bsc#1128045)
- commit 1478096
* Mon Apr  8 2019 mkubecek@suse.cz
- Update to 5.1-rc4
- Refresh configs
- commit e334e4f
* Mon Apr  1 2019 tiwai@suse.de
- efifb: Omit memory map check on legacy boot (bsc#1127339).
- commit 8a60576
* Mon Apr  1 2019 mkubecek@suse.cz
- Update to 5.1-rc3
- Eliminated 1 patch
- Config changes:
  - SECURITY_DEFAULT_* are back
  - enable CONFIG_OF in i386/pae and copy dependent options from default
- commit 7474ec2
* Thu Mar 28 2019 yousaf.kaukab@suse.com
- config: arm64: enable CPPC support
- commit c97748e
* Tue Mar 26 2019 msuchanek@suse.de
- Revert "Bluetooth: btusb: driver to enable the usb-wakeup
  feature" (boo#1130448).
  System still wakes up when connected BT device is powered off.
- Revert "Bluetooth: btusb: driver to enable the usb-wakeup
  feature" (boo#1130448).
- commit 1172cb0
* Tue Mar 26 2019 mkubecek@suse.cz
- Revert "parport: daisy: use new parport device model"
  (http://lkml.kernel.org/r/20190313064557.GA14531@unicorn.suse.cz).
- Delete
  patches.suse/parport-daisy-do-not-try-to-load-lowlevel-driver.patch.
- commit 7da01f5
* Tue Mar 26 2019 jbeulich@suse.com
- patches.suse/0005-x86-enter-Use-IBRS-on-syscall-and-interrupts.patch:
  Fix re-basing mistake - IBRS enabling should not be skipped for PV Xen.
- commit 177c0f8
* Tue Mar 26 2019 mkubecek@suse.cz
- parport: daisy: do not try to load lowlevel driver
  (http://lkml.kernel.org/r/20190313064557.GA14531@unicorn.suse.cz).
- commit 4f8876e
* Mon Mar 25 2019 mkubecek@suse.cz
- Update to 5.1-rc2
- New config options:
  - CHARLCD_BL_FLASH=y
  - PARPORT_PANEL=m (renamed from PANEL)
  - PANEL=m
- commit ede8a59
* Fri Mar 22 2019 msuchanek@suse.de
- Do not provide kernel-default-srchash from kernel-default-base.
- commit d6c71ce
* Thu Mar 21 2019 mkubecek@suse.cz
- config: apply recent changes to ARM configs
- CONFIG_PREEMPT_VOLUNTARY=y
- disable CONFIG_IMA_ARCH_POLICY
- enable CONFIG_IMA_APPRAISE_BOOTPARAM
- CONFIG_LSM=""
- commit fd95045
* Wed Mar 20 2019 yousaf.kaukab@suse.com
- config: arm64: Update to v5.1-rc1
- commit 590226b
* Wed Mar 20 2019 msuchanek@suse.de
- rpm/kernel-subpackage-build: handle arm kernel zImage.
- commit 81a63c3
* Wed Mar 20 2019 jslaby@suse.cz
- config: disable IMA_ARCH_POLICY for now
  When IMA_ARCH_POLICY was enabled during the 5.0-rc* stage, IMA causes
  kdump load to fail:
  kexec_file_load failed: Permission denied
  ima: impossible to appraise a kernel image without a file descriptor; try using kexec_file_load syscall.
  We have to fix kexec tooling before enabling IMA for everyone.
  BTW IMA_APPRAISE_BOOTPARAM was disabled by IMA_ARCH_POLICY=y. So
  restore the original state (and functionality).
- commit f738bd5
* Wed Mar 20 2019 yousaf.kaukab@suse.com
- config: armv6hl: Update to v5.1-rc1
  CONFIG_BPFILTER_UMH is disabled due to bsc#1127188
- commit 608f8e5
* Wed Mar 20 2019 tiwai@suse.de
- rpm/kernel-source.changes.old: Really drop old changelogs (bsc#1098995)
- commit 93056b5
* Tue Mar 19 2019 yousaf.kaukab@suse.com
- config: armv7hl: Update to v5.1-rc1
  CONFIG_BPFILTER_UMH is disabled due to bsc#1127188
- commit 0042582
* Mon Mar 18 2019 mkubecek@suse.cz
- Update to 5.1-rc1
- Eliminated 74 patches (73 stable, 1 other)
- ARM configs need update
- Refresh
  patches.suse/btrfs-btrfs-use-the-new-VFS-super_block_dev.patch
  patches.suse/btrfs-fs-super.c-add-new-super-block-devices-super_block_d.patch
  patches.suse/genksyms-add-override-flag.diff
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch
  patches.suse/readahead-request-tunables.patch
  patches.suse/supported-flag
  patches.suse/vfs-add-super_operations-get_inode_dev
- New config options:
  - General:
  - IO_URING=y
  - PRINTK_CALLER=n
  - File systems:
  - CONFIG_SUNRPC_DISABLE_INSECURE_ENCTYPES=n
  - VALIDATE_FS_PARSER=n
  - Networking:
  - NET_DEVLINK=y
  - XDP_SOCKETS_DIAG=m
  - MT7603E=m
  - TI_CPSW_PHY_SEL=n
  - Power management:
  - CPU_IDLE_GOV_TEO=y
  - DAX:
  - DEV_DAX_KMEM=m
  - DEV_DAX_PMEM_COMPAT=m
  - USB:
  - USB_AUTOSUSPEND_DELAY=2
  - USB_EHCI_FSL=m
  - Graphics:
  - DRM_ETNAVIV=n
  - DRM_NOUVEAU_SVM=n
  - VIDEO_FB_IVTV_FORCE_PAT=n
  - Sound:
  - SND_SOC_CROS_EC_CODEC=m
  - SND_SOC_CS35L36=m
  - SND_SOC_CS4341=m
  - SND_SOC_FSL_MICFIL=n
  - SND_SOC_MAX98373=m
  - SND_SOC_MT6358=n
  - SND_SOC_MTK_BTCVSD=m
  - SND_SOC_RK3328=n
  - SND_SOC_WM8904=n
  - SND_SOC_XILINX_AUDIO_FORMATTER=n
  - SND_SOC_XILINX_SPDIF=n
  - Input:
  - HID_MALTRON=m
  - HID_VIEWSONIC=m
  - TTY:
  - LDISC_AUTOLOAD=y
  - RTC:
  - RTC_DRV_ABEOZ9=m
  - RTC_DRV_RV3028=m
  - RTC_DRV_SD3078=m
  - RTC_DRV_WILCO_EC=m
  - Industrial IO:
  - AD7606_IFACE_PARALLEL=n
  - AD7606_IFACE_SPI=n
  - AD7768_1=n
  - MAX44009=m
  - PMS7003=n
  - SPS30=n
  - TI_DAC7612=n
  - Misc drivers:
  - ALTERA_FREEZE_BRIDGE=m
  - EDAC_I10NM=m
  - EXTCON_PTN5150=m
  - GNSS_MTK_SERIAL=m
  - GPIO_AMD_FCH=m
  - GPIO_TQMX86=m
  - HABANA_AI=m
  - INPUT_MSM_VIBRATOR=n
  - INTEL_MEI_HDCP=m
  - INTERCONNECT=m
  - IR_RCMM_DECODER=m
  - MFD_TQMX86=m
  - MLX_WDT=m
  - SPI_MTK_QUADSPI=m
  - SPI_NXP_FLEXSPI=n
  - SPI_SIFIVE=n
  - WILCO_EC=m
  - WILCO_EC_DEBUGFS=n
  - Virtualization:
  - HYPERV_IOMMU=y
  - Security:
  - LSM=""
  - SECURITY_SAFESETID=n
  - Testing:
  - TEST_LIVEPATCH=n
  - TEST_STACKINIT=n
  - TEST_VMALLOC=n
  - x86:
  - PCENGINES_APU2=m
  - ppc64/ppc64le:
  - NVRAM=m
  - KCOV=n
  - s390x:
  UID16=y
  DMA_FENCE_TRACE=n
  SCSI_GDTH=n
  UDMABUF=y
  - */debug:
  - PRINTK_CALLER=n
- commit b493de0
* Mon Mar 18 2019 msuchanek@suse.de
- Trim build dependencies of sample subpackage spec file (FATE#326579,
  jsc#SLE-4117, jsc#SLE-3853, bsc#1128910).
- commit 2eae420
* Sun Mar 17 2019 mkubecek@suse.cz
- Drop stale disabled patches
  As discussed in
  http://mailman.suse.de/mlarch/SuSE/kernel/2019/kernel.2019.02/msg00118.html
  http://mailman.suse.de/mlarch/SuSE/kernel/2019/kernel.2019.03/msg00016.html
  some of our patches have been disabled for quite long and attempts to get
  them reviewed failed. Let's drop them now:
  patches.suse/0036-arm-Add-BTB-invalidation-on-switch_mm-for-Cortex-A9-.patch
  patches.suse/0037-arm-Invalidate-BTB-on-prefetch-abort-outside-of-user.patch
  patches.suse/0038-arm-KVM-Invalidate-BTB-on-guest-exit.patch
  patches.suse/0039-arm-Add-icache-invalidation-on-switch_mm-for-Cortex-.patch
  patches.suse/0040-arm-Invalidate-icache-on-prefetch-abort-outside-of-u.patch
  patches.suse/0041-arm-KVM-Invalidate-icache-on-guest-exit-for-Cortex-A.patch
  patches.suse/binutils2_26.patch
  patches.suse/dm-mpath-accept-failed-paths
  patches.suse/pstore-backend-autoaction
- commit 55d6d1e
* Sun Mar 17 2019 mkubecek@suse.cz
- config: enable RANDOM_TRUST_CPU
  The outcome from mailing list discussion when this config option
  appeared was that it makes more sense to enable it by default and let
  those who do not trust their CPU override it on command line; but then
  I forgot to actually change the value.
- commit 138b5df
* Fri Mar 15 2019 tiwai@suse.de
- Update config files: disable CONFIG_FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER (bsc#1127552)
  The deferred fbcon takeover makes little sense with the current openSUSE
  boot setup, and it's harmful (more glitches, etc).  Disable it for now.
- commit 14fa903
* Fri Mar 15 2019 msuchanek@suse.de
- Remove the previous subpackage infrastructure.
  This partially reverts commit 9b3ca32c11854156b2f950ff5e26131377d8445e
  ("Add kernel-subpackage-build.spec (FATE#326579).")
- commit a5ee24e
* Fri Mar 15 2019 msuchanek@suse.de
- Add sample kernel-default-base spec file (FATE#326579, jsc#SLE-4117,
  jsc#SLE-3853, bsc#1128910).
- commit 35c4a52
* Thu Mar 14 2019 msuchanek@suse.de
- Install extra rpm scripts for kernel subpackaging (FATE#326579,
  jsc#SLE-4117, jsc#SLE-3853, bsc#1128910).
- commit ad7c227
* Thu Mar 14 2019 jslaby@suse.cz
- Linux 5.0.2 (bnc#1012628).
- perf/x86/intel: Implement support for TSX Force Abort
  (bnc#1012628).
- x86: Add TSX Force Abort CPUID/MSR (bnc#1012628).
- perf/x86/intel: Generalize dynamic constraint creation
  (bnc#1012628).
- perf/x86/intel: Make cpuc allocations consistent (bnc#1012628).
- ath9k: Avoid OF no-EEPROM quirks without qca,no-eeprom
  (bnc#1012628).
- scripts/gdb: replace flags (MS_xyz -> SB_xyz) (bnc#1012628).
- staging: erofs: compressed_pages should not be accessed again
  after freed (bnc#1012628).
- staging: erofs: keep corrupted fs from crashing kernel in
  erofs_namei() (bnc#1012628).
- gfs2: Fix missed wakeups in find_insert_glock (bnc#1012628).
- bpf: Stop the psock parser before canceling its work
  (bnc#1012628).
- Revert "PCI/PME: Implement runtime PM callbacks" (bnc#1012628).
- media: Revert "media: rc: some events are dropped by userspace"
  (bnc#1012628).
- drm: disable uncached DMA optimization for ARM and arm64
  (bnc#1012628).
- ARM: dts: exynos: Fix max voltage for buck8 regulator on Odroid
  XU3/XU4 (bnc#1012628).
- ARM: dts: exynos: Add minimal clkout parameters to Exynos3250
  PMU (bnc#1012628).
- ARM: dts: exynos: Fix pinctrl definition for eMMC RTSN line
  on Odroid X2/U3 (bnc#1012628).
- arm64: dts: hikey: Revert "Enable HS200 mode on eMMC"
  (bnc#1012628).
- arm64: dts: hikey: Give wifi some time after power-on
  (bnc#1012628).
- arm64: dts: zcu100-revC: Give wifi some time after power-on
  (bnc#1012628).
- x86/PCI: Fixup RTIT_BAR of Intel Denverton Trace Hub
  (bnc#1012628).
- scsi: aacraid: Fix missing break in switch statement
  (bnc#1012628).
- iscsi_ibft: Fix missing break in switch statement (bnc#1012628).
- Input: elan_i2c - add id for touchpad found in Lenovo s21e-20
  (bnc#1012628).
- Input: wacom_serial4 - add support for Wacom ArtPad II tablet
  (bnc#1012628).
- media: uvcvideo: Fix 'type' check leading to overflow
  (bnc#1012628).
- commit 815c1bc
* Mon Mar 11 2019 mkubecek@suse.cz
- Update patches.suse/0001-media-usb-pwc-Don-t-use-coherent-DMA-buffers-for-ISO.patch
  upstream reference.
- commit ff7c8cd
* Sun Mar 10 2019 jslaby@suse.cz
- Linux 5.0.1 (bnc#1012628).
- exec: Fix mem leak in kernel_read_file (bnc#1012628).
- Bluetooth: Fix locking in bt_accept_enqueue() for BH context
  (bnc#1012628).
- Bluetooth: btrtl: Restore old logic to assume firmware is
  already loaded (bnc#1012628).
- selftests: firmware: fix verify_reqs() return value
  (bnc#1012628).
- Revert "selftests: firmware: remove use of non-standard diff
  - Z option" (bnc#1012628).
- Revert "selftests: firmware: add
  CONFIG_FW_LOADER_USER_HELPER_FALLBACK to config" (bnc#1012628).
- USB: serial: cp210x: fix GPIO in autosuspend (bnc#1012628).
- gnss: sirf: fix premature wakeup interrupt enable (bnc#1012628).
- xtensa: fix get_wchan (bnc#1012628).
- aio: Fix locking in aio_poll() (bnc#1012628).
- MIPS: irq: Allocate accurate order pages for irq stack
  (bnc#1012628).
- alpha: wire up io_pgetevents system call (bnc#1012628).
- applicom: Fix potential Spectre v1 vulnerabilities
  (bnc#1012628).
- usb: xhci: Fix for Enabling USB ROLE SWITCH QUIRK on
  INTEL_SUNRISEPOINT_LP_XHCI (bnc#1012628).
- xhci: tegra: Prevent error pointer dereference (bnc#1012628).
- tracing: Fix event filters and triggers to handle negative
  numbers (bnc#1012628).
- x86/boot/compressed/64: Do not read legacy ROM on EFI system
  (bnc#1012628).
- x86/CPU/AMD: Set the CPB bit unconditionally on F17h
  (bnc#1012628).
- tipc: fix RDM/DGRAM connect() regression (bnc#1012628).
- team: Free BPF filter when unregistering netdev (bnc#1012628).
- sky2: Disable MSI on Dell Inspiron 1545 and Gateway P-79
  (bnc#1012628).
- sctp: call iov_iter_revert() after sending ABORT (bnc#1012628).
- qmi_wwan: Add support for Quectel EG12/EM12 (bnc#1012628).
- net-sysfs: Fix mem leak in netdev_register_kobject
  (bnc#1012628).
- net: sched: put back q.qlen into a single location
  (bnc#1012628).
- net: mscc: Enable all ports in QSGMII (bnc#1012628).
- net: dsa: mv8e6xxx: fix number of internal PHYs for 88E6x90
  family (bnc#1012628).
- net: dsa: mv88e6xxx: handle unknown duplex modes gracefully
  in mv88e6xxx_port_set_duplex (bnc#1012628).
- net: dsa: mv88e6xxx: add call to mv88e6xxx_ports_cmode_init
  to probe for new DSA framework (bnc#1012628).
- ip6mr: Do not call __IP6_INC_STATS() from preemptible context
  (bnc#1012628).
- staging: android: ashmem: Avoid range_alloc() allocation with
  ashmem_mutex held (bnc#1012628).
- staging: android: ashmem: Don't call fallocate() with
  ashmem_mutex held (bnc#1012628).
- staging: android: ion: fix sys heap pool's gfp_flags
  (bnc#1012628).
- staging: wilc1000: fix to set correct value for 'vif_num'
  (bnc#1012628).
- staging: comedi: ni_660x: fix missing break in switch statement
  (bnc#1012628).
- staging: erofs: fix illegal address access under memory pressure
  (bnc#1012628).
- staging: erofs: fix race of initializing xattrs of a inode at
  the same time (bnc#1012628).
- staging: erofs: fix memleak of inode's shared xattr array
  (bnc#1012628).
- staging: erofs: fix fast symlink w/o xattr when fs xattr is on
  (bnc#1012628).
- driver core: Postpone DMA tear-down until after devres release
  (bnc#1012628).
- USB: serial: ftdi_sio: add ID for Hjelmslund Electronics USB485
  (bnc#1012628).
- USB: serial: cp210x: add ID for Ingenico 3070 (bnc#1012628).
- USB: serial: option: add Telit ME910 ECM composition
  (bnc#1012628).
- binder: create node flag to request sender's security context
  (bnc#1012628).
- staging: erofs: fix mis-acted TAIL merging behavior
  (bnc#1012628).
- cpufreq: Use struct kobj_attribute instead of struct global_attr
  (bnc#1012628).
- commit 47a2a02
* Thu Mar  7 2019 msuchanek@suse.de
- KMPs: provide and conflict a kernel version specific KMP name
  (bsc#1127155, bsc#1109137).
- commit 5568093
* Wed Mar  6 2019 msuchanek@suse.de
- Revert "Drop multiversion(kernel) from the KMP template (fate#323189)"
  (bsc#1109137).
  This reverts commit 71504d805c1340f68715ad41958e5ef35da2c351.
- commit adade9f
* Tue Mar  5 2019 mkubecek@suse.cz
- config: disable BPFILTER_UMH on non-x86 architectures (bsc#1127188)
  CONFIG_BPFILTER_UMH depends on ability to compile and link a userspace
  binary so that it currently doesn't work in our kbuild check setups using
  a cross compiler. Disable the option on architectures where cross compiler
  is used (i.e. all except x86_64 and i386).
- commit cfb8371
* Mon Mar  4 2019 msuchanek@suse.de
- KMPs: obsolete older KMPs of the same flavour (bsc#1127155, bsc#1109137).
- commit 821419f
* Mon Mar  4 2019 mkubecek@suse.cz
- Update to 5.0 final
- Refresh configs
- commit 8f71df2
* Wed Feb 27 2019 msuchanek@suse.de
- BPF: UMH: do not detect if compiler can link userspace program
  (boo#1127188).
- commit 784e336
* Mon Feb 25 2019 mkubecek@suse.cz
- Update to 5.0-rc8
- Eliminated 1 patch
- commit 4ddf057
* Fri Feb 22 2019 mkubecek@suse.cz
- net: crypto set sk to NULL when af_alg_release (CVE-2019-8912
  bsc#1125907).
- commit 3aed52e
* Fri Feb 22 2019 mkubecek@suse.cz
- config: enable PREEMPT_VOLUNTARY (bsc#1125004)
  Switch to PREEMPT_VOLUNTARY everywhere except s390x/zfcpdump.
- commit f62cec7
* Tue Feb 19 2019 mbenes@suse.cz
- rpm/klp-symbols: Remove the second column in Symbols.list
  Symbols.list file contains also a symbol type next to its name.
  klp-convert cannot handle it well and it is superfluous anyway.
- commit 62a0a00
* Mon Feb 18 2019 mkubecek@suse.cz
- Update to 5.0-rc7
- commit b094e66
* Mon Feb 11 2019 mkubecek@suse.cz
- Update to 5.0-rc6
- commit eb4b248
* Fri Feb  8 2019 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Build livepatch support in SUSE release
  projects (bsc#1124167).
- commit 7519080
* Mon Feb  4 2019 mkubecek@suse.cz
- Update to 5.0-rc5
- Config changes:
  - x86:
  - X86_RESCTRL renamed to X86_CPU_RESCTRL
- commit a42dcc6
* Wed Jan 30 2019 mwilck@suse.com
- rpm/kernel-binary.spec.in: fix initrd permissions (bsc#1123697)
  dracut has been using permissions 0600 for the initrd for a long
  time. On SLE15 or higher, that leads to a permission mismatch
  reported by "rpm -V". Set the permissions correctly for our
  ghost file.
- commit 9e5e2a5
* Mon Jan 28 2019 tiwai@suse.de
- doc/README.SUSE: Correct description for building a kernel (bsc#1123348)
  The obsoleted make cloneconfig is corrected.  Also the order of make
  scripts and make prepare are corrected as well.
- commit 17a2073
* Mon Jan 28 2019 tiwai@suse.de
- rpm/release-projects: Add SUSE:Maintenance:* for MU kernels (bsc#1123317)
- commit c784b79
* Mon Jan 28 2019 mkubecek@suse.cz
- Update to 5.0-rc4
- commit 8e6abff
* Thu Jan 24 2019 ptesarik@suse.cz
- Add product identifying information to VMCOREINFO (bsc#1123015).
- commit 68ca35e
* Thu Jan 24 2019 msuchanek@suse.de
- rpm/kernel-*.spec.in: replace update srchash dependencies (FATE#325312).
  Due to some limitations version cannot be matched so move the hash into
  the provide name.
- commit 219bcec
* Tue Jan 22 2019 oneukum@suse.com
- media: usb: pwc: Don't use coherent DMA buffers for ISO transfer
  (bsc#1054610).
- commit 59d243a
* Mon Jan 21 2019 mkubecek@suse.cz
- Update to 5.0-rc3
- Config changes:
  - ARM64:
  - HSA_AMD=y
- commit 05bf5c0
* Mon Jan 14 2019 mkubecek@suse.cz
- Update to 5.0-rc2
- Config changes:
  - x86:
  - RESCTRL renamed to X86_RESCTRL
- commit 879eb5c
* Fri Jan 11 2019 afaerber@suse.de
- config: arm64: Update to 5.0-rc1
- commit 88c2434
* Mon Jan  7 2019 mkubecek@suse.cz
- config: restore accidentally lost BPFILTER_UMH (ppc64, ppc64le, s390x)
- commit a56baa9
* Mon Jan  7 2019 mkubecek@suse.cz
- vfio_pci: Add local source directory as include.
- commit ea6d6e3
* Mon Jan  7 2019 mkubecek@suse.cz
- Update to 5.0-rc1
- Eliminated 1 patch
- ARM configs need update
- Config changes:
  - PM:
  - ENERGY_MODEL=y
  - Networking:
  - CAN_FLEXCAN=m
  - USB_NET_AQC111=m
  - QTNFMAC_PCIE=m
  - VIRT_WIFI=m
  - PCI:
  - PCI_MESON=n
  - SCSI:
  - SCSI_UFS_CDNS_PLATFORM=m
  - NVME:
  - NVME_TCP=m
  - NVME_TARGET_TCP=m
  - Graphics:
  - DRM_PANEL_OLIMEX_LCD_OLINUXINO=n
  - DRM_PANEL_SAMSUNG_S6D16D0=n
  - DRM_PANEL_TRULY_NT35597_WQXGA=n
  - TINYDRM_HX8357D=n
  - Sound:
  - SND_SOC_AMD_ACP3x=n
  - SND_SOC_INTEL_KBL_RT5660_MACH=m
  - SND_SOC_XILINX_I2S=n
  - SND_SOC_AK4118=n
  - Multimedia:
  - VIDEO_ASPEED=m
  - VIDEO_SECO_CEC=m
  - VIDEO_SECO_RC=y
  - I3C:
  - I3C=m
  - CDNS_I3C_MASTER=m
  - DW_I3C_MASTER=m
  - IIO:
  - AD7124=n
  - AD7949=n
  - TI_DAC7311=n
  - VCNL4035=n
  - SENSORS_RM3100_I2C=n
  - SENSORS_RM3100_SPI=n
  - MCP41010=m
  - PHY:
  - PHY_CADENCE_SIERRA=m
  - PHY_FSL_IMX8MQ_USB=m
  - misc drivers:
  - MTD_PHYSMAP_GPIO_ADDR=y
  - SPI_MXIC=n
  - MISC_ALCOR_PCI=m
  - RC_XBOX_DVD=m
  - PINCTRL_OCELOT=n
  - GPIO_CADENCE=m
  - SENSORS_OCC_P8_I2C=m
  - TQMX86_WDT=m
  - MMC_ALCOR=m
  - MMC_SDHCI_AM654=m
  - LEDS_TRIGGER_AUDIO=m
  - SERIO_OLPC_APSP=m
  - Security:
  - INTEGRITY_PLATFORM_KEYRING=y
  - IMA_ARCH_POLICY=y
  - Crypto:
  - CRYPTO_ADIANTUM=m
  - CRYPTO_STREEBOG=m
  - CRYPTO_STATS=n
  - Library:
  - RAID6_PQ_BENCHMARK=y (preserve current behaviour)
  - Testing:
  - TEST_OBJAGG=n
  - x86:
  - RESCTRL=y
  - HUAWEI_WMI=m
  - i386:
  - PVH=y
  - MTD_PHYSMAP_OF=m
  - ppc*:
  - PVPANIC=m
  - FB_LOGO_CENTER=n
  - FSI_OCC=m
  - DEBUG_VIRTUAL=n
  - SENSORS_OCC_P9_SBE=m
  - s390x:
  - PCCARD=n
  - RAPIDIO
  - other RapidIO options copy other architectures
  - DMADEVICES related options copy other architectures
  - */debug:
  - CRYPTO_STATS=y
  - TTY_PRINTK_LEVEL=6
- commit 6a4ceaa
* Mon Dec 24 2018 mkubecek@suse.cz
- Update to 4.20 final
- Eliminated 1 patch
- Refresh configs
- commit ba5c149
* Fri Dec 21 2018 mkubecek@suse.cz
- rtlwifi: Fix leak of skb when processing C2H_BT_INFO
  (bsc#1116448).
- commit 9d82d20
* Mon Dec 17 2018 mkubecek@suse.cz
- Update to 4.20-rc7
- Config changes:
  - ARM:
  - MEDIA_CONTROLLER_REQUEST_API=y
- commit 4731528
* Mon Dec 10 2018 afaerber@suse.de
- config: arm: Enable EFI support (boo#1104833)
- commit 7050650
* Mon Dec 10 2018 afaerber@suse.de
- config: armv7hl: Update to 4.20-rc5
- commit f01387b
* Mon Dec 10 2018 jslaby@suse.cz
- Delete
  patches.suse/blk-mq-fix-corruption-with-direct-issue.patch.
  It is in 4.20-rc6 as ffe81d45322c but was partially reverted by
  c616cbee97ae, so this patch still applies cleanly, but is unwanted.
  Drop it.
- commit 7670339
* Mon Dec 10 2018 mkubecek@suse.cz
- Update to 4.20-rc6
- Eliminated 1 patch
- Refresh configs
- commit 93f10c3
* Sat Dec  8 2018 msuchanek@suse.de
- Include modules.fips in kernel-binary as well as kernel-binary-base
  (FATE#323247).
- commit e42315d
* Fri Dec  7 2018 jslaby@suse.cz
- x86/build: Fix compiler support check for CONFIG_RETPOLINE
  (KMP build).
- commit fb5fd39
* Wed Dec  5 2018 mkubecek@suse.cz
- blk-mq: fix corruption with direct issue (bko#201685).
- commit 8970eff
* Tue Dec  4 2018 jroedel@suse.de
- blacklist.conf: Blacklist MAINTAINERS file
- commit c4b3c90
* Mon Dec  3 2018 afaerber@suse.de
- config: armv6hl: Update to 4.20-rc5
- commit c85b385
* Mon Dec  3 2018 guillaume.gardet@free.fr
- config: armv7hl: Build some options as modules (boo#1104833)
  Enable HISI_THERMAL=m while at it.
- commit c9b9dd6
* Mon Dec  3 2018 mkubecek@suse.cz
- Update to 4.20-rc5
- Config changes:
  - General:
  - PSI_DEFAULT_DISABLED=y
  - Sound:
  - SND_SOC_INTEL_SKYLAKE_HDAUDIO_CODEC=y
  - ARM:
  - ARM64_ERRATUM_1286807=y
- commit 2ccaf30
* Mon Nov 26 2018 mkubecek@suse.cz
- Update to 4.20-rc4
- Config changes:
  - Networking:
  - MT76_LEDS=y (split from MT76_CORE)
- commit 1ac69b7
* Fri Nov 23 2018 msuchanek@suse.de
- Build ppc64le for POWER8+ (FATE#325617).
- commit f6da51b
* Fri Nov 23 2018 msuchanek@suse.de
- Revert "Remove Cell/PS3 support from ppc64 kernel (boo#1114846)"
  This reverts commit fd6aaf7f98693355e7dcc5e4e1926fb1664d803b.
  Fixed upstream in 43c6494fa149 ("powerpc/io: Fix the IO workarounds code
  to work with Radix")
- commit 4f86993
* Tue Nov 20 2018 rgoldwyn@suse.com
- apparmor: fix unnecessary creation of net-compat (bsc#1116724).
- commit f5cf767
* Mon Nov 19 2018 mkubecek@suse.cz
- Update to 4.20-rc3
- Refresh configs
- commit 81d20d2
* Tue Nov 13 2018 msuchanek@suse.de
- Add kernel-subpackage-build.spec (FATE#326579).
  - add kernel-subpackage-build.spec.in and support scripts
  - hook it in mkspec
  - extend the mechanism that copies dependencies inside
  kernel-binary.spec.in from kernel-%%build_flavor to
  kernel-%%build_flavor-base to also handle
  kernel-subpackage-build.spec.in using BINARY DEPS marker.
  - expand %%name in kernel-%%build_flavor so the dependencies are expanded
  correctly in kernel-subpackage-build.spec.in
- commit 9b3ca32
* Mon Nov 12 2018 mkubecek@suse.cz
- Update to 4.20-rc2
- Eliminated 1 patch
- Config changes:
  - I2C:
    I2C_NVIDIA_GPU=m
  - USB:
    UCSI_CCG=m
- commit 1c08d7f
* Sun Nov 11 2018 afaerber@suse.de
- config: arm64: Update to 4.20-rc1
- commit 2d02cd8
* Thu Nov  8 2018 tiwai@suse.de
- rpm/kernel-source.spec.in: Add patches.drm for moved DRM patches
- commit 8592674
* Thu Nov  8 2018 jslaby@suse.cz
- doc/README.SUSE: correct GIT url
  No more gitorious, github we use.
- commit 31864f3
* Tue Nov  6 2018 mkubecek@suse.cz
- config: reenable BPFILTER_UMH on ppc64
- commit 46cb36e
* Tue Nov  6 2018 agraf@suse.de
- Remove Cell/PS3 support from ppc64 kernel (boo#1114846)
- commit fd6aaf7
* Mon Nov  5 2018 mkubecek@suse.cz
- scripts/mkmakefile: honor second argument.
- commit 78325a6
* Mon Nov  5 2018 mkubecek@suse.cz
- rpm/kernel-binary.spec.in: add macros.s into kernel-*-devel
  Starting with 4.20-rc1, file arch/*/kernel/macros.s is needed to build out
  of tree modules. Add it to kernel-${flavor}-devel packages if it exists.
- commit 09d14c8
* Mon Nov  5 2018 mkubecek@suse.cz
- series.conf: delete an obsolete comment
- commit c3bd57d
* Mon Nov  5 2018 jslaby@suse.cz
- Refresh
  patches.suse/0005-x86-enter-Use-IBRS-on-syscall-and-interrupts.patch.
  Adapt to 4.20.
- commit dcaec93
* Mon Nov  5 2018 mkubecek@suse.cz
- Update to 4.20-rc1
- ARM configs need updating
- disabled (needs refresh):
  patches.suse/0005-x86-enter-Use-IBRS-on-syscall-and-interrupts.patch
- Config changes:
  - General:
  - PSI=y
  - Networking:
  - NFT_XFRM=m
  - NET_SCH_TAPRIO=m
  - BATMAN_ADV_TRACING=n
  - NCSI_OEM_CMD_GET_MAC=y
  - EEPROM_EE1004=m
  - SCSI_UFS_BSG=y
  - SCSI_MYRB=m
  - SCSI_MYRS=m
  - IXGBE_IPSEC=y
  - IXGBEVF_IPSEC=y
  - IGC=m
  - NI_XGE_MANAGEMENT_ENET=m
  - MT76x0E=m
  - File systems:
  - EROFS_FS_IO_MAX_RETRIES=5 (default)
  - AFS_DEBUG_CURSOR=n
  - CONFIG_UBIFS_FS_AUTHENTICATION=y
  - Crypto:
  - CRYPTO_OFB=m
  - CRYPTO_STATS=n
  - ASYMMETRIC_TPM_KEY_SUBTYPE=m
  - PKCS8_PRIVATE_KEY_PARSER=m
  - TPM_KEY_PARSER=m
  - Graphics:
  - VIDEO_VICODEC=m
  - DRM_FBDEV_LEAK_PHYS_SMEM=n
  - DRM_I915_DEBUG_RUNTIME_PM=n
  - DRM_TOSHIBA_TC358764=n
  - DRM_TI_SN65DSI86=n
  - Sound:
  - SND_SOC_INTEL_KBL_DA7219_MAX98927_MACH=m
  - SND_SOC_INTEL_SKL_HDA_DSP_GENERIC_MACH=m
  - SND_SOC_MAX98088=n
  - SND_SOC_PCM3060_I2C=n
  - SND_SOC_PCM3060_SPI=n
  - SND_SOC_NAU8822=n
  - Input devices:
  - HID_BIGBEN_FF=m
  - Platform:
  - LG_LAPTOP=m
  - INTEL_ATOMISP2_PM=m
  - IIO:
  - ADXL372_SPI=n
  - ADXL372_I2C=n
  - MCP3911=n
  - QCOM_SPMI_ADC5=n
  - LTC1660=n
  - VL53L0X_I2C=m
  - Misc drivers:
  - UDMABUF=y
  - MFD_AT91_USART=n
  - LEDS_AN30259A=n
  - LEDS_TRIGGER_PATTERN=m
  - PHY_CADENCE_DP=m
  - STM_PROTO_BASIC=m
  - STM_PROTO_SYS_T=m
  - Testing:
  - TEST_XARRAY=n
  - TEST_MEMCAT_P=n
  - x86:
  - X86_CPA_STATISTICS=n (y for -debug)
  - i386:
  - MSCC_OCELOT_SWITCH_OCELOT=m
  - ppc64, ppc64le:
  - PAPR_SCM=m
  - PCI_P2PDMA=y
  - STACKPROTECTOR=y
  - STACKPROTECTOR_STRONG=n
  - BLK_DEV_PMEM=m
  - ND_BLK=m
  - BTT=y
  - NVDIMM_PFN=y
  - NVDIMM_DAX=y
  - OF_PMEM=m
  - DEV_DAX_PMEM=m
  - FAIL_FUNCTION=n
  - ENA_ETHERNET=m
  - s390:
  - VMAP_STACK=y
  - S390_AP_IOMMU=n
  - ZCRYPT_MULTIDEVNODES=y
  - KASAN=n
  - */debug:
  - INTEL_IOMMU_DEBUGFS=y
  - BPF_KPROBE_OVERRIDE=y
  - CONFIG_X86_CPA_STATISTICS=y
  - CONFIG_CRYPTO_STATS=y
- commit f29310b
* Sun Nov  4 2018 mkubecek@suse.cz
- rpm: use syncconfig instead of silentoldconfig where available
  Since mainline commit 0085b4191f3e ("kconfig: remove silentoldconfig
  target"), "make silentoldconfig" can be no longer used. Use "make
  syncconfig" instead if available.
- commit a239c6e
* Fri Nov  2 2018 mkubecek@suse.cz
- series.conf: more descriptive name for network driver section
  We have two networking sections in series.conf: one for networking core and
  one for network drivers. The latter is among other driver related sections
  but it may not be obvious that it is not intended for core networking
  patches. Change the label to "Network drivers" to make its purpose more
  apparent.
- commit 7968e32
* Fri Nov  2 2018 mkubecek@suse.cz
- config: enable SCSI_AACRAID on ppc64le and ppc64 (bsc#1114523)
- commit 5f3762b
* Tue Oct 30 2018 jslaby@suse.cz
- Refresh
  patches.suse/netfilter-bridge-define-INT_MIN-INT_MAX-in-userspace.patch.
  Update upstream status.
- commit 37417fa
* Tue Oct 30 2018 jmoreira@suse.de
- Add version information to KLP_SYMBOLS file
- commit f77f8d2
* Thu Oct 25 2018 mwilck@suse.com
- rpm/kernel-binary.spec.in: allow unsupported modules for -extra
  (bsc#1111183). SLE-15 and later only.
- commit 0d585a8
* Wed Oct 24 2018 mkubecek@suse.cz
- series.conf: move patches.suse/netfilter-bridge-define-INT_MIN-INT_MAX-in-userspace.patch to netfilter section
- commit 7656685
* Wed Oct 24 2018 jslaby@suse.cz
- netfilter: bridge: define INT_MIN & INT_MAX in userspace
  (4.19 fixes).
- commit e7213f6
* Mon Oct 22 2018 mkubecek@suse.cz
- Update to 4.19 final
- Refresh configs
- commit b4c35bb
* Mon Oct 15 2018 mkubecek@suse.cz
- Update to 4.19-rc8
- commit 2e61ca8
* Fri Oct 12 2018 tzimmermann@suse.de
- README: Clean-up trailing whitespace
- commit 06542f9
* Thu Oct 11 2018 tzimmermann@suse.de
- README: Update documentation wrt. Patch-mainline
  Common practice is to set Patch-mainline to a Linux release tag. More
  than 95%% of all patches follow this convention. The remaining 5%% have
  been fixed accordingly in SLE15.
  The README file is inconsistent wrt. to the content of Patch-mainline.
  In some places it refers to a release tag, in others it refers to a version
  number. With this cleanup, it refers to release tags everywhere.
  This change is a follow-up for commit 1d81d2699cd3.
- commit 57326f5
* Tue Oct  9 2018 msuchanek@suse.de
- Revert "Limit kernel-source build to architectures for which we build binaries"
  This reverts commit d6435125446d740016904abe30a60611549ae812.
- commit 48b03c4
* Mon Oct  8 2018 mkubecek@suse.cz
- Update to 4.19-rc7
- commit 63b130b
* Thu Oct  4 2018 mbrugger@suse.com
- arm64: Update config files. (bsc#1110716)
  Enable ST LPS25H pressure sensor.
- commit 9882f33
* Tue Oct  2 2018 nborisov@suse.com
- Update config files. (boo##1109665)
- commit 76516eb
* Mon Oct  1 2018 msuchanek@suse.de
- rpm/mkspec: fix ppc64 kernel-source build.
- commit 85c9272
* Sun Sep 30 2018 mkubecek@suse.cz
- Update to 4.19-rc6
- Eliminated 2 patches
- commit 80aa112
* Sat Sep 29 2018 lduncan@suse.com
- Added CVE numbers for two patches (bsc#1107829)
- commit e3ac2a8
* Fri Sep 28 2018 lduncan@suse.com
- scsi: target: iscsi: Use bin2hex instead of a re-implementation
  (bsc#1107829).
- scsi: target: iscsi: Use hex2bin instead of a re-implementation
  (bsc#1107829).
- commit 8791706
* Thu Sep 27 2018 msuchanek@suse.de
- rpm/mkspec: build dtbs for architectures marked -!needs_updating
- commit 2d47640
* Thu Sep 27 2018 msuchanek@suse.de
- Limit kernel-source build to architectures for which we build binaries
  (bsc#1108281).
- commit d643512
* Tue Sep 25 2018 mbrugger@suse.com
- arm64: Update config files.
  Increase NR_CPUS to 480 (fate#325592)
- commit d5464c0
* Mon Sep 24 2018 mkubecek@suse.cz
- Update to 4.19-rc5
- commit b44d7bc
* Mon Sep 17 2018 mkubecek@suse.cz
- Update to 4.19-rc4
- Eliminated 1 patch
- Config changes:
  - Filesystems:
  - EROFS_FS=m
  - EROFS_FS_DEBUG=n
  - EROFS_FS_XATTR=y
  - EROFS_FS_POSIX_ACL=y
  - EROFS_FS_SECURITY=y
  - EROFS_FS_USE_VM_MAP_RAM=n
  - EROFS_FAULT_INJECTION=n
  - EROFS_FS_ZIP=n
- commit 625b101
* Fri Sep 14 2018 mkubecek@suse.cz
- ip: frags: fix crash in ip_do_fragment() (bsc#1108533).
- commit ba41502
* Fri Sep 14 2018 msuchanek@suse.de
- doc/README.SUSE: Remove mentions of cloneconfig (bsc#1103636).
- commit 3371adc
* Thu Sep 13 2018 jbohac@suse.cz
- Delete patches.suse/x86_64-hpet-64bit-timer.patch.
  We removed the patch from SLE15 in commit
  20efbd0c034fea7c97243120a025587d0dbac1c2
  and we don't need it in future versions of SLE.
- commit aa4eb67
* Mon Sep 10 2018 msuchanek@suse.de
- macros.kernel-source: pass -b properly in kernel module package
  (bsc#1107870).
- commit 66709cd
* Mon Sep 10 2018 mkubecek@suse.cz
- Update to 4.19-rc3
- refresh configs
- commit d3995d7
* Fri Sep  7 2018 jeffm@suse.com
- config: disable HFS_FS
  It has no maintainer and has been a source of fuzzer bugs.  hfsplus handles
  the HFS+ file system that became the default on MacOS in 1998.
- commit 0d9481c
* Fri Sep  7 2018 tiwai@suse.de
- supported.conf: Add bpfilter to kernel-default-base (bsc#1106751)
- commit 8f1f1b6
* Mon Sep  3 2018 jslaby@suse.cz
- rpm/kernel-binary.spec.in: fix call of split-modules
  split-modules is called with some parameters depending on config
  options. But since we do not use backslash consistelny, the call to
  split-modules might be evaluated so that also the following cat
  command is appended. Avoid this behaviour by using backslashes
  everywhere and add %%nil to the end.
  This perhaps never happens, but stay on the safe side.
- commit 32df888
* Mon Sep  3 2018 mkubecek@suse.cz
- Update to 4.19-rc2
- refresh configs
- commit a9462db
* Sat Sep  1 2018 afaerber@suse.de
- config: arm64: Increase SERIAL_8250_RUNTIME_UARTS to 32 (boo#1073193)
  (cherry picked from commit 0dbc49ba128ef0931ca04cf22ec5c638534f5b23)
- commit 6aae50e
* Sat Sep  1 2018 afaerber@suse.de
- config: Enable SERIAL_SC16IS7XX_SPI on arm and x86 (bsc#1105672, fate#326668)
  (cherry picked from commit cdc9eced6d892ff77abbeef5f0d5eb38c114602c)
- commit 22a4d36
* Sat Sep  1 2018 afaerber@suse.de
- config: Consistently increase SERIAL_8250_NR_UARTS to 32 (boo#1073193)
  (cherry picked from commit acb36abf212a3a7428d958798d678d82351f4658)
- commit 090b553
* Sat Sep  1 2018 afaerber@suse.de
- config: armv7hl: Update to 4.19-rc1
- commit d1f42dc
* Sat Sep  1 2018 afaerber@suse.de
- config: armv7hl: Update to 4.18.5 (bsc#1012628)
  (cherry picked from commit fa0ebc5508eedec2c9108cafdf854a8c53a28a83)
  [AF: Don't re-enable the configs yet]
- commit f2722e4
* Sat Sep  1 2018 afaerber@suse.de
- config: armv6hl: Update to 4.19-rc1
- commit 2f56919
* Fri Aug 31 2018 afaerber@suse.de
- config: armv6hl: Update to 4.18.5 (bsc#1012628)
  (cherry picked from commit e9071067714392290f6b0d525c77c8abfa8cf075)
  [AF: Don't re-enable configs yet]
- commit d01db43
* Fri Aug 31 2018 afaerber@suse.de
- config: arm64: Update to 4.19-rc1
- commit a6a88d1
* Wed Aug 29 2018 mkubecek@suse.cz
- powerpc/boot: Fix missing crc32poly.h when building with
  KERNEL_XZ.
- Delete
  patches.rpmify/Revert-lib-Use-existing-define-with-polynomial.patch.
- commit cba84f7
* Wed Aug 29 2018 mkubecek@suse.cz
- kernel-binary: check also bzImage on s390/s390x
  Starting with 4.19-rc1, uncompressed image is no longer built on s390x.
  If file "image" is not found in arch/s390/boot after the build, try bzImage
  instead.
  For now, install bzImage under the name image-* until we know grub2 and our
  grub2 scripts can handle correct name.
- commit 92b52c6
* Tue Aug 28 2018 jbeulich@suse.com
- Refresh patches.suse/supported-flag after upstream commit b2c5cdcfd4.
- Refresh
  patches.suse/kernel-add-product-identifying-information-to-kernel-build.patch.
- commit 8b0e2e5
* Mon Aug 27 2018 mkubecek@suse.cz
- Revert "lib: Use existing define with polynomial".
- commit 1dc6366
* Mon Aug 27 2018 mkubecek@suse.cz
- Update to 4.19-rc1
- Eliminated 179 patches (167 stable, 12 other)
- ARM configs need updating
- Config changes:
  - Block:
  - BLK_CGROUP_IOLATENCY=y
  - Networking:
  - XFRM_INTERFACE=m
  - NETFILTER_NETLINK_OSF=m
  - NFT_TUNNEL=m
  - NFT_OSF=m
  - NFT_TPROXY=m
  - NET_SCH_ETF=m
  - NET_SCH_SKBPRIO=m
  - NET_SCH_CAKE=m
  - CAN_UCAN=m
  - BT_HCIUART_RTL=y
  - BT_MTKUART=m
  - BCMGENET=m
  - SYSTEMPORT=m
  - BNXT_HWMON=y
  - NET_VENDOR_CADENCE=y	(rename)
  - BE2NET_BE2=y
  - BE2NET_BE3=y
  - BE2NET_LANCER=y
  - BE2NET_SKYHAWK=y
  - MLX5_EN_ARFS=y
  - MLX5_EN_RXNFC=y
  - NET_VENDOR_NETERION=y
  - NET_VENDOR_PACKET_ENGINES=y
  - MT76x0U=m
  - MT76x2U=m
  - IEEE802154_HWSIM=m
  - File systems:
  - OVERLAY_FS_METACOPY=n
  - UBIFS_FS_XATTR=y
  - PSTORE_ZSTD_COMPRESS=y
  - CIFS_ALLOW_INSECURE_LEGACY=y
  - Security:
  - RANDOM_TRUST_CPU=n
  - IMA_APPRAISE_BUILD_POLICY=n
  - Hacking:
  - CONSOLE_LOGLEVEL_QUIET=4
  - KPROBE_EVENTS_ON_NOTRACE=n
  - TEST_BITFIELD=n
  - TEST_IDA=n
  - Library:
  - CRC64=m
  - Graphics:
  - VIDEO_CROS_EC_CEC=m
  - DRM_DP_CEC=y
  - DRM_VKMS=m
  - TINYDRM_ILI9341=n
  - FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER=y
  - Sound:
  - SND_SOC_INTEL_GLK_RT5682_MAX98357A_MACH=m
  - SND_SOC_ES7241=n
  - SND_SOC_SIMPLE_AMPLIFIER=n
  - Input:
  - TOUCHSCREEN_ADC=m
  - TOUCHSCREEN_BU21029=m
  - HID_COUGAR=m
  - USB:
  - TYPEC_DP_ALTMODE=m
  - Multifunction:
  - MFD_MADERA=m
  - MFD_MADERA_I2C=m
  - MFD_MADERA_SPI=m
  - GPIO_MADERA=m
  - MFD_CS47L35=y
  - MFD_CS47L85=y
  - MFD_CS47L90=y
  - IIO:
  - BME680=m
  - AD5758=n
  - SI1133=n
  - ISL29501=m
  - FPGA:
  - FPGA_DFL=m
  - FPGA_DFL_FME=m
  - FPGA_DFL_FME_MGR=m
  - FPGA_DFL_FME_BRIDGE=m
  - FPGA_DFL_FME_REGION=m
  - FPGA_DFL_AFU=m
  - FPGA_DFL_PCI=m
  - XILINX_PR_DECOUPLER=m
  - Power management:
  - IDLE_INJECT=y
  - CHARGER_ADP5061=m
  - CHARGER_CROS_USBPD=m
  - SENSORS_MLXREG_FAN=m
  - SENSORS_NPCM7XX=m
  - Misc drivers:
  - GNSS=m
  - GNSS_SERIAL=m
  - GNSS_SIRF_SERIAL=m
  - GNSS_UBX_SERIAL=m
  - MTD_SPI_NAND=m
  - NVM_PBLK_DEBUG=n
  - PINCTRL_ICELAKE=m
  - COMMON_CLK_MAX9485=n
  - IOMMU_DEFAULT_PASSTHROUGH=n
  - XEN:
  - XEN_GRANT_DMA_ALLOC=y
  - XEN_GNTDEV_DMABUF=y
  - x86:
  - STAGING_GASKET_FRAMEWORK=m
  - STAGING_APEX_DRIVER=m
  - XIL_AXIS_FIFO=m
  - TOUCHSCREEN_DMI=y
  - I2C_MULTI_INSTANTIATE=m
  - CROS_EC_I2C=m
  - CROS_EC_SPI=m
  - MLXREG_IO=m
  - i386:
  - PCIE_XILINX=y
  - MFD_ROHM_BD718XX=n
  - DRM_PANEL_ILITEK_ILI9881C=n
  - MMC_SDHCI_OF_DWCMSHC=n
  - PAGE_TABLE_ISOLATION=y
  - PowerPC:
  - I2C_MUX_PINCTRL=m
  - I2C_DEMUX_PINCTRL=m
  - I2C_FSI=m
  - DEBUG_PINCTRL=n
  - PINCTRL_AMD=m
  - PINCTRL_MCP23S08=n
  - PINCTRL_SINGLE=n
  - PINCTRL_SX150X=n
  - LEDS_AAT1290=n
  - FSI_NEW_DEV_NODE=n
  - FSI_SBEFIFO=m
  - S/390:
  - KERNEL_GZIP=y
  - S2IO=m
  - VXGE=m
  - VXGE_DEBUG_TRACE_ALL=n
  - HAMACHI=m
  - YELLOWFIN=m
  - MDIO_BCM_UNIMAC=m
  - ISM=m
  - */debug:
  - NVM_PBLK_DEBUG=y
  - IOMMU_DEBUGFS=y
  - PREEMPTIRQ_DELAY_TEST=m
- commit a3b9cac
* Fri Aug 24 2018 jslaby@suse.cz
- Linux 4.18.5 (bnc#1012628).
- reiserfs: fix broken xattr handling (heap corruption, bad
  retval) (bnc#1012628).
- i2c: imx: Fix race condition in dma read (bnc#1012628).
- i2c: core: ACPI: Properly set status byte to 0 for multi-byte
  writes (bnc#1012628).
- PCI: pciehp: Fix unprotected list iteration in IRQ handler
  (bnc#1012628).
- PCI: pciehp: Fix use-after-free on unplug (bnc#1012628).
- PCI: Skip MPS logic for Virtual Functions (VFs) (bnc#1012628).
- PCI: aardvark: Size bridges before resources allocation
  (bnc#1012628).
- PCI: hotplug: Don't leak pci_slot on registration failure
  (bnc#1012628).
- PCI / ACPI / PM: Resume all bridges on suspend-to-RAM
  (bnc#1012628).
- PCI: Restore resized BAR state on resume (bnc#1012628).
- parisc: Remove ordered stores from syscall.S (bnc#1012628).
- parisc: Remove unnecessary barriers from spinlock.h
  (bnc#1012628).
- drm/amdgpu/pm: Fix potential Spectre v1 (bnc#1012628).
- drm/i915/kvmgt: Fix potential Spectre v1 (bnc#1012628).
- ext4: fix spectre gadget in ext4_mb_regular_allocator()
  (bnc#1012628).
- powerpc64s: Show ori31 availability in spectre_v1 sysfs file
  not v2 (bnc#1012628).
- x86/mm/init: Remove freed kernel image areas from alias mapping
  (bnc#1012628).
- x86/mm/init: Add helper for freeing kernel image pages
  (bnc#1012628).
- x86/mm/init: Pass unconverted symbol addresses to
  free_init_pages() (bnc#1012628).
- mm: Allow non-direct-map arguments to free_reserved_area()
  (bnc#1012628).
- pty: fix O_CLOEXEC for TIOCGPTPEER (bnc#1012628).
- EDAC: Add missing MEM_LRDDR4 entry in edac_mem_types[]
  (bnc#1012628).
- commit d918293
* Fri Aug 24 2018 vbabka@suse.cz
- x86/speculation/l1tf: Suggest what to do on systems with too
  much RAM (bsc#1105536).
- x86/speculation/l1tf: Fix off-by-one error when warning that
  system has too much RAM (bsc#1105536).
- x86/speculation/l1tf: Fix overflow in l1tf_pfn_limit() on 32bit
  (OBS failures reported on IRC).
- commit f3b24ad
* Fri Aug 24 2018 jslaby@suse.cz
- Update config files.
- Delete
  patches.suse/revert-mm-relax-deferred-struct-page-requirements.patch.
  We actually do not this non-upstream revert. We only need the config
  change. That is: leave DEFERRED_STRUCT_PAGE_INIT=n for i386 as it was
  before 4.16.
- commit 161b8ee
* Wed Aug 22 2018 jslaby@suse.cz
- Linux 4.18.4 (bnc#1012628).
- l2tp: use sk_dst_check() to avoid race on sk->sk_dst_cache
  (bnc#1012628).
- net_sched: fix NULL pointer dereference when delete tcindex
  filter (bnc#1012628).
- net_sched: Fix missing res info when create new tc_index filter
  (bnc#1012628).
- r8169: don't use MSI-X on RTL8168g (bnc#1012628).
- ALSA: hda - Sleep for 10ms after entering D3 on Conexant codecs
  (bnc#1012628).
- ALSA: hda - Turn CX8200 into D3 as well upon reboot
  (bnc#1012628).
- ALSA: vx222: Fix invalid endian conversions (bnc#1012628).
- ALSA: virmidi: Fix too long output trigger loop (bnc#1012628).
- ALSA: cs5535audio: Fix invalid endian conversion (bnc#1012628).
- ALSA: dice: fix wrong copy to rx parameters for Alesis iO26
  (bnc#1012628).
- ALSA: hda: Correct Asrock B85M-ITX power_save blacklist entry
  (bnc#1012628).
- ALSA: memalloc: Don't exceed over the requested size
  (bnc#1012628).
- ALSA: vxpocket: Fix invalid endian conversions (bnc#1012628).
- ALSA: seq: Fix poll() error return (bnc#1012628).
- media: gl861: fix probe of dvb_usb_gl861 (bnc#1012628).
- USB: serial: sierra: fix potential deadlock at close
  (bnc#1012628).
- USB: serial: pl2303: add a new device id for ATEN (bnc#1012628).
- USB: option: add support for DW5821e (bnc#1012628).
- ACPI / PM: save NVS memory for ASUS 1025C laptop (bnc#1012628).
- tty: serial: 8250: Revert NXP SC16C2552 workaround
  (bnc#1012628).
- serial: 8250_exar: Read INT0 from slave device, too
  (bnc#1012628).
- serial: 8250_dw: always set baud rate in dw8250_set_termios
  (bnc#1012628).
- serial: 8250_dw: Add ACPI support for uart on Broadcom SoC
  (bnc#1012628).
- uio: fix wrong return value from uio_mmap() (bnc#1012628).
- misc: sram: fix resource leaks in probe error path
  (bnc#1012628).
- Revert "uio: use request_threaded_irq instead" (bnc#1012628).
- Bluetooth: avoid killing an already killed socket (bnc#1012628).
- isdn: Disable IIOCDBGVAR (bnc#1012628).
- net: sock_diag: Fix spectre v1 gadget in __sock_diag_cmd()
  (bnc#1012628).
- r8169: don't use MSI-X on RTL8106e (bnc#1012628).
- ip_vti: fix a null pointer deferrence when create vti fallback
  tunnel (bnc#1012628).
- net: ethernet: mvneta: Fix napi structure mixup on armada 3700
  (bnc#1012628).
- net: mvneta: fix mvneta_config_rss on armada 3700 (bnc#1012628).
- cls_matchall: fix tcf_unbind_filter missing (bnc#1012628).
- commit a7b92e4
* Wed Aug 22 2018 jslaby@suse.cz
- Linux 4.18.3 (bnc#1012628).
- x86/speculation/l1tf: Exempt zeroed PTEs from inversion
  (bnc#1012628).
- commit a14f6a3
* Wed Aug 22 2018 jslaby@suse.cz
- Linux 4.18.2 (bnc#1012628).
- x86/mm: Add TLB purge to free pmd/pte page interfaces
  (bnc#1012628).
- ioremap: Update pgtable free interfaces with addr (bnc#1012628).
- Bluetooth: hidp: buffer overflow in hidp_process_report
  (bnc#1012628).
- crypto: skcipher - fix crash flushing dcache in error path
  (bnc#1012628).
- crypto: skcipher - fix aligning block size in skcipher_copy_iv()
  (bnc#1012628).
- crypto: ablkcipher - fix crash flushing dcache in error path
  (bnc#1012628).
- crypto: blkcipher - fix crash flushing dcache in error path
  (bnc#1012628).
- crypto: vmac - separate tfm and request context (bnc#1012628).
- crypto: vmac - require a block cipher with 128-bit block size
  (bnc#1012628).
- crypto: x86/sha256-mb - fix digest copy in
  sha256_mb_mgr_get_comp_job_avx2() (bnc#1012628).
- crypto: ccp - Fix command completion detection race
  (bnc#1012628).
- crypto: ccp - Check for NULL PSP pointer at module unload
  (bnc#1012628).
- crypto: ccree - fix iv handling (bnc#1012628).
- crypto: ccree - fix finup (bnc#1012628).
- kbuild: verify that $DEPMOD is installed (bnc#1012628).
- x86/mm: Disable ioremap free page handling on x86-PAE
  (bnc#1012628).
- xen/pv: Call get_cpu_address_sizes to set x86_virt/phys_bits
  (bnc#1012628).
- x86/mm/pti: Clear Global bit more aggressively (bnc#1012628).
- x86/platform/UV: Mark memblock related init code and data
  correctly (bnc#1012628).
- x86/hyper-v: Check for VP_INVAL in hyperv_flush_tlb_others()
  (bnc#1012628).
- x86: i8259: Add missing include file (bnc#1012628).
- x86/l1tf: Fix build error seen if CONFIG_KVM_INTEL is disabled
  (bnc#1012628).
- commit 51ef786
* Wed Aug 22 2018 jslaby@suse.cz
- Linux 4.18.1 (bnc#1012628).
- x86/init: fix build with CONFIG_SWAP=n (bnc#1012628).
- cpu/hotplug: Non-SMP machines do not make use of booted_once
  (bnc#1012628).
- x86/smp: fix non-SMP broken build due to redefinition of
  apic_id_is_primary_thread (bnc#1012628).
- commit 7e40689
* Tue Aug 21 2018 msuchanek@suse.de
- ACPICA: Clear status of all events when entering sleep states
  (boo#1104529).
- commit 5d7a9a7
* Tue Aug 21 2018 msuchanek@suse.de
- Delete patches.suse/Revert-ACPICA-Events-Stop-unconditionally-clearing-A.patch.
- commit fb1dc2b
* Fri Aug 17 2018 mkubecek@suse.cz
- rpm/constraints.in: raise memory constraints
  Build statistics show that most architectures already need more than 2 GB.
  Require 4 GB except s390x where the memory usage is much lower and we might
  have trouble finding any compliant worker.
- commit 71aefb3
* Thu Aug 16 2018 msuchanek@suse.de
- Revert "ACPICA: Events: Stop unconditionally clearing ACPI
  IRQs during suspend/resume" (boo#1104529, bko#196249).
- commit 5dac824
* Wed Aug 15 2018 mkubecek@suse.cz
- Update config files.
- commit 07db4aa
* Wed Aug 15 2018 jslaby@suse.cz
- Linux 4.18.1-rc1
  It contains the L1TF fixes, so push the rc1 for now.
- x86/paravirt: Fix spectre-v2 mitigations for paravirt guests
  (bnc#1012628).
- x86/speculation: Protect against userspace-userspace spectreRSB
  (bnc#1012628).
- kprobes/x86: Fix %%p uses in error messages (bnc#1012628).
- x86/irqflags: Provide a declaration for native_save_fl
  (bnc#1012628).
- x86/speculation/l1tf: Increase 32bit PAE __PHYSICAL_PAGE_SHIFT
  (bnc#1012628).
- x86/speculation/l1tf: Change order of offset/type in swap entry
  (bnc#1012628).
- x86/speculation/l1tf: Protect swap entries against L1TF
  (bnc#1012628).
- x86/speculation/l1tf: Protect PROT_NONE PTEs against speculation
  (bnc#1012628).
- x86/speculation/l1tf: Make sure the first page is always
  reserved (bnc#1012628).
- x86/speculation/l1tf: Add sysfs reporting for l1tf
  (bnc#1012628).
- x86/speculation/l1tf: Disallow non privileged high MMIO
  PROT_NONE mappings (bnc#1012628).
- x86/speculation/l1tf: Limit swap file size to MAX_PA/2
  (bnc#1012628).
- x86/bugs: Move the l1tf function and define pr_fmt properly
  (bnc#1012628).
- sched/smt: Update sched_smt_present at runtime (bnc#1012628).
- x86/smp: Provide topology_is_primary_thread() (bnc#1012628).
- x86/topology: Provide topology_smt_supported() (bnc#1012628).
- cpu/hotplug: Make bringup/teardown of smp threads symmetric
  (bnc#1012628).
- cpu/hotplug: Split do_cpu_down() (bnc#1012628).
- cpu/hotplug: Provide knobs to control SMT (bnc#1012628).
- x86/cpu: Remove the pointless CPU printout (bnc#1012628).
- x86/cpu/AMD: Remove the pointless detect_ht() call
  (bnc#1012628).
- x86/cpu/common: Provide detect_ht_early() (bnc#1012628).
- x86/cpu/topology: Provide detect_extended_topology_early()
  (bnc#1012628).
- x86/cpu/intel: Evaluate smp_num_siblings early (bnc#1012628).
- x86/CPU/AMD: Do not check CPUID max ext level before parsing
  SMP info (bnc#1012628).
- x86/cpu/AMD: Evaluate smp_num_siblings early (bnc#1012628).
- x86/apic: Ignore secondary threads if nosmt=force (bnc#1012628).
- x86/speculation/l1tf: Extend 64bit swap file size limit
  (bnc#1012628).
- x86/cpufeatures: Add detection of L1D cache flush support
  (bnc#1012628).
- x86/CPU/AMD: Move TOPOEXT reenablement before reading
  smp_num_siblings (bnc#1012628).
- x86/speculation/l1tf: Protect PAE swap entries against L1TF
  (bnc#1012628).
- x86/speculation/l1tf: Fix up pte->pfn conversion for PAE
  (bnc#1012628).
- Revert "x86/apic: Ignore secondary threads if nosmt=force"
  (bnc#1012628).
- cpu/hotplug: Boot HT siblings at least once (bnc#1012628).
- x86/KVM: Warn user if KVM is loaded SMT and L1TF CPU bug being
  present (bnc#1012628).
- x86/KVM/VMX: Add module argument for L1TF mitigation
  (bnc#1012628).
- x86/KVM/VMX: Add L1D flush algorithm (bnc#1012628).
- x86/KVM/VMX: Add L1D MSR based flush (bnc#1012628).
- x86/KVM/VMX: Add L1D flush logic (bnc#1012628).
- x86/KVM/VMX: Split the VMX MSR LOAD structures to have an
  host/guest numbers (bnc#1012628).
- x86/KVM/VMX: Add find_msr() helper function (bnc#1012628).
- x86/KVM/VMX: Separate the VMX AUTOLOAD guest/host number
  accounting (bnc#1012628).
- x86/KVM/VMX: Extend add_atomic_switch_msr() to allow VMENTER
  only MSRs (bnc#1012628).
- x86/KVM/VMX: Use MSR save list for IA32_FLUSH_CMD if required
  (bnc#1012628).
- cpu/hotplug: Online siblings when SMT control is turned on
  (bnc#1012628).
- x86/litf: Introduce vmx status variable (bnc#1012628).
- x86/kvm: Drop L1TF MSR list approach (bnc#1012628).
- x86/l1tf: Handle EPT disabled state proper (bnc#1012628).
- x86/kvm: Move l1tf setup function (bnc#1012628).
- x86/kvm: Add static key for flush always (bnc#1012628).
- x86/kvm: Serialize L1D flush parameter setter (bnc#1012628).
- x86/kvm: Allow runtime control of L1D flush (bnc#1012628).
- cpu/hotplug: Expose SMT control init function (bnc#1012628).
- cpu/hotplug: Set CPU_SMT_NOT_SUPPORTED early (bnc#1012628).
- x86/bugs, kvm: Introduce boot-time control of L1TF mitigations
  (bnc#1012628).
- Documentation: Add section about CPU vulnerabilities
  (bnc#1012628).
- x86/speculation/l1tf: Unbreak !__HAVE_ARCH_PFN_MODIFY_ALLOWED
  architectures (bnc#1012628).
- x86/KVM/VMX: Initialize the vmx_l1d_flush_pages' content
  (bnc#1012628).
- Documentation/l1tf: Fix typos (bnc#1012628).
- cpu/hotplug: detect SMT disabled by BIOS (bnc#1012628).
- x86/KVM/VMX: Don't set l1tf_flush_l1d to true from
  vmx_l1d_flush() (bnc#1012628).
- x86/KVM/VMX: Replace 'vmx_l1d_flush_always' with
  'vmx_l1d_flush_cond' (bnc#1012628).
- x86/KVM/VMX: Move the l1tf_flush_l1d test to vmx_l1d_flush()
  (bnc#1012628).
- x86/irq: Demote irq_cpustat_t::__softirq_pending to u16
  (bnc#1012628).
- x86/KVM/VMX: Introduce per-host-cpu analogue of l1tf_flush_l1d
  (bnc#1012628).
- x86: Don't include linux/irq.h from asm/hardirq.h (bnc#1012628).
- x86/irq: Let interrupt handlers set kvm_cpu_l1tf_flush_l1d
  (bnc#1012628).
- x86/KVM/VMX: Don't set l1tf_flush_l1d from
  vmx_handle_external_intr() (bnc#1012628).
- Documentation/l1tf: Remove Yonah processors from not vulnerable
  list (bnc#1012628).
- x86/speculation: Simplify sysfs report of VMX L1TF vulnerability
  (bnc#1012628).
- x86/speculation: Use ARCH_CAPABILITIES to skip L1D flush on
  vmentry (bnc#1012628).
- KVM: VMX: Tell the nested hypervisor to skip L1D flush on
  vmentry (bnc#1012628).
- cpu/hotplug: Fix SMT supported evaluation (bnc#1012628).
- x86/speculation/l1tf: Invert all not present mappings
  (bnc#1012628).
- x86/speculation/l1tf: Make pmd/pud_mknotpresent() invert
  (bnc#1012628).
- x86/mm/pat: Make set_memory_np() L1TF safe (bnc#1012628).
- x86/mm/kmmio: Make the tracer robust against L1TF (bnc#1012628).
- tools headers: Synchronise x86 cpufeatures.h for L1TF additions
  (bnc#1012628).
- x86/microcode: Allow late microcode loading with SMT disabled
  (bnc#1012628).
- Refresh
  patches.suse/0001-x86-speculation-Add-basic-IBRS-support-infrastructur.patch.
- Update config files.
- commit a23e15c
* Tue Aug 14 2018 mkubecek@suse.cz
- Update upstream reference:
  patches.suse/hv-netvsc-Fix-NULL-dereference-at-single-queue-mode-.patch.
- commit 0425184
* Tue Aug 14 2018 tiwai@suse.de
- hv/netvsc: Fix NULL dereference at single queue mode fallback
  (bsc#1104708).
- commit a0cb9f6
* Mon Aug 13 2018 jslaby@suse.cz
- Refresh
  patches.suse/platform-x86-ideapad-laptop-Apply-no_hw_rfkill-to-Y2.
  Update upstream info.
- commit 799dc2a
* Mon Aug 13 2018 mkubecek@suse.cz
- Update to 4.18-final.
- Refresh configs
- commit 06ab9b3
* Tue Aug  7 2018 mkubecek@suse.cz
- config: refresh s390x/vanilla
  Add new option CONFIG_SYSTEM_DATA_VERIFICATION=n
- commit 3ee2023
* Mon Aug  6 2018 mkubecek@suse.cz
- Update to 4.18-rc8
- commit 9928e10
* Mon Jul 30 2018 mkubecek@suse.cz
- Update to 4.18-rc7
- commit 68c9705
* Tue Jul 24 2018 dmueller@suse.com
- Reenable v8.1/v8.2 aarch64 extensions
  These were enabled already in SLE15 and we want to default to the
  upstream defaults, which enable these features.
  Config changes:
  - aarch64:
    HW_AFDBM=y
    PAN=y
    LSE_ATOMICS=y
    VHE=y
    UAO=y
    SVE=y
- commit 7fdc027
* Mon Jul 23 2018 msuchanek@suse.de
- Update config files.
- commit 8efadc7
* Mon Jul 23 2018 tiwai@suse.de
- rpm/kernel-source.spec.in: Add more stuff to Recommends
  ... and move bc to Recommends as well.  All these packages are needed for
  building a kernel manually from scratch with kernel-source files.
- commit 6fcec9a
* Mon Jul 23 2018 mkubecek@suse.cz
- Update to 4.18-rc6
- Config changes:
  - NF_TABLES_SET=m (replaces NFT_SET_{RBTREE,HASH,BITMAP})
- commit 31ad2a8
* Sun Jul 22 2018 tiwai@suse.de
- rpm/kernel-source.spec.in: require bc for kernel-source
  This is needed for building include/generated/timeconst.h from
  kernel/time/timeconst.bc.
- commit d725e3b
* Tue Jul 17 2018 tiwai@suse.de
- Update config files: enable CONFIG_I2C_PXA for arm64 (bsc#1101465)
- commit d02f285
* Mon Jul 16 2018 rgoldwyn@suse.com
- apparmor: patch to provide compatibility with v2.x net rules (bsc#1100944).
- Delete patches.suse/0001-AppArmor-basic-networking-rules.patch.
- Delete
  patches.suse/0002-apparmor-update-apparmor-basic-networking-rules-for-.patch.
- Delete
  patches.suse/0003-apparmor-Fix-quieting-of-audit-messages-for-network-.patch.
- Delete patches.suse/apparmor-check-all-net-profiles.patch.
- commit 1947b35
* Mon Jul 16 2018 msuchanek@suse.de
- Pass x86 as architecture on x86_64 and i386 (bsc#1093118).
- commit 5f24fb0
* Mon Jul 16 2018 msuchanek@suse.de
- Revert "kconfig: only write '# CONFIG_FOO is not set' for
  visible symbols" (bsc#1093118).
- commit 2b9e26a
* Mon Jul 16 2018 mkubecek@suse.cz
- Update to 4.18-rc5
- commit b3f752f
* Mon Jul  9 2018 tiwai@suse.de
- alarmtimer: Prevent overflow for relative nanosleep
  (CVE-2018-13053 bsc#1099924).
- commit e98ba10
* Mon Jul  9 2018 mkubecek@suse.cz
- Update to 4.18-rc4
- Eliminated 1 patch
- Config changes:
  - s390x:
  - RSEQ=y
  - DEBUG_REQ=n
- commit 36e98dd
* Wed Jul  4 2018 dsterba@suse.com
- Update patches.suse/btrfs-8447-serialize-subvolume-mounts-with-potentially-mi.patch (bsc#951844 bsc#1024015 bsc#1099745).
  Refresh and update for Tumbleweed. No better patch version yet.
- commit dd5896f
* Mon Jul  2 2018 mkubecek@suse.cz
- Update to 4.18-rc3
- Eliminated 6 patches
- Config changes:
  - Input:
  - INPUT_SC27XX_VIBRA=m (aarch64 only)
- commit d44a642
* Fri Jun 29 2018 jslaby@suse.cz
- Refresh
  patches.suse/input-psmouse-fix-button-reporting-for-basic-protoco.patch.
  Update upstream status.
- commit 1e6a85a
* Wed Jun 27 2018 mkubecek@suse.cz
- bpf: enforce correct alignment for instructions (bsc#1099078).
- commit 55e3263
* Tue Jun 26 2018 tiwai@suse.de
- platform/x86: ideapad-laptop: Apply no_hw_rfkill to Y20-15IKBM,
  too (bsc#1098626).
- commit 0d1073f
* Mon Jun 25 2018 jslaby@suse.cz
- Input: psmouse - fix button reporting for basic protocols
  (bnc#1098392).
- commit faf690b
* Mon Jun 25 2018 msuchanek@suse.de
- rpm/kernel-source.changes.old: Add pre-SLE15 history (bsc#1098995).
- commit 631659e
* Mon Jun 25 2018 msuchanek@suse.de
- Refresh patches.suse/s390-fix-random-crashes-illegal-operation-0001-ilc-1.patch.
- commit ff0a7a4
* Sun Jun 24 2018 mkubecek@suse.cz
- Update to 4.18-rc2
- Eliminated 1 patch
- Config changes:
  - aarch64: reenable DWMAC_SOCFPGA (=m)
- commit cc9e91e
* Sun Jun 24 2018 afaerber@suse.de
- config: arm64: Update to 4.18-rc1
- commit b301d60
* Sat Jun 23 2018 mkubecek@suse.cz
- proc: fix missing final NUL in get_mm_cmdline() rewrite
  (https://www.mail-archive.com/linux-kernel@vger.kernel.org/msg1715032.html).
- commit f348790
* Sat Jun 23 2018 mkubecek@suse.cz
- Documentation: e1000: Fix docs build error.
- Documentation: e100: Fix docs build error.
- Documentation: e1000: Use correct heading adornment.
- Documentation: e100: Use correct heading adornment.
- commit 95284f7
* Sat Jun 23 2018 jslaby@suse.cz
- x86/stacktrace: Do not unwind after user regs (bnc#1058115).
- x86/stacktrace: Remove STACKTRACE_DUMP_ONCE (bnc#1058115).
- x86/stacktrace: Clarify the reliable success paths
  (bnc#1058115).
- x86/stacktrace: Do not fail for ORC with regs on stack
  (bnc#1058115).
- x86/unwind/orc: Detect the end of the stack (bnc#1058115).
- x86/stacktrace: Enable HAVE_RELIABLE_STACKTRACE for the ORC
  unwinder (bnc#1058115).
- Delete
  patches.suse/0001-x86-stacktrace-do-now-unwind-after-user-regs.patch.
- Delete
  patches.suse/0002-x86-stacktrace-make-clear-the-success-paths.patch.
- Delete
  patches.suse/0003-x86-stacktrace-remove-STACKTRACE_DUMP_ONCE-from-__sa.patch.
- Delete
  patches.suse/0004-x86-stacktrace-do-not-fail-for-ORC-with-regs-on-stac.patch.
- Delete
  patches.suse/0005-x86-stacktrace-orc-mark-it-as-reliable.patch.
  Replace the ORC patches by the upstream patches. Finally...
- commit c19d75b
* Thu Jun 21 2018 msuchanek@suse.de
- s390: Correct register corruption in critical section cleanup
  (boo#1095717).
- commit 62d3537
* Mon Jun 18 2018 msuchanek@suse.de
- macros.kernel-source: define linux_arch for KMPs (boo#1098050).
  CONFIG_64BIT is no longer defined so KMP spec files need to include
  %%{?linux_make_arch} in any make call to build modules or descent into
  the kernel directory for any reason.
- commit 5dc40af
* Mon Jun 18 2018 mkubecek@suse.cz
- config: update ppc64le configs
- commit fa9e020
* Mon Jun 18 2018 mkubecek@suse.cz
- config: enable NETDEVSIM (as module)
- commit e218eff
* Mon Jun 18 2018 mkubecek@suse.cz
- Update to 4.18-rc1.
- Eliminated 66 patches (62 stable, 4 other).
- ARM configs need updating.
- Config changes:
  - General:
  - RSEQ=y
  - i386:
  - BPF_JIT=y
  - BPF_JIT_ALWAYS_ON=y
  - powerpc:
  - LD_DEAD_CODE_DATA_ELIMINATION=n (experimental)
  - s390:
  - FW_LOADER_USER_HELPER=y
  - PCI:
  - PCI_HOST_GENERIC=y
  - Network:
  - TLS_DEVICE=y
  - XDP_SOCKETS=y
  - NFT_CONNLIMIT=m
  - NFT_SOCKET=m
  - IP_VS_MH=m
  - IP_VS_MH_TAB_INDEX=12 (default)
  - NF_TPROXY_IPV4=m
  - NF_TPROXY_IPV6=m
  - BPFILTER=y
  - BPFILTER_UMH=m
  - FAILOVER=m
  - MLX5_EN_TLS=y
  - NET_VENDOR_MICROSEMI=y
  - MSCC_OCELOT_SWITCH=m
  - MSCC_OCELOT_SWITCH_OCELOT=m
  - NFP_APP_ABM_NIC=y
  - MDIO_MSCC_MIIM=m
  - ASIX_PHY=m
  - DP83TC811_PHY=m
  - MICROCHIP_T1_PHY=m
  - NET_FAILOVER=m
  - Block:
  - DM_WRITECACHE=m
  - Input:
  - MOUSE_PS2_ELANTECH_SMBUS=y
  - TOUCHSCREEN_CHIPONE_ICN8505=m
  - HID_STEAM=m
  - Misc:
  - SPI_MEM=y
  - GPIOLIB_FASTPATH_LIMIT=512 (default)
  - VIDEO_CADENCE=y
  - LCD_OTM3225A=n
  - CHROMEOS_TBMC=m
  - FPGA_MGR_MACHXO2_SPI=m
  - Graphics:
  - DRM_I2C_NXP_TDA9950=m
  - DRM_I915_DEBUG_GUC=n
  - DRM_CDNS_DSI=n
  - DRM_THINE_THC63LVD1024=n
  - DRM_XEN=y
  - DRM_XEN_FRONTEND=m
  - Sound:
  - SND_SOC_SSM2305=n
  - SND_SOC_TSCS454=n
  - SND_SOC_WM8782=n
  - SND_SOC_MT6351=n
  - SND_XEN_FRONTEND=m
  - LED:
  - LEDS_CR0014114=m
  - LEDS_LM3601X=m
  - USB:
  - TYPEC_RT1711H=m
  - IIO:
  - AD5686_SPI=n
  - AD5696_I2C=n
  - TI_DAC5571=n
  - TSL2772=n
  - IIO_RESCALE=n
  - Filesystems:
  - PROC_VMCORE_DEVICE_DUMP=y
  - EVM_ADD_XATTRS=y
  - Testing:
  - TEST_OVERFLOW=n
  - Crypto:
  - CRYPTO_AEGIS128=m
  - CRYPTO_AEGIS128L=m
  - CRYPTO_AEGIS256=m
  - CRYPTO_AEGIS128_AESNI_SSE2=m
  - CRYPTO_AEGIS128L_AESNI_SSE2=m
  - CRYPTO_AEGIS256_AESNI_SSE2=m
  - CRYPTO_MORUS640=m
  - CRYPTO_MORUS640_SSE2=m
  - CRYPTO_MORUS1280=m
  - CRYPTO_MORUS1280_SSE2=m
  - CRYPTO_MORUS1280_AVX2=m
  - CRYPTO_ZSTD=m
- commit 549a5bb
* Mon Jun 18 2018 mkubecek@suse.cz
- rpm: ignore CONFIG_GCC_VERSION when checking for oldconfig changes
  Since 4.18-rc1, "make oldconfig" writes gcc version and capabilities into
  generated .config. Thus whenever we build the package or run checks with
  different gcc version than used to update config/*/*, check for "outdated
  configs" fails.
  As a quick band-aid, omit the lines with CONFIG_GCC_VERSION from both
  configs before comparing them. This way, the check won't fail unless run
  with newer gcc which would add new capabilities. More robust solution will
  require a wider discussion.
- commit 546ef32
* Sat Jun 16 2018 jslaby@suse.cz
- Revert "mm: relax deferred struct page requirements"
  (bnc#1092466).
- Update config files.
- commit 802b05f
* Sat Jun 16 2018 jslaby@suse.cz
- Linux 4.17.2 (bnc#1012628).
- crypto: omap-sham - fix memleak (bnc#1012628).
- crypto: vmx - Remove overly verbose printk from AES XTS init
  (bnc#1012628).
- crypto: vmx - Remove overly verbose printk from AES init
  routines (bnc#1012628).
- crypto: cavium - Limit result reading attempts (bnc#1012628).
- crypto: cavium - Fix fallout from CONFIG_VMAP_STACK
  (bnc#1012628).
- crypto: caam - fix size of RSA prime factor q (bnc#1012628).
- crypto: caam/qi - fix IV DMA mapping and updating (bnc#1012628).
- crypto: caam - fix IV DMA mapping and updating (bnc#1012628).
- crypto: caam - fix DMA mapping dir for generated IV
  (bnc#1012628).
- crypto: caam - strip input zeros from RSA input buffer
  (bnc#1012628).
- Input: elan_i2c - add ELAN0612 (Lenovo v330 14IKB) ACPI ID
  (bnc#1012628).
- Input: goodix - add new ACPI id for GPD Win 2 touch screen
  (bnc#1012628).
- crypto: ccree - correct host regs offset (bnc#1012628).
- tty: pl011: Avoid spuriously stuck-off interrupts (bnc#1012628).
- arm64: defconfig: Enable CONFIG_PINCTRL_MT7622 by default
  (bnc#1012628).
- doc: fix sysfs ABI documentation (bnc#1012628).
- vmw_balloon: fixing double free when batching mode is off
  (bnc#1012628).
- serial: 8250: omap: Fix idling of clocks for unused uarts
  (bnc#1012628).
- serial: samsung: fix maxburst parameter for DMA transactions
  (bnc#1012628).
- tty/serial: atmel: use port->name as name in request_irq()
  (bnc#1012628).
- serial: sh-sci: Stop using printk format %%pCr (bnc#1012628).
- usb: gadget: udc: renesas_usb3: disable the controller's irqs
  for reconnecting (bnc#1012628).
- usb: gadget: udc: renesas_usb3: should fail if devm_phy_get()
  returns error (bnc#1012628).
- usb: gadget: udc: renesas_usb3: should call devm_phy_get()
  before add udc (bnc#1012628).
- usb: gadget: udc: renesas_usb3: should call pm_runtime_enable()
  before add udc (bnc#1012628).
- usb: gadget: udc: renesas_usb3: should remove debugfs
  (bnc#1012628).
- usb: gadget: udc: renesas_usb3: fix double phy_put()
  (bnc#1012628).
- usb: gadget: function: printer: avoid wrong list handling in
  printer_write() (bnc#1012628).
- usb: typec: wcove: Remove dependency on HW FSM (bnc#1012628).
- usb: core: message: remove extra endianness conversion in
  usb_set_isoch_delay (bnc#1012628).
- phy: qcom-qusb2: Fix crash if nvmem cell not specified
  (bnc#1012628).
- Input: xpad - add GPD Win 2 Controller USB IDs (bnc#1012628).
- usb-storage: Add compatibility quirk flags for G-Technologies
  G-Drive (bnc#1012628).
- usb-storage: Add support for FL_ALWAYS_SYNC flag in the UAS
  driver (bnc#1012628).
- usbip: vhci_sysfs: fix potential Spectre v1 (bnc#1012628).
- NFC: pn533: don't send USB data off of the stack (bnc#1012628).
- staging: android: ion: Switch to pr_warn_once in
  ion_buffer_destroy (bnc#1012628).
- kvm: x86: use correct privilege level for
  sgdt/sidt/fxsave/fxrstor access (bnc#1012628).
- KVM: x86: pass kvm_vcpu to kvm_read_guest_virt and
  kvm_write_guest_virt_system (bnc#1012628).
- kvm: nVMX: Enforce cpl=0 for VMX instructions (bnc#1012628).
- kvm: fix typo in flag name (bnc#1012628).
- KVM: x86: introduce linear_{read,write}_system (bnc#1012628).
- KVM: X86: Fix reserved bits check for MOV to CR3 (bnc#1012628).
- blkdev_report_zones_ioctl(): Use vmalloc() to allocate large
  buffers (bnc#1012628).
- crypto: chelsio - request to HW should wrap (bnc#1012628).
- commit 202985c
* Thu Jun 14 2018 mkubecek@suse.cz
- socket: close race condition between sock_close() and
  sockfs_setattr() (CVE-2018-12232 bsc#1097593).
- commit 94bf968
* Thu Jun 14 2018 jslaby@suse.cz
- config.conf: disable syzkaller
  I doubt anybody else (other than me) uses the flavor, so save a lot of
  build resources by this. Leaving syzkaller configs and stuff in place
  so people still can build it if they want.
  The build is currently broken, so this "fixes" it too:
  ERROR: "__sanitizer_cov_trace_cmpd" [drivers/gpu/drm/amd/amdgpu/amdgpu.ko] undefined!
  ERROR: "__sanitizer_cov_trace_cmpf" [drivers/gpu/drm/amd/amdgpu/amdgpu.ko] undefined!
- commit bdee95f
* Tue Jun 12 2018 jslaby@suse.cz
- Linux 4.17.1 (bnc#1012628).
- netfilter: nf_flow_table: attach dst to skbs (bnc#1012628).
- bnx2x: use the right constant (bnc#1012628).
- ip6mr: only set ip6mr_table from setsockopt when ip6mr_new_table
  succeeds (bnc#1012628).
- ipv6: omit traffic class when calculating flow hash (bnc#1012628
  bsc#1095042).
- l2tp: fix refcount leakage on PPPoL2TP sockets (bnc#1012628).
- netdev-FAQ: clarify DaveM's position for stable backports
  (bnc#1012628).
- net: metrics: add proper netlink validation (bnc#1012628).
- net/packet: refine check for priv area size (bnc#1012628).
- rtnetlink: validate attributes in do_setlink() (bnc#1012628).
- sctp: not allow transport timeout value less than HZ/5 for
  hb_timer (bnc#1012628).
- team: use netdev_features_t instead of u32 (bnc#1012628).
- vrf: check the original netdevice for generating redirect
  (bnc#1012628).
- net: dsa: b53: Fix for brcm tag issue in Cygnus SoC
  (bnc#1012628).
- ipmr: fix error path when ipmr_new_table fails (bnc#1012628).
- PCI: hv: Do not wait forever on a device that has disappeared
  (bnc#1012628).
- Delete
  patches.suse/ipv6-omit-traffic-class-when-calculating-flow-hash.patch.
- commit 17c8abe
* Fri Jun  8 2018 tiwai@suse.de
- mtd: spi-nor: intel-spi: Fix atomic sequence handling
  (bsc#1073836).
- commit c31c53d
* Fri Jun  8 2018 mkubecek@suse.cz
- ipv6: omit traffic class when calculating flow hash
  (bsc#1095042).
- commit 1307c29
* Fri Jun  8 2018 tiwai@suse.de
- Delete patches.suse/iwlwifi-expose-default-fallback-ucode-api.
  The workaround is no longer needed as the upstream driver code catches
  up the actual firmware version
- commit d6e069d
* Fri Jun  8 2018 tiwai@suse.de
- Update patch tag of the upstreamed btusb fix
- commit f531f64
* Mon Jun  4 2018 mkubecek@suse.cz
- config: enable preemption in i386/debug
- commit b181e22
* Mon Jun  4 2018 mkubecek@suse.cz
- Update to 4.17-final
- commit fb45ad0
* Mon May 28 2018 mkubecek@suse.cz
- Update to 4.17-rc7
- Eliminated 1 patch
- Config changes:
  - reenable SSB_DRIVER_PCICORE and dependencies after revert of
    commit 882164a4a928
- commit c78299c
* Thu May 24 2018 tiwai@suse.de
- Bluetooth: Apply QCA Rome patches for some ATH3012 models
  (bsc#1082504).
- commit e2f793c
* Wed May 23 2018 msuchanek@suse.de
- mkspec: only build docs for default variant kernel.
- commit 045f5ac
* Mon May 21 2018 mkubecek@suse.cz
- Makefile: disable PIE before testing asm goto (bsc#1092456).
- commit 67bdb0d
* Mon May 21 2018 mkubecek@suse.cz
- Update to 4.17-rc6
- commit 6912f6b
* Thu May 17 2018 msuchanek@suse.de
- kernel-{binary,docs}.spec sort dependencies.
- commit d2ab971
* Thu May 17 2018 mgalbraith@suse.de
- Fix config/x86_64/debug, turn PREEMPT_NONE off, and PREEMPT_DEBUG on.
- commit 3ec7274
* Wed May 16 2018 msuchanek@suse.de
- macros.kernel-source: Fix building non-x86 KMPs
- commit 8631d05
* Tue May 15 2018 jeffm@suse.com
- reiserfs: package in separate KMP (FATE#323394).
- commit d14f152
* Mon May 14 2018 msuchanek@suse.de
- macros.kernel-source: ignore errors when using make to print kernel release
  There is no way to handle the errors anyway and including the error into
  package version does not give good results.
- commit 282e9a6
* Mon May 14 2018 mkubecek@suse.cz
- Update to 4.17-rc5
- commit 80e3a99
* Fri May 11 2018 msuchanek@suse.de
- Revert "kernel-binary: do not package extract-cert when not signing modules"
  This reverts commit 10a8bc496a553b8069d490a8ae7508bdb19f58d9.
- commit 1f7acca
* Mon May  7 2018 mkubecek@suse.cz
- Update to 4.17-rc4
- Eliminated 2 patches
- Update to 4.17-rc3
- Eliminated 2 patches
- commit a993a00
* Wed May  2 2018 msuchanek@suse.de
- kernel-binary: also default klp_symbols to 0 here.
- commit e35f14a
* Wed May  2 2018 msuchanek@suse.de
- klp_symbols: make --klp-symbols argument semantic sane
  It selects build of klp symbols and defaults to off
- commit 0e53042
* Wed May  2 2018 jslaby@suse.cz
- tools: power/acpi, revert to LD = gcc (build fix).
- Delete
  patches.suse/revert-tools-fix-cross-compile-var-clobbering.patch.
  Replace by the upstream commit.
- commit c7b3cf9
* Mon Apr 30 2018 mkubecek@suse.cz
- Update to 4.17-rc3
- Eliminated 1 patch
- Config changes:
  - x86_64 and i386
  - SND_SST_ATOM_HIFI2_PLATFORM_ACPI=m
  - armv7hl
  - CONFIG_NFT_REDIR_IPV4=m (sync with other configs)
  - CONFIG_NFT_REDIR_IPV6=m (sync with other configs)
- commit 088acbb
* Sun Apr 29 2018 afaerber@suse.de
- config: armv7hl: Update to 4.17-rc2
- commit e76ffdc
* Sun Apr 29 2018 afaerber@suse.de
- config: armv6hl: Update to 4.17-rc2
- commit 7ac1254
* Sun Apr 29 2018 afaerber@suse.de
- config: arm64: Update to 4.17-rc2
- commit 8535e20
* Fri Apr 27 2018 msuchanek@suse.de
- kernel-binary: only install modules.fips on modular kernels.
- commit 2cb2bec
* Tue Apr 24 2018 msuchanek@suse.de
- split-modules: use MAKE_ARGS
- commit d8fe174
* Tue Apr 24 2018 mcgrof@suse.com
- xfs: set format back to extents if xfs_bmap_extents_to_btree
  (bsc#1090717, CVE-2018-10323).
- commit 41ecb40
* Tue Apr 24 2018 msuchanek@suse.de
- kernel-binary: pass MAKE_ARGS to install script as well.
- commit ce62ae7
* Tue Apr 24 2018 mkubecek@suse.cz
- Update config files.
- commit becf16d
* Tue Apr 24 2018 msuchanek@suse.de
- kernel-binary: pass ARCH= to kernel build
  Recent kernel does not save CONFIG_64BIT so it has to be specified by
  arch.
- commit fb21b73
* Tue Apr 24 2018 mkubecek@suse.cz
- config: fix i386 configs
  Since mainline commit f467c5640c29 ("kconfig: only write '# CONFIG_FOO is
  not set' for visible symbols"), make silentoldconfig (or make syncconfig as
  it is called now) doesn't add CONFIG_64BIT line into i386 configs if called
  with ARCH=i386.
  During the build, it's called without ARCH=i386 so that it requests this
  option to be entered manually and the build fails. Long term solution would
  probably be passing ARCH=%%{cpu_arch} to all make commands; for now, just
  add CONFIG_64BIT line to i386/pae to fix the build as is.
- commit d9a33ad
* Tue Apr 24 2018 mkubecek@suse.cz
- Documentation: typec.rst: Use literal-block element with
  ascii art.
- commit 1aebada
* Mon Apr 23 2018 jeffm@suse.com
- README.BRANCH: Added Michal Kubecek as co-maintainer.
- commit 53ecad7
* Mon Apr 23 2018 mkubecek@suse.cz
- Update to 4.17-rc2
- Eliminated 2 patches
- Config changes:
  - s390x:
  - KEXEC_FILE=y
- commit 8aad964
* Fri Apr 20 2018 mkubecek@suse.cz
- Update to 4.17-rc1.
- Eliminated 55 patches (51 stable 4.16.x)
- ARM configs need updating.
- Config changes:
  - x86:
  - ACPI_TAD=m
  - s390:
  - EXPOLINE_FULL=y
  - VT=y
  - CONSOLE_TRANSLATIONS=y
  - VT_CONSOLE=y
  - VT_HW_CONSOLE_BINDING=n
  - DUMMY_CONSOLE_COLUMNS=80
  - DUMMY_CONSOLE_ROWS=25
  - SPEAKUP=n
  - Network:
  - NF_TABLES_INET=y
  - NF_TABLES_NETDEV=y
  - NF_TABLES_ARP=y
  - NF_TABLES_BRIDGE=y
  - NET_EMATCH_IPT=m
  - ICE=m
  - RSI_COEX=y
  - IEEE802154_MCR20A=m
  - INFINIBAND_EXP_LEGACY_VERBS_NEW_UAPI=n
  - Filesystems:
  - OVERLAY_FS_XINO_AUTO=n
  - PSTORE_DEFLATE_COMPRESS=m
  - PSTORE_LZ4HC_COMPRESS=m
  - PSTORE_842_COMPRESS=n
  - PSTORE_DEFLATE_COMPRESS_DEFAULT=deflate
  - Crypto:
  - CRYPTO_CFB=m
  - CRYPTO_SM4=m
  - CRYPTO_SPECK=m
  - CRYPTO_DEV_CHELSIO_TLS=m
  - Input:
  - JOYSTICK_PXRC=m
  - HID_ELAN=m
  - HID_GOOGLE_HAMMER=m
  - Sound:
  - SND_SOC_INTEL_CHT_BSW_NAU8824_MACH=m
  - SND_SOC_INTEL_KBL_DA7219_MAX98357A_MACH=m
  - SND_SOC_AK4458=n
  - SND_SOC_AK5558=n
  - SND_SOC_BD28623=n
  - SND_SOC_MAX9867=n
  - SND_SOC_PCM1789_I2C=n
  - SND_SOC_TDA7419=m
  - SND_SOC_MAX9759=n
  - USB:
  - TYPEC_MUX_PI3USB30532=m
  - USB_ROLES_INTEL_XHCI=m
  - GPIO:
  - GPIO_104_DIO_48E=m
  - GPIO_104_IDIO_16=m
  - GPIO_104_IDI_48=m
  - GPIO_GPIO_MM=m
  - GPIO_WINBOND=m
  - GPIO_WS16C48=m
  - Media:
  - CEC_PIN_ERROR_INJ=n
  - CXD2880_SPI_DRV=m
  - MTK_MMC=n
  - IIO:
  - 104_QUAD_8=m
  - CIO_DAC=n
  - AD5272=m
  - MCP4018=m
  - MLX90632=m
  - Other:
  - THERMAL_STATISTICS=y
  - EBC_C384_WDT=m
  - LEDS_MLXREG=m
  - COMMON_CLK_SI544=n
  - STX104=n
  - LV0104CS=n
  - Remote controlers:
  - IR_IMON_DECODER=m
  - IR_IMON_RAW=m
  - INTEL_TH_ACPI=m
  - Debugging:
  - DEBUG_RWSEMS=n
- commit 4e61ecf
* Fri Apr 20 2018 mkubecek@suse.cz
- config: enable TCP_MD5SIG (bsc#1090162)
- commit 1cfc938
* Fri Apr 20 2018 mkubecek@suse.cz
- x86/power/64: Fix page-table setup for temporary text mapping
  (https://patchwork.kernel.org/patch/10342491/).
- x86/ldt: Fix support_pte_mask filtering in map_ldt_struct()
  (https://patchwork.kernel.org/patch/10342491/).
- commit 3c56473
* Fri Apr 20 2018 msuchanek@suse.de
- HID: redragon: Fix modifier keys for Redragon Asura Keyboard
  (https://build.opensuse.org/request/show/597583).
  Update config files.
- commit e9bd8ea
* Thu Apr 19 2018 jslaby@suse.cz
- Linux 4.16.3 (bnc#1012628).
- cdc_ether: flag the Cinterion AHS8 modem by gemalto as WWAN
  (bnc#1012628).
- rds: MP-RDS may use an invalid c_path (bnc#1012628).
- slip: Check if rstate is initialized before uncompressing
  (bnc#1012628).
- vhost: fix vhost_vq_access_ok() log check (bnc#1012628).
- l2tp: fix races in tunnel creation (bnc#1012628).
- l2tp: fix race in duplicate tunnel detection (bnc#1012628).
- ip_gre: clear feature flags when incompatible o_flags are set
  (bnc#1012628).
- vhost: Fix vhost_copy_to_user() (bnc#1012628).
- lan78xx: Correctly indicate invalid OTP (bnc#1012628).
- sparc64: Properly range check DAX completion index
  (bnc#1012628).
- media: v4l2-compat-ioctl32: don't oops on overlay (bnc#1012628).
- media: v4l: vsp1: Fix header display list status check in
  continuous mode (bnc#1012628).
- ipmi: Fix some error cleanup issues (bnc#1012628).
- parisc: Fix out of array access in match_pci_device()
  (bnc#1012628).
- parisc: Fix HPMC handler by increasing size to multiple of 16
  bytes (bnc#1012628).
- iwlwifi: add a bunch of new 9000 PCI IDs (bnc#1012628).
- Drivers: hv: vmbus: do not mark HV_PCIE as perf_device
  (bnc#1012628).
- PCI: hv: Serialize the present and eject work items
  (bnc#1012628).
- PCI: hv: Fix 2 hang issues in hv_compose_msi_msg()
  (bnc#1012628).
- KVM: PPC: Book3S HV: trace_tlbie must not be called in realmode
  (bnc#1012628).
- perf intel-pt: Fix overlap detection to identify consecutive
  buffers correctly (bnc#1012628).
- perf intel-pt: Fix sync_switch (bnc#1012628).
- perf intel-pt: Fix error recovery from missing TIP packet
  (bnc#1012628).
- perf intel-pt: Fix timestamp following overflow (bnc#1012628).
- perf/core: Fix use-after-free in uprobe_perf_close()
  (bnc#1012628).
- radeon: hide pointless #warning when compile testing
  (bnc#1012628).
- x86/mce/AMD: Pass the bank number to smca_get_bank_type()
  (bnc#1012628).
- x86/mce/AMD, EDAC/mce_amd: Enumerate Reserved SMCA bank type
  (bnc#1012628).
- x86/mce/AMD: Get address from already initialized block
  (bnc#1012628).
- ath9k: Protect queue draining by rcu_read_lock() (bnc#1012628).
- x86/uapi: Fix asm/bootparam.h userspace compilation errors
  (bnc#1012628).
- x86/apic: Fix signedness bug in APIC ID validity checks
  (bnc#1012628).
- sunrpc: remove incorrect HMAC request initialization
  (bnc#1012628).
- f2fs: fix heap mode to reset it back (bnc#1012628).
- block: Change a rcu_read_{lock,unlock}_sched() pair into
  rcu_read_{lock,unlock}() (bnc#1012628).
- nvme: Skip checking heads without namespaces (bnc#1012628).
- lib: fix stall in __bitmap_parselist() (bnc#1012628).
- zboot: fix stack protector in compressed boot phase
  (bnc#1012628).
- blk-mq: Directly schedule q->timeout_work when aborting a
  request (bnc#1012628).
- blk-mq: order getting budget and driver tag (bnc#1012628).
- blk-mq: make sure that correct hctx->next_cpu is set
  (bnc#1012628).
- blk-mq: don't keep offline CPUs mapped to hctx 0 (bnc#1012628).
- ovl: Set d->last properly during lookup (bnc#1012628).
- ovl: fix lookup with middle layer opaque dir and absolute path
  redirects (bnc#1012628).
- ovl: set i_ino to the value of st_ino for NFS export
  (bnc#1012628).
- ovl: set lower layer st_dev only if setting lower st_ino
  (bnc#1012628).
- xen: xenbus_dev_frontend: Fix XS_TRANSACTION_END handling
  (bnc#1012628).
- hugetlbfs: fix bug in pgoff overflow checking (bnc#1012628).
- nfsd: fix incorrect umasks (bnc#1012628).
- scsi: scsi_dh: Don't look for NULL devices handlers by name
  (bnc#1012628).
- scsi: qla2xxx: Fix small memory leak in qla2x00_probe_one on
  probe failure (bnc#1012628).
- Revert "scsi: core: return BLK_STS_OK for DID_OK in
  __scsi_error_from_host_byte()" (bnc#1012628).
- apparmor: fix logging of the existence test for signals
  (bnc#1012628).
- apparmor: fix display of .ns_name for containers (bnc#1012628).
- apparmor: fix resource audit messages when auditing peer
  (bnc#1012628).
- block/loop: fix deadlock after loop_set_status (bnc#1012628).
- nfit: fix region registration vs block-data-window ranges
  (bnc#1012628).
- s390/qdio: don't retry EQBS after CCQ 96 (bnc#1012628).
- s390/qdio: don't merge ERROR output buffers (bnc#1012628).
- s390/ipl: ensure loadparm valid flag is set (bnc#1012628).
- s390/compat: fix setup_frame32 (bnc#1012628).
- get_user_pages_fast(): return -EFAULT on access_ok failure
  (bnc#1012628).
- mm/gup_benchmark: handle gup failures (bnc#1012628).
- getname_kernel() needs to make sure that ->name != ->iname in
  long case (bnc#1012628).
- Bluetooth: Fix connection if directed advertising and privacy
  is used (bnc#1012628).
- Bluetooth: hci_bcm: Treat Interrupt ACPI resources as always
  being active-low (bnc#1012628).
- rtl8187: Fix NULL pointer dereference in priv->conf_mutex
  (bnc#1012628).
- Refresh patches.suse/0001-AppArmor-basic-networking-rules.patch.
- commit 771261a
* Thu Apr 19 2018 msuchanek@suse.de
- objtool, perf: Fix GCC 8 -Wrestrict error (bsc#1084620).
- commit 0c6114f
* Wed Apr 18 2018 msuchanek@suse.de
- supported.conf: update from openSUSE-15.0
- commit 4ef3f17
* Mon Apr 16 2018 mbrugger@suse.com
- arm64: Update config files. (bsc#1089764)
  Increase NR_CPUS to 384
- commit 6f06d9e
* Thu Apr 12 2018 jslaby@suse.cz
- Linux 4.16.2 (bnc#1012628).
- nfp: use full 40 bits of the NSP buffer address (bnc#1012628).
- net_sched: fix a missing idr_remove() in u32_delete_key()
  (bnc#1012628).
- vti6: better validate user provided tunnel names (bnc#1012628).
- ip6_tunnel: better validate user provided tunnel names
  (bnc#1012628).
- ip6_gre: better validate user provided tunnel names
  (bnc#1012628).
- ipv6: sit: better validate user provided tunnel names
  (bnc#1012628).
- ip_tunnel: better validate user provided tunnel names
  (bnc#1012628).
- net: fool proof dev_valid_name() (bnc#1012628).
- vlan: also check phy_driver ts_info for vlan's real device
  (bnc#1012628).
- sky2: Increase D3 delay to sky2 stops working after suspend
  (bnc#1012628).
- sctp: sctp_sockaddr_af must check minimal addr length for
  AF_INET6 (bnc#1012628).
- sctp: do not leak kernel memory to user space (bnc#1012628).
- pptp: remove a buggy dst release in pptp_connect()
  (bnc#1012628).
- net/sched: fix NULL dereference in the error path of
  tcf_bpf_init() (bnc#1012628).
- net/ipv6: Increment OUTxxx counters after netfilter hook
  (bnc#1012628).
- net: dsa: Discard frames from unused ports (bnc#1012628).
- arp: fix arp_filter on l3slave devices (bnc#1012628).
- sparc64: Oracle DAX driver depends on SPARC64 (bnc#1012628).
- commit 8ea896b
* Wed Apr 11 2018 jslaby@suse.cz
- Update config files.
  s390x/vanilla fails to build without this.
- commit e8d83e8
* Tue Apr 10 2018 msuchanek@suse.de
- rpm/package-descriptions: fix typo in kernel-azure
- Add azure kernel description.
- commit af0f13e
* Mon Apr  9 2018 tiwai@suse.de
- media: v4l2-core: fix size of devnode_nums[] bitarray
  (bsc#1088640).
- commit 6fcb3b5
* Mon Apr  9 2018 jslaby@suse.cz
- Linux 4.16.1 (bnc#1012628).
- signal: Correct the offset of si_pkey and si_lower in struct
  siginfo on m68k (bnc#1012628).
- Fix slab name "biovec-(1<<(21-12))" (bnc#1012628).
- vt: change SGR 21 to follow the standards (bnc#1012628).
- Input: i8042 - enable MUX on Sony VAIO VGN-CS series to fix
  touchpad (bnc#1012628).
- Input: i8042 - add Lenovo ThinkPad L460 to i8042 reset list
  (bnc#1012628).
- Input: ALPS - fix TrackStick detection on Thinkpad L570 and
  Latitude 7370 (bnc#1012628).
- Revert "base: arch_topology: fix section mismatch build
  warnings" (bnc#1012628).
- staging: comedi: ni_mio_common: ack ai fifo error interrupts
  (bnc#1012628).
- siox: fix possible buffer overflow in device_add_store
  (bnc#1012628).
- Btrfs: fix unexpected cow in run_delalloc_nocow (bnc#1012628).
- Bluetooth: hci_bcm: Add 6 new ACPI HIDs (bnc#1012628).
- crypto: x86/cast5-avx - fix ECB encryption when long sg follows
  short one (bnc#1012628).
- crypto: arm,arm64 - Fix random regeneration of S_shipped
  (bnc#1012628).
- crypto: ccp - return an actual key size from RSA max_size
  callback (bnc#1012628).
- crypto: caam - Fix null dereference at error path (bnc#1012628).
- crypto: ahash - Fix early termination in hash walk
  (bnc#1012628).
- crypto: talitos - fix IPsec cipher in length (bnc#1012628).
- crypto: testmgr - Fix incorrect values in PKCS#1 test vector
  (bnc#1012628).
- crypto: inside-secure - fix clock management (bnc#1012628).
- crypto: talitos - don't persistently map req_ctx->hw_context
  and req_ctx->buf (bnc#1012628).
- crypto: ccp - Fill the result buffer only on digest, finup,
  and final ops (bnc#1012628).
- crypto: lrw - Free rctx->ext with kzfree (bnc#1012628).
- parport_pc: Add support for WCH CH382L PCI-E single parallel
  port card (bnc#1012628).
- media: usbtv: prevent double free in error case (bnc#1012628).
- /dev/mem: Avoid overwriting "err" in read_mem() (bnc#1012628).
- mei: remove dev_err message on an unsupported ioctl
  (bnc#1012628).
- serial: 8250: Add Nuvoton NPCM UART (bnc#1012628).
- USB: serial: cp210x: add ELDAT Easywave RX09 id (bnc#1012628).
- USB: serial: ftdi_sio: add support for Harman
  FirmwareHubEmulator (bnc#1012628).
- USB: serial: ftdi_sio: add RT Systems VX-8 cable (bnc#1012628).
- bitmap: fix memset optimization on big-endian systems
  (bnc#1012628).
- commit 4bf9d1e
* Fri Apr  6 2018 agraf@suse.de
- armv6hl: Disable uacces with memcpy (boo#1080435)
- commit 5eeeb1b
* Thu Apr  5 2018 rgoldwyn@suse.com
- apparmor: Check all profiles attached to the label (bsc#1085996).
- commit b249c9e
* Wed Apr  4 2018 jslaby@suse.cz
- Revert "tools: fix cross-compile var clobbering" (build fix).
- commit 590ff92
* Mon Apr  2 2018 jeffm@suse.com
- Update to 4.16-final.
- commit 1b10c5b
* Mon Mar 26 2018 tiwai@suse.de
- brcmsmac: allocate ucode with GFP_KERNEL (bsc#1085174).
- commit 2971d91
* Mon Mar 26 2018 jeffm@suse.com
- Update to 4.16-rc7.
- Eliminated 1 patch.
- commit 7a36f2f
* Fri Mar 23 2018 agraf@suse.de
- armv7hl: Disable uacces with memcpy (boo#1080435)
- commit b8a701a
* Mon Mar 19 2018 msuchanek@suse.de
- kernel-*.spec: remove remaining occurences of %%release from dependencies
  There is a mix of %%release and %%source_rel in manually added
  dependencies and the %%release dependencies tend to fail due to rebuild
  sync issues. So get rid of them.
- commit b4ec514
* Mon Mar 19 2018 jeffm@suse.com
- Update to 4.16-rc6.
- commit a98eb00
* Mon Mar 19 2018 jeffm@suse.com
- Refresh patches.suse/kernel-add-release-status-to-kernel-build.patch.
- commit cf5ff13
* Thu Mar 15 2018 tiwai@suse.de
- Bluebooth: btusb: Fix quirk for Atheros 1525/QCA6174
  (bsc#1082504).
- commit 8413b00
* Wed Mar 14 2018 jeffm@suse.com
- config: sync i386/default
  Some options had been removed completely.
- commit 95f48d7
* Wed Mar 14 2018 jeffm@suse.com
- rpm/kernel-source.spec.in: Add check-module-license to Sources
  The package builds in the build service but the script won't make it
  into the SRPM if it's not in the Sources list.
- commit 031ed9e
* Tue Mar 13 2018 msuchanek@suse.de
- mkspec: fix perl warning
- commit f15670f
* Mon Mar 12 2018 jeffm@suse.com
- Update to 4.16-rc5.
- Eliminated 1 patch.
- commit 0dfffad
* Sun Mar 11 2018 afaerber@suse.de
- config: armv7hl: Update to 4.16-rc4
- commit ad451a4
* Sun Mar 11 2018 afaerber@suse.de
- config: armv6hl: Update to 4.16-rc4
- commit 6c846e1
* Sat Mar 10 2018 tiwai@suse.de
- Refresh to upstream patch (bsc#1083694)
  patches.suse/Documentation-sphinx-Fix-Directive-import-error.patch
- commit 2d62679
* Sat Mar 10 2018 jeffm@suse.com
- kernel: add release status to kernel build (bsc#FATE#325281).
- commit c51605f
* Sat Mar 10 2018 jeffm@suse.com
- rpm: use %%_sourcedir prefix for release-projects
- rpm: set SUSE_KERNEL_RELEASED based on project name
  Set SUSE_KERNEL_RELEASED in the config only if the project name matches
  a list of projects that are part of official release channels.  This
  list of projects is maintained per-branch.
- commit a391a5b
* Fri Mar  9 2018 jeffm@suse.com
- config: added new 'kvmsmall' flavor
  This flavor is an unreleased internal configuration intended for kernel
  developers to use in simple virtual machines.  It contains only the
  device drivers necessary to use a KVM virtual machine *without* device
  passthrough enabled.  Common local and network file systems are enabled.
  All device mapper targets are enabled.  Only the network and graphics
  drivers for devices that qemu emulates are enabled.  Many subsystems
  enabled in the default kernel are entirely disabled.  This kernel is
  meant to be small and to build very quickly.  There will be no kABI
  stability and its configuration may be changed arbitrarily.
- commit 088f1da
* Fri Mar  9 2018 jeffm@suse.com
- config: convert kvmsmall to fragment config
- commit 7a5941a
* Fri Mar  9 2018 jeffm@suse.com
- config: disabled some more options for kvmsmall
  Disable CAN, BT, rare partition types, unused mouse protocols, UIO,
  STM, and others.
- commit 4707d44
* Fri Mar  9 2018 jeffm@suse.com
- config: added new 'kvmsmall' flavor
  This flavor is intended for kernel developers to use in simple virtual
  machines.  It contains only the device drivers necessary to use a
  KVM virtual machine *without* device passthrough enabled.  Common
  local and network file systems are enabled.  All device mapper targets
  are enabled.  Only the network and graphics drivers for devices that qemu
  emulates are enabled.  Many subsystems enabled in the default kernel
  are entirely disabled.  This kernel is meant to be small and to build
  very quickly.
- commit 3c99d1f
* Thu Mar  8 2018 msuchanek@suse.de
- mkspec: do not build dtbs for architectures with no kernel.
- commit 8394abf
* Thu Mar  8 2018 jeffm@suse.com
- kconfig: move SUSE options from init/Kconfig to init/Kconfig.suse
- commit b7f69ff
* Wed Mar  7 2018 afaerber@suse.de
- config: arm64: Update to 4.16-rc4
- commit 0bb9ed4
* Wed Mar  7 2018 tiwai@suse.de
- rpm/kernel-binary.spec.in: Check module licenses (bsc#1083215,bsc#1083527)
- commit e41de0c
* Tue Mar  6 2018 jslaby@suse.cz
- Update config files.
  Enable module signing (bnc#1082905):
  * CONFIG_MODULE_SIG=y
  * # CONFIG_MODULE_SIG_FORCE is not set
  * # CONFIG_MODULE_SIG_ALL is not set
  * # CONFIG_MODULE_SIG_SHA1 is not set
  * # CONFIG_MODULE_SIG_SHA224 is not set
  * CONFIG_MODULE_SIG_SHA256=y
  * # CONFIG_MODULE_SIG_SHA384 is not set
  * # CONFIG_MODULE_SIG_SHA512 is not set
  * CONFIG_MODULE_SIG_HASH="sha256"
  * CONFIG_MODULE_SIG_KEY="certs/signing_key.pem"
  * CONFIG_SECONDARY_TRUSTED_KEYRING=y
  * CONFIG_SYSTEM_BLACKLIST_KEYRING=y
  * CONFIG_SYSTEM_BLACKLIST_HASH_LIST=""
  This commit synchronizes these options with SLE15.
  We do not add patches for loading keys from the shim layer (as in
  SLE15) for the time being. They were rejected multiple times in
  upstream and we do not want to forward-port them infinitely. This only
  means that loading KMPs with none/invalid signatures generates this:
  <module_name>: loading out-of-tree module taints kernel.
  <module_name>: module verification failed: signature and/or required key missing - tainting kernel
  But the modules load fine after that as we have MODULE_SIG_FORCE set
  to 'n'.
  Tested in qemu+OVMF and bare metal and everything looks fine.
- commit 2539ea5
* Mon Mar  5 2018 msuchanek@suse.de
- rpm: provide %%name%%-srchash = <kernel-source commit hash> (FATE#325312).
  - Also use for kernel-obs-build dependency.
- commit b6fccdf
* Mon Mar  5 2018 jeffm@suse.com
- Refresh
  patches.suse/0001-x86-speculation-Add-basic-IBRS-support-infrastructur.patch.
- Refresh
  patches.suse/0002-x86-speculation-Add-inlines-to-control-Indirect-Bran.patch.
- Refresh
  patches.suse/0005-x86-enter-Use-IBRS-on-syscall-and-interrupts.patch.
- commit 1ba5305
* Mon Mar  5 2018 jeffm@suse.com
- Update to 4.16-rc4.
- IBRS patches need review.
- commit 061459a
* Sun Mar  4 2018 msuchanek@suse.de
- arch-symbols: use bash as interpreter since the script uses bashism.
- commit 4cdfb23
* Fri Mar  2 2018 msuchanek@suse.de
- kernel-binary: do not BuildIgnore m4.
  It is actually needed for regenerating zconf when it is not up-to-date
  due to merge.
- commit 967b28b
* Fri Mar  2 2018 mkubecek@suse.cz
- rpm/kernel-binary.spec.in: add build requirement for flex
  In addition to bison, we also need flex for "make oldconfig".
- commit 83d831c
* Fri Mar  2 2018 mkubecek@suse.cz
- rpm/kernel-binary.spec.in: remove m4 from BuildIgnore list
  As bison depends on m4, we cannot set !BuildIgnore for it any more.
- commit d7695e1
* Fri Mar  2 2018 tiwai@suse.de
- Documentation/sphinx: Fix Directive import error (bsc#1083694).
- commit 7f94eb1
* Wed Feb 28 2018 msuchanek@suse.de
- bs-upload-kernel: do not set %%opensuse_bs
  Since SLE15 it is not set in the distribution project so do not set it
  for kernel projects either.
- commit d696aa0
* Wed Feb 28 2018 jslaby@suse.cz
- Linux 4.15.7 (bnc#1012628).
- microblaze: fix endian handling (bnc#1012628).
- drm/i915/breadcrumbs: Ignore unsubmitted signalers
  (bnc#1012628).
- arm64: __show_regs: Only resolve kernel symbols when running
  at EL1 (bnc#1012628).
- drm/amdgpu: add new device to use atpx quirk (bnc#1012628).
- drm/amdgpu: Avoid leaking PM domain on driver unbind (v2)
  (bnc#1012628).
- drm/amdgpu: add atpx quirk handling (v2) (bnc#1012628).
- drm/amdgpu: only check mmBIF_IOV_FUNC_IDENTIFIER on tonga/fiji
  (bnc#1012628).
- drm/amdgpu: Add dpm quirk for Jet PRO (v2) (bnc#1012628).
- drm/amdgpu: fix VA hole handling on Vega10 v3 (bnc#1012628).
- drm/amdgpu: disable MMHUB power gating on raven (bnc#1012628).
- drm: Handle unexpected holes in color-eviction (bnc#1012628).
- drm/atomic: Fix memleak on ERESTARTSYS during non-blocking
  commits (bnc#1012628).
- drm/cirrus: Load lut in crtc_commit (bnc#1012628).
- usb: renesas_usbhs: missed the "running" flag in usb_dmac with
  rx path (bnc#1012628).
- usb: gadget: f_fs: Use config_ep_by_speed() (bnc#1012628).
- usb: gadget: f_fs: Process all descriptors during bind
  (bnc#1012628).
- Revert "usb: musb: host: don't start next rx urb if current
  one failed" (bnc#1012628).
- usb: ldusb: add PIDs for new CASSY devices supported by this
  driver (bnc#1012628).
- usb: phy: mxs: Fix NULL pointer dereference on i.MX23/28
  (bnc#1012628).
- usb: dwc3: ep0: Reset TRB counter for ep0 IN (bnc#1012628).
- usb: dwc3: gadget: Set maxpacket size for ep0 IN (bnc#1012628).
- usb: host: ehci: use correct device pointer for dma ops
  (bnc#1012628).
- drm/edid: Add 6 bpc quirk for CPT panel in Asus UX303LA
  (bnc#1012628).
- Add delay-init quirk for Corsair K70 RGB keyboards
  (bnc#1012628).
- arm64: cpufeature: Fix CTR_EL0 field definitions (bnc#1012628).
- arm64: Disable unhandled signal log messages by default
  (bnc#1012628).
- arm64: Remove unimplemented syscall log message (bnc#1012628).
- usb: ohci: Proper handling of ed_rm_list to handle race
  condition between usb_kill_urb() and finish_unlinks()
  (bnc#1012628).
- ohci-hcd: Fix race condition caused by ohci_urb_enqueue()
  and io_watchdog_func() (bnc#1012628).
- net: thunderbolt: Run disconnect flow asynchronously when
  logout is received (bnc#1012628).
- net: thunderbolt: Tear down connection properly on suspend
  (bnc#1012628).
- PCI/cxgb4: Extend T3 PCI quirk to T4+ devices (bnc#1012628).
- irqchip/mips-gic: Avoid spuriously handling masked interrupts
  (bnc#1012628).
- irqchip/gic-v3: Use wmb() instead of smb_wmb() in
  gic_raise_softirq() (bnc#1012628).
- uapi/if_ether.h: move __UAPI_DEF_ETHHDR libc define
  (bnc#1012628).
- mm: don't defer struct page initialization for Xen pv guests
  (bnc#1012628).
- mm, swap, frontswap: fix THP swap if frontswap enabled
  (bnc#1012628).
- x86/oprofile: Fix bogus GCC-8 warning in nmi_setup()
  (bnc#1012628).
- x86/apic/vector: Handle vector release on CPU unplug correctly
  (bnc#1012628).
- Kbuild: always define endianess in kconfig.h (bnc#1012628).
- iio: adis_lib: Initialize trigger before requesting interrupt
  (bnc#1012628).
- iio: buffer: check if a buffer has been set up when poll is
  called (bnc#1012628).
- iio: srf08: fix link error "devm_iio_triggered_buffer_setup"
  undefined (bnc#1012628).
- iio: adc: stm32: fix stm32h7_adc_enable error handling
  (bnc#1012628).
- RDMA/uverbs: Sanitize user entered port numbers prior to access
  it (bnc#1012628).
- RDMA/uverbs: Fix circular locking dependency (bnc#1012628).
- RDMA/uverbs: Fix bad unlock balance in ib_uverbs_close_xrcd
  (bnc#1012628).
- RDMA/uverbs: Protect from command mask overflow (bnc#1012628).
- RDMA/uverbs: Protect from races between lookup and destroy of
  uobjects (bnc#1012628).
- genirq/matrix: Handle CPU offlining proper (bnc#1012628).
- extcon: int3496: process id-pin first so that we start with
  the right status (bnc#1012628).
- PKCS#7: fix certificate blacklisting (bnc#1012628).
- PKCS#7: fix certificate chain verification (bnc#1012628).
- X.509: fix NULL dereference when restricting key with
  unsupported_sig (bnc#1012628).
- X.509: fix BUG_ON() when hash algorithm is unsupported
  (bnc#1012628).
- i2c: bcm2835: Set up the rising/falling edge delays
  (bnc#1012628).
- i2c: designware: must wait for enable (bnc#1012628).
- cfg80211: fix cfg80211_beacon_dup (bnc#1012628).
- MIPS: Drop spurious __unused in struct compat_flock
  (bnc#1012628).
- scsi: ibmvfc: fix misdefined reserved field in
  ibmvfc_fcp_rsp_info (bnc#1012628).
- xtensa: fix high memory/reserved memory collision (bnc#1012628).
- MIPS: boot: Define __ASSEMBLY__ for its.S build (bnc#1012628).
- kconfig.h: Include compiler types to avoid missed struct
  attributes (bnc#1012628).
- arm64: mm: don't write garbage into TTBR1_EL1 register
  (bnc#1012628).
- netfilter: drop outermost socket lock in getsockopt()
  (bnc#1012628).
- commit 48cfb35
* Wed Feb 28 2018 jeffm@suse.com
- kernel: add product-identifying information to kernel build (FATE#325281).
- commit 450b8db
* Tue Feb 27 2018 msuchanek@suse.de
- Revert "rpm/kernel-binary.spec.in: Also require m4 for build."
  This reverts commit 0d7b4b3f948c2efb67b7d1b95b5e1dcae225991c.
- commit f5686d2
* Tue Feb 27 2018 tiwai@suse.de
- kernel-binary: do not package extract-cert when not signing modules
  (boo#1080250).
- commit 10a8bc4
* Tue Feb 27 2018 jeffm@suse.com
- Update to 4.16-rc3.
- Eliminated 2 patches.
- commit a1d0a5c
* Tue Feb 27 2018 jeffm@suse.com
- Update to 4.16-rc2.
- Eliminated 1 patch.
- Config changes:
  - i386:
  - X86_MINIMUM_CPU_FAMILY (set automatically by oldconfig).
- commit 70f217f
* Tue Feb 27 2018 jeffm@suse.com
- Update to 4.16-rc1.
- Eliminated 624 patches (mostly 4.15.x).
- ARM configs need updating.
- Config changes:
  - General:
  - CC_STACKPROTECTOR_REGULAR=y
  - x86:
  - ACPI_SPCR_TABLE=y
  - ACER_WIRELESS=m
  - GPD_POCKET_FAN=m
  - INTEL_CHTDC_TI_PWRBTN=m
  - MELLANOX_PLATFORM=y
  - MLXREG_HOTPLUG=m
  - JAILHOUSE_GUEST=y
  - i386:
  - MLX_PLATFORM=m
  - DEFERRED_STRUCT_PAGE_INIT=y
  - powerpc:
  - PPC_MEM_KEYS=y
  - OCXL=m
  - PPC_IRQ_SOFT_MASK_DEBUG=n
  - s390:
  - KERNEL_NOBP=y
  - EXPOLINE=y
  - EXPOLINE_FULL=y
  - PCI:
  - PCIE_CADENCE_HOST=y
  - PCIE_CADENCE_EP=y
  - Network:
  - NF_FLOW_TABLE=m
  - NF_FLOW_TABLE_IPV4=m
  - NF_FLOW_TABLE_IPV6=m
  - IP6_NF_MATCH_SRH=m
  - BT_HCIBTUSB_AUTOSUSPEND=y
  - NET_VENDOR_CORTINA=y
  - GEMINI_ETHERNET=m
  - NET_VENDOR_SOCIONEXT=y
  - NETDEVSIM=n
  - NFT_FLOW_OFFLOAD=m
  - NF_FLOW_TABLE_INET=m
  - Block:
  - BLK_DEV_NULL_BLK_FAULT_INJECTION=n
  - SATA_MOBILE_LPM_POLICY=0
  - DM_UNSTRIPED=m
  - MMC_SDHCI_F_SDH30=n
  - Misc:
  - MISC_RTSX_PCI=m
  - MISC_RTSX_USB=m
  - HW_RANDOM_TPM=y (from m)
  - I2C_GPIO_FAULT_INJECTOR=n
  - PINCTRL_AXP209=m
  - GPIO_WINBOND=m
  - GPIO_PCIE_IDIO_24=m
  - SENSORS_W83773G=m
  - MFD_CROS_EC_CHARDEV=n
  - RAVE_SP_CORE=n
  CAVIUM_PTP=m
  - Graphics:
  - DRM_PANEL_ILITEK_IL9322=n
  - TINYDRM_ILI9225=n
  - TINYDRM_ST7735R=n
  - Sound:
  - SND_SOC_INTEL_SST_TOPLEVEL=y
  - SND_SST_ATOM_HIFI2_PLATFORM_PCI=m
  - SND_SOC_INTEL_BYT_MAX98090_MACH=m
  - SND_SOC_INTEL_BYT_RT5640_MACH=m
  - SND_SOC_MAX98373=n
  - SND_SOC_PCM186X_I2C=n
  - SND_SOC_PCM186X_SPI=n
  - SND_SOC_TAS6424=n
  - SND_SOC_TLV320AIC32X4_I2C=n
  - SND_SOC_TLV320AIC32X4_SPI=n
  - SND_SOC_TSCS42XX=n
  - SOUNDWIRE=y
  - SOUNDWIRE_INTEL=m
  - Input:
  - HID_JABRA=n
  - USB:
  - USB_XHCI_DBGCAP=n
  - LEDS:
  - LEDS_LM3692X=n
  - LEDS_TRIGGER_NETDEV=m
  - LEDS_LP8860=n
  - RTC:
  - RTC_DRV_CROS_EC=n
  - VIRT:
  - VBOXGUEST=m
  - VIRTIO_MENU=y
  - KVM_AMD_SEV=y
  - Filesystems:
  - CIFS_SMB_DIRECT=n (still experimental)
  - Other:
  - UNISYSSPAR=n
  - XILINX_VCU=n
  - IIO_BUFFER_HW_CONSUMER=n
  - SD_ADC_MODULATOR=n
  - OF_FPGA_REGION=n
  - SIOX=n
  - SLIMBUS=n
  - BPF_KPROBE_OVERRIDE=n
  - FPGA_BRIDGE=n
  - Sensors:
  - ST_UVIS25=n
  - ZOPT2201=n
  - Media:
  - MT76x2E=m
  - LIRC=y
  - DVB_MMAP=n (still experimental)
  - DVB_ULE_DEBUG=n
  - Testing:
  - FAIL_FUNCTION=n
  - RUNTIME_TESTING_MENU=y
  - FIND_BIT_BENCHMARK=n
  - Crypto:
  - CHELSIO_IPSEC_INLINE=n
  - CRYPTO_DEV_SP_PSP=y
- commit 955d7ce
* Sun Feb 25 2018 jslaby@suse.cz
- bpf: cpumap: use GFP_KERNEL instead of GFP_ATOMIC in
  __cpu_map_entry_alloc() (git-fixes).
- commit b050949
* Sun Feb 25 2018 jslaby@suse.cz
- ptr_ring: prevent integer overflow when calculating size
  (git-fixes).
- commit f95a8d4
* Sun Feb 25 2018 jslaby@suse.cz
- Linux 4.15.6 (bnc#1012628).
- vmalloc: fix __GFP_HIGHMEM usage for vmalloc_32 on 32b systems
  (bnc#1012628).
- mei: me: add cannon point device ids for 4th device
  (bnc#1012628).
- mei: me: add cannon point device ids (bnc#1012628).
- crypto: s5p-sss - Fix kernel Oops in AES-ECB mode (bnc#1012628).
- usbip: keep usbip_device sockfd state in sync with tcp_socket
  (bnc#1012628).
- xhci: fix xhci debugfs errors in xhci_stop (bnc#1012628).
- xhci: xhci debugfs device nodes weren't removed after device
  plugged out (bnc#1012628).
- xhci: Fix xhci debugfs devices node disappearance after
  hibernation (bnc#1012628).
- xhci: Fix NULL pointer in xhci debugfs (bnc#1012628).
- staging: iio: ad5933: switch buffer mode to software
  (bnc#1012628).
- staging: iio: adc: ad7192: fix external frequency setting
  (bnc#1012628).
- staging: fsl-mc: fix build testing on x86 (bnc#1012628).
- binder: replace "%%p" with "%%pK" (bnc#1012628).
- binder: check for binder_thread allocation failure in
  binder_poll() (bnc#1012628).
- staging: android: ashmem: Fix a race condition in pin ioctls
  (bnc#1012628).
- ANDROID: binder: synchronize_rcu() when using POLLFREE
  (bnc#1012628).
- ANDROID: binder: remove WARN() for redundant txn error
  (bnc#1012628).
- dn_getsockoptdecnet: move nf_{get/set}sockopt outside sock lock
  (bnc#1012628).
- arm64: dts: add #cooling-cells to CPU nodes (bnc#1012628).
- ARM: 8743/1: bL_switcher: add MODULE_LICENSE tag (bnc#1012628).
- video: fbdev/mmp: add MODULE_LICENSE (bnc#1012628).
- ASoC: ux500: add MODULE_LICENSE tag (bnc#1012628).
- soc: qcom: rmtfs_mem: add missing
  MODULE_DESCRIPTION/AUTHOR/LICENSE (bnc#1012628).
- net_sched: gen_estimator: fix lockdep splat (bnc#1012628).
- net: avoid skb_warn_bad_offload on IS_ERR (bnc#1012628).
- rds: tcp: atomically purge entries from rds_tcp_conn_list
  during netns delete (bnc#1012628).
- rds: tcp: correctly sequence cleanup on netns deletion
  (bnc#1012628).
- netfilter: xt_RATEEST: acquire xt_rateest_mutex for hash insert
  (bnc#1012628).
- netfilter: xt_cgroup: initialize info->priv in
  cgroup_mt_check_v1() (bnc#1012628).
- netfilter: on sockopt() acquire sock lock only in the required
  scope (bnc#1012628).
- netfilter: ipt_CLUSTERIP: fix out-of-bounds accesses in
  clusterip_tg_check() (bnc#1012628).
- netfilter: x_tables: avoid out-of-bounds reads in
  xt_request_find_{match|target} (bnc#1012628).
- netfilter: x_tables: fix int overflow in xt_alloc_table_info()
  (bnc#1012628).
- kcov: detect double association with a single task
  (bnc#1012628).
- KVM: x86: fix escape of guest dr6 to the host (bnc#1012628).
- blk_rq_map_user_iov: fix error override (bnc#1012628).
- staging: android: ion: Switch from WARN to pr_warn
  (bnc#1012628).
- staging: android: ion: Add __GFP_NOWARN for system contig heap
  (bnc#1012628).
- crypto: x86/twofish-3way - Fix %%rbp usage (bnc#1012628).
- media: pvrusb2: properly check endpoint types (bnc#1012628).
- selinux: skip bounded transition processing if the policy
  isn't loaded (bnc#1012628).
- selinux: ensure the context is NUL terminated in
  security_context_to_sid_core() (bnc#1012628).
- ptr_ring: try vmalloc() when kmalloc() fails (bnc#1012628).
- ptr_ring: fail early if queue occupies more than
  KMALLOC_MAX_SIZE (bnc#1012628).
- tun: fix tun_napi_alloc_frags() frag allocator (bnc#1012628).
- commit 71fd692
* Thu Feb 22 2018 jslaby@suse.cz
- powerpc/pseries: Add empty update_numa_cpu_lookup_table()
  for NUMA=n (git-fixes).
- commit 4a82466
* Thu Feb 22 2018 jslaby@suse.cz
- Linux 4.15.5 (bnc#1012628).
- scsi: smartpqi: allow static build ("built-in") (bnc#1012628).
- IB/umad: Fix use of unprotected device pointer (bnc#1012628).
- IB/qib: Fix comparison error with qperf compare/swap test
  (bnc#1012628).
- IB/mlx4: Fix incorrectly releasing steerable UD QPs when have
  only ETH ports (bnc#1012628).
- IB/core: Fix two kernel warnings triggered by rxe registration
  (bnc#1012628).
- IB/core: Fix ib_wc structure size to remain in 64 bytes boundary
  (bnc#1012628).
- IB/core: Avoid a potential OOPs for an unused optional parameter
  (bnc#1012628).
- selftests: seccomp: fix compile error seccomp_bpf (bnc#1012628).
- kselftest: fix OOM in memory compaction test (bnc#1012628).
- RDMA/rxe: Fix a race condition related to the QP error state
  (bnc#1012628).
- RDMA/rxe: Fix a race condition in rxe_requester() (bnc#1012628).
- RDMA/rxe: Fix rxe_qp_cleanup() (bnc#1012628).
- cpufreq: powernv: Dont assume distinct pstate values for
  nominal and pmin (bnc#1012628).
- swiotlb: suppress warning when __GFP_NOWARN is set
  (bnc#1012628).
- PM / devfreq: Propagate error from devfreq_add_device()
  (bnc#1012628).
- mwifiex: resolve reset vs. remove()/shutdown() deadlocks
  (bnc#1012628).
- ocfs2: try a blocking lock before return AOP_TRUNCATED_PAGE
  (bnc#1012628).
- trace_uprobe: Display correct offset in uprobe_events
  (bnc#1012628).
- powerpc/radix: Remove trace_tlbie call from radix__flush_tlb_all
  (bnc#1012628).
- powerpc/kernel: Block interrupts when updating TIDR
  (bnc#1012628).
- powerpc/vas: Don't set uses_vas for kernel windows
  (bnc#1012628).
- powerpc/numa: Invalidate numa_cpu_lookup_table on cpu remove
  (bnc#1012628).
- powerpc/mm: Flush radix process translations when setting MMU
  type (bnc#1012628).
- powerpc/xive: Use hw CPU ids when configuring the CPU queues
  (bnc#1012628).
- dma-buf: fix reservation_object_wait_timeout_rcu once more v2
  (bnc#1012628).
- s390: fix handling of -1 in set{,fs}[gu]id16 syscalls
  (bnc#1012628).
- arm64: dts: msm8916: Correct ipc references for smsm
  (bnc#1012628).
- ARM: lpc3250: fix uda1380 gpio numbers (bnc#1012628).
- ARM: dts: STi: Add gpio polarity for "hdmi,hpd-gpio" property
  (bnc#1012628).
- ARM: dts: nomadik: add interrupt-parent for clcd (bnc#1012628).
- arm: dts: mt7623: fix card detection issue on bananapi-r2
  (bnc#1012628).
- arm: spear600: Add missing interrupt-parent of rtc
  (bnc#1012628).
- arm: spear13xx: Fix dmas cells (bnc#1012628).
- arm: spear13xx: Fix spics gpio controller's warning
  (bnc#1012628).
- x86/gpu: add CFL to early quirks (bnc#1012628).
- x86/kexec: Make kexec (mostly) work in 5-level paging mode
  (bnc#1012628).
- x86/xen: init %%gs very early to avoid page faults with stack
  protector (bnc#1012628).
- x86: PM: Make APM idle driver initialize polling state
  (bnc#1012628).
- mm, memory_hotplug: fix memmap initialization (bnc#1012628).
- x86/entry/64: Clear extra registers beyond syscall arguments,
  to reduce speculation attack surface (bnc#1012628).
- x86/entry/64/compat: Clear registers for compat syscalls,
  to reduce speculation attack surface (bnc#1012628).
- compiler-gcc.h: Introduce __optimize function attribute
  (bnc#1012628).
- compiler-gcc.h: __nostackprotector needs gcc-4.4 and up
  (bnc#1012628).
- crypto: sun4i_ss_prng - fix return value of
  sun4i_ss_prng_generate (bnc#1012628).
- crypto: sun4i_ss_prng - convert lock to _bh in
  sun4i_ss_prng_generate (bnc#1012628).
- powerpc/mm/radix: Split linear mapping on hot-unplug
  (bnc#1012628).
- x86/mm/pti: Fix PTI comment in entry_SYSCALL_64() (bnc#1012628).
- x86/speculation: Update Speculation Control microcode blacklist
  (bnc#1012628).
- x86/speculation: Correct Speculation Control microcode blacklist
  again (bnc#1012628).
- Revert "x86/speculation: Simplify
  indirect_branch_prediction_barrier()" (bnc#1012628).
- KVM/x86: Reduce retpoline performance impact in
  slot_handle_level_range(), by always inlining iterator helper
  methods (bnc#1012628).
- X86/nVMX: Properly set spec_ctrl and pred_cmd before merging
  MSRs (bnc#1012628).
- KVM/nVMX: Set the CPU_BASED_USE_MSR_BITMAPS if we have a valid
  L02 MSR bitmap (bnc#1012628).
- x86/speculation: Clean up various Spectre related details
  (bnc#1012628).
- PM / runtime: Update links_count also if !CONFIG_SRCU
  (bnc#1012628).
- PM: cpuidle: Fix cpuidle_poll_state_init() prototype
  (bnc#1012628).
- platform/x86: wmi: fix off-by-one write in wmi_dev_probe()
  (bnc#1012628).
- x86/entry/64: Clear registers for exceptions/interrupts,
  to reduce speculation attack surface (bnc#1012628).
- x86/entry/64: Merge SAVE_C_REGS and SAVE_EXTRA_REGS, remove
  unused extensions (bnc#1012628).
- x86/entry/64: Merge the POP_C_REGS and POP_EXTRA_REGS macros
  into a single POP_REGS macro (bnc#1012628).
- x86/entry/64: Interleave XOR register clearing with PUSH
  instructions (bnc#1012628).
- x86/entry/64: Introduce the PUSH_AND_CLEAN_REGS macro
  (bnc#1012628).
- x86/entry/64: Use PUSH_AND_CLEAN_REGS in more cases
  (bnc#1012628).
- x86/entry/64: Get rid of the ALLOC_PT_GPREGS_ON_STACK and
  SAVE_AND_CLEAR_REGS macros (bnc#1012628).
- x86/entry/64: Indent PUSH_AND_CLEAR_REGS and POP_REGS properly
  (bnc#1012628).
- x86/entry/64: Fix paranoid_entry() frame pointer warning
  (bnc#1012628).
- x86/entry/64: Remove the unused 'icebp' macro (bnc#1012628).
- selftests/x86: Fix vDSO selftest segfault for vsyscall=none
  (bnc#1012628).
- selftests/x86: Clean up and document sscanf() usage
  (bnc#1012628).
- selftests/x86/pkeys: Remove unused functions (bnc#1012628).
- selftests/x86: Fix build bug caused by the 5lvl test which
  has been moved to the VM directory (bnc#1012628).
- selftests/x86: Do not rely on "int $0x80" in test_mremap_vdso.c
  (bnc#1012628).
- gfs2: Fixes to "Implement iomap for block_map" (bnc#1012628).
- selftests/x86: Do not rely on "int $0x80" in
  single_step_syscall.c (bnc#1012628).
- selftests/x86: Disable tests requiring 32-bit support on pure
  64-bit systems (bnc#1012628).
- objtool: Fix segfault in ignore_unreachable_insn()
  (bnc#1012628).
- x86/debug, objtool: Annotate WARN()-related UD2 as reachable
  (bnc#1012628).
- x86/debug: Use UD2 for WARN() (bnc#1012628).
- x86/speculation: Fix up array_index_nospec_mask() asm constraint
  (bnc#1012628).
- nospec: Move array_index_nospec() parameter checking into
  separate macro (bnc#1012628).
- x86/speculation: Add <asm/msr-index.h> dependency (bnc#1012628).
- x86/mm: Rename flush_tlb_single() and flush_tlb_one() to
  __flush_tlb_one_[user|kernel]() (bnc#1012628).
- selftests/x86/mpx: Fix incorrect bounds with old _sigfault
  (bnc#1012628).
- x86/cpu: Rename cpu_data.x86_mask to cpu_data.x86_stepping
  (bnc#1012628).
- x86/spectre: Fix an error message (bnc#1012628).
- x86/cpu: Change type of x86_cache_size variable to unsigned int
  (bnc#1012628).
- x86/entry/64: Fix CR3 restore in paranoid_exit() (bnc#1012628).
- drm/ttm: Don't add swapped BOs to swap-LRU list (bnc#1012628).
- drm/ttm: Fix 'buf' pointer update in ttm_bo_vm_access_kmap()
  (v2) (bnc#1012628).
- drm/qxl: unref cursor bo when finished with it (bnc#1012628).
- drm/qxl: reapply cursor after resetting primary (bnc#1012628).
- drm/amd/powerplay: Fix smu_table_entry.handle type
  (bnc#1012628).
- drm/ast: Load lut in crtc_commit (bnc#1012628).
- drm: Check for lessee in DROP_MASTER ioctl (bnc#1012628).
- arm64: Add missing Falkor part number for branch predictor
  hardening (bnc#1012628).
- drm/radeon: Add dpm quirk for Jet PRO (v2) (bnc#1012628).
- drm/radeon: adjust tested variable (bnc#1012628).
- x86/smpboot: Fix uncore_pci_remove() indexing bug when
  hot-removing a physical CPU (bnc#1012628).
- rtc-opal: Fix handling of firmware error codes, prevent busy
  loops (bnc#1012628).
- mbcache: initialize entry->e_referenced in
  mb_cache_entry_create() (bnc#1012628).
- mmc: sdhci: Implement an SDHCI-specific bounce buffer
  (bnc#1012628).
- mmc: bcm2835: Don't overwrite max frequency unconditionally
  (bnc#1012628).
- Revert "mmc: meson-gx: include tx phase in the tuning process"
  (bnc#1012628).
- mlx5: fix mlx5_get_vector_affinity to start from completion
  vector 0 (bnc#1012628).
- Revert "apple-gmux: lock iGP IO to protect from vgaarb changes"
  (bnc#1012628).
- jbd2: fix sphinx kernel-doc build warnings (bnc#1012628).
- ext4: fix a race in the ext4 shutdown path (bnc#1012628).
- ext4: save error to disk in __ext4_grp_locked_error()
  (bnc#1012628).
- ext4: correct documentation for grpid mount option
  (bnc#1012628).
- mm: hide a #warning for COMPILE_TEST (bnc#1012628).
- mm: Fix memory size alignment in devm_memremap_pages_release()
  (bnc#1012628).
- MIPS: Fix typo BIG_ENDIAN to CPU_BIG_ENDIAN (bnc#1012628).
- MIPS: CPS: Fix MIPS_ISA_LEVEL_RAW fallout (bnc#1012628).
- MIPS: Fix incorrect mem=X@Y handling (bnc#1012628).
- PCI: Disable MSI for HiSilicon Hip06/Hip07 only in Root Port
  mode (bnc#1012628).
- PCI: iproc: Fix NULL pointer dereference for BCMA (bnc#1012628).
- PCI: pciehp: Assume NoCompl+ for Thunderbolt ports
  (bnc#1012628).
- PCI: keystone: Fix interrupt-controller-node lookup
  (bnc#1012628).
- video: fbdev: atmel_lcdfb: fix display-timings lookup
  (bnc#1012628).
- console/dummy: leave .con_font_get set to NULL (bnc#1012628).
- rbd: whitelist RBD_FEATURE_OPERATIONS feature bit (bnc#1012628).
- xen: Fix {set,clear}_foreign_p2m_mapping on autotranslating
  guests (bnc#1012628).
- xenbus: track caller request id (bnc#1012628).
- seq_file: fix incomplete reset on read from zero offset
  (bnc#1012628).
- tracing: Fix parsing of globs with a wildcard at the beginning
  (bnc#1012628).
- mpls, nospec: Sanitize array index in mpls_label_ok()
  (bnc#1012628).
- rtlwifi: rtl8821ae: Fix connection lost problem correctly
  (bnc#1012628).
- arm64: proc: Set PTE_NG for table entries to avoid traversing
  them twice (bnc#1012628).
- xprtrdma: Fix calculation of ri_max_send_sges (bnc#1012628).
- xprtrdma: Fix BUG after a device removal (bnc#1012628).
- blk-wbt: account flush requests correctly (bnc#1012628).
- target/iscsi: avoid NULL dereference in CHAP auth error path
  (bnc#1012628).
- iscsi-target: make sure to wake up sleeping login worker
  (bnc#1012628).
- dm: correctly handle chained bios in dec_pending()
  (bnc#1012628).
- Btrfs: fix deadlock in run_delalloc_nocow (bnc#1012628).
- Btrfs: fix crash due to not cleaning up tree log block's dirty
  bits (bnc#1012628).
- Btrfs: fix extent state leak from tree log (bnc#1012628).
- Btrfs: fix use-after-free on root->orphan_block_rsv
  (bnc#1012628).
- Btrfs: fix unexpected -EEXIST when creating new inode
  (bnc#1012628).
- 9p/trans_virtio: discard zero-length reply (bnc#1012628).
- mtd: nand: vf610: set correct ooblayout (bnc#1012628).
- ALSA: hda - Fix headset mic detection problem for two Dell
  machines (bnc#1012628).
- ALSA: usb-audio: Fix UAC2 get_ctl request with a RANGE attribute
  (bnc#1012628).
- ALSA: hda/realtek - Add headset mode support for Dell laptop
  (bnc#1012628).
- ALSA: hda/realtek - Enable Thinkpad Dock device for ALC298
  platform (bnc#1012628).
- ALSA: hda/realtek: PCI quirk for Fujitsu U7x7 (bnc#1012628).
- ALSA: usb-audio: add implicit fb quirk for Behringer UFX1204
  (bnc#1012628).
- ALSA: usb: add more device quirks for USB DSD devices
  (bnc#1012628).
- ALSA: seq: Fix racy pool initializations (bnc#1012628).
- mvpp2: fix multicast address filter (bnc#1012628).
- usb: Move USB_UHCI_BIG_ENDIAN_* out of USB_SUPPORT
  (bnc#1012628).
- x86/mm, mm/hwpoison: Don't unconditionally unmap kernel 1:1
  pages (bnc#1012628).
- ARM: dts: exynos: fix RTC interrupt for exynos5410
  (bnc#1012628).
- ARM: pxa/tosa-bt: add MODULE_LICENSE tag (bnc#1012628).
- arm64: dts: msm8916: Add missing #phy-cells (bnc#1012628).
- ARM: dts: s5pv210: add interrupt-parent for ohci (bnc#1012628).
- arm: dts: mt7623: Update ethsys binding (bnc#1012628).
- arm: dts: mt2701: Add reset-cells (bnc#1012628).
- ARM: dts: Delete bogus reference to the charlcd (bnc#1012628).
- media: r820t: fix r820t_write_reg for KASAN (bnc#1012628).
- mmc: sdhci-of-esdhc: fix eMMC couldn't work after kexec
  (bnc#1012628).
- mmc: sdhci-of-esdhc: fix the mmc error after sleep on ls1046ardb
  (bnc#1012628).
- Refresh
  patches.suse/0001-x86-speculation-Add-basic-IBRS-support-infrastructur.patch.
- Refresh
  patches.suse/0002-x86-speculation-Add-inlines-to-control-Indirect-Bran.patch.
- Refresh
  patches.suse/0005-x86-enter-Use-IBRS-on-syscall-and-interrupts.patch.
- commit 078aac5
* Thu Feb 22 2018 lpechacek@suse.com
- rpm/kernel-spec-macros: Try harder to detect Build Service environment (bsc#1078788)
- commit a5f1a4a
* Wed Feb 21 2018 msuchanek@suse.de
- kernel-binary undefine unique_debug_names
  Some tools do not understand names like
  usr/lib/debug/boot/vmlinux-4.12.14-11.10-default-4.12.14-11.10.ppc64le.debug
- commit 2b90c1e
* Tue Feb 20 2018 jeffm@suse.com
- config: enable IMA and EVM
- commit 8c97198
* Sun Feb 18 2018 afaerber@suse.de
- config: arm64: Enable MAX77620 for Nvidia Jetson TX1 (boo#1081473)
- commit 5cbffaf
* Sat Feb 17 2018 jslaby@suse.cz
- Linux 4.15.4 (bnc#1012628).
- watchdog: indydog: Add dependency on SGI_HAS_INDYDOG
  (bnc#1012628).
- cifs: Fix missing put_xid in cifs_file_strict_mmap
  (bnc#1012628).
- cifs: Fix autonegotiate security settings mismatch
  (bnc#1012628).
- CIFS: zero sensitive data when freeing (bnc#1012628).
- cpufreq: mediatek: add mediatek related projects into blacklist
  (bnc#1012628).
- dmaengine: dmatest: fix container_of member in dmatest_callback
  (bnc#1012628).
- ssb: Do not disable PCI host on non-Mips (bnc#1012628).
- watchdog: gpio_wdt: set WDOG_HW_RUNNING in gpio_wdt_stop
  (bnc#1012628).
- Revert "drm/i915: mark all device info struct with __initconst"
  (bnc#1012628).
- sched/rt: Use container_of() to get root domain in
  rto_push_irq_work_func() (bnc#1012628).
- sched/rt: Up the root domain ref count when passing it around
  via IPIs (bnc#1012628).
- media: dvb-usb-v2: lmedm04: Improve logic checking of warm start
  (bnc#1012628).
- media: dvb-usb-v2: lmedm04: move ts2020 attach to
  dm04_lme2510_tuner (bnc#1012628).
- media: hdpvr: Fix an error handling path in hdpvr_probe()
  (bnc#1012628).
- arm64: cpu_errata: Add Kryo to Falkor 1003 errata (bnc#1012628).
- arm64: kpti: Make use of nG dependent on
  arm64_kernel_unmapped_at_el0() (bnc#1012628).
- arm64: mm: Permit transitioning from Global to Non-Global
  without BBM (bnc#1012628).
- arm64: kpti: Add ->enable callback to remap swapper using nG
  mappings (bnc#1012628).
- arm64: Force KPTI to be disabled on Cavium ThunderX
  (bnc#1012628).
- arm64: entry: Reword comment about post_ttbr_update_workaround
  (bnc#1012628).
- arm64: idmap: Use "awx" flags for .idmap.text .pushsection
  directives (bnc#1012628).
- arm64: barrier: Add CSDB macros to control data-value prediction
  (bnc#1012628).
- arm64: Implement array_index_mask_nospec() (bnc#1012628).
- arm64: Make USER_DS an inclusive limit (bnc#1012628).
- arm64: Use pointer masking to limit uaccess speculation
  (bnc#1012628).
- arm64: entry: Ensure branch through syscall table is bounded
  under speculation (bnc#1012628).
- arm64: uaccess: Prevent speculative use of the current
  addr_limit (bnc#1012628).
- arm64: uaccess: Don't bother eliding access_ok checks in __{get,
  put}_user (bnc#1012628).
- arm64: uaccess: Mask __user pointers for __arch_{clear,
  copy_*}_user (bnc#1012628).
- arm64: futex: Mask __user pointers prior to dereference
  (bnc#1012628).
- arm64: cpufeature: __this_cpu_has_cap() shouldn't stop early
  (bnc#1012628).
- arm64: entry: Apply BP hardening for high-priority synchronous
  exceptions (bnc#1012628).
- arm64: entry: Apply BP hardening for suspicious interrupts
  from EL0 (bnc#1012628).
- arm64: KVM: Increment PC after handling an SMC trap
  (bnc#1012628).
- arm/arm64: KVM: Consolidate the PSCI include files
  (bnc#1012628).
- arm/arm64: KVM: Add PSCI_VERSION helper (bnc#1012628).
- arm/arm64: KVM: Add smccc accessors to PSCI code (bnc#1012628).
- arm/arm64: KVM: Implement PSCI 1.0 support (bnc#1012628).
- arm/arm64: KVM: Advertise SMCCC v1.1 (bnc#1012628).
- arm/arm64: KVM: Turn kvm_psci_version into a static inline
  (bnc#1012628).
- arm64: KVM: Report SMCCC_ARCH_WORKAROUND_1 BP hardening support
  (bnc#1012628).
- arm64: KVM: Add SMCCC_ARCH_WORKAROUND_1 fast handling
  (bnc#1012628).
- firmware/psci: Expose PSCI conduit (bnc#1012628).
- firmware/psci: Expose SMCCC version through psci_ops
  (bnc#1012628).
- arm/arm64: smccc: Make function identifiers an unsigned quantity
  (bnc#1012628).
- arm/arm64: smccc: Implement SMCCC v1.1 inline primitive
  (bnc#1012628).
- arm64: Add ARM_SMCCC_ARCH_WORKAROUND_1 BP hardening support
  (bnc#1012628).
- arm64: Kill PSCI_GET_VERSION as a variant-2 workaround
  (bnc#1012628).
- mtd: cfi: convert inline functions to macros (bnc#1012628).
- mtd: nand: brcmnand: Disable prefetch by default (bnc#1012628).
- mtd: nand: Fix nand_do_read_oob() return value (bnc#1012628).
- mtd: nand: sunxi: Fix ECC strength choice (bnc#1012628).
- ubi: Fix race condition between ubi volume creation and udev
  (bnc#1012628).
- ubi: fastmap: Erase outdated anchor PEBs during attach
  (bnc#1012628).
- ubi: block: Fix locking for idr_alloc/idr_remove (bnc#1012628).
- ubifs: free the encrypted symlink target (bnc#1012628).
- nfs/pnfs: fix nfs_direct_req ref leak when i/o falls back to
  the mds (bnc#1012628).
- nfs41: do not return ENOMEM on LAYOUTUNAVAILABLE (bnc#1012628).
- NFS: Add a cond_resched() to nfs_commit_release_pages()
  (bnc#1012628).
- NFS: Fix nfsstat breakage due to LOOKUPP (bnc#1012628).
- NFS: commit direct writes even if they fail partially
  (bnc#1012628).
- NFS: reject request for id_legacy key without auxdata
  (bnc#1012628).
- NFS: Fix a race between mmap() and O_DIRECT (bnc#1012628).
- nfsd: Detect unhashed stids in nfsd4_verify_open_stid()
  (bnc#1012628).
- kernfs: fix regression in kernfs_fop_write caused by wrong type
  (bnc#1012628).
- ahci: Annotate PCI ids for mobile Intel chipsets as such
  (bnc#1012628).
- ahci: Add PCI ids for Intel Bay Trail, Cherry Trail and Apollo
  Lake AHCI (bnc#1012628).
- ahci: Add Intel Cannon Lake PCH-H PCI ID (bnc#1012628).
- crypto: hash - introduce crypto_hash_alg_has_setkey()
  (bnc#1012628).
- crypto: cryptd - pass through absence of ->setkey()
  (bnc#1012628).
- crypto: mcryptd - pass through absence of ->setkey()
  (bnc#1012628).
- crypto: poly1305 - remove ->setkey() method (bnc#1012628).
- crypto: hash - annotate algorithms taking optional key
  (bnc#1012628).
- crypto: hash - prevent using keyed hashes without setting key
  (bnc#1012628).
- media: v4l2-ioctl.c: use check_fmt for enum/g/s/try_fmt
  (bnc#1012628).
- media: v4l2-ioctl.c: don't copy back the result for -ENOTTY
  (bnc#1012628).
- media: v4l2-compat-ioctl32.c: add missing VIDIOC_PREPARE_BUF
  (bnc#1012628).
- media: v4l2-compat-ioctl32.c: fix the indentation (bnc#1012628).
- media: v4l2-compat-ioctl32.c: move 'helper' functions to
  __get/put_v4l2_format32 (bnc#1012628).
- media: v4l2-compat-ioctl32.c: avoid sizeof(type) (bnc#1012628).
- media: v4l2-compat-ioctl32.c: copy m.userptr in put_v4l2_plane32
  (bnc#1012628).
- media: v4l2-compat-ioctl32.c: fix ctrl_is_pointer (bnc#1012628).
- media: v4l2-compat-ioctl32.c: copy clip list in
  put_v4l2_window32 (bnc#1012628).
- media: v4l2-compat-ioctl32.c: drop pr_info for unknown buffer
  type (bnc#1012628).
- media: v4l2-compat-ioctl32.c: don't copy back the result for
  certain errors (bnc#1012628).
- media: v4l2-compat-ioctl32.c: refactor compat ioctl32 logic
  (bnc#1012628).
- media: v4l2-compat-ioctl32.c: make ctrl_is_pointer work for
  subdevs (bnc#1012628).
- crypto: caam - fix endless loop when DECO acquire fails
  (bnc#1012628).
- crypto: sha512-mb - initialize pending lengths correctly
  (bnc#1012628).
- crypto: talitos - fix Kernel Oops on hashing an empty file
  (bnc#1012628).
- arm: KVM: Fix SMCCC handling of unimplemented SMC/HVC calls
  (bnc#1012628).
- KVM: nVMX: Fix races when sending nested PI while dest
  enters/leaves L2 (bnc#1012628).
- KVM: nVMX: Fix bug of injecting L2 exception into L1
  (bnc#1012628).
- KVM: PPC: Book3S HV: Make sure we don't re-enter guest without
  XIVE loaded (bnc#1012628).
- KVM: PPC: Book3S HV: Drop locks before reading guest memory
  (bnc#1012628).
- KVM: arm/arm64: Handle CPU_PM_ENTER_FAILED (bnc#1012628).
- KVM: PPC: Book3S PR: Fix broken select due to misspelling
  (bnc#1012628).
- ASoC: acpi: fix machine driver selection based on quirk
  (bnc#1012628).
- ASoC: rockchip: i2s: fix playback after runtime resume
  (bnc#1012628).
- ASoC: skl: Fix kernel warning due to zero NHTL entry
  (bnc#1012628).
- ASoC: compress: Correct handling of copy callback (bnc#1012628).
- watchdog: imx2_wdt: restore previous timeout after
  suspend+resume (bnc#1012628).
- afs: Add missing afs_put_cell() (bnc#1012628).
- afs: Need to clear responded flag in addr cursor (bnc#1012628).
- afs: Fix missing cursor clearance (bnc#1012628).
- afs: Fix server list handling (bnc#1012628).
- btrfs: Handle btrfs_set_extent_delalloc failure in fixup worker
  (bnc#1012628).
- Btrfs: raid56: iterate raid56 internal bio with
  bio_for_each_segment_all (bnc#1012628).
- kasan: don't emit builtin calls when sanitization is off
  (bnc#1012628).
- kasan: rework Kconfig settings (bnc#1012628).
- media: dvb_frontend: be sure to init dvb_frontend_handle_ioctl()
  return code (bnc#1012628).
- media: dvb-frontends: fix i2c access helpers for KASAN
  (bnc#1012628).
- media: dt-bindings/media/cec-gpio.txt: mention the CEC/HPD
  max voltages (bnc#1012628).
- media: ts2020: avoid integer overflows on 32 bit machines
  (bnc#1012628).
- media: vivid: fix module load error when enabling fb and
  no_error_inj=1 (bnc#1012628).
- media: cxusb, dib0700: ignore XC2028_I2C_FLUSH (bnc#1012628).
- fs/proc/kcore.c: use probe_kernel_read() instead of memcpy()
  (bnc#1012628).
- kernel/async.c: revert "async: simplify lowest_in_progress()"
  (bnc#1012628).
- kernel/relay.c: revert "kernel/relay.c: fix potential memory
  leak" (bnc#1012628).
- pipe: actually allow root to exceed the pipe buffer limits
  (bnc#1012628).
- pipe: fix off-by-one error when checking buffer limits
  (bnc#1012628).
- HID: quirks: Fix keyboard + touchpad on Toshiba Click Mini
  not working (bnc#1012628).
- Bluetooth: btsdio: Do not bind to non-removable BCM43341
  (bnc#1012628).
- Revert "Bluetooth: btusb: fix QCA Rome suspend/resume"
  (bnc#1012628).
- Bluetooth: btusb: Restore QCA Rome suspend/resume fix with a
  "rewritten" version (bnc#1012628).
- ipmi: use dynamic memory for DMI driver override (bnc#1012628).
- signal/openrisc: Fix do_unaligned_access to send the proper
  signal (bnc#1012628).
- signal/sh: Ensure si_signo is initialized in do_divide_error
  (bnc#1012628).
- alpha: fix crash if pthread_create races with signal delivery
  (bnc#1012628).
- alpha: osf_sys.c: fix put_tv32 regression (bnc#1012628).
- alpha: Fix mixed up args in EXC macro in futex operations
  (bnc#1012628).
- alpha: fix reboot on Avanti platform (bnc#1012628).
- alpha: fix formating of stack content (bnc#1012628).
- xtensa: fix futex_atomic_cmpxchg_inatomic (bnc#1012628).
- EDAC, octeon: Fix an uninitialized variable warning
  (bnc#1012628).
- genirq: Make legacy autoprobing work again (bnc#1012628).
- pinctrl: intel: Initialize GPIO properly when used through
  irqchip (bnc#1012628).
- pinctrl: mcp23s08: fix irq setup order (bnc#1012628).
- pinctrl: sx150x: Unregister the pinctrl on release
  (bnc#1012628).
- pinctrl: sx150x: Register pinctrl before adding the gpiochip
  (bnc#1012628).
- pinctrl: sx150x: Add a static gpio/pinctrl pin range mapping
  (bnc#1012628).
- pktcdvd: Fix pkt_setup_dev() error path (bnc#1012628).
- pktcdvd: Fix a recently introduced NULL pointer dereference
  (bnc#1012628).
- blk-mq: quiesce queue before freeing queue (bnc#1012628).
- clocksource/drivers/stm32: Fix kernel panic with multiple timers
  (bnc#1012628).
- lib/ubsan.c: s/missaligned/misaligned/ (bnc#1012628).
- lib/ubsan: add type mismatch handler for new GCC/Clang
  (bnc#1012628).
- objtool: Fix switch-table detection (bnc#1012628).
- arm64: dts: marvell: add Ethernet aliases (bnc#1012628).
- drm/i915: Avoid PPS HW/SW state mismatch due to rounding
  (bnc#1012628).
- ACPI: sbshc: remove raw pointer from printk() message
  (bnc#1012628).
- acpi, nfit: fix register dimm error handling (bnc#1012628).
- ovl: force r/o mount when index dir creation fails
  (bnc#1012628).
- ovl: fix failure to fsync lower dir (bnc#1012628).
- ovl: take mnt_want_write() for work/index dir setup
  (bnc#1012628).
- ovl: take mnt_want_write() for removing impure xattr
  (bnc#1012628).
- ovl: hash directory inodes for fsnotify (bnc#1012628).
- mn10300/misalignment: Use SIGSEGV SEGV_MAPERR to report a
  failed user copy (bnc#1012628).
- devpts: fix error handling in devpts_mntget() (bnc#1012628).
- ftrace: Remove incorrect setting of glob search field
  (bnc#1012628).
- scsi: core: Ensure that the SCSI error handler gets woken up
  (bnc#1012628).
- scsi: lpfc: Fix crash after bad bar setup on driver attachment
  (bnc#1012628).
- scsi: cxlflash: Reset command ioasc (bnc#1012628).
- rcu: Export init_rcu_head() and destroy_rcu_head() to GPL
  modules (bnc#1012628).
- media: dvb_frontend: fix return error code (git-fixes).
- mtd: ubi: wl: Fix error return code in ubi_wl_init()
  (git-fixes).
- Update config files.
- commit 4d42c34
* Thu Feb 15 2018 jmoreira@suse.de
- Add kernel livepatch-devel package
  Resolving non-exported static symbols in kernel livepatches cannot
  be done implicitly. For such, the relocations of these symbols must
  follow a specially crafted format in the respective elf file. Willing
  to make the task of converting the elf into the right format, a tool
  named klp-convert was proposed. Through a file that maps all kernel
  symbols into their respective kernel object, this tool infers which
  non-exported symbol is relative to a livepatch relocation and
  automatically formats the final elf file.
  Add support to the generation of a map file right after the kernel
  compilation.
  Add the package kernel-<flavour>-livepatch-devel that brings
  the map file.
- commit 0b1b4d3
* Tue Feb 13 2018 jslaby@suse.cz
- Linux 4.15.3 (bnc#1012628).
- crypto: tcrypt - fix S/G table for test_aead_speed()
  (bnc#1012628).
- gpio: uniphier: fix mismatch between license text and
  MODULE_LICENSE (bnc#1012628).
- media: tegra-cec: add missing MODULE_DESCRIPTION/AUTHOR/LICENSE
  (bnc#1012628).
- media: soc_camera: soc_scale_crop: add missing
  MODULE_DESCRIPTION/AUTHOR/LICENSE (bnc#1012628).
- media: mtk-vcodec: add missing MODULE_LICENSE/DESCRIPTION
  (bnc#1012628).
- net: sched: fix use-after-free in tcf_block_put_ext
  (bnc#1012628).
- net_sched: get rid of rcu_barrier() in tcf_block_put_ext()
  (bnc#1012628).
- soreuseport: fix mem leak in reuseport_add_sock() (bnc#1012628).
- ipv6: Fix SO_REUSEPORT UDP socket with implicit sk_ipv6only
  (bnc#1012628).
- cls_u32: add missing RCU annotation (bnc#1012628).
- tcp_bbr: fix pacing_gain to always be unity when using lt_bw
  (bnc#1012628).
- rocker: fix possible null pointer dereference in
  rocker_router_fib_event_work (bnc#1012628).
- net: ipv6: send unsolicited NA after DAD (bnc#1012628).
- Revert "defer call to mem_cgroup_sk_alloc()" (bnc#1012628).
- ipv6: change route cache aging logic (bnc#1012628).
- ipv6: addrconf: break critical section in addrconf_verify_rtnl()
  (bnc#1012628).
- vhost_net: stop device during reset owner (bnc#1012628).
- tcp: release sk_frag.page in tcp_disconnect (bnc#1012628).
- r8169: fix RTL8168EP take too long to complete driver
  initialization (bnc#1012628).
- qmi_wwan: Add support for Quectel EP06 (bnc#1012628).
- qlcnic: fix deadlock bug (bnc#1012628).
- net: igmp: add a missing rcu locking section (bnc#1012628).
- ip6mr: fix stale iterator (bnc#1012628).
- commit e7bb737
* Tue Feb 13 2018 jslaby@suse.cz
- ext4: llseek, do not crop offset on 32bit (bsc#1079747).
- commit c6ab9c6
* Sun Feb 11 2018 afaerber@suse.de
- config: arm64: Enable Hi6421 PMU (bsc#1080449)
- commit 77a784c
* Fri Feb  9 2018 jslaby@suse.cz
- Update i386 config files.
  Switch from almost unusable UNWINDER_GUESS to UNWINDER_FRAME_POINTER
  (which enables FRAME_POINTERs). It will slow down the kernel a bit,
  but improves the stack traces by the order of magnitude. Sad is that
  we have no ORCs on i386...
- commit 1d39996
* Fri Feb  9 2018 jslaby@suse.cz
- Update config files.
  Sync vanilla configs to 4.15.
- commit 85c7881
* Thu Feb  8 2018 msuchanek@suse.de
- rpm/kernel-binary.spec.in: Also require m4 for build.
- commit 0d7b4b3
* Thu Feb  8 2018 jslaby@suse.cz
- Linux 4.15.2 (bnc#1012628).
- KVM: x86: Make indirect calls in emulator speculation safe
  (bnc#1012628).
- KVM: VMX: Make indirect call speculation safe (bnc#1012628).
- x86/alternative: Print unadorned pointers (bnc#1012628).
- auxdisplay: img-ascii-lcd: add missing
  MODULE_DESCRIPTION/AUTHOR/LICENSE (bnc#1012628).
- iio: adc/accel: Fix up module licenses (bnc#1012628).
- pinctrl: pxa: pxa2xx: add missing
  MODULE_DESCRIPTION/AUTHOR/LICENSE (bnc#1012628).
- ASoC: pcm512x: add missing MODULE_DESCRIPTION/AUTHOR/LICENSE
  (bnc#1012628).
- KVM: nVMX: Eliminate vmcs02 pool (bnc#1012628).
- KVM: VMX: introduce alloc_loaded_vmcs (bnc#1012628).
- objtool: Improve retpoline alternative handling (bnc#1012628).
- objtool: Add support for alternatives at the end of a section
  (bnc#1012628).
- objtool: Warn on stripped section symbol (bnc#1012628).
- x86/mm: Fix overlap of i386 CPU_ENTRY_AREA with FIX_BTMAP
  (bnc#1012628).
- x86/entry/64: Remove the SYSCALL64 fast path (bnc#1012628).
- x86/entry/64: Push extra regs right away (bnc#1012628).
- x86/asm: Move 'status' from thread_struct to thread_info
  (bnc#1012628).
- x86/spectre: Fix spelling mistake: "vunerable"-> "vulnerable"
  (bnc#1012628).
- x86/paravirt: Remove 'noreplace-paravirt' cmdline option
  (bnc#1012628).
- KVM: VMX: make MSR bitmaps per-VCPU (bnc#1012628).
- x86/kvm: Update spectre-v1 mitigation (bnc#1012628).
- x86/retpoline: Avoid retpolines for built-in __init functions
  (bnc#1012628).
- x86/speculation: Fix typo IBRS_ATT, which should be IBRS_ALL
  (bnc#1012628).
- KVM/x86: Update the reverse_cpuid list to include CPUID_7_EDX
  (bnc#1012628).
- KVM/x86: Add IBPB support (bnc#1012628).
- KVM/VMX: Emulate MSR_IA32_ARCH_CAPABILITIES (bnc#1012628).
- KVM/VMX: Allow direct access to MSR_IA32_SPEC_CTRL
  (bnc#1012628).
- KVM/SVM: Allow direct access to MSR_IA32_SPEC_CTRL
  (bnc#1012628).
- serial: core: mark port as initialized after successful IRQ
  change (bnc#1012628).
- fpga: region: release of_parse_phandle nodes after use
  (bnc#1012628).
- commit 54903ae
* Wed Feb  7 2018 msuchanek@suse.de
- rpm/kernel-binary.spec.in: install ksym-provides tool (bsc#1077692).
- commit 679f5c5
* Wed Feb  7 2018 msuchanek@suse.de
- rpm/kernel-binary.spec.in: require bison for build.
  linux-next tends to have outdated generated files so it needs bison to
  regenerate them.
- commit 4ad1ede
* Wed Feb  7 2018 msuchanek@suse.de
- Add ksym-provides tool (bsc#1077692).
- commit 9cd1e1e
* Mon Feb  5 2018 jslaby@suse.cz
- x86/pti: Mark constant arrays as __initconst (bsc#1068032
  CVE-2017-5753).
- x86/cpuid: Fix up "virtual" IBRS/IBPB/STIBP feature bits on
  Intel (bsc#1068032 CVE-2017-5753).
- commit 7d4f257
* Mon Feb  5 2018 jslaby@suse.cz
- x86/speculation: Add basic IBRS support infrastructure
  (bsc#1068032 CVE-2017-5753).
- x86/pti: Do not enable PTI on CPUs which are not vulnerable
  to Meltdown (bsc#1068032 CVE-2017-5753).
- x86/cpufeature: Blacklist SPEC_CTRL/PRED_CMD on early Spectre
  v2 microcodes (bsc#1068032 CVE-2017-5753).
- x86/nospec: Fix header guards names (bsc#1068032 CVE-2017-5753).
- x86/bugs: Drop one "mitigation" from dmesg (bsc#1068032
  CVE-2017-5753).
- x86/cpu/bugs: Make retpoline module warning conditional
  (bsc#1068032 CVE-2017-5753).
- x86/cpufeatures: Clean up Spectre v2 related CPUID flags
  (bsc#1068032 CVE-2017-5753).
- x86/retpoline: Simplify vmexit_fill_RSB() (bsc#1068032
  CVE-2017-5753).
- x86/speculation: Simplify indirect_branch_prediction_barrier()
  (bsc#1068032 CVE-2017-5753).
- module/retpoline: Warn about missing retpoline in module
  (bsc#1068032 CVE-2017-5753).
- x86/spectre: Check CONFIG_RETPOLINE in command line parser
  (bsc#1068032 CVE-2017-5753).
- x86/speculation: Use Indirect Branch Prediction Barrier in
  context switch (bsc#1068032 CVE-2017-5753).
- Refresh
  patches.suse/0001-x86-cpufeatures-Add-CPUID_7_EDX-CPUID-leaf.patch.
- Refresh
  patches.suse/0002-x86-cpufeatures-Add-Intel-feature-bits-for-Speculati.patch.
- Refresh
  patches.suse/0003-x86-cpufeatures-Add-AMD-feature-bits-for-Speculation.patch.
- Refresh
  patches.suse/0004-x86-msr-Add-definitions-for-new-speculation-control-.patch.
- Refresh
  patches.suse/0007-x86-speculation-Add-basic-IBPB-Indirect-Branch-Predi.patch.
- Refresh patches.suse/supported-flag.
- Delete
  patches.suse/0005-x86-pti-Do-not-enable-PTI-on-processors-which-are-no.patch.
- Delete
  patches.suse/0006-x86-cpufeature-Blacklist-SPEC_CTRL-on-early-Spectre-.patch.
- Delete patches.suse/0008-x86-kvm-Add-IBPB-support.patch.
- Delete
  patches.suse/0009-x86-speculation-Use-Indirect-Branch-Prediction-Barri.patch.
- Delete
  patches.suse/0010-x86-mm-Only-flush-indirect-branches-when-switching-i.patch.
- Delete
  patches.suse/0011-x86-speculation-Add-basic-IBRS-support-infrastructur.patch.
- Delete
  patches.suse/0017-x86-ibrs-Add-new-helper-macros-to-save-restore-MSR_I-fix.patch.
- Delete
  patches.suse/0017-x86-ibrs-Add-new-helper-macros-to-save-restore-MSR_I.patch.
- Delete
  patches.suse/0018-x86-vmx-Direct-access-to-MSR_IA32_SPEC_CTRL.patch.
  Update to the patches from 4.16-rc1 and the updated IBRS patches from
  the dwmw's repo.
- commit cd20d46
* Mon Feb  5 2018 jslaby@suse.cz
- Documentation: Document array_index_nospec (bsc#1068032
  CVE-2017-5715).
- array_index_nospec: Sanitize speculative array de-references
  (bsc#1068032 CVE-2017-5715).
- x86: Implement array_index_mask_nospec (bsc#1068032
  CVE-2017-5715).
- x86: Introduce barrier_nospec (bsc#1068032 CVE-2017-5715).
- x86: Introduce __uaccess_begin_nospec() and uaccess_try_nospec
  (bsc#1068032 CVE-2017-5715).
- x86/usercopy: Replace open coded stac/clac with
  __uaccess_{begin, end} (bsc#1068032 CVE-2017-5715).
- x86/syscall: Sanitize syscall table de-references under
  speculation (bsc#1068032 CVE-2017-5715).
- nl80211: Sanitize array index in parse_txq_params (bsc#1068032
  CVE-2017-5715).
- x86/spectre: Report get_user mitigation for spectre_v1
  (bsc#1068032 CVE-2017-5715).
- Delete patches.suse/0001-Documentation-document-array_ptr.patch.
- Delete
  patches.suse/0002-asm-nospec-array_ptr-sanitize-speculative-array-de-r.patch.
- Delete patches.suse/0003-x86-implement-array_ptr_mask.patch.
- Delete
  patches.suse/0004-x86-introduce-__uaccess_begin_nospec-and-ifence.patch.
- Delete
  patches.suse/0007-x86-narrow-out-of-bounds-syscalls-to-sys_read-under-.patch.
- Delete
  patches.suse/0009-kvm-x86-update-spectre-v1-mitigation.patch.
- Delete
  patches.suse/0010-nl80211-sanitize-array-index-in-parse_txq_params.patch.
  Replace by the patches from 4.16-rc1.
- commit 8343cab
* Mon Feb  5 2018 jslaby@suse.cz
- scsi: aacraid: remove redundant setting of variable c
  (git-fixes).
- commit 143e25c
* Sun Feb  4 2018 jslaby@suse.cz
- Linux 4.15.1 (bnc#1012628).
- x86/efi: Clarify that reset attack mitigation needs appropriate
  userspace (bnc#1012628).
- Input: synaptics-rmi4 - do not delete interrupt memory too early
  (bnc#1012628).
- Input: synaptics-rmi4 - unmask F03 interrupts when port is
  opened (bnc#1012628).
- test_firmware: fix missing unlock on error in
  config_num_requests_store() (bnc#1012628).
- iio: chemical: ccs811: Fix output of IIO_CONCENTRATION channels
  (bnc#1012628).
- iio: adc: stm32: fix scan of multiple channels with DMA
  (bnc#1012628).
- spi: imx: do not access registers while clocks disabled
  (bnc#1012628).
- serial: imx: Only wakeup via RTSDEN bit if the system has
  RTS/CTS (bnc#1012628).
- serial: 8250_dw: Revert "Improve clock rate setting"
  (bnc#1012628).
- serial: 8250_uniphier: fix error return code in
  uniphier_uart_probe() (bnc#1012628).
- serial: 8250_of: fix return code when probe function fails to
  get reset (bnc#1012628).
- mei: me: allow runtime pm for platform with D0i3 (bnc#1012628).
- android: binder: use VM_ALLOC to get vm area (bnc#1012628).
- ANDROID: binder: remove waitqueue when thread exits
  (bnc#1012628).
- usb/gadget: Fix "high bandwidth" check in
  usb_gadget_ep_match_desc() (bnc#1012628).
- usb: uas: unconditionally bring back host after reset
  (bnc#1012628).
- usb: f_fs: Prevent gadget unbind if it is already unbound
  (bnc#1012628).
- USB: serial: simple: add Motorola Tetra driver (bnc#1012628).
- usbip: list: don't list devices attached to vhci_hcd
  (bnc#1012628).
- usbip: prevent bind loops on devices attached to vhci_hcd
  (bnc#1012628).
- USB: serial: io_edgeport: fix possible sleep-in-atomic
  (bnc#1012628).
- CDC-ACM: apply quirk for card reader (bnc#1012628).
- USB: cdc-acm: Do not log urb submission errors on disconnect
  (bnc#1012628).
- USB: serial: pl2303: new device id for Chilitag (bnc#1012628).
- usb: option: Add support for FS040U modem (bnc#1012628).
- tty: fix data race between tty_init_dev and flush of buf
  (bnc#1012628).
- staging: ccree: fix fips event irq handling build (bnc#1012628).
- staging: ccree: NULLify backup_info when unused (bnc#1012628).
- staging: lustre: separate a connection destroy from free struct
  kib_conn (bnc#1012628).
- scsi: storvsc: missing error code in storvsc_probe()
  (bnc#1012628).
- scsi: aacraid: Fix hang in kdump (bnc#1012628).
- scsi: aacraid: Fix udev inquiry race condition (bnc#1012628).
- ima/policy: fix parsing of fsuuid (bnc#1012628).
- igb: Free IRQs when device is hotplugged (bnc#1012628).
- mtd: nand: denali_pci: add missing
  MODULE_DESCRIPTION/AUTHOR/LICENSE (bnc#1012628).
- gpio: ath79: add missing MODULE_DESCRIPTION/LICENSE
  (bnc#1012628).
- gpio: iop: add missing MODULE_DESCRIPTION/AUTHOR/LICENSE
  (bnc#1012628).
- power: reset: zx-reboot: add missing
  MODULE_DESCRIPTION/AUTHOR/LICENSE (bnc#1012628).
- HID: wacom: Fix reporting of touch toggle
  (WACOM_HID_WD_MUTE_DEVICE) events (bnc#1012628).
- HID: wacom: EKR: ensure devres groups at higher indexes are
  released (bnc#1012628).
- crypto: af_alg - whitelist mask and type (bnc#1012628).
- crypto: sha3-generic - fixes for alignment and big endian
  operation (bnc#1012628).
- crypto: inside-secure - avoid unmapping DMA memory that was
  not mapped (bnc#1012628).
- crypto: inside-secure - fix hash when length is a multiple of
  a block (bnc#1012628).
- crypto: aesni - Fix out-of-bounds access of the AAD buffer in
  generic-gcm-aesni (bnc#1012628).
- crypto: aesni - Fix out-of-bounds access of the data buffer
  in generic-gcm-aesni (bnc#1012628).
- crypto: aesni - add wrapper for generic gcm(aes) (bnc#1012628).
- crypto: aesni - fix typo in generic_gcmaes_decrypt
  (bnc#1012628).
- crypto: aesni - handle zero length dst buffer (bnc#1012628).
- crypto: ecdh - fix typo in KPP dependency of CRYPTO_ECDH
  (bnc#1012628).
- ALSA: hda - Reduce the suspend time consumption for ALC256
  (bnc#1012628).
- gpio: Fix kernel stack leak to userspace (bnc#1012628).
- gpio: stmpe: i2c transfer are forbiden in atomic context
  (bnc#1012628).
- tools/gpio: Fix build error with musl libc (bnc#1012628).
- Bluetooth: hci_serdev: Init hci_uart proto_lock to avoid oops
  (bnc#1012628).
- commit 671bf29
* Thu Feb  1 2018 matwey.kornilov@gmail.com
- config: arm64: Enable RockChip 8xx
  We need RockChip RK-808 support to run openSUSE on Rock64 board (RK3328).
  Currently, even voltage regulator is missed.
- commit a348749
* Mon Jan 29 2018 jeffm@suse.com
- Update to 4.15-final.
- Eliminated 5 patches.
- commit 36830f7
* Mon Jan 29 2018 jeffm@suse.com
- btrfs: fix btrfs_evict_inode to handle abnormal inodes correctly (bsc#1078019).
- commit d3f1d2c
* Fri Jan 26 2018 yousaf.kaukab@suse.com
- config: arm64: enable UNMAP_KERNEL_AT_EL0 and HARDEN_BRANCH_PREDICTOR
- commit c41900c
* Fri Jan 26 2018 yousaf.kaukab@suse.com
- arm64: Turn on KPTI only on CPUs that need it (bsc#1068032).
- arm64: Branch predictor hardening for Cavium ThunderX2
  (bsc#1068032).
- arm64: Run enable method for errata work arounds on late CPUs
  (bsc#1068032).
- arm64: Move BP hardening to check_and_switch_context
  (bsc#1068032).
- arm: KVM: Invalidate icache on guest exit for Cortex-A15
  (bsc#1068032).
- arm: Invalidate icache on prefetch abort outside of user
  mapping on Cortex-A15 (bsc#1068032).
- arm: Add icache invalidation on switch_mm for Cortex-A15
  (bsc#1068032).
- arm: KVM: Invalidate BTB on guest exit (bsc#1068032).
- arm: Invalidate BTB on prefetch abort outside of user mapping
  on Cortex A8, A9, A12 and A17 (bsc#1068032).
- arm: Add BTB invalidation on switch_mm for Cortex-A9, A12 and
  A17 (bsc#1068032).
- arm64: cputype: Add MIDR values for Cavium ThunderX2 CPUs
  (bsc#1068032).
- arm64: Implement branch predictor hardening for Falkor
  (bsc#1068032).
- arm64: Implement branch predictor hardening for affected
  Cortex-A CPUs (bsc#1068032).
- arm64: cputype: Add missing MIDR values for Cortex-A72 and
  Cortex-A75 (bsc#1068032).
- arm64: KVM: Make PSCI_VERSION a fast path (bsc#1068032).
- arm64: KVM: Use per-CPU vector when BP hardening is enabled
  (bsc#1068032).
- arm64: Add skeleton to harden the branch predictor against
  aliasing attacks (bsc#1068032).
- arm64: Move post_ttbr_update_workaround to C code (bsc#1068032).
- drivers/firmware: Expose psci_get_version through psci_ops
  structure (bsc#1068032).
- arm64: Take into account ID_AA64PFR0_EL1.CSV3 (bsc#1068032).
- arm64: Kconfig: Reword UNMAP_KERNEL_AT_EL0 kconfig entry
  (bsc#1068032).
- arm64: use RET instruction for exiting the trampoline
  (bsc#1068032).
- arm64: capabilities: Handle duplicate entries for a capability
  (bsc#1068032).
- arm64: cpufeature: Pass capability structure to ->enable
  callback (bsc#1068032).
- arm64: kpti: Fix the interaction between ASID switching and
  software PAN (bsc#1068032).
- arm64: kaslr: Put kernel vectors address in separate data page
  (bsc#1068032).
- arm64: mm: Introduce TTBR_ASID_MASK for getting at the ASID
  in the TTBR (bsc#1068032).
- perf: arm_spe: Fail device probe when
  arm64_kernel_unmapped_at_el0() (bsc#1068032).
- arm64: Kconfig: Add CONFIG_UNMAP_KERNEL_AT_EL0 (bsc#1068032).
- arm64: entry: Add fake CPU feature for unmapping the kernel
  at EL0 (bsc#1068032).
- arm64: tls: Avoid unconditional zeroing of tpidrro_el0 for
  native tasks (bsc#1068032).
- arm64: erratum: Work around Falkor erratum #E1003 in trampoline
  code (bsc#1068032).
- arm64: entry: Hook up entry trampoline to exception vectors
  (bsc#1068032).
- arm64: entry: Explicitly pass exception level to kernel_ventry
  macro (bsc#1068032).
- arm64: mm: Map entry trampoline into trampoline and kernel
  page tables (bsc#1068032).
- arm64: entry: Add exception trampoline page for exceptions
  from EL0 (bsc#1068032).
- arm64: mm: Invalidate both kernel and user ASIDs when performing
  TLBI (bsc#1068032).
- arm64: mm: Add arm64_kernel_unmapped_at_el0 helper
  (bsc#1068032).
- arm64: mm: Allocate ASIDs in pairs (bsc#1068032).
- arm64: mm: Fix and re-enable ARM64_SW_TTBR0_PAN (bsc#1068032).
- arm64: mm: Rename post_ttbr0_update_workaround (bsc#1068032).
- arm64: mm: Remove pre_ttbr0_update_workaround for Falkor
  erratum #E1003 (bsc#1068032).
- arm64: mm: Move ASID from TTBR0 to TTBR1 (bsc#1068032).
- arm64: mm: Temporarily disable ARM64_SW_TTBR0_PAN (bsc#1068032).
- arm64: mm: Use non-global mappings for kernel space
  (bsc#1068032).
- commit cdf2ded
* Fri Jan 26 2018 yousaf.kaukab@suse.com
- config: arm64: enable rk3399 missing drivers
  These drivers are required for Rockchip RK3399 Sapphire board
- commit 94b8551
* Fri Jan 26 2018 jslaby@suse.cz
- x86/ibrs: Add new helper macros to save/restore
  MSR_IA32_SPEC_CTRL fix (bsc#1068032 CVE-2017-5753).
- commit 13295d4
* Thu Jan 25 2018 jslaby@suse.cz
- x86/cpufeature: Move processor tracing out of scattered features
  (bsc#1068032 CVE-2017-5753).
- Refresh
  patches.suse/0001-x86-cpufeatures-Add-CPUID_7_EDX-CPUID-leaf.patch.
- Refresh
  patches.suse/0007-x86-speculation-Add-basic-IBPB-Indirect-Branch-Predi.patch.
- commit 8d8b718
* Wed Jan 24 2018 jslaby@suse.cz
- x86/retpoline: Add LFENCE to the retpoline/RSB filling RSB
  macros (bsc#1068032 CVE-2017-5753).
- commit 8dc7c71
* Wed Jan 24 2018 jslaby@suse.cz
- x86/vmx: Direct access to MSR_IA32_SPEC_CTRL (bsc#1068032
  CVE-2017-5753).
- x86/ibrs: Add new helper macros to save/restore
  MSR_IA32_SPEC_CTRL (bsc#1068032 CVE-2017-5753).
- x86/enter: Use IBRS on syscall and interrupts (bsc#1068032
  CVE-2017-5753).
- x86/enter: Create macros to restrict/unrestrict Indirect Branch
  Speculation (bsc#1068032 CVE-2017-5753).
- x86/idle: Control Indirect Branch Speculation in idle
  (bsc#1068032 CVE-2017-5753).
- x86: Simplify spectre_v2 command line parsing (bsc#1068032
  CVE-2017-5753).
- x86/speculation: Add inlines to control Indirect Branch
  Speculation (bsc#1068032 CVE-2017-5753).
- x86/speculation: Add basic IBRS support infrastructure
  (bsc#1068032 CVE-2017-5753).
- x86/mm: Only flush indirect branches when switching into non
  dumpable process (bsc#1068032 CVE-2017-5753).
- x86/speculation: Use Indirect Branch Prediction Barrier in
  context switch (bsc#1068032 CVE-2017-5753).
- x86/kvm: Add IBPB support (bsc#1068032 CVE-2017-5753).
- x86/speculation: Add basic IBPB (Indirect Branch Prediction
  Barrier) support (bsc#1068032 CVE-2017-5753).
- x86/cpufeature: Blacklist SPEC_CTRL on early Spectre v2
  microcodes (bsc#1068032 CVE-2017-5753).
- x86/pti: Do not enable PTI on processors which are not
  vulnerable to Meltdown (bsc#1068032 CVE-2017-5753).
- x86/msr: Add definitions for new speculation control MSRs
  (bsc#1068032 CVE-2017-5753).
- x86/cpufeatures: Add AMD feature bits for Speculation Control
  (bsc#1068032 CVE-2017-5753).
- x86/cpufeatures: Add Intel feature bits for Speculation Control
  (bsc#1068032 CVE-2017-5753).
- x86/cpufeatures: Add CPUID_7_EDX CPUID leaf (bsc#1068032
  CVE-2017-5753).
- x86/retpoline: Optimize inline assembler for vmexit_fill_RSB
  (bsc#1068032 CVE-2017-5753).
- x86/retpoline: Fill RSB on context switch for affected CPUs
  (bsc#1068032 CVE-2017-5753).
- commit e36ab4f
* Wed Jan 24 2018 jslaby@suse.cz
- Documentation: document array_ptr (bsc#1068032 CVE-2017-5715).
- asm/nospec, array_ptr: sanitize speculative array de-references
  (bsc#1068032 CVE-2017-5715).
- x86: implement array_ptr_mask() (bsc#1068032 CVE-2017-5715).
- x86: introduce __uaccess_begin_nospec and ifence (bsc#1068032
  CVE-2017-5715).
- x86, __get_user: use __uaccess_begin_nospec (bsc#1068032
  CVE-2017-5715).
- x86, get_user: use pointer masking to limit speculation
  (bsc#1068032 CVE-2017-5715).
- x86: narrow out of bounds syscalls to sys_read under speculation
  (bsc#1068032 CVE-2017-5715).
- vfs, fdtable: prevent bounds-check bypass via speculative
  execution (bsc#1068032 CVE-2017-5715).
- kvm, x86: update spectre-v1 mitigation (bsc#1068032
  CVE-2017-5715).
- nl80211: sanitize array index in parse_txq_params (bsc#1068032
  CVE-2017-5715).
- Delete
  patches.suse/0003-locking-barriers-introduce-new-observable-speculatio.patch.
- Delete
  patches.suse/0004-bpf-prevent-speculative-execution-in-eBPF-interprete.patch.
- Delete
  patches.suse/0005-x86-bpf-jit-prevent-speculative-execution-when-JIT-i.patch.
- Delete
  patches.suse/0006-uvcvideo-prevent-speculative-execution.patch.
- Delete
  patches.suse/0007-carl9170-prevent-speculative-execution.patch.
- Delete
  patches.suse/0008-p54-prevent-speculative-execution.patch.
- Delete
  patches.suse/0009-qla2xxx-prevent-speculative-execution.patch.
- Delete
  patches.suse/0010-cw1200-prevent-speculative-execution.patch.
- Delete
  patches.suse/0011-Thermal-int340x-prevent-speculative-execution.patch.
- Delete
  patches.suse/0012-ipv4-prevent-speculative-execution.patch.
- Delete
  patches.suse/0013-ipv6-prevent-speculative-execution.patch.
- Delete patches.suse/0014-fs-prevent-speculative-execution.patch.
- Delete
  patches.suse/0015-net-mpls-prevent-speculative-execution.patch.
- Delete
  patches.suse/0016-udf-prevent-speculative-execution.patch.
- Delete
  patches.suse/0017-userns-prevent-speculative-execution.patch.
  Replace by the potential upstream solution.
- commit 804f8a1
* Mon Jan 22 2018 msuchanek@suse.de
- rpm/mkspec-dtb: Remove COPYING file (bsc#1076905).
  It conflicts between different versions of dtb package.
- commit 0e5fcf9
* Thu Jan 18 2018 jslaby@suse.cz
- Update config files (bsc#1068032 CVE-2017-5715).
  Enable RETPOLINE -- the compiler is capable of them already.
- commit 5d5345e
* Wed Jan 17 2018 rjschwei@suse.com
- kernel-obs-build.spec.in: enable xfs module
  This allows the public cloud team to build images with XFS
  as root filesystem
- commit 95a2d6f
* Wed Jan 17 2018 msuchanek@suse.de
- macros.kernel-source: pass -f properly in module subpackage (boo#1076393).
- commit 66bd9b8
* Mon Jan 15 2018 jeffm@suse.com
- Update to 4.15-rc8.
- Eliminated 3 patches.
- Config changes:
  - Security:
  - BPF_JIT_ALWAYS_ON=y
  - RETPOLINE=n (depends on gcc with -mindirect-branch=thunk-extern)
- commit 05e4405
* Fri Jan 12 2018 jslaby@suse.cz
- bpf, array: fix overflow in max_entries and undefined behavior
  in index_mask (bsc#1068032 CVE-2017-5753).
- commit 5fdfc1a
* Fri Jan 12 2018 jslaby@suse.cz
- bpf: prevent out-of-bounds speculation (bsc#1068032
  CVE-2017-5753).
- commit 0eca303
* Thu Jan 11 2018 matwey.kornilov@gmail.com
- config: arm64: Enable Aardvark PCIe controller
  Aardvark PCIe controller is a part of Marvel Armada 3700 SoC.
  This option is required to support PCIe for JeOS-espressobin.
- commit b0bb655
* Thu Jan 11 2018 lpechacek@suse.com
- rpm/kernel-binary.spec.in: more specific kGraft Provides: (fate#323682)
  Follow openSUSE packaging practices described at
  https://en.opensuse.org/openSUSE:Package_dependencies#Renaming_a_package.
- commit 050081b
* Wed Jan 10 2018 jslaby@suse.cz
- x86/cpu/AMD: Make LFENCE a serializing instruction (bsc#1068032
  CVE-2017-5754).
- x86/cpu/AMD: Use LFENCE_RDTSC in preference to MFENCE_RDTSC
  (bsc#1068032 CVE-2017-5754).
- Delete
  patches.suse/0001-x86-cpu-AMD-Make-the-LFENCE-instruction-serialized.patch.
- Delete
  patches.suse/0002-x86-cpu-AMD-Remove-now-unused-definition-of-MFENCE_R.patch.
  Use the variants from upstream (tip tree).
- commit 33b16eb
* Mon Jan  8 2018 msuchanek@suse.de
- kernel-obs-build.spec.in: add --no-hostonly-cmdline to dracut invocation (boo#1062303).
  call dracut with --no-hostonly-cmdline to avoid the random rootfs UUID
  being added into the initrd's /etc/cmdline.d/95root-dev.conf
- commit da5186f
* Mon Jan  8 2018 jeffm@suse.com
- Update to 4.15-rc7.
- Eliminated 1 patch.
- commit b07c570
* Sat Jan  6 2018 jslaby@suse.cz
- rpm/constraints.in: lower kernel-syzkaller's mem requirements
  OBS now reports that it needs only around 2G, so lower the limit to
  8G, so that more compliant workers can be used.
- commit a73399a
* Wed Jan  3 2018 jeffm@suse.com
- config: x86, PAGE_TABLE_ISOLATION=y (bsc#1068032).
- commit 4343d87
* Tue Jan  2 2018 jslaby@suse.cz
- userns: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- udf: prevent speculative execution (bnc#1068032 CVE-2017-5753).
- net: mpls: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- fs: prevent speculative execution (bnc#1068032 CVE-2017-5753).
- ipv6: prevent speculative execution (bnc#1068032 CVE-2017-5753).
- ipv4: prevent speculative execution (bnc#1068032 CVE-2017-5753).
- Thermal/int340x: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- cw1200: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- qla2xxx: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- p54: prevent speculative execution (bnc#1068032 CVE-2017-5753).
- carl9170: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- uvcvideo: prevent speculative execution (bnc#1068032
  CVE-2017-5753).
- x86, bpf, jit: prevent speculative execution when JIT is enabled
  (bnc#1068032 CVE-2017-5753).
- bpf: prevent speculative execution in eBPF interpreter
  (bnc#1068032 CVE-2017-5753).
- locking/barriers: introduce new observable speculation barrier
  (bnc#1068032 CVE-2017-5753).
- x86/cpu/AMD: Remove now unused definition of MFENCE_RDTSC
  feature (bnc#1068032 CVE-2017-5753).
- x86/cpu/AMD: Make the LFENCE instruction serialized (bnc#1068032
  CVE-2017-5753).
- commit ee4aa62
* Tue Jan  2 2018 jeffm@suse.com
- Update to 4.15-rc6.
- Config changes:
  - x86: PAGE_TABLE_ISOLATION=n (default, performance)
- commit cd70bd8
* Mon Dec 25 2017 jeffm@suse.com
- config: disable BUG_ON_DATA_CORRUPTION
  On its face this option makes sense but it brings along with it
  DEBUG_LIST, which is very expensive and obvious on benchmarks.
- commit 9fcc9f1
* Mon Dec 25 2017 jeffm@suse.com
- config: refresh i386/default
  Commit 4735d41aeeb added a disabled CONFIG_SPI_INTEL_SPI_PLATFORM option
  that doesn't exist on i386/default (at least in 4.15-rc5).
- commit 84167ae
* Sun Dec 24 2017 jeffm@suse.com
- Update to 4.15-rc5.
- Config changes:
  - i386: NR_CPUS 128->64
  - 7bbcbd3d1cd (x86/Kconfig: Limit NR_CPUS on 32-bit to a sane amount)
- commit 9e8deb3
* Thu Dec 21 2017 msuchanek@suse.de
- kernel-obs-build: use pae and lpae kernels where available
  (bsc#1073579).
- commit 1ac1946
* Thu Dec 21 2017 tiwai@suse.de
- Disable CONFIG_SPI_INTEL_SPI_PCI as well (bsc#1073836)
- commit ddb33b2
* Thu Dec 21 2017 tiwai@suse.de
- Disable CONFIG_SPI_INTEL_SPI_PLATFORM for BIOS breakge on Lenovo laptops
  (bsc#1073836)
- commit 4735d41
* Tue Dec 19 2017 jeffm@suse.com
- Update to 4.15-rc4.
- Eliminated 1 patch.
- Config changes:
  - ARM:
  - QCOM_FALKOR_ERRATUM_E1041=y
  - Overlayfs:
  - OVERLAY_FS_REDIRECT_ALWAYS_FOLLOW=y (preserves existing behavior)
- commit ff8819c
* Fri Dec 15 2017 jslaby@suse.cz
- x86/stacktrace: make clear the success paths (bnc#1058115).
- Refresh
  patches.suse/0003-x86-stacktrace-remove-STACKTRACE_DUMP_ONCE-from-__sa.patch.
- Refresh
  patches.suse/0004-x86-stacktrace-do-not-fail-for-ORC-with-regs-on-stac.patch.
- Delete
  patches.suse/0002-x86-stacktrace-remove-unwind_state-error.patch.
  Fix livepatch to succeed also for kthreads and idle tasks.
- commit 5292470
* Wed Dec 13 2017 msuchanek@suse.de
- s390/sclp: disable FORTIFY_SOURCE for early sclp code (-).
- commit 62412b6
* Mon Dec 11 2017 jeffm@suse.com
- Update to 4.15-rc3.
- Eliminated 1 patch.
- commit 383d72f
* Sat Dec  9 2017 afaerber@suse.de
- config: armv7hl: Enable SUN4I_A10_CCU for Allwinner A20 (boo#1072032)
- commit 170d177
* Fri Dec  8 2017 msuchanek@suse.de
- Add undefine _unique_build_ids (bsc#964063)
- commit 47e91a1
* Tue Dec  5 2017 jslaby@suse.cz
- x86/stacktrace: do now unwind after user regs (bnc#1058115).
- x86/stacktrace: remove unwind_state->error (bnc#1058115).
- x86/stacktrace: remove STACKTRACE_DUMP_ONCE from
  __save_stack_trace_reliable (bnc#1058115).
- x86/stacktrace: do not fail for ORC with regs on stack
  (bnc#1058115).
  More make-ORC-reliable patches.
- commit ef715eb
* Mon Dec  4 2017 jeffm@suse.com
- Update to 4.15-rc2.
- Eliminated 2 patches.
- commit 68549b6
* Thu Nov 30 2017 jslaby@suse.cz
- Refresh
  patches.suse/apparmor-fix-oops-in-audit_signal_cb-hook.patch.
  Update upstream status.
- commit ee861fd
* Thu Nov 30 2017 jslaby@suse.cz
- mmc: sdhci: Avoid swiotlb buffer being full (bnc#1068877).
- commit 2659efd
* Wed Nov 29 2017 msuchanek@suse.de
- rpm/kernel-binary.spec.in: fix incorrectly moved comment
  While moving # END COMMON DEPS moved following comment with it.
- commit 858b7e7
* Tue Nov 28 2017 afaerber@suse.de
- config: armv7hl: Update to 4.15-rc1
- commit b4c7f19
* Tue Nov 28 2017 afaerber@suse.de
- config: armv6hl: Update to 4.15-rc1
- commit edcdf48
* Tue Nov 28 2017 afaerber@suse.de
- config: arm64: Update to 4.15-rc1
- commit 3278861
* Mon Nov 27 2017 jeffm@suse.com
- Update to 4.15-rc1.
- Eliminated 74 patches.
- ARM configs need updating.
- Config changes:
  - General:
  - CPU_ISOLATION=y
  - GUP_BENCHMARK=n
  - x86:
  - X86_INTEL_UMIP=y
  - PINCTRL_CEDARFORK=m
  - INTEL_SOC_PMIC_CHTDC_TI=m
  - INTEL_WMI_THUNDERBOLT=m
  - DELL_SMBIOS_WMI=m
  - DELL_SMBIOS_SMM=m
  - CHT_DC_TI_PMIC_OPREGION=y
  - RPMSG_CHAR=m
  - i386:
  - IR_SPI=m
  - IR_GPIO_CIR=m
  - IR_GPIO_TX=m
  - IR_PWM_TX=m
  - powerpc:
  - PPC_RADIX_MMU_DEFAULT=y (default)
  - MEM_SOFT_DIRTY=n (needs arch expert review)
  - PINCTRL=n
  - PPC_FAST_ENDIAN_SWITCH=n (default)
  - s390:
  - GCC_PLUGINS=n
  - MEM_SOFT_DIRTY=(needs arch expert review)
  - PINCTRL=n
  - FORTIFY_SOURCE=y
  - s390/zfcpdump:
  - BPF_STREAM_PARSER=n
  - MTD=n
  - Network:
  - NET_SCH_CBS=m
  - VSOCKETS_DIAG=m
  - DP83822_PHY=m
  - RENESAS_PHY=m
  - THUNDERBOLT_NET=m
  - Input:
  - TOUCHSCREEN_EXC3000=m
  - TOUCHSCREEN_HIDEEP=m
  - TOUCHSCREEN_S6SY761=m
  - DRM_I2C_ADV7511_CEC=y
  - Misc:
  - IPMI_PROC_INTERFACE=y
  - GPIO_MAX3191X=m
  - MANAGER_SBS=m
  - W1_SLAVE_DS28E17=m
  - SENSORS_MAX6621=m
  - SENSORS_MAX31785=m
  - CEC_GPIO=m
  - TYPEC_TPS6598X=m
  - RPMSG_VIRTIO=m
  - IIO_CROS_EC_ACCEL_LEGACY=m
  - RFD77402=m
  - NTB_SWITCHTEC=m
  - MMC_SDHCI_OMAP=m
  - Filesystems:
  - XFS_ONLINE_SCRUB=n (still experimental)
  - BTRFS_FS_REF_VERIFY=n
  - CRAMFS_BLOCKDEV=y
  - CRAMFS_MTD=y
  - INTEGRITY_TRUSTED_KEYRING=y
  - Crypto:
  - CRYPTO_SM3=m
  - SIGNED_PE_FILE_VERIFICATION=y
  - SYSTEM_TRUSTED_KEYS (empty)
  - SYSTEM_EXTRA_CERTIFICATE=n
  - SECONDARY_TRUSTED_KEYRING=n
  - LEDS:
  - LEDS_APU=m
  - LEDS_TRIGGER_ACTIVITY=m
  - RTC:
  - RTC_DRV_PCF85363=m
  - Xen:
  - XEN_PVCALLS_FRONTEND=n
  - Graphics:
  - DRM_AMD_DC=y
  - DRM_AMD_DC_PRE_VEGA=y
  - DRM_AMD_DC_FBC=y ?
  - DRM_AMD_DC_DCN1_0=y
  - DEBUG_KERNEL_DC=n
  - NOUVEAU_DEBUG_MMU=n
  - Storage:
  - NVME_MULTIPATH=y
  - IB:
  - MLX4_CORE_GEN2=y
  - Sound:
  - SND_SOC_INTEL_SST_TOPLEVEL=m
  - SND_SOC_INTEL_BAYTRAIL=m
  - Testing:
  - KCOV_ENABLE_COMPARISONS=y (syzkaller)
  - BOOTPARAM_LOCKDEP_CROSSRELEASE_FULLSTACK=n
  - PREEMPTIRQ_EVENTS=y
  - TEST_FIND_BIT=n
  - PKCS7_TEST_KEY=n
  - CHASH_SELFTEST=n
  - CHASH_STATS=n
- commit bc47c49
* Sun Nov 26 2017 afaerber@suse.de
- config: armv6hl: Enable 8250 irq sharing for RPi Zero W (boo#1069828)
- commit 01942c4
* Sat Nov 25 2017 afaerber@suse.de
- config: armv6hl: Enable brcmfmac for RPi Zero W (boo#1069830)
- commit 56423d9
* Sat Nov 25 2017 afaerber@suse.de
- config: armv6hl: Enable 8250 serial console for RPi Zero W (boo#1069828)
- commit 3a3001a
* Fri Nov 24 2017 bp@suse.de
- dvb_frontend: don't use-after-free the frontend struct
  (bsc#1067087 CVE-2017-16648).
- media: dvb-core: always call invoke_release() in fe_free()
  (bsc#1067087).
- commit 2a04ad0
* Fri Nov 24 2017 tiwai@suse.de
- rpm/kernel-binary.spec.in: Correct supplements for recent SLE products (bsc#1067494)
- commit 8f05b9f
* Fri Nov 24 2017 jbeulich@suse.com
- supported:conf: Remove stale Xen driver entries.
- commit c46464b
* Fri Nov 24 2017 jslaby@suse.cz
- ipmi_si: fix memory leak on new_smi (git-fixes).
- commit 4ca3b35
* Fri Nov 24 2017 jslaby@suse.cz
- Linux 4.14.2 (bnc#1012628).
- af_netlink: ensure that NLMSG_DONE never fails in dumps
  (bnc#1012628).
- vxlan: fix the issue that neigh proxy blocks all icmpv6 packets
  (bnc#1012628).
- net: cdc_ncm: GetNtbFormat endian fix (bnc#1012628).
- fealnx: Fix building error on MIPS (bnc#1012628).
- net/sctp: Always set scope_id in sctp_inet6_skb_msgname
  (bnc#1012628).
- ima: do not update security.ima if appraisal status is not
  INTEGRITY_PASS (bnc#1012628).
- serial: omap: Fix EFR write on RTS deassertion (bnc#1012628).
- serial: 8250_fintek: Fix finding base_port with activated
  SuperIO (bnc#1012628).
- tpm-dev-common: Reject too short writes (bnc#1012628).
- rcu: Fix up pending cbs check in rcu_prepare_for_idle
  (bnc#1012628).
- mm/pagewalk.c: report holes in hugetlb ranges (bnc#1012628).
- ocfs2: fix cluster hang after a node dies (bnc#1012628).
- ocfs2: should wait dio before inode lock in ocfs2_setattr()
  (bnc#1012628).
- ipmi: fix unsigned long underflow (bnc#1012628).
- mm/page_alloc.c: broken deferred calculation (bnc#1012628).
- mm/page_ext.c: check if page_ext is not prepared (bnc#1012628).
- coda: fix 'kernel memory exposure attempt' in fsync
  (bnc#1012628).
- ipmi: Prefer ACPI system interfaces over SMBIOS ones
  (bnc#1012628).
- commit 295c90a
* Thu Nov 23 2017 jslaby@suse.cz
- apparmor: fix oops in audit_signal_cb hook (bnc#1069562).
- Refresh patches.suse/0001-AppArmor-basic-networking-rules.patch.
- commit d091ad8
* Thu Nov 23 2017 jslaby@suse.cz
- bio: ensure __bio_clone_fast copies bi_partno (bnc#1069605).
- commit 59c6ade
* Tue Nov 21 2017 jslaby@suse.cz
- Update config files.
  After renaming the UNWINDER config options, vanilla has the old names
  and they need to be in configs. For example, x86_64 default config
  has CONFIG_UNWINDER_ORC=y, vanilla has CONFIG_ORC_UNWINDER=y.
- commit d0dab46
* Tue Nov 21 2017 jslaby@suse.cz
- objtool: Print top level commands on incorrect usage
  (bnc#1058115).
- commit 6603336
* Tue Nov 21 2017 jslaby@suse.cz
- x86/unwind: Make CONFIG_UNWINDER_ORC=y the default in kconfig
  for 64-bit (bnc#1058115).
- Update config files.
- x86/unwind: Rename unwinder config options to
  'CONFIG_UNWINDER_*' (bnc#1058115).
- Refresh patches.suse/0001-orc-mark-it-as-reliable.patch.
- Update config files.
- x86/unwinder: Make CONFIG_UNWINDER_ORC=y the default in the
  64-bit defconfig (bnc#1058115).
- commit c81ce89
* Tue Nov 21 2017 jslaby@suse.cz
- x86/stacktrace: Avoid recording save_stack_trace() wrappers
  (bnc#1058115).
- commit fa72e96
* Tue Nov 21 2017 jslaby@suse.cz
- Refresh
  patches.suse/0001-objtool-Don-t-report-end-of-section-error-after-an-e.patch.
- Refresh
  patches.suse/0002-x86-head-Remove-confusing-comment.patch.
- Refresh
  patches.suse/0003-x86-head-Remove-unused-bad_address-code.patch.
- Refresh
  patches.suse/0004-x86-head-Fix-head-ELF-function-annotations.patch.
- Refresh
  patches.suse/0005-x86-boot-Annotate-verify_cpu-as-a-callable-function.patch.
- Refresh
  patches.suse/0006-x86-xen-Fix-xen-head-ELF-annotations.patch.
- Refresh
  patches.suse/0007-x86-xen-Add-unwind-hint-annotations.patch.
- Refresh
  patches.suse/0008-x86-head-Add-unwind-hint-annotations.patch.
  Update upstream status.
- commit f655f80
* Tue Nov 21 2017 jslaby@suse.cz
- move all patches to patches.suse/
- commit 6fafae6
* Tue Nov 21 2017 jslaby@suse.cz
- Linux 4.14.1 (bnc#1012628).
- EDAC, sb_edac: Don't create a second memory controller if HA1
  is not present (bnc#1012628).
- dmaengine: dmatest: warn user when dma test times out
  (bnc#1012628).
- crypto: dh - Fix double free of ctx->p (bnc#1012628).
- crypto: dh - Don't permit 'p' to be 0 (bnc#1012628).
- crypto: dh - Don't permit 'key' or 'g' size longer than 'p'
  (bnc#1012628).
- crypto: brcm - Explicity ACK mailbox message (bnc#1012628).
- USB: early: Use new USB product ID and strings for DbC device
  (bnc#1012628).
- USB: usbfs: compute urb->actual_length for isochronous
  (bnc#1012628).
- USB: Add delay-init quirk for Corsair K70 LUX keyboards
  (bnc#1012628).
- usb: gadget: f_fs: Fix use-after-free in ffs_free_inst
  (bnc#1012628).
- USB: serial: metro-usb: stop I/O after failed open
  (bnc#1012628).
- USB: serial: Change DbC debug device binding ID (bnc#1012628).
- USB: serial: qcserial: add pid/vid for Sierra Wireless EM7355
  fw update (bnc#1012628).
- USB: serial: garmin_gps: fix I/O after failed probe and remove
  (bnc#1012628).
- USB: serial: garmin_gps: fix memory leak on probe errors
  (bnc#1012628).
- selftests/x86/protection_keys: Fix syscall NR redefinition
  warnings (bnc#1012628).
- x86/MCE/AMD: Always give panic severity for UC errors in kernel
  context (bnc#1012628).
- platform/x86: peaq-wmi: Add DMI check before binding to the
  WMI interface (bnc#1012628 bsc#1059807).
- platform/x86: peaq_wmi: Fix missing terminating entry for
  peaq_dmi_table (bnc#1012628).
- HID: cp2112: add HIDRAW dependency (bnc#1012628).
- HID: wacom: generic: Recognize WACOM_HID_WD_PEN as a type of
  pen collection (bnc#1012628).
- rpmsg: glink: Add missing MODULE_LICENSE (bnc#1012628).
- staging: wilc1000: Fix bssid buffer offset in Txq (bnc#1012628).
- staging: sm750fb: Fix parameter mistake in poke32 (bnc#1012628).
- staging: ccree: fix 64 bit scatter/gather DMA ops (bnc#1012628).
- staging: greybus: spilib: fix use-after-free after
  deregistration (bnc#1012628).
- staging: vboxvideo: Fix reporting invalid
  suggested-offset-properties (bnc#1012628).
- staging: rtl8188eu: Revert 4 commits breaking ARP (bnc#1012628).
- spi: fix use-after-free at controller deregistration
  (bnc#1012628).
- sparc32: Add cmpxchg64() (bnc#1012628).
- sparc64: mmu_context: Add missing include files (bnc#1012628).
- sparc64: Fix page table walk for PUD hugepages (bnc#1012628).
- commit b1ba0c0
* Wed Nov 15 2017 rgoldwyn@suse.com
- apparmor: Fix quieting of audit messages for network mediation
  (FATE#300516, boo#1065536).
- apparmor: update apparmor-basic-networking-rules for 4.11-rc1
  (FATE#300516, boo#1065536).
- AppArmor: basic networking rules (FATE#300516, boo#1065536).
- commit fca1de8
* Wed Nov 15 2017 rgoldwyn@suse.com
- VFS: Handle lazytime in do_mount() (boo#1068256).
- commit 0f12060
* Mon Nov 13 2017 jeffm@suse.com
- Update to 4.14-final.
- commit c152297
* Thu Nov  9 2017 lpechacek@suse.com
- rpm/kernel-binary.spec.in: rename kGraft to KLP (fate#323682)
- commit 0ed191d
* Wed Nov  8 2017 tiwai@suse.de
- media: dib0700: fix invalid dvb_detach argument (CVE-2017-16646
  bsc#1067105).
- commit c6cd519
* Mon Nov  6 2017 jeffm@suse.com
- Update to 4.14-rc8.
- commit 0fbdeee
* Mon Nov  6 2017 tiwai@suse.de
- media: imon: Fix null-ptr-deref in imon_probe (CVE-2017-16537
  bsc#1066573).
- [media] cx231xx-cards: fix NULL-deref on missing association
  descriptor (CVE-2017-16536 bsc#1066606).
- commit 0cd38c2
* Mon Nov  6 2017 jkosina@suse.cz
- rpm/kernel-binary.spec.in: add explicit dependency of kernel-*-devel on
  libelf-devel.
  Otherwise warning that got turned into error by upstream 3dd40cb3 ("objtool:
  Upgrade libelf-devel warning to error...") would trigger and cause any
  packages being built against kernel-*-devel (such as KMPs, crash) not to have
  the libelf dependency included, and fail to build.
- rpm/kernel-binary.spec.in: add explicit dependency of kernel-*-devel on
  libelf-devel. Otherwise warning that got turned into error by e683952999
  ("objtool: Upgrade libelf-devel warning to error...") would trigger and
  cause any packages being built against kernel-*-devel (such as KMPs,
  crash) not to have the libelf dependency included, and fail to build.
- commit f6c0f80
* Mon Oct 30 2017 neilb@suse.com
- REVERT:  md/bitmap: copy correct data for bitmap super
  (bsc#1062597).
- commit 9382440
* Mon Oct 30 2017 jeffm@suse.com
- Update to 4.14-rc7.
- commit dbf3e9b
* Fri Oct 27 2017 jslaby@suse.cz
- futex: futex_wake_op, fix sign_extend32 sign bits (bnc#1064590).
- commit a6d946f
* Thu Oct 26 2017 neilb@suse.com
- VFS: expedite unmount (bsc#1024412).
- commit 10c4365
* Mon Oct 23 2017 jeffm@suse.com
- Update to 4.14-rc6.
- Eliminated 2 patches.
- commit 8b364ca
* Wed Oct 18 2017 mcgrof@suse.com
- mac80211: accept key reinstall without changing anything (CVE-2017-13080 bsc#1063667).
- commit 19d19fc
* Mon Oct 16 2017 jeffm@suse.com
- Update to 4.14-rc5.
- commit 39eecab
* Fri Oct 13 2017 msuchanek@suse.de
- Revert "rpm/constraints.in: Lower default disk space requirement from 25G to 24G"
  This reverts commit 406abda1467c038842febffe264faae1fa2e3c1d.
  ok, did not wait long enough to see the failure.
- commit ed99981
* Fri Oct 13 2017 msuchanek@suse.de
- rpm/constraints.in: Lower default disk space requirement from 25G to 24G
  25G is rejected by the build service on ARM.
- commit 406abda
* Mon Oct  9 2017 jeffm@suse.com
- Update to 4.14-rc4.
- commit 879f297
* Fri Oct  6 2017 msuchanek@suse.de
- rpm/kernel-binary.spec.in: add the kernel-binary dependencies to
  kernel-binary-base (bsc#1060333).
- commit 955681c
* Fri Oct  6 2017 pmladek@suse.com
- Delete
  patches.suse/ftrace-x86-xen-use-kernel-identity-mapping-only-when.patch.
  The change is not longer needed with PVOPS Xen (bsc#873195).
- commit 8366b6a
* Thu Oct  5 2017 jeffm@suse.com
- Delete patches.rpmify/cloneconfig.diff.
- commit 437d08e
* Thu Oct  5 2017 jeffm@suse.com
- Only use patches.suse for patches.
  This eliminates patches.arch, patches.drivers, and patches.fixes, and moves
  the patches contained in them to patches.suse.
  Also update feedback for Patch-mainline tags.
- commit 343996e
* Wed Oct  4 2017 jeffm@suse.com
- Delete patches.suse/suse-hv-storvsc-sg_tablesize.patch.
  Per Olaf Hering, this is no longer needed.
- commit 83b19a6
* Wed Oct  4 2017 jslaby@suse.cz
- orc: mark it as reliable (bnc#1058115).
- Update config files.
- commit 3c7d429
* Wed Oct  4 2017 hare@suse.de
- Delete patches.fixes/sd_liberal_28_sense_invalid.diff.
- Delete patches.suse/dm-emulate-blkrrpart-ioctl.
- Delete patches.suse/scsi-netlink-ml.
- commit b8f0083
* Wed Oct  4 2017 agraf@suse.de
- Delete patches.arch/arm-OMAP-Fix-missing-usb.h-include.patch.
  (no longer needed)
- Delete patches.arch/arm-arndale-usb.patch. (no longer needed)
- Delete
  patches.arch/arm64-0006-arm64-Select-reboot-driver-for-X-Gene-platform.patch.
  (not needed, our config already includes the driver)
- Delete patches.arch/ppc64le-build-vmlinux.patch. (no longer needed)
- commit 2b9d327
* Tue Oct  3 2017 jeffm@suse.com
- Disable patches.suse/binutils2_26.patch for testing.
  The issue addressed by this patch should be handled via upstream
  commit 6d92bc9d483 (x86/build: Build compressed x86 kernels as PIE).
- commit f27997b
* Tue Oct  3 2017 neilb@suse.com
- Delete
  patches.fixes/0001-Revert-SUNRPC-xs_sock_mark_closed-does-not-need-to-t.patch.
  Not needed, bug was fixed some other way since that patch
  was created.
- commit d55ee70
* Tue Oct  3 2017 mgorman@suse.de
- Delete patches.suse/connector-read-mostly.
- commit 8ae100a
* Tue Oct  3 2017 jeffm@suse.com
- series.conf: remove commented out lines for removed patches
- commit 7ea9bcc
* Tue Oct  3 2017 jeffm@suse.com
- Delete patches.arch/arm-refresh-mach-types.diff.
  It was marked for refresh in 12/2016 and hasn't been updated.
- commit 8e357d7
* Mon Oct  2 2017 jeffm@suse.com
- Remove s390 message catalog patches.
- Delete patches.arch/kmsg-fix-parameter-limitations.
- Delete patches.arch/s390-message-catalog.diff.
- commit 865e88d
* Mon Oct  2 2017 jeffm@suse.com
- Refresh patches.suse/dm-mpath-accept-failed-paths.
- commit 04a0a7a
* Mon Oct  2 2017 jeffm@suse.com
- Moved powerpc-Blacklist-GCC-5.4-6.1-and-6.2.patch to patches.rpmify.
  It's a compiler blacklist addition and should be applied to vanilla too.
- commit e34eae8
* Mon Oct  2 2017 jeffm@suse.com
- Update to 4.14-rc3.
- Eliminated 2 patches.
- Config changes:
  - Crypto:
  - Crypto changes brought by Kconfig changes:
  - CONFIG_CRYPTO_GHASH=y (Kconfig dependency change)
  - CONFIG_CRYPTO_GCM=y (Kconfig dependency change)
  - armv7hl:
  - DRM_SUN4I_HDMI_CEC=y
  - CONFIG_CEC_PIN=y (dependency)
  - s390x/zfcpdump:
  - Crypto changes brought by Kconfig changes, consistent with other configs:
  - CRYPTO_MANAGER_DISABLE_TESTS=n
  - CRYPTO_DRBG_HASH=y
  - CRYPTO_DRBG_CTR=y
  - Lots of dependencies
- commit 37f329b
* Mon Oct  2 2017 jslaby@suse.cz
- Refresh
  patches.suse/0001-objtool-Don-t-report-end-of-section-error-after-an-e.patch.
- Refresh
  patches.suse/0002-x86-head-Remove-confusing-comment.patch.
- Refresh
  patches.suse/0003-x86-head-Remove-unused-bad_address-code.patch.
- Refresh
  patches.suse/0004-x86-head-Fix-head-ELF-function-annotations.patch.
- Refresh
  patches.suse/0005-x86-boot-Annotate-verify_cpu-as-a-callable-function.patch.
- Refresh
  patches.suse/0006-x86-xen-Fix-xen-head-ELF-annotations.patch.
- Refresh
  patches.suse/0007-x86-xen-Add-unwind-hint-annotations.patch.
- Refresh
  patches.suse/0008-x86-head-Add-unwind-hint-annotations.patch.
- Delete
  patches.suse/0002-dwarf-do-not-throw-away-unwind-info.patch.
  Update upstream status and drop the dwarf remainder.
- commit 8d5b116
* Thu Sep 28 2017 jeffm@suse.com
- Update to 4.14-rc2.
- Eliminated 21 patches.
- commit b61ed0c
* Mon Sep 25 2017 jslaby@suse.cz
- x86/asm: Fix inline asm call constraints for Clang
  (bnc#1058115).
- objtool: Handle another GCC stack pointer adjustment bug
  (bnc#1058115).
- commit 7544781
* Sun Sep 24 2017 msuchanek@suse.de
- rpm/kernel-binary.spec.in: only rewrite modules.dep if non-zero in size
  (bsc#1056979).
- commit 75691fd
* Fri Sep 22 2017 jslaby@suse.cz
- crypto: x86/blowfish - Fix RBP usage (bnc#1058115).
- crypto: x86/camellia - Fix RBP usage (bnc#1058115).
- crypto: x86/cast5 - Fix RBP usage (bnc#1058115).
- crypto: x86/cast6 - Fix RBP usage (bnc#1058115).
- crypto: x86/des3_ede - Fix RBP usage (bnc#1058115).
- crypto: x86/sha1-avx2 - Fix RBP usage (bnc#1058115).
- crypto: x86/sha1-ssse3 - Fix RBP usage (bnc#1058115).
- crypto: x86/sha256-avx - Fix RBP usage (bnc#1058115).
- crypto: x86/sha256-avx2 - Fix RBP usage (bnc#1058115).
- crypto: x86/sha256-ssse3 - Fix RBP usage (bnc#1058115).
- crypto: sha512-avx2 - Fix RBP usage (bnc#1058115).
- crypto: x86/twofish - Fix RBP usage (bnc#1058115).
  Update upstream status.
- commit 6627c5a
* Thu Sep 21 2017 jeffm@suse.com
- drm/tegra: trace: Fix path to include (build fix).
- commit aecd9be
* Wed Sep 20 2017 afaerber@suse.de
- config: armv7hl: Update to 4.14-rc1
- commit 9d284f8
* Wed Sep 20 2017 afaerber@suse.de
- config: armv6hl: Update to 4.14-rc1
- commit 0c2764f
* Wed Sep 20 2017 afaerber@suse.de
- config: arm64: Update to 4.14-rc1
- commit d6909a3
* Wed Sep 20 2017 jeffm@suse.com
- Revert "KVM: Don't accept obviously wrong gsi values via
  KVM_IRQFD" (build fix).
- commit f436aa0
* Wed Sep 20 2017 mcgrof@suse.com
- nl80211: check for the required netlink attributes presence
  (bsc#1058410 CVE-2017-12153).
- commit 6d93561
* Wed Sep 20 2017 lduncan@suse.com
- Fix incorrect backport of compatibility patch (bsc#1053501)
  This fixes commit fe56e414dcf9, which incorrectly placed
  the back-ported macros in libc-compat.h in the wrong place.
  It is important for __UAPI_DEF_IOVEC to be defined
  correctly with and without GLIBC being defined.
- commit 102e6e3
* Tue Sep 19 2017 jslaby@suse.cz
- objtool: Fix object file corruption (bnc#1058115).
- objtool: Do not retrieve data from empty sections (bnc#1058115).
- objtool: Fix memory leak in elf_create_rela_section()
  (bnc#1058115).
- commit 7fb990b
* Tue Sep 19 2017 jslaby@suse.cz
- x86/crypto: Fix RBP usage in twofish-avx-x86_64-asm_64.S
  (bnc#1058115).
- x86/crypto: Fix RBP usage in sha512-avx2-asm.S (bnc#1058115).
- x86/crypto: Fix RBP usage in sha256-ssse3-asm.S (bnc#1058115).
- x86/crypto: Fix RBP usage in sha256-avx2-asm.S (bnc#1058115).
- x86/crypto: Fix RBP usage in sha256-avx-asm.S (bnc#1058115).
- x86/crypto: Fix RBP usage in sha1_ssse3_asm.S (bnc#1058115).
- x86/crypto: Fix RBP usage in sha1_avx2_x86_64_asm.S
  (bnc#1058115).
- x86/crypto: Fix RBP usage in des3_ede-asm_64.S (bnc#1058115).
- x86/crypto: Fix RBP usage in cast6-avx-x86_64-asm_64.S
  (bnc#1058115).
- x86/crypto: Fix RBP usage in cast5-avx-x86_64-asm_64.S
  (bnc#1058115).
- x86/crypto: Fix RBP usage in camellia-x86_64-asm_64.S
  (bnc#1058115).
- x86/crypto: Fix RBP usage in blowfish-x86_64-asm_64.S
  (bnc#1058115).
- commit cb96cd5
* Tue Sep 19 2017 jeffm@suse.com
- Update to 4.14-rc1.
- Eliminated 17 patches.
- ARM configs need updating.
- Config changes:
  - General:
  - HMM_MIRROR=n
  - DEVICE_PRIVATE=n
  - DEVICE_PUBLIC=n
  - SQUASHFS_ZSTD=y
  - ZRAM_WRITEBACK=y
  - x86:
  - INTEL_RDT=y (renamed option)
  - XEN_PVCALLS_BACKEND=y
  - X86_5LEVEL=n (will only boot on systems that support it)
  - AMD_MEM_ENCRYPT=y
  - AMD_MEM_ENCRYPT_ACTIVE_BY_DEFAULT=n
  - ppc:
  - PPC_MEMTRACE=y
  - PPC_VAS=y
  - s390:
  - CMA_DEBUG=n
  - CMA_DEBUGFS=n
  - CMA_AREAS=7 (default)
  - DMA_CMA=n
  - VMCP_CMA_SIZE=4 (default)
  - Netfilter:
  - NFT_FIB_NETDEV
  - Hyperv:
  - HYPERV_VSOCKETS
  - Network:
  - NET_NSH
  - BPF_STREAM_PARSER=y (build fix)
  - BNXT_FLOWER_OFFLOAD=y
  - HINIC
  - MLX5_MPFS=y
  - MLX5_ESWITCH=y
  - RMNET=n
  - ROCKCHIP_PHY
  - WIL6210_DEBUGFS=n
  - ATH10K_USB
  - Bluetooth:
  - BT_LEGACY_IOCTL=y (default)
  - SPI:
  - SPI_INTEL_SPI_PCI
  - Misc:
  - INPUT_PWM_VIBRA=m
  - SERIO_GPIO_PS2=m
  - PINCTRL_DENVERTON
  - PINCTRL_LEWISBURG
  - W1_SLAVE_DS2805
  - BATTERY_BQ27XXX_HDQ=m
  - BATTERY_MAX1721X
  - SENSORS_IBM_CFFPS
  - SENSORS_TPS53679
  - CLOCK_THERMAL=y
  - DEVFREQ_THERMAL=y
  - MFD_BD9571MWV=n
  - INTEL_SOC_PMIC_CHTWC=y
  - MFD_TPS68470=n
  - IR_GPIO_TX=n
  - IR_PWM_TX=n
  - DVB_DDBRIDGE
  - DVB_DDBRIDGE_MSIENABLE=n
  - TINYDRM_REPAPER=n
  - TINYDRM_ST7586=n
  - SND_SOC_CS43130=n
  - SND_SOC_WM8524=n
  - MMC_SPI
  - LEDS_AS3645A=n
  - LEDS_PCA955X_GPIO=y
  - INFINIBAND_EXP_USER_ACCESS=y [?]
  - CONFIG_ALTERA_MSGDMA
  - R8822BE
  - PI433=n
  - CLK_HSDK=n
  - EXTCON_USBC_CROS_EC
  - DLN2_ADC=m
  - LTC2471=n
  - CCS811=n
  - RESET_HSDK_V1=n
  - FPGA_MGR_ALTERA_CVP=m
  - FPGA_MGR_ALTERA_PS_SPI=m
  - CRYPTO_DEV_SP_CCP=y
  - I2C_CHT_WC=m
  - RESET_ATTACK_MITIGATION=y
- commit 08ca987
* Tue Sep 19 2017 jslaby@suse.cz
- Refresh
  patches.suse/0001-objtool-Don-t-report-end-of-section-error-after-an-e.patch.
- Refresh
  patches.suse/0002-x86-head-Remove-confusing-comment.patch.
- Refresh
  patches.suse/0003-x86-head-Remove-unused-bad_address-code.patch.
- Refresh
  patches.suse/0004-x86-head-Fix-head-ELF-function-annotations.patch.
- Refresh
  patches.suse/0005-x86-boot-Annotate-verify_cpu-as-a-callable-function.patch.
- Refresh
  patches.suse/0006-x86-xen-Fix-xen-head-ELF-annotations.patch.
- Refresh
  patches.suse/0007-x86-xen-Add-unwind-hint-annotations.patch.
- Refresh
  patches.suse/0008-x86-head-Add-unwind-hint-annotations.patch.
- Delete
  patches.suse/0007-x86-xen-Add-unwind-hint-annotations-fix.patch.
  Update to the submitted v2.
- commit 27de3c0
* Sun Sep 17 2017 jdelvare@suse.de
- drm/amdgpu: revert tile table update for oland (boo#1027378,
  boo#1039806, bko#194761).
- Delete
  patches.fixes/drm-amdgpu-revert-update-tile-table-for-oland-hainan.patch.
- commit 51745cf
* Thu Sep 14 2017 jslaby@suse.cz
- Linux 4.13.2 (bnc#1012628 bsc#1055826).
- Delete
  patches.drivers/rt2800-fix-TX_PIN_CFG-setting-for-non-MT7620-chips.
- Delete
  patches.fixes/Bluetooth-validate-output-buffer-length-for-config-r.patch.
- commit 96d9efa
* Wed Sep 13 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Fix a thinko for xmlto buildreq condition
- commit 0ef59d3
* Wed Sep 13 2017 jslaby@suse.cz
- Bluetooth: validate output buffer length for config requests
  and responses (bnc#1057389 CVE-2017-1000251).
- commit c0b7e1f
* Tue Sep 12 2017 jslaby@suse.cz
- fix annotations of xen-head.S (bnc#1058115).
- commit d4c88a5
* Tue Sep 12 2017 msuchanek@suse.de
- rpm/kernel-docs.spec.in: make unpack scripts executable
- commit 1ba3766
* Tue Sep 12 2017 jslaby@suse.cz
- x86/head: Add unwind hint annotations (bnc#1058115).
- x86/xen: Add unwind hint annotations (bnc#1058115).
- x86/xen: Fix xen head ELF annotations (bnc#1058115).
- x86/boot: Annotate verify_cpu() as a callable function
  (bnc#1058115).
- x86/head: Fix head ELF function annotations (bnc#1058115).
- x86/head: Remove unused 'bad_address' code (bnc#1058115).
- x86/head: Remove confusing comment (bnc#1058115).
- objtool: Don't report end of section error after an empty
  unwind hint (bnc#1058115).
- commit 53af152
* Tue Sep 12 2017 jslaby@suse.cz
- objtool: Assume unannotated UD2 instructions are dead ends
  (bnc#1058115).
- objtool: Fix gcov check for older versions of GCC (bnc#1058115).
- objtool: Fix objtool fallthrough detection with function padding
  (bnc#1058115).
- objtool: Fix validate_branch() return codes (bnc#1058115).
- objtool: Handle GCC stack pointer adjustment bug (bnc#1058115).
- x86/asm: Add ASM_UNREACHABLE (bnc#1058115).
- x86/asm: Fix UNWIND_HINT_REGS macro for older binutils
  (bnc#1058115).
- x86/asm: Make objtool unreachable macros independent from GCC
  version (bnc#1058115).
- objtool: Skip unreachable warnings for 'alt' instructions
  (bnc#1058115).
- objtool: Track DRAP separately from callee-saved registers
  (bnc#1058115).
- Refresh patches.suse/0001-x86-unwind-Add-the-ORC-unwinder.patch.
  Take all ORC upstream patches. This will go to stable & SLE15 too.
- commit 831ca01
* Mon Sep 11 2017 jslaby@suse.cz
- Refresh
  patches.suse/0001-x86-entry-64-Refactor-IRQ-stacks-and-make-them-NMI-s.patch.
- Refresh patches.suse/0001-x86-unwind-Add-the-ORC-unwinder.patch.
- Refresh
  patches.suse/0002-x86-entry-64-Initialize-the-top-of-the-IRQ-stack-bef.patch.
- Refresh
  patches.suse/0002-x86-kconfig-Make-it-easier-to-switch-to-the-new-ORC-.patch.
- Refresh
  patches.suse/0003-x86-dumpstack-Fix-occasionally-missing-registers.patch.
- Refresh
  patches.suse/0003-x86-kconfig-Consolidate-unwinders-into-multiple-choi.patch.
- Refresh
  patches.suse/0004-x86-dumpstack-Fix-interrupt-and-exception-stack-boun.patch.
- Refresh
  patches.suse/0005-objtool-Add-ORC-unwind-table-generation.patch.
- Refresh
  patches.suse/0006-objtool-x86-Add-facility-for-asm-code-to-provide-unw.patch.
- Refresh
  patches.suse/0007-x86-entry-64-Add-unwind-hint-annotations.patch.
- Refresh
  patches.suse/0008-x86-asm-Add-unwind-hint-annotations-to-sync_core.patch.
- Delete
  patches.suse/0001-linkage-new-macros-for-assembler-symbols.patch.
- Delete
  patches.suse/0003-DWARF-EH-frame-based-stack-unwinding.patch.
- Delete patches.suse/stack-unwind-disable-kasan.patch.
  Update upstream status of ORC and drop already-disabled DWARF unwinder.
- commit 2e9b944
* Mon Sep 11 2017 jslaby@suse.cz
- rpm/constraints.in: build ARM on at least 2 cpus
- commit b7edeaf
* Mon Sep 11 2017 jslaby@suse.cz
- rpm/constraints.in: increase memory for kernel-syzkaller
  And see if it helps. If so, push it to packaging...
- commit 7193e65
* Sun Sep 10 2017 afaerber@suse.de
- config: arm64: Enable legacy instruction emulation (boo#1029158)
  Needed for execution of older e.g. ARMv6 code.
- commit a4e05e8
* Sun Sep 10 2017 afaerber@suse.de
- config: arm64: Enable ACPI_DOCK for consistency
- commit cec354f
* Sun Sep 10 2017 afaerber@suse.de
- config: arm64: Enable some network options
- Marvell Armada 7K/8K Ethernet driver
- Microchip ENC28J60 and related SPI Ethernet drivers
- Micrel KS8851 SPI Ethernet driver
- MMIO MDIO mux driver
- commit cf926f4
* Sun Sep 10 2017 jslaby@suse.cz
- Linux 4.13.1 (bnc#1012628).
- commit 8740849
* Fri Sep  8 2017 jslaby@suse.cz
- rpm/kernel-binary.spec.in: package ftrace-mod.o on arm64
  It is needed for building modules since 4.13:
  CC [M]  /suse/jslaby/a/aaa.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC      /suse/jslaby/a/aaa.mod.o
  LD [M]  /suse/jslaby/a/aaa.ko
  ld: cannot find ./arch/arm64/kernel/ftrace-mod.o: No such file or directory
  ...
- commit 07da115
* Thu Sep  7 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Expand kernel tree directly from sources (bsc#1057199)
- commit a61b4d9
* Wed Sep  6 2017 mcgrof@suse.com
- supported.conf: add test_syctl to new kselftests-kmp package FATE#323821
  As per FATE#323821 we will require new FATE requests per each
  new selftest driver. We don't want to support these module on
  production runs but we do want to support them for QA / testing
  uses. The compromise is to package them into its own package,
  this will be the kselftests-kmp package.
  Selftests can also be used as proof of concept vehicle for issues
  by customers or ourselves.
  Vanilla kernels do not get test_sysctl given that driver was
  using built-in defaults, this also means we cannot run sefltests
  on config/s390x/zfcpdump which does not enable modules.
  Likeweise, since we had to *change* the kernel for test_syctl, it
  it also means we can't test test_syctl with vanilla kernels. It
  should be possible with other selftests drivers if they are
  present in vanilla kernels though.
- commit ae8069f
* Wed Sep  6 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Re-add xmlto buildreq conditionally for SLE15 & co
- commit 259b49e
* Wed Sep  6 2017 mchandras@suse.de
- rpm/group-source-files.pl: Add arch/*/tools/* files to the devel package
  Commit b71c9ffb1405 ("powerpc: Add arch/powerpc/tools directory")
  introduced in v4.12-rc1 release, moved the scripts into the tools
  directory. However, this location is not considered for the kernel devel
  package and the following error occurs when building a kmp for powerpc
  make[2]: /usr/src/linux-4.12.9-1/arch/powerpc/tools/gcc-check-mprofile-kernel.sh: Command not found
- commit 5f1ff53
* Tue Sep  5 2017 jeffm@suse.com
- Update to 4.13-final.
- commit 3fdcb17
* Thu Aug 31 2017 tiwai@suse.de
- rt2800: fix TX_PIN_CFG setting for non MT7620 chips
  (bsc#1055826).
- commit 8116757
* Thu Aug 31 2017 jeffm@suse.com
- Update to 4.13-rc7.
- Eliminate 2 patches.
- commit dd00417
* Thu Aug 31 2017 jthumshirn@suse.de
- scsi: qla2xxx: Fix an integer overflow in sysfs code
  (bsc#1056588, CVE-2017-14051).
- commit aacb454
* Tue Aug 29 2017 tiwai@suse.de
- Update config files: enable CONFIG_SPI_PXA2XX for MacBook (bsc#1055817)
- commit 3ce18e9
* Mon Aug 28 2017 tiwai@suse.de
- rpm/kernel-binary.spec.in: Update drm-kmp obsolete for SLE12-SP3/Leap-42.3
- commit 77ccbd0
* Mon Aug 28 2017 tiwai@suse.de
- Refresh patch tags of patches.fixes/Input-ALPS-Fix-Alps-Touchpad-two-finger-scroll-does-
- commit 0b3ef4c
* Mon Aug 28 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Disable PDF build again
  ... due to the breakage with the recent TeXLive 2017.
  Also add the missing dependency on texlive-varwidth.
- commit 9f682b5
* Wed Aug 23 2017 tiwai@suse.de
- ALSA: hda - Add stereo mic quirk for Lenovo G50-70 (17aa:3978)
  (bsc#1020657).
- commit 3f6a0b2
* Tue Aug 22 2017 tiwai@suse.de
- ALSA: ice1712: Add support for STAudio ADCIII (bsc#1048934).
- commit 99a99ef
* Tue Aug 22 2017 tiwai@suse.de
- ALSA: hda - Implement mic-mute LED mode enum (bsc#1055013).
- commit a3c362f
* Mon Aug 21 2017 jeffm@suse.com
- Update to 4.13-rc6.
- commit ee50b89
* Fri Aug 18 2017 msuchanek@suse.de
- Do not ship firmware (bsc#1054239).
  Pull firmware from kernel-firmware instead.
- commit 0b0b5c9
* Thu Aug 17 2017 jeffm@suse.com
- supported.conf: clear mistaken external support flag for cifs.ko (bsc#1053802).
- commit 75e287e
* Thu Aug 17 2017 jeffm@suse.com
- supported.conf: mark reiserfs unsupported (FATE#323394).
  ReiserFS is not supported in SLE15.  ReiserFS file systems must be
  transferred or converted before installing.
- commit 8a547c5
* Thu Aug 17 2017 jeffm@suse.com
- Update to 4.13-rc5.
- commit c3fb699
* Wed Aug 16 2017 msuchanek@suse.de
- s390: export symbols for crash-kmp (bsc#1053915).
- commit 7dd9b75
* Tue Aug 15 2017 hare@suse.de
- Delete patches.fixes/scsi-dh-queuedata-accessors.
- commit ee998ab
* Tue Aug 15 2017 hare@suse.de
- Delete patches.suse/dm-mpath-detach-existing-hardware-handler.
- commit a8291cd
* Tue Aug 15 2017 hare@suse.de
- Delete patches.suse/no-partition-scan (FATE#323406)
- commit e1cccca
* Sat Aug 12 2017 lduncan@suse.com
- uapi: add a compatibility layer between linux/uio.h and glibc
  (bsc#1053501).
- commit fe56e41
* Thu Aug 10 2017 msuchanek@suse.de
- Refresh vanilla config.
- commit ae18928
* Thu Aug 10 2017 msuchanek@suse.de
- rpm/modules.fips include module list from dracut
- commit f70bab5
* Wed Aug  9 2017 ohering@suse.de
- Delete stale patches.fixes/scsi-ibmvscsi-module_alias.patch.
- Delete stale patches.suse/suse-ppc64-branding.
- commit 1c8934b
* Tue Aug  8 2017 jeffm@suse.com
- Update to 4.13-rc4.
- commit 94b098f
* Wed Aug  2 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Fix package list and enable building PDFs
  Finally it works!  Added some missing pieces (ImageMagick, some texlive
  subpkgs) in addition to use explicitly python3-Sphinx stuff.
- commit c117a0c
* Tue Aug  1 2017 agraf@suse.de
- Clean up upstreamed patches list. Annotate the remaining ones
  with their current status.
- Delete patches.arch/arm-exynos-dwmmc-modalias.patch.
- Delete
  patches.arch/arm64-Relocate-screen_info.lfb_base-on-PCI-BAR-alloc.patch.
- commit 3f654d5
* Mon Jul 31 2017 jeffm@suse.com
- Update to 4.13-rc3.
- commit 4ef483a
* Thu Jul 27 2017 jslaby@suse.cz
- x86/kconfig: Make it easier to switch to the new ORC unwinder
  (bnc#1018348).
- x86/kconfig: Consolidate unwinders into multiple choice
  selection (bnc#1018348).
- Update config files.
- Refresh
  patches.suse/0001-x86-entry-64-Refactor-IRQ-stacks-and-make-them-NMI-s.patch.
- Refresh
  patches.suse/0002-dwarf-do-not-throw-away-unwind-info.patch.
- Refresh
  patches.suse/0002-x86-entry-64-Initialize-the-top-of-the-IRQ-stack-bef.patch.
  Update to version from -tip. ORC is in -tip completely. So make sure
  we use the upstream version.
- commit 903e200
* Wed Jul 26 2017 jeffm@suse.com
- Update to 4.13-rc2.
- Eliminated 1 patch.
- Config changes:
  - DRM_VBOXVIDEO=m
- commit b545b87
* Wed Jul 26 2017 tiwai@suse.de
- Input: ALPS - Fix Alps Touchpad two finger scroll does not
  work on right side (bsc#1050582).
- commit 474729b
* Sun Jul 23 2017 stefan.bruens@rwth-aachen.de
- config: arm64: Enable RTC and SPI on Allwinner A64/H5
  A64 and H5 share the RTC and SPI functional blocks with older SoCs,
  enable the corresponding drivers.
- commit b5bf58a
* Wed Jul 19 2017 mmarek@suse.cz
- rpm/kernel-binary.spec.in: find-debuginfo.sh should not touch build-id
  This needs rpm-4.14+ (bsc#964063).
- commit f622d60
* Tue Jul 18 2017 afaerber@suse.de
- config: armv7hl: Update to v4.13-rc1
- commit 1d72b01
* Tue Jul 18 2017 afaerber@suse.de
- config: armv6hl: Update to v4.13-rc1
- commit 5ede81f
* Tue Jul 18 2017 afaerber@suse.de
- config: arm64: Update to v4.13-rc1
- commit 7d005f8
* Tue Jul 18 2017 jslaby@suse.cz
- Refresh
  patches.suse/0001-x86-entry-64-Refactor-IRQ-stacks-and-make-them-NMI-s.patch.
- Refresh
  patches.suse/0002-x86-entry-64-Initialize-the-top-of-the-IRQ-stack-bef.patch.
- Refresh
  patches.suse/0003-x86-dumpstack-fix-occasionally-missing-registers.patch.
- Refresh
  patches.suse/0004-x86-dumpstack-fix-interrupt-and-exception-stack-boun.patch.
- Refresh
  patches.suse/0005-objtool-add-ORC-unwind-table-generation.patch.
- Refresh
  patches.suse/0006-objtool-x86-add-facility-for-asm-code-to-provide-unw.patch.
- Refresh
  patches.suse/0007-x86-entry-64-add-unwind-hint-annotations.patch.
- Refresh
  patches.suse/0008-x86-asm-add-unwind-hint-annotations-to-sync_core.patch.
  Update upstream information.
- commit ff15779
* Tue Jul 18 2017 tiwai@suse.de
- Delete patches.fixes/drm-i915-Fix-S4-resume-breakage.
  The workaround wasn't merged to upstream, and it seems becoming
  superfluous with the recent i915 driver, so let's drop this one.
- commit f6f228c
* Tue Jul 18 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Drop unnecessary xmlto for 4.13+
- commit e47dc84
* Tue Jul 18 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Correct kernel-docs package summary/description
- commit 697b763
* Tue Jul 18 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: refresh dependencies for PDF build (bsc#1048129)
  But it still doesn't work with Tex Live 2017, thus disabled yet.
  Also add texlive-anyfontsize for HTML math handling.
- commit ead44a1
* Tue Jul 18 2017 jslaby@suse.cz
- Delete patches.rpmify/drm-i915-disable-KASAN-for-handlers.patch.
  It was never accepted, is under discussion. But we disabled
  CONFIG_DRM_I915_WERROR in commit 5fc7b327348b, so we are safe anyway.
- commit e2957b5
* Tue Jul 18 2017 jslaby@suse.cz
- Delete patches.rpmify/get_builtin_firmware-gcc-7.patch.
  This was never accepted. Instead this seems to be fixed in gcc.
- commit c048497
* Mon Jul 17 2017 jeffm@suse.com
- Updated to 4.13-rc1.
- Eliminated 13 patches.
- ARM configs need updating.
- Config changes:
  - General:
  - SLAB_MERGE_DEFAULT=y (current behavior)
  - REFCOUNT_FULL=n (current behavior)
  - PERCPU_STATS=n (default)
  - FORTIFY_SOURCE=n (needs performance analysis)
  - WARN_ALL_UNSEEDED_RANDOM=n
  - TRACE_EVAL_MAP_FILE=n
  - TEST_SYSCTL=n
  - TEST_KMOD=n
  - Storage:
  - DM_ZONED=m
  - IB:
  - Options for MLX5:
  - MLX5_FPGA
  - MLX5_EN_IPSEC=y
  - MLXFW=m
  - SECURITY_INFINIBAND=y
  - Network:
  - Options for NFP:
  - NFP_APP_FLOWER=y
  - CORTINA_PHY=n (intended for embedded apps)
  - ATH10K_SDIO=m
  - QTNFMAC_PEARL_PCIE=m
  - DRM:
  - DRM_I915_SW_FENCE_CHECK_DAG=n
  - Sound:
  - SND_SOC_INTEL_BYT_CHT_ES8316_MACH=m
  - SND_SOC_INTEL_KBL_RT5663_MAX98927_MACH=m
  - SND_SOC_INTEL_KBL_RT5663_RT5514_MAX98927_MACH=m
  - SND_SOC_ZX_AUD96P22=n
  - HID:
  - HID_ITE=n
  - HID_RETRODE=m
  - USB:
  - TYPEC_UCSI=m
  - UCSI_ACPI=m
  - Misc:
  - RTC_NVMEM=y
  - RTC_DRV_DS3232_HWMON=y
  - WMI_BMOF=m
  - PEAQ_WMI=m
  - INTEL_INT0002_VGPIO=m
  - CROS_EC_LPC_MEC=y
  - EXTCON_INTEL_CHT_WC=m
  - NTB_IDT=m
  - MULTIPLEXER=m
  - KEYBOARD_DLINK_DIR685=n
  - TOUCHSCREEN_STMFTS=n
  - I2C_DESIGNWARE_SLAVE=n
  - SPI_SLAVE=n
  - PINCTRL_MCP23S08=n
  - PINCTRL_CANNONLAKE=m
  - GPIO_XRA1403=n
  - BATTERY_BQ27XXX_DT_UPDATES_NVM=n
  - CHARGER_LTC3651=n
  - SENSORS_IR35221=n
  - WATCHDOG_HANDLE_BOOT_ENABLED=y (default)
  - File Systems:
  - OVERLAY_FS_INDEX=n (mounting on an older kernel read-write will cause unexpected results)
  - CIFS_DEBUG_DUMP_KEYS=n
  - Crypto:
  - CRC4=m
  - X86:
  - INTEL_SOC_PMIC_CHTWC=m
  - CHT_WC_PMIC_OPREGION=y
  - ppc64/ppc64le:
  - CONFIG_IRQ_TIME_ACCOUNTING=n
  - CONFIG_LD_HEAD_STUB_CATCH=n
  - ZONE_DEVICE=y
  - ppc64le:
  - STRICT_KERNEL_RWX=y
  - s390x:
  - CRYPTO_PAES_S390=m
- commit d418532
* Mon Jul 17 2017 jeffm@suse.com
- Delete patches.drivers/ppc64-adb.
  This hardware was discontinued in 2006 and the patch was never accepted
  upstream.
- commit 995698b
* Mon Jul 17 2017 jeffm@suse.com
- Delete patches.arch/ppc-prom-nodisplay.patch.
  We no longer support 32-bit ppc and this hardware only existed with a
  32-bit CPU.
- commit d94ed1e
* Mon Jul 17 2017 jeffm@suse.com
- Delete patches.arch/ppc-pegasos-console-autodetection.patch.
  We no longer support 32-bit ppc and this hardware only existed with a
  32-bit CPU.
- commit b42ddc6
* Mon Jul 17 2017 jeffm@suse.com
- Delete patches.suse/ppc-powerbook-usb-fn-key-default.patch.
  We no longer support 32-bit ppc and there were no 64-bit powerbooks.
- commit 9e9a512
* Mon Jul 17 2017 jeffm@suse.com
- Disable patches.suse/pstore-backend-autoaction.
  It needs updating and there now exists a mount option instead of a module
  parameter.
- commit 87a5ab7
* Mon Jul 17 2017 jeffm@suse.com
- Delete patches.fixes/block-copy-bi_vcnt-in-_bio_clone_fast.
  This was obsoleted by 764f612c6c3c ("blk-merge: don't compute
  bi_phys_segments from bi_vcnt for cloned bio").
- commit f0c2642
* Mon Jul 17 2017 jslaby@suse.cz
- netfilter: expect: fix crash when putting uninited expectation
  (bnc#1048935).
- commit cc9efac
* Mon Jul 17 2017 mmarek@suse.cz
- Drop multiversion(kernel) from the KMP template (fate#323189)
- commit 71504d8
* Tue Jul 11 2017 tiwai@suse.de
- rpm/kernel-docs.spec.in: Fix and cleanup for 4.13 doc build (bsc#1048129)
  The whole DocBook stuff has been deleted.  The PDF build still non-working
  thus the sub-packaging disabled so far.
- commit 8e7de10
* Fri Jun  2 2017 afaerber@suse.de
- rpm/dtb.spec.in.in: Fix new include path
  Commit 89de3db69113d58cdab14d2c777de6080eac49dc ("rpm/dtb.spec.in.in:
  Update include path for dt-bindings") introduced an additional include
  path for 4.12. The commit message had it correct, but the spec file
  template lacked a path component, breaking the aarch64 build while
  succeeding on armv7hl. Fix that.
- commit c8d853a
* Wed May 31 2017 afaerber@suse.de
- rpm/dtb.spec.in.in: Update include path for dt-bindings
  Kernels before 4.12 had arch/{arm,arm64}/boot/dts/include/ directories
  with a symlink to include/dt-bindings/.
  In 4.12 those include/ directories were dropped.
  Therefore use include/ directly.
  Additionally some cross-architecture .dtsi reuse was introduced, which
  requires scripts/dtc/include-prefixes/ that didn't exist on older kernels.
- commit 466f108
* Fri Jan  6 2017 afaerber@suse.de
- rpm: Add arm64 dtb-zte subpackage
  4.9 added arch/arm64/boot/dts/zte/.
- commit 073d831
* Fri Jan  6 2017 afaerber@suse.de
- rpm: Add arm64 dtb-allwinner subpackage
  4.10 added arch/arm64/boot/dts/allwinner/.
- commit dfeb94a
* Tue Dec 20 2016 xxxxxmichl@googlemail.com
- added De0-Nanos-SoC board support (and others based on Altera SOC).
- commit 9278339
* Tue Apr 26 2016 mmarek@suse.cz
- Drop sysctl files for dropped archs, add ppc64le and arm (bsc#1178838).
- commit 87cd715
* Tue Mar 31 2009 jeffm@suse.de
- doc/README.KSYMS: Add to repo.
- commit 04ec451

