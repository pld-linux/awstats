%include	/usr/lib/rpm/macros.perl
Summary:	Advanced Web Statistics is a free powerful server log file analyzer
Summary(pl):	Zaawansowany program do analizowania logów serwera
Name:		awstats
Version:	5.9
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/awstats/%{name}-%{version}.tgz
# Source0-md5:	be251e7506df16642b367789f5078ad9
Source1:	%{name}-cron
Patch0:		%{name}_conf.patch
URL:		http://awstats.sourceforge.net/
BuildRequires:	rpm-perlprov
Requires:	perl-Geo-IP
Requires:	perl-Time-HiRes
Requires:	perl-Storable
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		wwwdir	/home/services/httpd/html

%description
Advanced Web Statistics is a powerful and featureful tool that
generates advanced web server graphic statistics. This server log
analyzer works from command line or as a CGI and shows you all
information your log contains, in graphical web pages. It can analyze
a lot of web/wap/proxy servers like Apache, IIS, Weblogic, Webstar,
Squid, ... but also mail or ftp servers.

This program can measure visits, unique vistors, authenticated users,
pages, domains/countries, OS busiest times, robot visits, type of
files, search engines/keywords used, visits duration, HTTP errors and
more... Statistics can be updated from a browser or your scheduler.
The program also supports virtual servers, plugins and a lot of
features.

%description -l pl
awstats (Advanced Web Statistics - zaawansowane statystyki WWW) to
potê¿ne i bogate w mo¿liwo¶ci narzêdzie generuj±ce zaawansowane
graficzne statystyki serwera WWW. Ten analizator logów serwera
dzia³a z linii poleceñ lub jako CGI i pokazuje wszystkie informacje
zawarte w logu w postaci graficznych stron WWW. Mo¿e analizowaæ logi
wielu serwerów WWW/WAP/proxy, takich jak Apache, IIS, Weblogic,
Webstar, Squid... ale tak¿e serwerów pocztowych lub ftp.

Ten program mo¿e mierzyæ odwiedziny, odwiedzaj±cych, uwierzytelnionych
u¿ytkowników, strony, domeny/kraje, najbardziej zajête godziny,
odwiedziny robotów, rodzaje plików, u¿ywane wyszukiwarki i s³owa
kluczowe, czasy trwania odwiedzin, b³êdy HTTP... a nawet wiêcej.
Statystyki mog± byæ uaktualniane z przegl±darki lub schedulera.
Program obs³uguje tak¿e serwery wirtualne, wtyczki i wiele innych
rzeczy.

%prep
%setup -q
%patch -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/awstats/lang
install -d $RPM_BUILD_ROOT%{_datadir}/awstats/lib
install -d $RPM_BUILD_ROOT%{_datadir}/awstats/plugins/example
install -d $RPM_BUILD_ROOT%{wwwdir}/cgi-bin
install -d $RPM_BUILD_ROOT%{wwwdir}/html/icon/browser
install -d $RPM_BUILD_ROOT%{wwwdir}/html/icon/clock
install -d $RPM_BUILD_ROOT%{wwwdir}/html/icon/cpu
install -d $RPM_BUILD_ROOT%{wwwdir}/html/icon/flags
install -d $RPM_BUILD_ROOT%{wwwdir}/html/icon/os
install -d $RPM_BUILD_ROOT%{wwwdir}/html/icon/other
#mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/awstats

install -m 755 tools/logresolvemerge.pl $RPM_BUILD_ROOT%{_bindir}/logresolvemerge.pl
install -m 755 tools/awstats_buildstaticpages.pl $RPM_BUILD_ROOT%{_bindir}/awstats_buildstaticpages.pl
install -m 755 tools/awstats_exportlib.pl $RPM_BUILD_ROOT%{_bindir}/awstats_exportlib.pl
install -m 755 tools/awstats_updateall.pl $RPM_BUILD_ROOT%{_bindir}/awstats_updateall.pl
install -m 755 wwwroot/cgi-bin/awstats.pl $RPM_BUILD_ROOT%{wwwdir}/cgi-bin/awstats.pl
install -m 755 wwwroot/cgi-bin/lib/* $RPM_BUILD_ROOT%{_datadir}/awstats/lib
install -m 755 wwwroot/cgi-bin/plugins/*.pm $RPM_BUILD_ROOT%{_datadir}/awstats/plugins
install -m 755 wwwroot/cgi-bin/plugins/example/* $RPM_BUILD_ROOT%{_datadir}/awstats/plugins/example
install wwwroot/cgi-bin/awstats.model.conf $RPM_BUILD_ROOT%{_sysconfdir}/awstats.conf
install -m 444 wwwroot/icon/browser/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/browser
install -m 444 wwwroot/icon/clock/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/clock
install -m 444 wwwroot/icon/cpu/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/cpu
install -m 444 wwwroot/icon/flags/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/flags
install -m 444 wwwroot/icon/os/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/os
install -m 444 wwwroot/icon/other/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/other
install -m 444 wwwroot/cgi-bin/lang/* $RPM_BUILD_ROOT%{_datadir}/awstats/lang
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/00awstats

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.TXT docs/*
%config %{_sysconfdir}/awstats.conf
%attr(750,root,root) %{_sysconfdir}/cron.hourly/00awstats
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
%attr(750,root,root) %{wwwdir}/cgi-bin/*
%{wwwdir}/html/*
