use strict;
#  Author: Audris Mockus
#
#Extract each revision from cvs log output
#
use Time::Local;

my %paths = ();
my $comments = "";
my ($rev, $login, $date, $line, $comments) = ("","","", "");
my ($getHeader, $getPaths, $getComments) = (0, 0, 0);

sub output {
	foreach my $f (keys %paths){
		$line =~ s/1 line/1/;
		$line =~ s/ lines//;
		$comments =~ s/\r/ /g;
		$comments =~ s/\n/__NEWLINE__/g;
		print "$rev\;$login\;$line\;$date\;$f\;$paths{$f}\;$comments\n";
	}
	%paths = ();
	($rev, $date, $login, $line, $comments) = ("","","", "");	
}


while(<STDIN>){
	chop ();	
	#catch end of last revision information
	if (/^------------------------------------------------------------------------$/){
		&output () if $getComments;
		#print STDERR "here $getPaths $getHeader $getComments\n"; 
		$getHeader=1;$getPaths=0;$getComments=0;
		next;
	}
	#process file header
	if ($getHeader){
		$_ =~ s/ \| /\|/g;
		($rev, $login, $date, $line) = split(/\|/, $_, -1);
		$getHeader = 0;
		#print STDERR "getHeader $rev, $login, $date, $line\n"; 
	}
	if (/^Changed paths:/){
		$getPaths = 1;
		next;
	}
	if ($getPaths){
		if ($_ =~ /^$/){
			$getPaths = 0;
			$getComments = 1;
			next;
		}
		$_ =~ s/^\s*//;
		$_ =~ s/ \((.*)\)$//; #remove (from /branches/spark1_1/resource/icons/icon_radio buttonon_on.jpg:5368)
		my $from = $1;
		$from =~ s/^from //;
		my ($type, @rest) = split(/ /, $_, -1);
		$paths{(join ' ', @rest)}="$type:$from";
		#print STDERR "getPaths $type:$from\n"; 
	}
	if ($getComments){
		$comments .= "$_\n";
	}				
}






