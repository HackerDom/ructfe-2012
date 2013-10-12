#!/usr/bin/perl -lw

my ($SERVICE_OK, $FLAG_GET_ERROR, $SERVICE_CORRUPT, $SERVICE_FAIL, $INTERNAL_ERROR) = (101, 102, 103, 104, 110);
my %MODES = (check => \&check, get => \&get, put => \&put);

sub fail {
	print $_[1] if(@_ > 1);
	exit $_[0];
}

my $service_port = 10800;
my ($mode, $ip) = (shift // '', shift // '');
unless ($mode ~~ %MODES and $ip =~ /(\d{1,3}\.){3}\d{1,3}/) {
	fail($INTERNAL_ERROR, "Invalid input data. Corrupt mode or ip address.");
}

my $dd;

use LWP::UserAgent;
use HTTP::Cookies;
use JSON qw( decode_json );

my $ua = LWP::UserAgent->new;
$ua->timeout(25);
my $cookie_jar = HTTP::Cookies->new;
$ua->cookie_jar($cookie_jar);
my $url = "http://$ip:$service_port";

exit $MODES{$mode}->(@ARGV);

sub do_exit {
	my ($code, $msg, $log) = @_;
	print $msg if (defined $msg);
	print STDERR $log if (defined $log);
	exit $code;
}

sub generate_random_string {
	my $length_of_randomstring=shift || 10;
	my @chars=('a'..'z','0'..'9','_');
	my $random_string;
	foreach (1..$length_of_randomstring) 
	{
		$random_string.=$chars[rand @chars];
	}
	return $random_string;
}
sub login {
	my $user = shift;
	my $r = $ua->get("$url/_ah/login?email=$user&action=Login&continue=http\%3A\%2F\%2F$ip\%3A$service_port%2F");
	do_exit($SERVICE_FAIL, "Service login error") unless $r->is_success;
	$cookie_jar->extract_cookies($r);
}
sub new_user {
	return generate_random_string(6).'@'.generate_random_string(6).'org';
}
sub check {
	if (int(rand(3)) == 1) {
		login(new_user());
	}

	my $r = $ua->get($url);
	do_exit($SERVICE_FAIL, "Service error") unless $r->is_success;
	do_exit($SERVICE_OK);
}

sub put {
	my ($id, $flag) = @_;

	my $user = new_user();
	login($user);
	my $project = generate_random_string(10);
	my $file = generate_random_string(10);

# project types
	my $r = $ua->get("$url/api/project_types/list");
	do_exit($SERVICE_CORRUPT, "Could not get project types") unless $r->is_success;

	my $v;
	eval {
		$v = decode_json($r->content);
	};
	if ($@)
	{
		do_exit($SERVICE_CORRUPT, "Wrong JSON");
	}
	do_exit($SERVICE_CORRUPT, "Could not get project types") if (!$v->{'success'});
	my $t = undef;
	for (@{$v->{'data'}}) {
		if($_->{'name'} eq 'Flight Process') {
			$t = $_->{'id'};
		}
	}
	do_exit($SERVICE_CORRUPT, "Could not get project type Flight Process") if (!defined($t));

# add project
	$r = $ua->get("$url/api/projects/add?name=${project}&type=${t}");
	do_exit($SERVICE_CORRUPT, "Could not add project") unless $r->is_success;

	eval {
		$v = decode_json($r->content);
	};
	if ($@)
	{
		do_exit($SERVICE_CORRUPT, "Wrong JSON");
	}
	do_exit($SERVICE_CORRUPT, "Could not add project") if (!$v->{'success'});

# set project private
	$r = $ua->get("$url/api/projects/set_properties/${project}?description=&public=false&status=0");
	#do_exit($SERVICE_CORRUPT, "Could not set project private") unless $r->is_success;

	#$v = decode_json($r->content);
	#do_exit($SERVICE_CORRUPT, "Could not set project private") if (!$v->{'success'});

# file types
	$r = $ua->get("$url/api/project_types/list_files/${t}");
	do_exit($SERVICE_CORRUPT, "Could not get file types") unless $r->is_success;

	eval {
		$v = decode_json($r->content);
	};
	if ($@)
	{
		do_exit($SERVICE_CORRUPT, "Wrong JSON");
	}
	do_exit($SERVICE_CORRUPT, "Could not get file types") if (!$v->{'success'});
	$t = undef;
	for (@{$v->{'data'}}) {
		if($_->{'name'} eq 'Flight Process Markup Language') {
			$t = $_->{'id'};
		}
	}
	do_exit($SERVICE_CORRUPT, "Could not get file type Flight Process Markup Language") if (!defined($t));

# add file
	my $gen = "<nodes><node><links><link><to>2</to></link></links><id>1</id><x>-237</x><y>-12.5</y><type>takeoff</type></node><node><links><link><to>3</to></link><link><to>9</to><activation>1</activation><stream>1</stream></link></links><id>2</id><x>-122</x><y>-66.5</y><type>log</type><state>qq</state><message>flagflagflagflagflagflagflagflag=</message></node><node><links><link><to>4</to></link></links><id>3</id><x>24</x><y>-61.5</y><type>land</type></node><node><links><link><to>5</to></link></links><id>4</id><x>122</x><y>21.5</y><type>b_unload</type></node><node><links><link><to>6</to></link></links><id>5</id><x>254</x><y>30.5</y><type>ladder</type></node><node><links><link><to>7</to></link></links><id>6</id><x>387</x><y>-22.5</y><type>bus</type></node><node><links><link><to>8</to><activation>1</activation><stream>1</stream></link></links><id>7</id><x>249</x><y>-110.5</y><type>registration_request</type><user>dkjdlfg</user><service_pass>$flag</service_pass></node><node><links><array/></links><id>8</id><x>133</x><y>-143.5</y><type>p_load</type></node><node><id>9</id><x>-23</x><y>-140.5</y><type>crash</type><links><array/></links></node></nodes>";
	$r = $ua->post("$url/api/files/add/${project}/?name=${file}&type=${t}&category=", {'content' => $gen});
	do_exit($SERVICE_CORRUPT, "Could not add file") unless $r->is_success;

	eval {
		$v = decode_json($r->content);
	};
	if ($@)
	{
		do_exit($SERVICE_CORRUPT, "Wrong JSON");
	}
	do_exit($SERVICE_CORRUPT, "Could not add file") if (!$v->{'success'});
	$t = $v->{'data'}{'file'}{'id'};
	$file = $t;

# compile file
	$r = $ua->post("$url/api/compile/start/${project}/?file_id=${t}&start_params=%7B'created_by'%3A+'perl script'%7D");
	do_exit($SERVICE_CORRUPT, "Could not compile file") unless $r->is_success;

	eval {
		$v = decode_json($r->content);
	};
	if ($@)
	{
		do_exit($SERVICE_CORRUPT, "Wrong JSON");
	}
	do_exit($SERVICE_CORRUPT, "Could not compile file") if (!$v->{'success'});

	$dd = $v->{'data'};
	do_exit($FLAG_GET_ERROR, "Compilation error") if ($dd!~/$flag/s);

	print $user.'|'.$project.'|'.$file;
	do_exit($SERVICE_OK);
}

sub get {
	my ($id, $flag) = @_;

	my ($user,$project,$file) = split(/\|/, $id);

	login($user);

# compile file
	my $r = $ua->post("$url/api/compile/start/${project}/?file_id=${file}&start_params=%7B'created_by'%3A+'perl script'%7D");
	do_exit($SERVICE_CORRUPT, "Could not compile file") unless $r->is_success;

	my $v;
	eval {
		$v = decode_json($r->content);
	};
	if ($@)
	{
		do_exit($SERVICE_CORRUPT, "Wrong JSON");
	}
	do_exit($SERVICE_CORRUPT, "Could not compile file") if (!$v->{'success'});

	$dd = $v->{'data'};
	do_exit($FLAG_GET_ERROR, "Compilation error") if ($dd!~/$flag/s);

	do_exit($SERVICE_OK);
}
