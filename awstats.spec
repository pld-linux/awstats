# - SECURITY: http://securitytracker.com/alerts/2004/Aug/1010993.html
%include	/usr/lib/rpm/macros.perl
Summary:	Advanced Web Statistics is a free powerful server log file analyzer
Summary(pl):	Zaawansowany program do analizowania logów serwera
Name:		awstats
Version:	6.2
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://awstats.sourceforge.net/files/%{name}-%{version}.tgz
# Source0-md5:	f538e225340490433ea008c37ec92427
Source1:	%{name}-cron
Patch0:		%{name}_conf.patch
URL:		http://awstats.sourceforge.net/
BuildRequires:	rpm-perlprov
Requires:	perl-Geo-IP
Requires:	perl-Time-HiRes
Requires:	perl-Storable
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		wwwdir	/home/services/httpd

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
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/cron.hourly,%{_bindir}} \
	$RPM_BUILD_ROOT%{_datadir}/awstats/{lang,lib,plugins/example} \
	$RPM_BUILD_ROOT%{wwwdir}/{cgi-bin,html/icon/{browser,clock,cpu,flags,os,other}}

install tools/logresolvemerge.pl $RPM_BUILD_ROOT%{_bindir}/logresolvemerge.pl
install tools/awstats_buildstaticpages.pl $RPM_BUILD_ROOT%{_bindir}/awstats_buildstaticpages.pl
install tools/awstats_exportlib.pl $RPM_BUILD_ROOT%{_bindir}/awstats_exportlib.pl
install tools/awstats_updateall.pl $RPM_BUILD_ROOT%{_bindir}/awstats_updateall.pl
install wwwroot/cgi-bin/awstats.pl $RPM_BUILD_ROOT%{wwwdir}/cgi-bin/awstats.pl
install wwwroot/cgi-bin/lib/* $RPM_BUILD_ROOT%{_datadir}/awstats/lib
install wwwroot/cgi-bin/plugins/*.pm $RPM_BUILD_ROOT%{_datadir}/awstats/plugins
install wwwroot/cgi-bin/plugins/example/* $RPM_BUILD_ROOT%{_datadir}/awstats/plugins/example
install wwwroot/cgi-bin/awstats.model.conf $RPM_BUILD_ROOT%{_sysconfdir}/awstats.conf
install wwwroot/icon/browser/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/browser
install wwwroot/icon/clock/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/clock
install wwwroot/icon/cpu/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/cpu
install wwwroot/icon/flags/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/flags
install wwwroot/icon/os/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/os
install wwwroot/icon/other/* $RPM_BUILD_ROOT%{wwwdir}/html/icon/other
cp -a wwwroot/cgi-bin/lang/* $RPM_BUILD_ROOT%{_datadir}/awstats/lang
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/cron.hourly/00awstats

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.TXT docs/*
%config %{_sysconfdir}/awstats.conf
%attr(750,root,root) %{_sysconfdir}/cron.hourly/00awstats
%attr(755,root,root) %{_bindir}/*
%{_datadir}/*
%attr(750,root,http) %{wwwdir}/cgi-bin/*
%{wwwdir}/html/*
