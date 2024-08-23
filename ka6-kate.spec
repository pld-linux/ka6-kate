#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.08.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kate

Summary:	K Desktop Environment - Advanced Text Editor
Summary(pl.UTF-8):	K Desktop Environment -  Zaawansowany edytor tekstu
Name:		ka6-%{kaname}
Version:	24.08.0
Release:	1
License:	GPL
Group:		X11/Applications/Editors
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	bdb43ea4ec735e3a9c81701257581ad6
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Sql-devel
BuildRequires:	Qt6Test-devel >= 5.4.0
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kjobwidgets-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-ktexteditor-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	shared-mime-info
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE advanced text editor featuring among others:
- fast opening/editing of files even the big ones (opens a 50MB file
  in a few seconds)
- powerful syntaxhighlighting engine, extensible via XML files
- Code Folding capabilities for C++, C, PHP and more
- Dynamic Word Wrap - long lines are wrapped at the window border on
  the fly for better overview
- multiple views allows you to view more instances of the same
  document and/or more documents at one time
- support for different encodings globally and at write time
- built in dockable terminal emulation
- sidebars with a list of open documents, a directory viewer with a
  directory chooser, a filter chooser and more
- a plugin interface to allow third party plugins
- a "Filter" command allows you to run selected text through a shell
  command

KWrite is a simple texteditor, with syntaxhighlighting, codefolding,
dynamic word wrap and more, it's the lightweight version of Kate,
providing more speed for minor tasks.

%description -l pl.UTF-8
Kate (KDE advanced text editor) to zaawansowany edytor tekstu KDE o
możliwościach obejmujących m.in.:
- szybkie otwieranie i edycję nawet dużych plików (otwiera plik 50MB w
  parę sekund)
- potężny silnik podświetlania składni, rozszerzalny za pomocą plików
  XML
- możliwość zwijania kodu dla C++, C, PHP i innych języków
- dynamiczne zawijanie wierszy - długie linie są zawijane na granicy
  okna w locie dla lepszej widoczności
- wiele widoków pozwalających oglądać więcej instancji tego samego
  dokumentu i/lub więcej dokumentów w tym samym czasie
- obsługę różnych kodowań globalnie i w czasie zapisu
- wbudowaną emulację dokowalnego terminala
- paski z listą otwartych dokumentów, przeglądarkę katalogów z
  możliwością wybierania katalogu i filtrów
- interfejs wtyczek obsługujący zewnętrzne wtyczki
- polecenie "Filtr" pozwalające przepuszczać zaznaczony tekst przez
  polecenie powłoki

KWrite to prosty edytor tekstu z podświetlaniem składni, zwijaniem
kodu, dynamicznym zawijaniem wierszy itp. Jest lżejszą wersją Kate,
szybszą dla mniejszych zadań.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications/Editors
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%package devel
Summary:	kate development files
Summary(pl.UTF-8):	Pliki dla programistów kate
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}
Obsoletes:	kate-devel <= 4.8.0

%description devel
kate development files.

%description devel -l pl.UTF-8
Pliki dla programistów kate.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/ko
# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kate
%attr(755,root,root) %{_bindir}/kwrite
%attr(755,root,root) %{_libdir}/libkateprivate.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/cmaketoolsplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/compilerexplorer.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/eslintplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/externaltoolsplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/formatplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katebacktracebrowserplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katebuildplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katecloseexceptplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katecolorpickerplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katectagsplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katefilebrowserplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katefiletreeplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/kategdbplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/kategitblameplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katekonsoleplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/kateprojectplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katereplicodeplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katesearchplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katesnippetsplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katesymbolviewerplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katexmlcheckplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katexmltoolsplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/keyboardmacrosplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/ktexteditorpreviewplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/latexcompletionplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/lspclientplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/openlinkplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/rainbowparens.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/tabswitcherplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/textfilterplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/rbqlplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/ktexteditor/katesqlplugin.so

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.kate.desktop
%{_desktopdir}/org.kde.kwrite.desktop
%{_iconsdir}/hicolor/128x128/apps/kate.png
%{_iconsdir}/hicolor/128x128/apps/kwrite.png
%{_iconsdir}/hicolor/150x150/apps/kate.png
%{_iconsdir}/hicolor/150x150/apps/kwrite.png
%{_iconsdir}/hicolor/16x16/apps/kate.png
%{_iconsdir}/hicolor/16x16/apps/kwrite.png
%{_iconsdir}/hicolor/22x22/apps/kate.png
%{_iconsdir}/hicolor/22x22/apps/kwrite.png
%{_iconsdir}/hicolor/256x256/apps/kate.png
%{_iconsdir}/hicolor/256x256/apps/kwrite.png
%{_iconsdir}/hicolor/310x310/apps/kate.png
%{_iconsdir}/hicolor/310x310/apps/kwrite.png
%{_iconsdir}/hicolor/32x32/apps/kate.png
%{_iconsdir}/hicolor/32x32/apps/kwrite.png
%{_iconsdir}/hicolor/44x44/apps/kate.png
%{_iconsdir}/hicolor/44x44/apps/kwrite.png
%{_iconsdir}/hicolor/48x48/apps/kate.png
%{_iconsdir}/hicolor/48x48/apps/kwrite.png
%{_iconsdir}/hicolor/512x512/apps/kate.png
%{_iconsdir}/hicolor/512x512/apps/kwrite.png
%{_iconsdir}/hicolor/64x64/apps/kate.png
%{_iconsdir}/hicolor/64x64/apps/kwrite.png
%{_iconsdir}/hicolor/scalable/apps/kate.svg
%{_iconsdir}/hicolor/scalable/apps/kwrite.svg
%{_datadir}/kateproject/kateproject.example
%{_datadir}/katexmltools/html4-loose.dtd.xml
%{_datadir}/katexmltools/html4-strict.dtd.xml
%{_datadir}/katexmltools/kcfg.dtd.xml
%{_datadir}/katexmltools/kde-docbook.dtd.xml
%{_datadir}/katexmltools/kpartgui.dtd.xml
%{_datadir}/katexmltools/language.dtd.xml
%{_datadir}/katexmltools/simplify_dtd.xsl
%{_datadir}/katexmltools/testcases.xml
%{_datadir}/katexmltools/xhtml1-frameset.dtd.xml
%{_datadir}/katexmltools/xhtml1-strict.dtd.xml
%{_datadir}/katexmltools/xhtml1-transitional.dtd.xml
%{_datadir}/katexmltools/xslt-1.0.dtd.xml
%{_mandir}/ca/man1/kate.1*
%{_mandir}/de/man1/kate.1*
%{_mandir}/eo/man1/kate.1*
%{_mandir}/es/man1/kate.1*
%{_mandir}/fr/man1/kate.1*
%{_mandir}/it/man1/kate.1*
%{_mandir}/man1/kate.1*
%{_mandir}/nl/man1/kate.1*
%{_mandir}/pt/man1/kate.1*
%{_mandir}/pt_BR/man1/kate.1*
%{_mandir}/ru/man1/kate.1*
%{_mandir}/sv/man1/kate.1*
%{_mandir}/tr/man1/kate.1*
%{_mandir}/uk/man1/kate.1*
%{_datadir}/metainfo/org.kde.kate.appdata.xml
%{_datadir}/metainfo/org.kde.kwrite.appdata.xml
