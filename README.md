# django-hms

## Hostel Room Management System

### Introduction
The aim of the project is to build a hostel room management system which allows students to select their rooms online. It also allows wardens to see the status of rooms and its occupants.


### Views
* Login Page
* Landing Page
* Profile View
* Room Confirm View
* Room View
* Selection Page


### Models
* Student: For holding student details
* Room: To hold room occupancy


### Functions
* A Login page for authentication purpose (student or warden)
* Allows students to view rooms and select rooms
* Show Student Profile
* Allows warden to view room status, its occupancy and the student details

### Workflow

* Student
	* Landing page presented
	* Option to Sign Up or Login
	* If Logged in 
		* shows user profile and allotted room
	* If new user:
		* Has to sign up
		* After sign up redirected to user profile
		* Option to select room is given
		* Onclick, list of rooms available shown
		* After selection, room is confirmed, and redirected to user profile
		
		
* Warden
	* Can login from home (sign up is done by admin only)
	* Presented with All Rooms and an option to view inmates
	* Option to add room, which sends to another page to fill in room details

