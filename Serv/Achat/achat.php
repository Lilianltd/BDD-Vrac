<?php
include_once("db_connect.php");
$request_method = $_SERVER["REQUEST_METHOD"];

function getLastId()
{
	global $conn;
	$query = "SELECT MAX(`Id achat`) FROM `Achat`;";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = floatval($row[0]);
	}
	return $response[0];
}

function addCart($request_info)
{
	global $conn;
	$Liste = $request_info['Liste'];
	$Quantite = $request_info['Quantite'];
	$id = getLastId()+1;
    $Prix = $request_info['Prix'];
	$query = "INSERT INTO `Achat` VALUES (".$id.",'".$Liste."','".$Quantite."','".$Prix."') ";
	mysqli_query($conn,$query);
}

switch ($request_method) {
  	case 'PUT': 
    	break;
	case 'GET':
		if ($_GET['lastId'] == True) {
			echo getLastId();
		}
		break;
	case 'POST':
		addCart($_GET);
		break;
    case 'DELETE':
        break;
	default:
    	break;
}

?>			