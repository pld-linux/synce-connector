# TODO:
# - check connector-dccm requirements
# - udev? bluetooth?
#
# Conditional build:
%bcond_without	dbus	# build without dbus support
%bcond_without	dccm	# build without dccm file support
%bcond_with	hal	# build without hal support
%bcond_without	odccm	# build without odccm support

%if %{without dbus}
%undefine with_odccm
%undefine with_hal
%endif
Summary:	Connection framework and dccm-implementation for WinCE devices
Name:		synce-connector
Version:	0.15.2
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://downloads.sourceforge.net/synce/%{name}-%{version}.tar.gz
# Source0-md5:	d557b3fd89b8ecdff6772bd7e1d2451e
URL:		http://www.synce.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.4
%{?with_dbus:BuildRequires:	dbus-glib-devel >= 0.60}
%{?with_hal:BuildRequires:	hal-devel >= 0.5.8}
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	synce-libsynce-devel >= 0.11
Requires:	dhcp-client
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Synce-connector is a connection framework and dccm-implementation for
Windows Mobile devices that integrates with HAL or udev.

%description -l pl.UTF-8
Biblioteka libsynce to część projektu SynCE. Jest wymagana dla (co
najmniej) następujących części projektu: librapi2, dccmd.

%package hal
Summary:	Provides Connection via HAL for WinCE devices
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-hal

%description hal
Provides Connection via HAL for WinCE devices.

%package odccm
Summary:	Provides Connection via odccm for WinCE devices
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	synce-odccm

%description -n synce-connector-odccm
Provides Connection via odccm for WinCE devices.

%package dccm
Summary:	Provides Connection via dccm for WinCE devices
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
# check what is actually required
Requires:	synce-vdccm

%description dccm
Provides Connection via dccm for WinCE devices.

%prep
%setup -q

%build
DHCLIENTPATH=/sbin/dhclient \
%configure \
%if %{with hal}
	--with-hal-addon-dir=%{_libdir}/hal/scripts
%endif

#	%{!?with_dccm: --disable-dccm-file-support} \
#	%{!?with_hal: --disable-hal-support} \
#	%{!?with_odccm: --disable-odccm-support}
#
#  --enable-udev		   Build for udev
#  --enable-bluetooth-support Build in bluetooth support
#  --with-hal-addon-dir=PATH	 Location of the hal addon scripts.
#  --with-udev-dir=PATH	 Location of the udev config.

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO ChangeLog
%attr(755,root,root) %{_bindir}/synce-unlock.py
%attr(755,root,root) %{_libdir}/synce-serial-chat
%dir %{_datadir}/synce-connector
%{_datadir}/synce-connector/dhclient.conf
%{_datadir}/synce-connector/synceconnector.py

%if %{with hal}
%files hal
%defattr(644,root,root,755)
/etc/dbus-1/system.d/org.freedesktop.Hal.Device.Synce.conf
%{_datadir}/hal/fdi/policy/20thirdparty/10-synce.fdi
%attr(755,root,root) %{_libdir}/hal/scripts/hal-synce-rndis
%attr(755,root,root) %{_libdir}/hal/scripts/hal-synce-serial
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
