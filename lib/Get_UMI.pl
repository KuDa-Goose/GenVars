my $in=shift;
my $in2=shift;
my $out=shift;
my $out2=shift;
my %hash=();

open(OUT, ">$out");
open(IN, "$in") || die "Can't open file $in\n";
while(my $line = <IN>){
    chomp($line);
    my $seq = <IN>;
    chomp($seq);
    <IN>;
    my $Qual = <IN>;
    chomp($Qual);
    my @ID = split/ /,$line;
    my $Seq = substr($seq,15,);
    my $umi = substr($seq,0,15);
    my $A = substr($umi,2,2);
    my $B = substr($umi,6,2);
    my $C = substr($umi,10,2);
    my $D = substr($umi,14,1);
    my $BaseSeq = $A.$B.$C.$D;
    my $Map = 0;
    my $String = "CACACAC";
    my @RefBase = split//,$String;
    my @MapBase = split//,$BaseSeq;
    #if(($A eq "CA") && ($B eq "CA") && ($C eq "CA") && ($D eq "C")){
    for(my $i=0;$i<length($BaseSeq);$i++){
        if($MapBase[$i] eq $RefBase[$i]){
            $Map++;
        }
    }
    if(int($Map) >= 6){
        my $quality = substr($Qual,15,);
        my $id = $ID[0].":".$umi." ".$ID[1];
        $hash{$ID[0]} = $umi;
        print OUT $line."\n".$seq."\n"."+"."\n".$Qual."\n";
    }else{
        next;
    }
}
open(OUTT, ">$out2");
open(IN2, "$in2") || die "Can't open file $in2\n";
while(my $Line = <IN2>){
    chomp($Line);
    my $Seq = <IN2>;
    chomp($Seq);
    <IN2>;
    my $Qual = <IN2>;
    chomp($Qual);
    my @ID = split/ /,$Line;
    if(exists $hash{$ID[0]}){
        my $id = $ID[0].":".$hash{$ID[0]}." ".$ID[1];
        print OUTT $Line."\n".$Seq."\n"."+"."\n".$Qual."\n";
    }else{
        next;
    }
}

close IN;
close OUT;
close IN2;
close OUTT;
