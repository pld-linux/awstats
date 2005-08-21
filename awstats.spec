#
# TODO:
#	- think about some trigger to upgrade from 6.5-1 and older 
#         (I suggest just to forget about those broken version,
#          unfortunately they have already landed in Ac)
#
%include	/usr/lib/rpm/macros.perl
Summary:	Advanced Web Statistics is a free powerful server log file analyzer
Summary(pl):	Zaawansowany program do analizowania log�w serwera
Name:		awstats
Version:	6.5
Release:	1.5
License:	GPL
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
pot�ne i bogate w mo�liwo�ci narz�dzie generuj�ce zaawansowane
graficzne statystyki serwera WWW. Ten analizator log�w serwera dzia�a
z linii polece� lub jako CGI i pokazuje wszystkie informacje zawarte w
logu w postaci graficznych stron WWW. Mo�e analizowa� logi wielu
serwer�w WWW/WAP/proxy, takich jak Apache, IIS, Weblogic, Webstar,
Squid... ale tak�e serwer�w pocztowych lub FTP.

Ten program mo�e mierzy� odwiedziny, odwiedzaj�cych, uwierzytelnionych
u�ytkownik�w, strony, domeny/kraje, najbardziej zaj�te godziny,
odwiedziny robot�w, rodzaje plik�w, u�ywane wyszukiwarki i s�owa
kluczowe, czasy trwania odwiedzin, b��dy HTTP... a nawet wi�cej.
Statystyki mog� by� uaktualniane z przegl�darki lub schedulera.
Program obs�uguje tak�e serwery wirtualne, wtyczki i wiele innych
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
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf
ln -s %{_datadir}/awstats/wwwroot/cgi-bin/awstats.pl $RPM_BUILD_ROOT%{_bindir}

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*/%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.TXT docs/* tools/webmin tools/xslt
%dir %{_sysconfdir}/awstats
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/awstats/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
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
