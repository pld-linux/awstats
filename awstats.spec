# TODO:
# - think about some trigger to upgrade from 6.5-1 and older
#   (I suggest just to forget about those broken version,
#   unfortunately they have already landed in Ac)
# - apache1 config
# - security CVE-2006-1945, CVE-2006-2237: http://security.gentoo.org/glsa/glsa-200606-06.xml
%include	/usr/lib/rpm/macros.perl
Summary:	Advanced Web Statistics is a free powerful server log file analyzer
Summary(pl.UTF-8):	Zaawansowany program do analizowania logów serwera
Name:		awstats
Version:	7.7
Release:	2
License:	GPL v3+
Group:		Applications/Networking
Source0:	http://awstats.sourceforge.net/files/%{name}-%{version}.tar.gz
# Source0-md5:	a69ee5127fcf38b12d47856fab3d57e4
Source1:	%{name}.crontab
Source2:	%{name}-httpd.conf
Source3:	%{name}.conf
Source4:	%{name}-lighttpd.conf
Patch0:		%{name}_conf.patch
Patch1:		%{name}-created_dir_mode.patch
Patch2:		%{name}-PLD.patch
URL:		http://awstats.sourceforge.net/
BuildRequires:	rpm-perlprov
BuildRequires:	rpmbuild(macros) >= 1.264
Requires(triggerpostun):	sed >= 4.0
Requires:	perl-Geo-IP
Requires:	perl-Storable
Requires:	perl-Time-HiRes
Requires:	webapps
Suggests:	crondaemon
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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

%description -l pl.UTF-8
awstats (Advanced Web Statistics - zaawansowane statystyki WWW) to
potężne i bogate w możliwości narzędzie generujące zaawansowane
graficzne statystyki serwera WWW. Ten analizator logów serwera działa
z linii poleceń lub jako CGI i pokazuje wszystkie informacje zawarte w
logu w postaci graficznych stron WWW. Może analizować logi wielu
serwerów WWW/WAP/proxy, takich jak Apache, IIS, Weblogic, Webstar,
Squid... ale także serwerów pocztowych lub FTP.

Ten program może mierzyć odwiedziny, odwiedzających, uwierzytelnionych
użytkowników, strony, domeny/kraje, najbardziej zajęte godziny,
odwiedziny robotów, rodzaje plików, używane wyszukiwarki i słowa
kluczowe, czasy trwania odwiedzin, błędy HTTP... a nawet więcej.
Statystyki mogą być uaktualniane z przeglądarki lub schedulera.
Program obsługuje także serwery wirtualne, wtyczki i wiele innych
rzeczy.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
find . '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.d,%{_sysconfdir},%{_bindir}} \
	$RPM_BUILD_ROOT{%{_datadir}/awstats,/var/lib/awstats}

install -p tools/awstats_* $RPM_BUILD_ROOT%{_bindir}
install -p tools/{logresolvemerge,maillogconvert,urlaliasbuilder}.pl $RPM_BUILD_ROOT%{_bindir}
cp -r wwwroot $RPM_BUILD_ROOT%{_datadir}/awstats
mv $RPM_BUILD_ROOT%{_datadir}/awstats/wwwroot/cgi-bin/awstats.model.conf $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_datadir}/awstats/wwwroot/cgi-bin/{lang,lib,plugins} $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/awstats
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
ln -s %{_datadir}/awstats/wwwroot/cgi-bin/awstats.pl $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- %{name} < 6.5-2.1
# rescue app configs.
for i in awstats.conf awstats.model.conf; do
	if [ -f /etc/%{name}/$i.rpmsave ]; then
		mv -f %{_sysconfdir}/$i{,.rpmnew}
		mv -f /etc/%{name}/$i.rpmsave %{_sysconfdir}/$i
	fi
done

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache.conf.rpmsave ]; then
	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/%{name}/apache.conf.rpmsave
fi

rm -f /etc/httpd/httpd.conf/99_%{name}.conf
/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc README.md docs/* tools/webmin tools/xslt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(644,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/awstats*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/awstats

%attr(755,root,root) %{_bindir}/*.pl
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/lang
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/plugins
%dir %{_datadir}/%{name}/wwwroot
%dir %{_datadir}/%{name}/wwwroot/cgi-bin
%attr(755,root,root) %{_datadir}/%{name}/wwwroot/cgi-bin/awdownloadcsv.pl
%attr(755,root,root) %{_datadir}/%{name}/wwwroot/cgi-bin/awredir.pl
%attr(755,root,root) %{_datadir}/%{name}/wwwroot/cgi-bin/awstats.pl
%{_datadir}/%{name}/wwwroot/classes
%{_datadir}/%{name}/wwwroot/css
%{_datadir}/%{name}/wwwroot/icon
%{_datadir}/%{name}/wwwroot/js
%attr(775,root,stats) /var/lib/%{name}
