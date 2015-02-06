Summary:	DVB mpegtools libdvb - base tools
Name:		libdvb
Version:	0.5.5.1
Release:	11
License:	GPLv2+
Group:		Video
URL:		http://www.metzlerbros.org/dvb/
Source0:	http://www.metzlerbros.org/dvb/%{name}-%{version}.tar.gz
Patch0:		libdvb-0.5.5.1-long.patch
Patch3:		libdvb-0.5.5.1-pkgconfig.patch
Patch4:		libdvb-maindvb.patch
Patch5:		libdvb-0.5.5.1-gcc43.patch
Provides:	dvb-mpegtools
BuildRequires:	gcc-c++
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Manipulation of various MPEG file formats and their DVB variants

%package	devel
Summary:	DVB mpegtools libdvb - developer tools
Group:		Development/Other
Provides:	dvb-mpegtools-devel

%description	devel
manipulation of various MPEG file formats and their DVB variants

%prep

%setup -q
%patch0 -p1
%patch3 -p1 -b .pkgconfig
%patch4
%patch5 -p1

# no `configure` here..

%build
# (anssi) no shared libraries provided; build static libs with -fPIC:
make  PREFIX=%_prefix CFLAGS="%optflags -fPIC" CXX="g++ %{ldflags}" CC="gcc %{ldflags}"
make pkgconfig \
  PREFIX=%_prefix LIBDIR=%_libdir

%install
rm -rf %{buildroot}

# make install DESTDIR=%buildroot
%__mkdir_p %buildroot%_bindir
make install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir
make pkgconfig-install DESTDIR=%buildroot PREFIX=%_prefix LIBDIR=%_libdir

# prefix binaries with dvb_
for i in %buildroot%_bindir/* ; do 
  dir=`dirname $i` ; file=`basename $i` 
  case "$file" in
  dvb*) ;; 
  *)  mv $dir/$file $dir/dvb_$file ;;
  esac
done
# but keep aliases for ts* and pes*
for i in %buildroot%_bindir/dvb_ts* %buildroot%_bindir/dvb_pes* ; do
  dir=`dirname $i` ; file=`basename $i` 
  (cd $dir && ln -s $file `echo $file | sed -e 's/^dvb_//'`)
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%_bindir/*

%files devel
%defattr(-,root,root)
%_libdir/libdvb.a
%_libdir/libdvbci.a
%_libdir/libdvbmpegtools.a
%_libdir/pkgconfig/libdvb*.pc
%_includedir/*


%changelog
* Tue Dec 06 2011 Götz Waschk <waschk@mandriva.org> 0.5.5.1-10mdv2012.0
+ Revision: 738112
- yearly rebuild

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.5.5.1-9mdv2011.0
+ Revision: 609741
- rebuild

* Sun Jun 27 2010 Anssi Hannula <anssi@mandriva.org> 0.5.5.1-8mdv2010.1
+ Revision: 549193
- update license tag
- drop now unneeded include hacks
- apply ldflags

  + Götz Waschk <waschk@mandriva.org>
    - remove debug files

* Tue Oct 06 2009 Funda Wang <fwang@mandriva.org> 0.5.5.1-7mdv2010.0
+ Revision: 454503
- fix installation

* Fri Apr 10 2009 Funda Wang <fwang@mandriva.org> 0.5.5.1-7mdv2009.1
+ Revision: 365559
- fix patch num

* Sun Jun 29 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5.5.1-7mdv2009.0
+ Revision: 229912
- added a gcc43 patch (gentoo)
- slight spec file massage

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 0.5.5.1-5mdv2008.1
+ Revision: 150554
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Jun 29 2007 Anssi Hannula <anssi@mandriva.org> 0.5.5.1-4mdv2008.0
+ Revision: 45885
- apply optflags
- build static libs with -fPIC as no shared ones exist


* Sat Oct 21 2006 Götz Waschk <waschk@mandriva.org> 0.5.5.1-3mdv2007.0
+ Revision: 71571
+ Status: not released
- fix this patch again
- Import libdvb

* Sat Oct 21 2006 Götz Waschk <waschk@mandriva.org> 0.5.5.1-3mdv2007.1
- fix patch 3

* Fri Feb 10 2006 Götz Waschk <waschk@mandriva.org> 0.5.5.1-2mdk
- patch for 64 bit

* Thu Feb 09 2006 Götz Waschk <waschk@mandriva.org> 0.5.5.1-1mdk
- drop prefix
- drop patch 1
- drop merged patch 2
- New release 0.5.5.1
- use mkrel

* Sat Jul 17 2004 Michael Scherer <misc@mandrake.org> 0.5.4-2mdk 
- rebuild for new gcc

* Thu Mar 04 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.5.4-1mdk
- from Guido Draheim <guidod-2003-@gmx.de>

* Wed Feb 25 2004 Lenny Cartier <lenny@mandrakesoft.com> 0.5.4-1mdk
- new

