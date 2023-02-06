var login = document.getElementById("submit");
var goToReset = document.getElementById("userpass_reset");
var goToCreate = document.getElementById("create_user");
var createUser = document.getElementById("add_user");
var submitNew = document.getElementById("submit_new_pass");
var userInSession = "Please Log In!";
	const login_dict = [
	{
		username: "cagosta",
		password: "123456"
	},
	{
		username: "aweber",
		password: "234567"
	}
	]
function goToResetPage() {
	window.location = "ResetPageGroup5.html";
}

function resetPass() {
	var username = document.getElementById("newUser").value;
	var newPass = document.getElementById( "newPass").value;
	
	for (i=0; i < login_dict.length; i++) {
		if(username == login_dict[i].username) {
			login_dict[i].password = newPass;
			console.log("test");
		}
	}
	if(username != login_dict[i].username){
		console.log("Username: " + username + " is not found in the database. Try creating an account.");
		alert("Username is not found, try creating account.");
	}
}

function tryLogin() {

	var username = document.getElementById("bkuser").value;
	var password = document.getElementById("bkpass").value;

	for (i = 0; i < login_dict.length; i++) {
		if(username == login_dict[i].username && password == login_dict[i].password) {
			userInSession = login_dict[i].username;
			window.location = "Group5InventoryPage.html";
			newTitle = "Welcome, "+ userInSession +", to Group 5's Bakery Inventory Manager";
			document.title = newTitle;
			console.log(userInSession + " has logged in.");
		}
		
		else if(username == login_dict[i].username && password != login_dict[i].password) {
			document.getElementById("message").innerHTML = "<span style='color:red;'>Username found, Incorrect Password given.</span>"; 
		}

		else if (username == ""){
			document.getElementById("message").innerHTML = "<span style='color:red;'>Please submit a username.</span>";
		}
	}
}

function newUser() {
	window.location = "CreateUserGroup5.html";
}

function addUser() {
	var newuser = document.getElementById("newuser");
	var newpass = document.getElementById("newpass");
}
login.addEventListener('click', tryLogin);
goToReset.addEventListener('click', goToResetPage);
goToCreate.addEventListener('click', newUser);
submitNew.addEventListener('click', resetPass);
createUser.addEventListener('click', addUser);