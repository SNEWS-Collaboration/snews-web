#!/usr/bin/perl
     
use CGI;
 
$query = new CGI;

print $query->header;
print $query->start_html("Questionnaire for Astronomers");
print "<H1> Questionnaire for Astronomers</H1>\n";
&print_prompt($query);
&do_work($query);
&print_tail;
print $query->end_html;
 
sub print_prompt {
   my($query) = @_;
 
   print $query->start_multipart_form;
   print "<EM>Name:</EM><BR>";
   print $query->textfield('name');
   print "<P><EM>Affiliation:</EM><BR>";
   print $query->textfield('affil');
   print "<P><EM>Email:</EM><BR>";
   print $query->textfield('email');
 

   print "<P><EM>Research Interests:</EM><BR>";
   print $query->textarea(-name=>'research',
                          -rows=>3,
                          -columns=>50);

   print "<P><H2> 1. Value of an Early Alert </H2>";
   print "<P><EM>1a. What, in your opinion, would be the main value of
an early supernova alert?</EM><BR>";
   print $query->textarea(-name=>'question1a',
                          -rows=>4,
                          -columns=>70);

   print "<P><EM>1b. What types of observations
of early supernova would be interest you the most
if a supernova were caught in its earlier stages? </EM><BR>";
 
   print $query->textarea(-name=>'question1b',
                          -rows=>4,
                          -columns=>70);


   print "<P><H2> 2. Interested Parties </H2>";

    print "<P><EM>2.1 Would you or your research group want to be alerted if a neutrino burst were detected?</EM><BR>";
 
   print $query->checkbox_group(
                                -name=>'interest',
                                -values=>[Yes,No],
                                -defaults=>[Yes]);

   print "<P><H3>If no: </H3><EM> 2.2a Can you recommend people or groups who might be interested in being on the list?  </EM><BR>";
 
   print $query->textarea(-name=>'question2_2a',
                          -rows=>2,
                          -columns=>70);

   print "<P><H3>If yes: </H3><EM> 2.2b Please give details/references on your research/facilities;
also please answer the questions in section 3.</EM><BR>";
 
   print $query->textarea(-name=>'question2_2b',
                          -rows=>4,
                          -columns=>70);


   print "<P><H2> 3. Courses of Action by Supernova Hunters </H2>";


    print "<P><EM> 3.1 If your group were given an early alert that a gravitational collapse had occurred in the galaxy, what would be your course of action? </EM><BR>";
 
    print $query->textarea(-name=>'question3_1',
                           -rows=>4,
                           -columns=>70);

    print "<P><EM> 3.2 Would this course of action depend strongly on how well the source direction was known?  If there were no source direction available from the neutrino signal would you still think it worth looking? </EM><BR>";
 
    print $query->textarea(-name=>'question3_2',
                           -rows=>4,
                           -columns=>70);


    print "<P><EM> 3.3 Are the facilities you have access to available at any time for an \"emergency\" supernova search?  What would such a search entail? </EM><BR>";
 
    print $query->textarea(-name=>'question3_3',
                           -rows=>4,
                           -columns=>70);

    print "<P><EM> 3.4 How soon could there be a supernova search response from your group?</EM><BR>";
 
    print $query->textarea(-name=>'question3_4',
                           -rows=>4,
                           -columns=>70);

    print "<P><EM> 3.5 What fraction of the sky could be scanned in what period of time? What would be the probability of finding the early supernova source as a function of time and pointing accuracy from the neutrino signal?</EM><BR>";
 
    print $query->textarea(-name=>'question3_5',
                           -rows=>4,
                           -columns=>70);

    print "<P><EM> 3.6 What rate of \"false alarms\" would be acceptable?  None?  1 per  year?  >1 per 10 years? (In other words, how \"expensive\" would a false alarm be?) </EM><BR>";
 
    print $query->textarea(-name=>'question3_6',
                           -rows=>4,
                           -columns=>70);

    print "<P><EM> 3.7 Can you think of any practical details not mentioned here that should be considered?</EM><BR>";
 
    print $query->textarea(-name=>'question3_7',
                           -rows=>4,
                           -columns=>70);


   print "<P><H2> 4. Means of Notification  </H2>";

    print "<P><EM> 4.1 What form of early supernova alert would be most useful to you? </EM><BR>";
 
    print $query->scrolling_list(-name=>'notification',
                                 -values=>['WWW','IAU circular','email','telegram','phone call','beeper'],
				 -size=>6,
				 -multiple=>'true');

    print "<P><EM>Other: </EM><BR>";
    print $query->textfield('othernot');

   print "<P><H2> 5. What sort of information is needed/useful?  </H2>";

    print "<P><EM> 5.1  Clearly source direction is useful; how useful? (similar to 3.2)</EM><BR>";
 
    print $query->textarea(-name=>'question5_1',
                           -rows=>4,
                           -columns=>70);

    print "<P><EM> 5.2 How important is promptness of warning?</EM><BR>";
 
    print $query->textarea(-name=>'question5_2',
                           -rows=>4,
                           -columns=>70);

   print "<P><H2> 6.  Please give any more comments or suggestions you may have. </H2>";

    print $query->textarea(-name=>'question6',
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
    $affil  = $query->param('affil');
    $email  = $query->param('email');
    $question1a  = $query->param('question1a');
    $question1b  = $query->param('question1b');
    $interest = $query->param('interest');
    $question2_2a  = $query->param('question2_2a');
    $question2_2b  = $query->param('question2_2b');
    $question3_1  = $query->param('question3_1');
    $question3_2  = $query->param('question3_2');
    $question3_3  = $query->param('question3_3');
    $question3_4  = $query->param('question3_4');
    $question3_5  = $query->param('question3_5');
    $question3_6  = $query->param('question3_6');
    $question3_7  = $query->param('question3_7');
    $notif = $query->param('notification');
    $othernot  = $query->param('othernot');
    $question5_1  = $query->param('question5_1');
    $question5_2  = $query->param('question5_2');
    $question6  = $query->param('question6');



    open (SENDMAIL, "| mail -t schol" );
    print SENDMAIL <<End_of_Mail
      From: $name
      Affiliation: $affil
      Email: $email
      1a: $question1a	  
      1b: $question1b	  
      Interest: $interest
      2_2a: $question2_2a
      2_2b: $question2_2b	  
      3_1: $question3_1	  
      3_2: $question3_2	  
      3_3: $question3_3	  
      3_4: $question3_4	  
      3_5: $question3_5	  
      3_6: $question3_6	  
      3_7: $question3_7
      Notification: $notif
      Other notification: $othernot
      5_1: $question5_1
      5_2: $question5_2
      6: $question6
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
<A HREF="http://hep.bu.edu/~snnet/">International Early Supernova Alert Page</A>
END
    ;
}
