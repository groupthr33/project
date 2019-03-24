## User Manual

<h5>NAME</h5> 

<b>login</b> – logs user into account 
 
<h5>SYNOPSIS</h5>

login <u>username</u> <u>password</u>

<h5>DESCRIPTION</h5> 

Once executed with a valid <u>username</u> correct associated <u>password</u>,   
the user will be logged into the application. If a password isn’t yet associated   
with the account, the initial password will be set to <u>password</u>.  

<br>

<h5>NAME</h5>

<b>cr_account</b> – create an account for a new user
 
<h5>SYNOPSIS</h5> 

cr_account <u>username</u> <u>name</u> <u>roles...</u>

<h5>DESCRIPTION</h5> 

Create a new account with the assigned </u>roles...</u> and <u>username</u> for   
user with name <u>name</u>. This command is for administrators or supervisors only.

<br>
<h5>NAME</h5> 

<b>logout</b> – logout current user 

<h5>SYNOPSIS</h5>

logout 

<h5>DESCRIPTION</h5> 

Log the currently logged in user out of their account.
  
<br>
<h5>NAME</h5> 

<b>cr_course</b> - create a course (one section)

<h5>SYNOPSIS</h5>

course <u>course_id</u> <u>section_id</u> <u>course_name</u> <u>course_schedule</u> 

<h5>DESCRIPTION</h5>

Create a new course with a <u>course_id</u>, <u>section_id</u>, <u>course_name</u>,   
and <u>course_schedule</u>. This command is for administrators or supervisors only.   
<u>course_schedule</u> is of the form DDSSSSEEEE, where D represents a day that   
the lecture takes place, SSSS is the start time, and EEEE is the end time.   
e.g. MW14001550 is a class that meets on Monday and Wednesday from 2pm to 3:50pm.

<br>
<h5>NAME</h5>

<b>assign_ins</b> – assigns an instructor to a specific section and course

<h5>SYNOPSIS</h5>

assign_ins <u>instructor</u> <u>course_id</u> <u>section_id</u>

<h5>DESCRIPTION</h5>

Assign <u>instructor</u> to section with <u>section_id</u> for course with   
<u>course_id</u>. Can only be used by users with the supervisor role. 
