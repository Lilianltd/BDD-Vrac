<?php
include_once("db_connect.php");
$request_method = $_SERVER["REQUEST_METHOD"];

function getLastId()
{
	global $conn;
	$query = "SELECT count(*) FROM `Client`";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = floatval($row[0]);
	}
	return $response[0];
}

function addClient($request_info)
{
	global $conn;
	$Nom = $request_info['Nom'];
	$Prenom = $request_info['Prenom'];
	$id = getLastId();
	$query = "INSERT INTO `Client` VALUES (".$id.",'".$Nom."','".$Prenom."','Actif') ";
	mysqli_query($conn,$query);
}

function getClient($request_info)
{
	global $conn;
	$Id = $request_info['Id'];
	$query = "SELECT * FROM `Client` WHERE Id = '".$Id."'; ";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = $row;
	}
	header('Content-Type: application/json');
	return json_encode($response);
}

function getClient2($request_info)
{
	global $conn;
	$nom = $_GET['Nom'];
	$prenom = $_GET['Prenom'];
	$query = "SELECT Id FROM `Client` WHERE Nom = '".$nom."' AND Prenom = '".$prenom."'; ";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = intval($row[0]);
	}
	header('Content-Type: application/json');
	return json_encode($response);
}

function getClients()
{
	global $conn;
	$query = "SELECT Nom, Prenom FROM `Client` WHERE `Actif/Passif` = 'Actif'";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = $row;
	}
	header('Content-Type: application/json');
	return json_encode($response);
}

function delClient($request_info)
{
	global $conn;
	$Nom = $request_info['Nom'];
	$Prenom = $request_info['Prenom'];
	$query = "UPDATE `Client` SET `Actif/Passif` = 'Passif' WHERE Nom = '".$Nom."' AND Prenom = '".$Prenom."' ";
	mysqli_query($conn, $query);
}

switch ($request_method) {
  	case 'PUT':
    	break;
	case 'GET':
		if (count($_GET) == 0) {
			echo getClients();
		}
		elseif (count($_GET) == 2) {
			echo getClient2($_GET);
		}
		else {
			echo getClient($_GET);
		}
		break;
	case 'POST':
		addClient($_GET);
		break;
	case 'DELETE':
		delClient($_GET);
	default:
    	break;
}

?>		