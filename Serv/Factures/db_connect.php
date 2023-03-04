<?php
	$server = "liliannadmin.mysql.db";
	$username = "liliannadmin";
	$password = "Lilian02";
	$db = "liliannadmin";
	$conn = mysqli_connect($server, $username, $password, $db);

if (!$conn) {
	echo mysqli_connect_error();
}
?>