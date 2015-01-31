# NOTE: for versions >= 0.16 see synce-core.spec
# TODO:
# - replace all this stuff with synce-core
# - check connector-dccm requirements
# - bluetooth?
#
# Conditional build:
%bcond_without	dbus	# build without DBus support
%bcond_without	dccm	# build without dccm file support
%bcond_with	hal	# build without HAL support
%bcond_without	udev	# build without UDEV support
%bcond_with	odccm	# build without odccm support

# UDEV disables HAL
%if %{with udev}
%undefine	with_hal
%endif

%if %{without dbus}
%undefine	with_odccm
%undefine	with_hal
%endif

Summary:	Connection framework and DCCM implementation for WinCE devices
Summary(pl.UTF-8):	Szkielet połączeń oraz implementacja DCCM dla urządzeń WinCE
Name:		synce-connector
Version:	0.15.2
Release:	5
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	d557b3fd89b8ecdff6772bd7e1d2451e
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.60}
BuildRequires:	gnet-devel
%{?with_hal:BuildRequires:	hal-devel >= 0.5.8}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	synce-libsynce-devel >= 0.11
%{?with_udev:BuildRequires:	udev-devel}
%{?with_udev:BuildRequires:	udev-glib-devel}
Requires:	dhcp-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Synce-connector is a connection framework and DCCM implementation for
Windows Mobile devices that integrates with HAL or udev.

%description -l pl.UTF-8
Synce-connector to szkielet połączeń oraz implementacja DCCM dla
urządzeń Windows Mobile; integruje się z HAL lub udev.

%package hal
Summary:	Connection via HAL for WinCE devices
Summary(pl.UTF-8):	Połączenie poprzez HAL z urządzeniami WinCE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-hal

%description hal
This package provides connection via HAL for WinCE devices.

%description hal -l pl.UTF-8
Ten pakiet zapewnia połączenie poprzez HAL z urządzeniami WinCE.

%package odccm
Summary:	Connection via odccm for WinCE devices
Summary(pl.UTF-8):	Połączenie poprzez odccm z urządzeniami WinCE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-odccm

%description odccm
This package provides connection via odccm for WinCE devices.

%description odccm -l pl.UTF-8
Ten pakiet zapewnia połączenie poprzez odccm z urządzeniami WinCE.

%package dccm
Summary:	Connection via dccm for WinCE devices
Summary(pl.UTF-8):	Połączenie poprzez dccm z urządzeniami WinCE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
# check what is actually required
Requires:	synce-vdccm

%description dccm
This package provides connection via dccm for WinCE devices.

%description dccm -l pl.UTF-8
Ten pakiet zapewnia połączenie poprzez dccm z urządzeniami WinCE.

%package udev
Summary:	Connection via UDEV for WinCE devices
Summary(pl.UTF-8):	Połączenie poprzez UDEV z urządzeniami WinCE
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description udev
This package provides connection via UDEV for WinCE devices.

%description udev -l pl.UTF-8
Ten pakiet zapewnia połączenie poprzez UDEV z urządzeniami WinCE.

%prep
%setup -q

%build
DHCLIENTPATH=/sbin/dhclient \
UDEVADMPATH=/sbin/udevadm \
%configure \
	%{?with_udev:--enable-udev} \
	%{!?with_udev:--disable-udev} \
	%{!?with_odccm:--disable-odccm-support} \
%if %{with hal}
	--with-hal-addon-dir=%{_libdir}/hal/scripts
%else
	--disable-hal-support
%endif

#	%{!?with_dccm: --disable-dccm-file-support} \
#
#  --enable-bluetooth-support Build in bluetooth support

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_postclean %{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/synce-unlock
%attr(755,root,root) %{_libdir}/synce-serial-chat
%dir %{_datadir}/synce-connector
%{_datadir}/synce-connector/dhclient.conf
%{_datadir}/synce-connector/synceconnector.py[co]

%if %{with hal}
%files hal
%defattr(644,root,root,755)
/etc/dbus-1/system.d/org.freedesktop.Hal.Device.Synce.conf
%{_datadir}/hal/fdi/policy/20thirdparty/10-synce.fdi
%attr(755,root,root) %{_libdir}/hal/scripts/hal-synce-rndis
%attr(755,root,root) %{_libdir}/hal/scripts/hal-synce-serial
%endif

%if %{with udev}
%files udev
%defattr(644,root,root,755)
/etc/dbus-1/system.d/org.synce.dccm.conf
/lib/udev/rules.d/85-synce.rules
%attr(755,root,root) %{_bindir}/synce-serial
%attr(755,root,root) /lib/udev/synce-udev-rndis
%attr(755,root,root) /lib/udev/synce-udev-serial
%{_datadir}/dbus-1/system-services/org.synce.dccm.service
%attr(755,root,root) %{_datadir}/synce-connector/udev-synce-rndis
%attr(755,root,root) %{_datadir}/synce-connector/udev-synce-serial
%endif

%if %{with odccm}
%files odccm
%defattr(644,root,root,755)
%endif

%if %{with dccm}
%files dccm
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/dccm
%endif
