<?php
include_once("db_connect.php");
$request_method = $_SERVER["REQUEST_METHOD"];

function getProduct($request_info)
{
	global $conn;
    $Nom = $request_info['Nom'];
	$query = "SELECT * FROM `Stock` WHERE Nom = '".$Nom."'";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = $row;
	}
    header('Content-Type: application/json');
	return json_encode($response);
}

function getProducts()
{
    global $conn;
	$query = "SELECT * FROM `Stock`";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = $row;
	}
    header('Content-Type: application/json');
	return json_encode($response);
}

function getProductsName()
{
    global $conn;
    $query = "SELECT Nom FROM `Stock`";
    $response = array();
    $result = mysqli_query($conn, $query);
    while($row = mysqli_fetch_array($result))
    {
        $response[] = $row[0];
    }
    header('Content-Type: application/json');
    return json_encode($response);
}

function addProduct($request_info)
{
	global $conn;
	$Nom = $request_info['Nom'];
    $Prix = $request_info['Prix'];
	$Type = $request_info['Type'];
	$query = "INSERT INTO `Stock` VALUES ('".$Nom."',".$Prix.",".$Type.",0) ";
	mysqli_query($conn,$query);
}

function delProduct($request_info)
{
	global $conn;
	$Nom = $request_info["Nom"];
	$query = "DELETE FROM `Stock` WHERE Nom = '".$Nom."';";
	mysqli_query($conn, $query);
}

switch ($request_method) {
    case 'GET':
		if (count($_GET) == 0) 
		{
			echo getProducts();	
		}
		else
		{
            if ($_GET['getName'] == True) 
            {
                echo getProductsName();
            } 
            else 
            {
                echo getProduct($_GET);
            }
			    
		}
		break;
    case 'POST':
		addProduct($_GET);
		break;
	case 'DELETE':
		delProduct($_GET);
		break;
	default:
    	break;
}

?>		