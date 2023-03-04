<?php
include_once("db_connect.php");
$request_method = $_SERVER["REQUEST_METHOD"];

function getPrice($request_info)
{
	global $conn;
    $Nom = $request_info['Nom'];
	$query = "SELECT Prix FROM `Stock` WHERE Nom = '".$Nom."'";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = floatval($row[0]);
	}
    header('Content-Type: application/json');
	return json_encode($response);
}

function modifyPrice($request_info)
{
	global $conn;
	$Nom = $request_info['Nom'];
    $Prix = $request_info['Prix'];
	$query = "UPDATE `Stock` SET Prix = ".$Prix." WHERE Nom = '".$Nom."' ";
	mysqli_query($conn,$query);
}

switch ($request_method) {
    case 'GET':
        echo getPrice($_GET);
		break;
    case 'PUT':
		modifyPrice($_GET);
		break;
	default:
    	break;
}

?>