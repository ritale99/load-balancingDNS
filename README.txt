Steven Nguyen - shn27
Rithvik Aleshetty - rra76

1. Briefly discuss how you implemented the LS functionality of
   tracking which TS responded to the query and timing out if neither
   TS responded.
	I used select to handle which TS responded to the query.
	I put the sockets of both TS in select to wait for whichever is availible first or if it times out.

2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.
	Using select to recv the first availible TS or timing out has a problem.
		When a TS responds after the select times out, it will be received in the next select.
		This causes the wrong output to the next and all other requests to the LS.

3. What problems did you face developing code for this project?
	Working with the timeout
	Figuring out which TS had responded to the query without the threading

4. What did you learn by working on this project?
	How a load balancing server can work
	How to use select
