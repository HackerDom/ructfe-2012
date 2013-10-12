#!/usr/bin/perl -lw

use strict;

my ($SERVICE_OK, $FLAG_GET_ERROR, $SERVICE_CORRUPT, $SERVICE_FAIL, $INTERNAL_ERROR) = (101, 102, 103, 104, 110);
my %MODES = (check => \&check, get => \&get, put => \&put);

sub fail {
	print $_[1] if(@_ > 1);
	exit $_[0];
}

my $sclient_port = 10900;
my $service_port = 10901;
my ($mode, $ip) = (shift // '', shift // '');
unless ($mode ~~ %MODES and $ip =~ /(\d{1,3}\.){3}\d{1,3}/) {
	fail($INTERNAL_ERROR, "Invalid input data. Corrupt mode or ip address.");
}

my $jury_secret = "B[Lf;t<bnmYtkmpzXnjKb";
my @clients = (
	['10.23.201.150',10901],
	['10.23.201.150',10902],
	['10.23.201.150',10903],
	['10.23.201.150',10904],
	['10.23.201.150',10905],
	['10.23.201.150',10906],
	['10.23.201.150',10907],
	['10.23.201.150',10908],
	['10.23.201.150',10909],
	['10.23.201.150',10910],
	['10.23.201.150',10911],
	['10.23.201.150',10912],
	['10.23.201.150',10913],
	['10.23.201.150',10914],
	['10.23.201.150',10915],
	['10.23.201.150',10916],
	['10.23.201.150',10917],
	['10.23.201.150',10918],
	['10.23.201.150',10919],
	['10.23.201.150',10920],
	['10.23.201.150',10921],
	['10.23.201.150',10922],
	['10.23.201.150',10923],
	['10.23.201.150',10924],
	['10.23.201.150',10925],
	['10.23.201.150',10926],
	['10.23.201.150',10927],
	['10.23.201.150',10928],
	['10.23.201.150',10929],
	['10.23.201.150',10930],
	['10.23.201.150',10931],
	['10.23.201.150',10932],
	['10.23.201.150',10933],
	['10.23.201.150',10934],
	['10.23.201.150',10935],
	['10.23.201.150',10936],
	['10.23.201.150',10937],
	['10.23.201.150',10938],
	['10.23.201.150',10939],
	['10.23.201.150',10940]
);
my @num = (4,8,15,16,23,42);
exit $MODES{$mode}->(@ARGV);

sub send_to_service {
	my ($address,$port,$data) = @_;
	use IO::Socket::INET;
	$| = 1;
	my $socket = new IO::Socket::INET (
		PeerHost => $address,
		PeerPort => $port,
		Proto => 'tcp',
		Timeout => 25
	) or fail($SERVICE_FAIL, "$address:$port $!");
	print $socket "$data\n";
	$data = <$socket>;
	#sysread($socket, $data, 4096);
	$socket->close();
	return $data;
}

sub generate_random_string {
	my $length_of_randomstring=shift || 10;
	my @chars=('a'..'z','A'..'Z','0'..'9','_');
	my $random_string;
	foreach (1..$length_of_randomstring) 
	{
		$random_string.=$chars[rand @chars];
	}
	return $random_string;
}

sub check {
	send_to_service($ip, $service_port, generate_random_string(10).'|PUSH|'.generate_random_string(10).'|{"name": "update", "value": "record'.$num[int(rand(@num))].'"}');
    return $SERVICE_OK;
}

sub get {
    my ($id, $flag) = @_;
	my ($service_id, $client_id, $client_ip, $client_port) = split(/:/, $id);
	my $res = send_to_service($ip, $sclient_port, $client_id.':0:'.$service_id);
	if ($res =~ /$flag/s) {
		return $SERVICE_OK;
	}
	print "Flag receive failed";
	return $FLAG_GET_ERROR;
}

sub put {
    my ($id, $flag) = @_;
	my $service_id = generate_random_string(10);
	my $client_id = generate_random_string(10);
	print STDERR send_to_service($ip, $service_port, $service_id.'|PUSH|'.$client_id.'|'.$flag);
	sleep(3);
	my ($client_ip, $client_port) = @{$clients[int(rand(@clients))]};
	#print STDERR "|$client_ip:$client_port";
	my $res = send_to_service($ip, $sclient_port, $client_id.':0:'.$service_id);
	#my $res = send_to_service($client_ip, $client_port, $jury_secret.'|'.$ip.'|'.$client_id.'|'.$service_id);
	if ($res =~ /$flag/s) {
		print $service_id.':'.$client_id.':'.$client_ip.':'.$client_port;
		return $SERVICE_OK;
	}
	print STDERR $res;
	print "Flag install failed";
	return $SERVICE_CORRUPT;
}
