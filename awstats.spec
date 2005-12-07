#
# TODO:
# - think about some trigger to upgrade from 6.5-1 and older
#         (I suggest just to forget about those broken version,
#          unfortunately they have already landed in Ac)
# - apache1 config
#
%include	/usr/lib/rpm/macros.perl
Summary:	Advanced Web Statistics is a free powerful server log file analyzer
Summary(pl):	Zaawansowany program do analizowania logów serwera
Name:		awstats
Version:	6.5
Release:	2
License:	GPL v2
Group:		Applications/Networking
Source0:	http://awstats.sourceforge.net/files/%{name}-%{version}.tgz
# Source0-md5:	8a4a5f1ad25c45c324182ba369893a5a
Source1:	%{name}.crontab
Source2:	%{name}-httpd.conf
Source3:	%{name}.conf
Patch0:		%{name}_conf.patch
Patch1:		%{name}-created_dir_mode.patch
URL:		http://awstats.sourceforge.net/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.221
Requires(triggerpostun):	sed >= 4.0
Requires:	perl-Geo-IP
Requires:	perl-Time-HiRes
Requires:	perl-Storable
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Advanced Web Statistics is a powerful and featureful tool that
generates advanced web server graphic statistics. This server log
analyzer works from command line or as a CGI and shows you all
information your log contains, in graphical web pages. It can analyze
a lot of web/wap/proxy servers like Apache, IIS, Weblogic, Webstar,
Squid, ... but also mail or FTP servers.

This program can measure visits, unique vistors, authenticated users,
pages, domains/countries, OS busiest times, robot visits, type of
files, search engines/keywords used, visits duration, HTTP errors and
more... Statistics can be updated from a browser or your scheduler.
The program also supports virtual servers, plugins and a lot of
features.

%description -l pl
awstats (Advanced Web Statistics - zaawansowane statystyki WWW) to
potê¿ne i bogate w mo¿liwo¶ci narzêdzie generuj±ce zaawansowane
graficzne statystyki serwera WWW. Ten analizator logów serwera dzia³a
z linii poleceñ lub jako CGI i pokazuje wszystkie informacje zawarte w
logu w postaci graficznych stron WWW. Mo¿e analizowaæ logi wielu
serwerów WWW/WAP/proxy, takich jak Apache, IIS, Weblogic, Webstar,
Squid... ale tak¿e serwerów pocztowych lub FTP.

Ten program mo¿e mierzyæ odwiedziny, odwiedzaj±cych, uwierzytelnionych
u¿ytkowników, strony, domeny/kraje, najbardziej zajête godziny,
odwiedziny robotów, rodzaje plików, u¿ywane wyszukiwarki i s³owa
kluczowe, czasy trwania odwiedzin, b³êdy HTTP... a nawet wiêcej.
Statystyki mog± byæ uaktualniane z przegl±darki lub schedulera.
Program obs³uguje tak¿e serwery wirtualne, wtyczki i wiele innych
rzeczy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{httpd,cron.d},%{_sysconfdir}/awstats,%{_bindir}} \
	$RPM_BUILD_ROOT{%{_datadir}/awstats,/var/lib/awstats}

install tools/awstats_* $RPM_BUILD_ROOT%{_bindir}
install tools/{logresolvemerge,maillogconvert,urlaliasbuilder}.pl $RPM_BUILD_ROOT%{_bindir}
cp -r wwwroot $RPM_BUILD_ROOT%{_datadir}/awstats
mv $RPM_BUILD_ROOT%{_datadir}/awstats/wwwroot/cgi-bin/awstats.model.conf $RPM_BUILD_ROOT%{_sysconfdir}/awstats
mv $RPM_BUILD_ROOT%{_datadir}/awstats/wwwroot/cgi-bin/{lang,lib,plugins} $RPM_BUILD_ROOT%{_datadir}/%{name}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/awstats
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/apache.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
ln -s %{_datadir}/awstats/wwwroot/cgi-bin/awstats.pl $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/awstats/apache.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%triggerpostun -- %{name} < 6.5-1.10
# migrate from old config location (only apache2, as there was no apache1 support)
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/apache-%{name}.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/awstats/apache.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# nuke very-old config location
if [ ! -d /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

# apache2
if [ -d /etc/httpd/httpd.conf ]; then
	ln -sf %{_sysconfdir}/awstats/apache.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd reload 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README.TXT docs/* tools/webmin tools/xslt
%dir %{_sysconfdir}/awstats
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/awstats/awstats*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/awstats/apache.conf
%attr(640,root,root) /etc/cron.d/awstats
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lang
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/wwwroot
%dir %{_datadir}/%{name}/wwwroot/cgi-bin
%attr(755,root,root) %{_datadir}/%{name}/wwwroot/cgi-bin/*
%{_datadir}/%{name}/wwwroot/classes
%{_datadir}/%{name}/wwwroot/css
%{_datadir}/%{name}/wwwroot/icon
%{_datadir}/%{name}/wwwroot/js
%attr(775,root,stats) /var/lib/%{name}
