#!/usr/bin/perl
     
use CGI;
 
$query = new CGI;

print $query->header;
print $query->start_html("Videocon time survey");
print "<H1> Videocon time survey</H1>\n";
&print_prompt($query);
&do_work($query);
&print_tail;
print $query->end_html;
 
sub print_prompt {
   my($query) = @_;
 
   print $query->start_multipart_form;
   print "<EM>Name:</EM><BR>";
   print $query->textfield('name');

   print "<p><b>Please rate the following times:</b><p>";

   print "For definiteness, assume it is Monday March 13 EST<p>";
   print "<table border>";

   $gifurl = "http://hep.bu.edu/~snnet/";
   for ($est=0;$est<24;$est++)
     {
       $pst = ($est+21)%24;
       $japan = ($est+14)%24;
       $europe = ($est+6)%24;


       if ($est%4 == 0)
	 {
	   print "<tr><th>West Coast</th><th>East Coast</th><th>Europe</th><th>Japan</th>  <th>Excellent <img src=$gifurl/smile6.gif></th> <th>Not bad<img src=$gifurl/wally.gif></th> <th>So-so<img src=$gifurl/soso.gif></th><th>Urrghhh, but do-able<img src=$gifurl/mean.gif></th><th>Impossible<img src=$gifurl/skull.gif></th></tr>";

	 }
       print "<tr><td align=center>$pst:00</td><td align=center>$est:00</td><td align=center>$europe:00</td><td align=center>$japan:00</td><td colspan=5>";
       $name = "est".$est;
   print $query->radio_group(-name=>$name,
	    -values=>['Excellent','Not bad', 'So-so','Urrghh, but do-able','Impossible'],
		  -default=>'Excellent');
   print "</td></tr>";


     }
   print "</table><p>";

   print "<p>";
   print "<EM>Additional Comments:</EM><BR>"; 
   print $query->textarea(-name=>'comment',
                           -rows=>10,
                           -columns=>70);


   print "<P>",$query->reset;
   print $query->submit('Action','Submit');
   print $query->endform;
   print "<HR>\n";
        }
 
sub do_work {
    my($query) = @_;
    my(@values,$key);

    @qp = $query->param;
    $qpn = $#qp;
    if($qpn == -1) { return }	# Only print if form is submitted

    $name  = $query->param('name');
    $comment  = $query->param('comment');
    $est0 = $query->param('est0');
    $est1 = $query->param('est1');
    $est2 = $query->param('est2');
    $est3 = $query->param('est3');
    $est4 = $query->param('est4');
    $est5 = $query->param('est5');
    $est6 = $query->param('est6');
    $est7 = $query->param('est7');
    $est8 = $query->param('est8');
    $est9 = $query->param('est9');
    $est10 = $query->param('est10');
    $est11 = $query->param('est11');
    $est12 = $query->param('est12');
    $est13 = $query->param('est13');
    $est14 = $query->param('est14');
    $est15 = $query->param('est15');
    $est16 = $query->param('est16');
    $est17 = $query->param('est17');
    $est18 = $query->param('est18');
    $est19 = $query->param('est19');
    $est20 = $query->param('est20');
    $est21 = $query->param('est21');
    $est22 = $query->param('est22');
    $est23 = $query->param('est23');

    open (SENDMAIL, "| mail -t schol" );
    print SENDMAIL <<End_of_Mail
      From: $name
      Comment: $comment
      EST00: $est0
      EST01: $est1
      EST02: $est2
      EST03: $est3
      EST04: $est4
      EST05: $est5
      EST06: $est6
      EST07: $est7
      EST08: $est8
      EST09: $est9
      EST10: $est10
      EST11: $est11
      EST12: $est12
      EST13: $est13
      EST14: $est14
      EST15: $est15
      EST16: $est16
      EST17: $est17
      EST18: $est18
      EST19: $est19
      EST20: $est20
      EST21: $est21
      EST22: $est22
      EST23: $est23
End_of_Mail
    ;

    print "<H2>THANK YOU!</H2>";

#    print "<H2>Here are the current settings in this form</H2>";

#    foreach $key ($query->param) {
#        print "<STRONG>$key</STRONG> -> ";
#        @values = $query->param($key);
#        print join(", ",@values),"<BR>\n";
#    }

}
 
sub print_tail {
    print <<END
<HR>
<ADDRESS>Kate Scholberg</ADDRESS><BR>
END
    ;
}
