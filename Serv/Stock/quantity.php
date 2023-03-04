<?php
include_once("db_connect.php");
$request_method = $_SERVER["REQUEST_METHOD"];

function getQuantity($request_info)
{
	global $conn;
    $Nom = $request_info['Nom'];
	$query = "SELECT Quantite FROM `Stock` WHERE Nom = '".$Nom."'";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = floatval($row[0]);
	}
    header('Content-Type: application/json');
	return json_encode($response);
}

function modifyQuantity($request_info)
{
	global $conn;
	$Nom = $request_info['Nom'];
    $Quantite = $request_info['Quantite'];
	$query = "UPDATE `Stock` SET Quantite = ".$Quantite." WHERE Nom = '".$Nom."' ";
	mysqli_query($conn,$query);
}

switch ($request_method) {
    case 'GET':
        echo getQuantity($_GET);
		break;
    case 'PUT':
		modifyQuantity($_GET);
		break;
	default:
    	break;
}

?>		