#/usr/bin/perl

use warnings;
use strict;
use POSIX ":sys_wait_h";

if (@ARGV == 1){
    my $in = $ARGV[0];
    &Single_run($in);
} elsif (@ARGV == 2) {
    my $parallel_num = $ARGV[0];
    my $list_file = $ARGV[1];

    my @shellS = &read_List("$list_file");
    &multiple_process($parallel_num, @shellS);
} else {
    print "Arguments number not correct, the program won\'t run.\n";
    exit 0;
}

sub read_List{
    my $INFILE = shift;
    my @Sample_List = ();
    
    # open FQL, "<$fqList" or die "$!";
    open (LISTF, "<", $INFILE) or die "Error: open file: $INFILE error!\n $!\n"; 
    while (<LISTF>){
        chomp;
        push @Sample_List, $_;
    }
    close LISTF;
    return (@Sample_List);
}

##### Function -- Executate shell script for each sample #####

sub Single_run{
    my $Sample_shell = shift;
    print "sh $Sample_shell >$Sample_shell.log 2>$Sample_shell.err \n";
    system("sh $Sample_shell >$Sample_shell.log 2>$Sample_shell.err");
}

##### Function -- Multiple program processing     #####

sub multiple_process{

    (my $paral_num, my @shellScripts) = @_ ; 
    my $num_proc    = 0;
    my $num_collect = 0;
    my $collect;
    my @all_pid;
    
    $SIG{CHLD} = sub { $num_proc-- };
    
    my $i = 0;
    foreach my $ele (@shellScripts){
        $i ++;
        my $pid = fork();
        
        if (!defined($pid)){
            print "Error in fork: $!";
            exit 1;
        }
        if ($pid == 0) {
            my $pid = $$;
            push @all_pid, $pid;
            print "\n ===== $ele Modular Analysis Start\n";
            &Single_run($ele);
            
            exit 0;
        }
        $num_proc ++;

        if(($i-$num_proc-$num_collect) > 0) {
            while (($collect = waitpid(-1, WNOHANG)) > 0) {
                $num_collect ++;
            }
        }
        
        while($num_proc >= $paral_num){
            sleep(45);
        }
    }
    
    while ($num_proc >= 1){
        sleep(45);
    }
    print "Analysis for all samples Done!\n";
}
