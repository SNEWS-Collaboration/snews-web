#!/usr/bin/perl

# Generate template for a shift calendar for an input year

# Run like: ./gencal 2004 > schedule_2004_template.html

$year = $ARGV[0];

if ($year == ""){
    print "You must give year as argument \n";
    exit;
}

print "<body bgcolor=\"\#eee8f8\"><HTML><Title>SNEWS Shift Schedule</Title>\n";
print "<P><center><h2>SNEWS Shift Schedule</h2></center>\n";
# Modified without testing
print "<P><center><h4>$year</h4></center>\n";

for ($month=1;$month<=12;$month++)
{

    print "<br><CENTER><TABLE border>\n";

    $stuff = `cal $month $year`;
    @lines = split /^/m, $stuff;

    foreach $line (@lines){

	$line =~ s/\s*//;
	$line=~s/\s+/ /g;
	@days = split / /, $line;

	if ($line =~ /$year/){ 
	    print $line;
	}
	elsif ($line =~ /Su/){
	    print "<tr>";
	    foreach $day (@days) {
		print "<th> ",$day,"</th> ";
	    }
	    print "</tr>\n";
	}	
	elsif ($line =~ /[0-9]/) {
	    # Line of days
	    print "<tr>";

	    # "Justify" the days  (pad with spaces in the right way)
	    $num=0;
	    # Is there a Perl function to count elements? 
	    #   Should be, but Can't find it
	    foreach $day (@days) {
		$num++;
	    }

	    if ($days[0] == 1) {

		# Right justify 

		$start = 7-$num;
	    }
	    else {
		$start = 0;
	    }

#	    print "num ",$num, "start ",$start,"\n";

	    for ($i=0;$i<7;$i++)
	    {
		if ($i<$start){
		    $newday[$i] = " ";
#		    print "i, start, newday ",$i," ",$start," ",$newday[$i],"\n";

		}
		else {
		    $newday[$i]=$days[$i-$start];
#		    print "i ",$i," start  ",$start," newday ",$newday[$i]," days ",$days[$i-$start],"\n";

		}
	    }
	
	    foreach $day (@newday) {

		if ($day =~ /[0-9]/){
		    print "<th>  ",$day," ----- </th> ";
		}
		else {
		    print "<th>  ",$day,"  </th> ";
		}

	    }
	    print "</tr>\n";

	} # End of line of days

    } # End of loop over lines
    print "</TABLE><tr></center>\n";

} # End of loop over months
