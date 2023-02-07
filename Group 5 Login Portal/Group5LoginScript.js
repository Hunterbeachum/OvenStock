//////////////////////////////////////////////////////////////////////
//      File Name: Group5LoginScript.js
//		Date Created: February 2nd, 2023*
//		Author: Caleb Agosta, with help from group members
//////////////////////////////////////////////////////////////////////


// Creating our buttons for the login page. 
var login = document.getElementById("submit");
var goToReset = document.getElementById("userpass_reset");
var goToCreate = document.getElementById("create_user");

// Trying to create a functional title change, to show the user when they are logged in
var userInSession = "Please Log In!";
document.getElementById("title").innerHTML = userInSession;

//  Creating key user Pairs test userkey 1 and 2:
const login_dict = [
	{
		userkey: "2",
		username: "cagosta",
		password: "123456"
	
	},
	{
		userkey: "3",
		username: "aweber",
		password: "234567"
	}
]

// Setting user dummy information
let user = {userkey: "1", username: "test_user", password: "12345"};
login_dict.unshift(user);

// Function Name: goToResetPage(userInSession)
//	 	This function will take us to the Password Reset page and create an event listener for
// 		the reset page's button.
function goToResetPage() {
	window.location = "ResetPageGroup5.html";
	var submitNew = document.getElementById("submit_new_pass");
	submitNew.addEventListener('click', resetPass);	
}

// Function Name: resetPass()
//		This function will trigger when the user presses the submit button on the reset page
//		It will take the username and the new password and check if the new password is different.
//		If it is, it will replace the old password for that specific username.
function resetPass() {
	var username = document.getElementById("newUser").value;
	var newPass = document.getElementById( "newPass").value;
	
	for (i=0; i < login_dict.length; i++) {
		if(username == login_dict[i].username) {
			if (newPass = login_dict[i].password) {
				document.getElementById("message").innerHTML = "";
				document.getElementById("message").innerHTML = "<span style='color:red;'>This is the current password for this account!</span>";
			}
			else {
			login_dict[i].password = newPass;
			console.log("password accepted.");
			}
		}
		else {
			document.getElementById("message").innerHTML = "";
			document.getElementById("message").innerHTML = "<span style='color:red;'>This username is not found, try creating an account.</span>";
		}
	}
}

// Function Name: tryLogin()
//		This function will trigger when the user presses the log in button on the login page.
//		It will take the username submitted and check the dictionary for a matching value, then
//		it will check the password submitted against the password in the dictionary. If either value
//		is incorrect, it will display a message warning the user that the values are wrong.
function tryLogin() {
	// getting the username and password submitted by the user
	var username = document.getElementById("bkuser").value;
	var password = document.getElementById("bkpass").value;

	for (i = 0; i < login_dict.length; i++) {
		if(username == login_dict[i].username)	{
			// console output test to see if username is accepted.
			console.log("Username accepted: " + username);
		
			if (password == login_dict[i].password) {
				userInSession = login_dict[i].username;
				window.location = "Group5InventoryPage.html";
				newTitle = "Welcome, "+ userInSession +", to Group 5's Bakery Inventory Manager";
				document.title = newTitle;
				console.log(userInSession + " has logged in.");
			}
		}
		else if (username != login_dict[i].username) {
			if (username == "") {
				document.getElementById("message").innerHTML = "";
				document.getElementById("message").innerHTML = "<span style='color:red;'>Please enter your username.</span>";
			}
		
		else {
			document.getElementById("message").innerHTML = "";
			document.getElementById("message").innerHTML = "<span style='color:red;'>Username or password is incorrect. Try creating an account?</span>";
		}
		}
	}
}

// Function Name: newUser()
//		This function will load the Create User page, and create an event listener for the add_user button.
function newUser() {
	window.location = "CreateUserGroup5.html";
	var createUser = document.getElementById("add_user");
	createUser.addEventListener('click', addUser);
}

// Function name: addUser()
//		This function will take the newuser and newpass values, and check to see if the newuser value
//		is already in the dictionary. If it isn't, it will add the newuser to the dictionary with the
//		submitted password value.
function addUser() {
	var newuser = document.getElementById("newuser");
	var newpass = document.getElementById("newpass");
	for (i = 0; i <= login_dict.length; i++) {
		if (login_dict[i].username == newuser) {
			document.getElementById("messageAdd").innerHTML = "";
			document.getElementById("messageAdd").innerHTML = "<span style='color:red;'>Username already exists!</span>";
		}
		else {
			login_dict.put("username", newuser)
		}
	}
}

// These event listeners are added to the login page's buttons, but I would rather have them load in
// on the main page only. I couldn't find a way to get them to be created onload. *****HELP*****
login.addEventListener('click', tryLogin);
goToReset.addEventListener('click', goToResetPage);
goToCreate.addEventListener('click', newUser);