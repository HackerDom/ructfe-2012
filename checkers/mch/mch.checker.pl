#!/usr/bin/perl -lw

use strict;
use Mojo::UserAgent;
use Mojo::URL;
use Mojo::Asset::Memory;
use Mojo::Asset::File;
use Mojo::Log;
use Data::Dumper;

$Data::Dumper::Indent = 0;
$Data::Dumper::Terse = 1;

my ($SERVICE_OK, $FLAG_GET_ERROR, $SERVICE_CORRUPT, $SERVICE_FAIL, $INTERNAL_ERROR) = (101, 102, 103, 104, 110);
my %MODES = (check => \&check, get => \&get, put => \&put);

my ($mode, $ip) = (shift // '', shift // '');
unless ($mode ~~ %MODES and $ip =~ /(\d{1,3}\.){3}\d{1,3}/) {
    warn "Invalid input data. Corrupt mode or ip address.";
    exit $INTERNAL_ERROR;
}

mkdir 'sessions';
my $service_url = Mojo::URL->new("http://$ip:8080/");
my $ua = Mojo::UserAgent->new(max_redirects => 5);
my $log = Mojo::Log->new;
exit $MODES{$mode}->(@ARGV);

sub check {
    $service_url->path('/');
    $log->info("CHECK for $ip");
    my $tx = $ua->get($service_url);
    if (my $res = $tx->success) {
        if (my $head = $res->dom->at('div.container h1')) {
            if ($head->text eq 'Mch > index') {
                return $SERVICE_OK;
            } else {
                print 'Index page invalid';
                return $SERVICE_CORRUPT;
            }
        } else {
            print 'Index page invalid';
            return $SERVICE_CORRUPT;
        }
    } else {
        my ($err, $code) = $tx->error;
        if ($code) {
            $log->info("Finish get for $service_url fail: [$code:$err]");
            print "GET $service_url, $code:$err";
            return $SERVICE_CORRUPT;
        } else {
            $log->info("Finish get for $service_url fail: [$err]");
            print "GET $service_url, $err";
            return $SERVICE_FAIL;
        }
    }
}

sub get {
    my ($id, $flag) = @_;
    $service_url->path('/');
    $log->info("GET for $ip: [$id:$flag]");
    my $asset = Mojo::Asset::File->new(path => "sessions/$id");
    my $cookies = Mojo::Cookie::Response->new->parse($asset->slurp);
    $ua->cookie_jar(Mojo::UserAgent::CookieJar->new->add(@$cookies));
    $log->info("Start get for $service_url");
    my $tx = $ua->get($service_url);
    if (my $res = $tx->success) {
        $log->info("Finish get for $service_url success");
        if (my $data = $res->dom->at('div.container span.data')) {
            $log->info("Private data is [$data]");
            if ($data->text eq '') {
                $service_url->path('/get_updates');
                $service_url->query(ts => '0', c => '[]');
                $log->info("Start get for $service_url");
                my $tx = $ua->get($service_url);
                if (my $res = $tx->success) {
                    $log->info("Finish get for $service_url success: " . Dumper($res->json));
                    my @chats = @{$res->json->{chats}};
                    my $find = 0;
                    L: for my $chat (@chats) {
                        for my $message (@{$chat->{messages}}) {
                            if ($flag eq $message->{data}) {
                                $find = 1;
                                last L;
                            }
                        }
                    }
                    if ($find == 1) {
                        return $SERVICE_OK;
                    } else {
                        print 'Message not found in chat';
                        return $FLAG_GET_ERROR;
                    }
                } else {
                    my ($err, $code) = $tx->error;
                    if ($code) {
                        $log->info("Finish get for $service_url fail: [$code:$err]");
                        print "GET $service_url, $code:$err";
                        return $SERVICE_CORRUPT;
                    } else {
                        $log->info("Finish get for $service_url fail: [$err]");
                        print "GET $service_url, $err";
                        return $SERVICE_FAIL;
                    }
                }
            } else {
                if ($flag eq $data->text) {
                    return $SERVICE_OK;
                } else {
                    print 'Private info not found';
                    return $FLAG_GET_ERROR;
                }
            }
        } else {
            print 'Private info not found';
            return $SERVICE_CORRUPT;
        }
    } else {
        my ($err, $code) = $tx->error;
        if ($code) {
            $log->info("Finish get for $service_url fail: [$code:$err]");
            print "GET $service_url, $code:$err";
            return $SERVICE_CORRUPT;
        } else {
            $log->info("Finish get for $service_url fail: [$err]");
            print "GET $service_url, $err";
            return $SERVICE_FAIL;
        }
    }
}

sub put {
    my ($id, $flag) = @_;
    my $flag_in_message = int rand 2;
    $service_url->path('/login');
    $log->info("PUT for $ip: [$id:$flag]");
    $log->info("Flag in message: $flag_in_message");
    my $post_data = {name => $id, data => $flag_in_message ? '' : $flag};
    $log->info("Start post_form for $service_url with " . Dumper($post_data));
    my $tx = $ua->post_form($service_url => $post_data);
    if (my $res = $tx->success) {
        $log->info("Finish post_form for $service_url success");
        my @cookies = $ua->cookie_jar->all;
        $log->info("Cookie: " . Dumper(@cookies));
        unless (@cookies) {
            print "Wrong answer while login!";
            return $SERVICE_CORRUPT;
        }
        my $new_id = $cookies[0]->value;
        my $asset = Mojo::Asset::Memory->new;
        $asset->add_chunk($cookies[0]);
        $asset->move_to("sessions/$new_id");
        $log->info("Cookie: $new_id");
        if ($flag_in_message) {
            $service_url->path('/create_chat');
            my $post_data = {name => 'mch', private => 'on'};
            $log->info("Start post_form for $service_url with " . Dumper($post_data));
            my $tx = $ua->post_form($service_url => $post_data);
            if (my $res = $tx->success) {
                $log->info("Finish post_form for $service_url success: " . Dumper($res->json));
                my $chat_id = $res->json->{chat_id};
                $service_url->path('/send_message');
                my $post_data = {chat => $chat_id, data => $flag};
                $log->info("Start post_form for $service_url with " . Dumper($post_data));
                my $tx = $ua->post_form($service_url, $post_data);
                if (my $res = $tx->success) {
                    $log->info("Finish post_form for $service_url success: " . Dumper($res->json));
                    print $new_id;
                    return $SERVICE_OK;
                } else {
                    my ($err, $code) = $tx->error;
                    if ($code) {
                        $log->info("Finish post_form for $service_url fail: [$code:$err]");
                        print "POST $service_url, $code:$err";
                        return $SERVICE_CORRUPT;
                    } else {
                        $log->info("Finish post_form for $service_url fail: [$err]");
                        print "POST $service_url, $err";
                        return $SERVICE_FAIL;
                    }
                }
            } else {
                my ($err, $code) = $tx->error;
                if ($code) {
                    $log->info("Finish post_form for $service_url fail: [$code:$err]");
                    print "POST $service_url, $code:$err";
                    return $SERVICE_CORRUPT;
                } else {
                    $log->info("Finish post_form for $service_url fail: [$err]");
                    print "POST $service_url, $err";
                    return $SERVICE_FAIL;
                }
            }
        } else {
            print $new_id;
            return $SERVICE_OK;
        }
    } else {
        my ($err, $code) = $tx->error;
        if ($code) {
            $log->info("Finish post_form for $service_url fail: [$code:$err]");
            print "POST $service_url, $code:$err";
            return $SERVICE_CORRUPT;
        } else {
            $log->info("Finish post_form for $service_url fail: [$err]");
            print "POST $service_url, $err";
            return $SERVICE_FAIL;
        }
    }
}
