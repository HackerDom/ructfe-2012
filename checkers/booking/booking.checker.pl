#!/usr/bin/perl

use LWP::UserAgent;

use constant {
	DEBUG => 0,

	CHECKER_OK => 101,
	CHECKER_NOFLAG => 102,
	CHECKER_MUMBLE => 103,
	CHECKER_DOWN => 104,
	CHECKER_ERROR => 110
};

# TODO : актуализировать
@agents = (
  "Ubuntu APT-HTTP/1.3 (0.7.23.1ubuntu2)",
  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.215 Safari/535.1",
  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.205 Safari/534.16",
  "curl/7.19.5 (i586-pc-mingw32msvc) libcurl/7.19.5 OpenSSL/0.9.8l zlib/1.2.3",
  "Emacs-W3/4.0pre.46 URL/p4.0pre.46 (i686-pc-linux; X11)",
  "Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Safari/531.2+ Epiphany/2.29.5",
  "Mozilla/5.0 (X11; U; Linux armv61; en-US; rv:1.9.1b2pre) Gecko/20081015 Fennec/1.0a1",
  "Mozilla/5.0 (Windows NT 7.0; Win64; x64; rv:3.0b2pre) Gecko/20110203 Firefox/4.0b12pre",
  "Mozilla/5.0 (X11; Linux i686; rv:6.0.2) Gecko/20100101 Firefox/6.0.2",
  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0) Gecko/20100101 Firefox/5.0",
  "Mozilla/5.0 (Linux; U; Android 1.1; en-gb; dream) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2",
  "Mozilla/4.5 RPT-HTTPClient/0.3-2",
  "Mozilla/5.0 (compatible; Konqueror/4.0; Linux) KHTML/4.0.5 (like Gecko)",
  "Links (2.1pre31; Linux 2.6.21-omap1 armv6l; x)",
  "Lynx/2.8.5dev.16 libwww-FM/2.14 SSL-MM/1.4.1 OpenSSL/0.9.6b",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100508 SeaMonkey/2.0.4",
  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; InfoPath.3; Creative AutoUpdate v1.40.02)",
  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB6.4; .NET CLR 1.1.4322; FDM; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
  "Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Rogers Hi�Speed Internet; (R1 1.3))",
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6",
  "Opera/9.80 (J2ME/MIDP; Opera Mini/4.2.13221/25.623; U; en) Presto/2.5.25 Version/10.54",
  "Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/19.916; U; en) Presto/2.5.25",
  "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
  "Wget/1.8.1"
);

@dates = ("24NOV", "25NOV", "26NOV", "27NOV", "28NOV", "29NOV", "30NOV");

@names = (
     "COB", "MASON", "WILLIAM", "JAYDEN", "NOAH", "MICHAEL", "ETHAN",
     "ALEXANDER", "AIDEN", "DANIEL", "ANTHONY", "MATTHEW", "ELIJAH",
     "JOSHUA", "LIAM", "ANDREW", "JAMES", "DAVID", "BENJAMIN",
     "LOGAN", "CHRISTOPHER", "JOSEPH", "JACKSON", "GABRIEL", "RYAN",
     "SAMUEL", "JOHN", "NATHAN", "LUCAS", "CHRISTIAN", "JONATHAN",
     "CALEB", "DYLAN", "LANDON", "ISAAC", "GAVIN", "BRAYDEN",
     "TYLER", "LUKE", "EVAN", "CARTER", "NICHOLAS", "ISAIAH",
     "OWEN", "JACK", "JORDAN", "BRANDON", "WYATT", "JULIAN",
     "AARON", "JEREMIAH", "ANGEL", "CAMERON", "CONNOR", "HUNTER",
     "ADRIAN", "HENRY", "ELI", "JUSTIN", "AUSTIN", "ROBERT",
     "CHARLES", "THOMAS", "ZACHARY", "JOSE", "LEVI", "KEVIN",
     "SEBASTIAN", "CHASE", "AYDEN", "JASON", "IAN", "BLAKE",
     "COLTON", "BENTLEY", "DOMINIC", "XAVIER", "OLIVER", "PARKER",
     "JOSIAH", "ADAM", "COOPER", "BRODY", "NATHANIEL", "CARSON",
     "JAXON", "TRISTAN", "LUIS", "JUAN", "HAYDEN", "CARLOS",
     "JESUS", "NOLAN", "COLE", "ALEX", "MAX", "GRAYSON",
     "BRYSON", "DIEGO", "JADEN", "VINCENT", "EASTON", "ERIC",
     "MICAH", "KAYDEN", "JACE", "AIDAN", "RYDER", "ASHTON",
     "BRYAN", "RILEY", "HUDSON", "ASHER", "BRYCE", "MILES",
     "KALEB", "GIOVANNI", "ANTONIO", "KADEN", "COLIN", "KYLE",
     "BRIAN", "TIMOTHY", "STEVEN", "SEAN", "MIGUEL", "RICHARD",
     "IVAN", "JAKE", "ALEJANDRO", "SANTIAGO", "AXEL", "JOEL",
     "MAXWELL", "BRADY", "CADEN", "PRESTON", "DAMIAN", "ELIAS",
     "JAXSON", "JESSE", "VICTOR", "PATRICK", "JONAH", "MARCUS",
     "RYLAN", "EMMANUEL", "EDWARD", "LEONARDO", "CAYDEN", "GRANT",
     "JEREMY", "BRAXTON", "GAGE", "JUDE", "WESLEY", "DEVIN",
     "ROMAN", "MARK", "CAMDEN", "KAIDEN", "OSCAR", "ALAN"
);

@surnames = (
     "SMITH", "JOHNSON", "WILLIAMS", "JONES", "BROWN", "DAVIS", "MILLER",
     "WILSON", "MOORE", "TAYLOR", "ANDERSON", "THOMAS", "JACKSON", "WHITE",
     "HARRIS", "MARTIN", "THOMPSON", "GARCIA", "MARTINEZ", "ROBINSON", "CLARK",
     "RODRIGUEZ", "LEWIS", "LEE", "WALKER", "HALL", "ALLEN", "YOUNG", "GRIFFIN",
     "HERNANDEZ", "KING", "WRIGHT", "LOPEZ", "HILL", "SCOTT", "GREEN",
     "ADAMS", "BAKER", "GONZALEZ", "NELSON", "CARTER", "MITCHELL", "PEREZ",
     "ROBERTS", "TURNER", "PHILLIPS", "CAMPBELL", "PARKER", "EVANS", "EDWARDS",
     "COLLINS", "STEWART", "SANCHEZ", "MORRIS", "ROGERS", "REED", "COOK",
     "MORGAN", "BELL", "MURPHY", "BAILEY", "RIVERA", "COOPER", "RICHARDSON",
     "COX", "HOWARD", "WARD", "TORRES", "PETERSON", "GRAY", "RAMIREZ",
     "JAMES", "WATSON", "BROOKS", "KELLY", "SANDERS", "PRICE", "BENNETT",
     "WOOD", "BARNES", "ROSS", "HENDERSON", "COLEMAN", "JENKINS", "PERRY",
     "POWELL", "LONG", "PATTERSON", "HUGHES", "FLORES", "WASHINGTON", "BUTLER",
     "SIMMONS", "FOSTER", "GONZALES", "BRYANT", "ALEXANDER", "RUSSELL",
     "DIAZ", "HAYES", "MYERS", "FORD", "HAMILTON", "GRAHAM", "SULLIVAN",
     "WALLACE", "WOODS", "COLE", "WEST", "JORDAN", "OWENS", "REYNOLDS",
     "FISHER", "ELLIS", "HARRISON", "GIBSON", "MCDONALD", "CRUZ", "MARSHALL",
     "ORTIZ", "GOMEZ", "MURRAY", "FREEMAN", "WELLS", "WEBB", "SIMPSON",
     "STEVENS", "TUCKER", "PORTER", "HUNTER", "HICKS", "CRAWFORD", "HENRY",
     "BOYD", "MASON", "MORALES", "KENNEDY", "WARREN", "DIXON", "RAMOS",
     "REYES", "BURNS", "GORDON", "SHAW", "HOLMES", "RICE", "ROBERTSON",
     "HUNT", "BLACK", "DANIELS", "PALMER", "MILLS", "NICHOLS", "GRANT",
     "KNIGHT", "FERGUSON", "ROSE", "STONE", "HAWKINS", "DUNN", "PERKINS",
     "HUDSON", "SPENCER", "GARDNER", "STEPHENS", "PAYNE", "PIERCE", "BERRY",
     "MATTHEWS", "ARNOLD", "WAGNER", "WILLIS", "RAY", "WATKINS", "OLSON",
     "CARROLL", "DUNCAN", "SNYDER", "HART", "CUNNINGHAM", "BRADLEY", "LANE",
     "ANDREWS", "RUIZ", "HARPER", "FOX", "RILEY", "ARMSTRONG", "CARPENTER",
     "WEAVER", "GREENE", "LAWRENCE", "ELLIOTT", "CHAVEZ", "SIMS", "AUSTIN",
     "PETERS", "KELLEY", "FRANKLIN", "LAWSON", "FIELDS", "GUTIERREZ", "RYAN",
     "SCHMIDT", "CARR", "VASQUEZ", "CASTILLO", "WHEELER", "CHAPMAN", "OLIVER",
     "MONTGOMERY", "RICHARDS", "WILLIAMSON", "JOHNSTON", "BANKS", "MEYER",
     "MCCOY", "HOWELL", "ALVAREZ", "MORRISON", "HANSEN", "FERNANDEZ", "GARZA",
     "HARVEY", "LITTLE", "BURTON", "STANLEY", "NGUYEN", "GEORGE", "JACOBS"
);

sub is_error {
	return /\<title\>ERROR/ for shift;
}

$port = 8000;
($mode, $ip, $id, $flag) = @ARGV;
%handlers = (
	'check' => \&check,
	'put' => \&put,
	'get' => \&get
);

$ua = LWP::UserAgent->new;
$ua->agent ($agents [int rand @agents]);

$url = "http://$ip:$port";

$handlers {$mode}->($id, $flag);

sub do_exit {
	my ($code, $msg, $log) = @_;

	if (DEBUG) { $msg = "\nOK" if CHECKER_OK == $code; }

	print $msg;
	print STDERR $log;
	exit $code;
}

sub check {
	my $date = $dates [int rand @dates];

	my $r = $ua->get ("$url/search?d=$date");

	do_exit (CHECKER_MUMBLE) if is_error ($r->content);
	do_exit (CHECKER_DOWN, "Could not connect to the service") unless $r->is_success;

	do_exit (CHECKER_OK);
}

sub put {
	my $date = $dates [int rand @dates];

	my ($id, $flag) = @_;
	$flag =~ s/=/%3d/g;

	my $r = $ua->get ("$url/search?d=$date");

	do_exit (CHECKER_MUMBLE, "Could not find flights") if is_error ($r->content);
	do_exit (CHECKER_DOWN, "Could not connect to the service") unless $r->is_success;

	my @flights = ($r->content =~ /\<a href="(.+?)" class="flight"\>/g);
	my $flight = $flights [int rand @flights];

	$r = $ua->get ("$url$flight");

	do_exit (CHECKER_MUMBLE, "Could not view flight") if is_error ($r->content);
	do_exit (CHECKER_DOWN, "Could not connect for view flight") unless $r->is_success;

	my @classes = ($r->content =~ /\<div.*?show_reserve\('(.)'\)/g);
	my $class = $classes [int rand @classes];

	$r->content =~ /FLIGHT «(..) (\d+)»/;
	my ($carrier, $flight) = ($1, $2);

	$r->content =~ /name="from" value="(.{3})"/; $from = $1;
	$r->content =~ /name="to" value="(.{3})"/; $to = $1;

	my $name = $names [int rand @names];
	my $surname = $surnames [int rand @surnames];

	$r = $ua->post ("$url/reserve", {
		name => $name,
		surname => $surname,
		from => $from,
		to => $to,
		date => $date,
		carrier => $carrier,
		flight => $flight,
		class => $class
	});

	do_exit (CHECKER_MUMBLE, "Could not reserve ticket") if is_error ($r->content);
	do_exit (CHECKER_DOWN, "Could not connect for reserve ticket") unless $r->is_success;

	$r->content =~ /RESERVATION ID: (\w{6})/;
	my $rid = $1;

	my $seat = (sprintf "%02d", int rand 31) . (['A' .. 'J']->[int rand 10]);
	$ua->get ("$url/buy?r=$rid&c=$flag&s=$seat");

	do_exit (CHECKER_MUMBLE, "Could not buy ticket") if is_error ($r->content);
	do_exit (CHECKER_DOWN, "Could not connect for buy ticket") unless $r->is_success;

	print $rid;
	do_exit (CHECKER_OK);
}

sub get {
	my ($id, $flag) = @_;

	my $r = $ua->get ("$url/view?r=$id");
	do_exit (CHECKER_MUMBLE, "Could not view ticket") if is_error ($r->content);
	do_exit (CHECKER_DOWN, "Could not connect for view ticket") unless $r->is_success;

	do_exit (CHECKER_NOFLAG, "Flag not found") unless $r->content =~ qr/$flag/;
	do_exit (CHECKER_OK);
}

