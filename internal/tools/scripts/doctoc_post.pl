#!/usr/bin/perl
use strict;
use warnings;
use File::Find;

my ($root) = @ARGV or die "Usage: $0 <directory>\n";

find(
    {
        wanted => sub {
            return unless -f $_;
            return unless $_ =~ /\.md$/i;   # only Markdown files

            my $file = $File::Find::name;

            local $/ = undef;
            open my $fh, '<', $file or die "Cannot read $file: $!";
            my $content = <$fh>;
            close $fh;

            my $orig = $content;

            # Replace END marker
            $content =~ s{<!--\s*END\ doctoc\ generated\ TOC\ please\ keep\ comment\ here\ to\ allow\ auto\ update\s*-->}{<!-- END doctoc -->}gx;

            # Replace START block (two lines)
            $content =~ s{
                <!--\s*START\ doctoc\ generated\ TOC\ please\ keep\ comment\ here\ to\ allow\ auto\ update\s*-->\s*
                <!--\s*DON'T\ EDIT\ THIS\ SECTION,\ INSTEAD\ RE-RUN\ doctoc\ TO\ UPDATE\s*-->
            }{<!-- START doctoc -->}gxs;

            # Only write if changed
            return if $content eq $orig;

            open my $out, '>', $file or die "Cannot write $file: $!";
            print $out $content;
            close $out;

            print "Updated: $file\n";
        },
        no_chdir => 1,
    },
    $root
);
