my $in=shift;
my $in2=shift;
my $out=shift;
my %hash=();

open(IN,"$in") || die "Can't open file $in\n";
while(my $line = <IN>){
    chomp($line);
    my $seq = <IN>;
    <IN>;
    my $qual = <IN>;
    my @Name = split/ /,$line;
    $hash{$Name[0]} = 1;
}
close IN;

open(OUT, ">$out");
open(IN2,"$in2") || die "Can't open file $in2\n";
while(my $Line=<IN2>){
    chomp($Line);
    my $Seq = <IN2>;
    my $Str = <IN2>;
    my $Qual = <IN2>;
    my @name = split/ /,$Line;
    if(exists $hash{$name[0]}){
        print OUT $Line."\n".$Seq.$Str.$Qual;
    }
}
close IN2;
close OUT;
