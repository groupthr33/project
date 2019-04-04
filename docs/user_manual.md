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

<br>
<h5>NAME</h5>

<b>assign_ta_course</b> - assigns a TA to a course

<h5>SYNOPSIS</h5>

<b>assign_ta_course</b> <u>ta_user_name</u> <u>course_id</u>   
<u>course_section_id</u> [-l <u>num_labs</u>]

<b>DESCRIPTION</b>

Assign TA with <u>ta_user_name</u> to course with <u>course_id</u> and   
<u>course_section_id</u>, optionally specifying a number of labs. Without specifying   
a number of labs, the TA will be assigned as a grader. Can only be used by the Supervisor. 

Options: 

-l <u>number_of_labs</u> - allocates <u>number_of_labs</u> lab sections to TA with <u>ta_user_name</u>

<br>
<h5>NAME</h5>

<b>assign_ta_lab</b> - assigns a TA to specific lab sections within a course

<h5>SYNOPSIS</h5>

<b>assign_ta_lab</b> <u>ta_user_name</u> <u>course_id</u>   
<u>course_section_id</u> <u>lab_sections...</u>

<b>DESCRIPTION</b>

Assign TA with <u>ta_user_name</u> to <u>lab_sections...</u> for course with <u>course_id</u>   
and <u>course_section_id</u>, optionally specifying a number of labs. Without specifying   
a number of labs, the TA will be assigned as a grader. Can only be used by the Supervisor.


<br>
<h5>NAME</h5>

<b>cr_lab</b> - creates a lab for a given course and course section

<h5>SYNOPSIS</h5>

<b>cr_lab</b> <u>lab_id</u> <u>course_id</u> <u>course_section_id</u> <u>schedule</u>

<b>DESCRIPTION</b>

Create a lab section with id <u>lab_id</u> for course <u>course_id</u>-<u>course_section_id</u>.

<br>
<h5>NAME</h5>

<b>course_assignments</b> - view the instructor and TA(s) assigned to a course

<h5>SYNOPSIS</h5>

<b>course_assignments</b> <u>course_id</u> <u>course_section_id</u>

<b>DESCRIPTION</b>

Display the name of instructor and TA(s) assigned to course  <u>course_id</u>-<u>course_section_id</u>
and how many more lab sections each TA can be assigned to.


<br>
<h5>NAME</h5>

<b>set_password</b> - sets the password for the current user

<h5>SYNOPSIS</h5>

<b>set_password</b> <u>old_password</u> <u>new_password</u>


<b>DESCRIPTION</b>

Set the password of the requesting user to <u>new_password</u> if their current password matches   
<u>old_password</u>
