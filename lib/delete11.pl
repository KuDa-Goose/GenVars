
#!//usr/bin/perl
$fq1=shift;
$fq2=shift;
$fq3=shift;
open(IN,"$fq1");
while($line=<IN>){
    $hash_title{$line}=1;
    <IN>;
    <IN>;
    <IN>;
    }
close IN;
open(OUT,">$fq3");
open(IN,"$fq2");
while($line=<IN>){
undef $title;
undef $seq;
$title=$line;
$seq=<IN>.<IN>.<IN>;
if(!$hash_title{$title}){
print OUT $title.$seq;
    }
}
close OUT;

