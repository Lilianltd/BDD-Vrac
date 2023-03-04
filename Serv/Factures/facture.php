<?php
include_once("db_connect.php");
$request_method = $_SERVER["REQUEST_METHOD"];

function addfacture($request_info)
{
	global $conn;
	$idAchat = $_GET['idAchat'];
	$idClient = $_GET['idClient'];
    $total = $request_info['total'];
	$payWay = $request_info['payWay'];
	date_default_timezone_set('Europe/Paris');
	$date = date('Y-m-d');
	$query = "INSERT INTO `Factures` VALUES (".$idAchat.",".$idClient.",'".$date."',".$total.",'".$payWay."') ";
	mysqli_query($conn,$query);
}

function getListDate()
{
	global $conn;
	$query = "SELECT DISTINCT Date From `Factures`";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$response[] = $row[0];
	}
	header('Content-Type: application/json');
	return json_encode($response);
}

function extractcsv($request_info)
{
	global $conn;
	$date = $request_info['date'];
	$query = "SELECT Nom, Prenom, Moyen,Total,Achat.Liste,Achat.Quantite,Achat.Prix FROM Factures 
			JOIN Achat ON Achat.`Id achat`=Factures.`Id achat`
			JOIN Client ON Factures.`Id clients` = Client.Id
			WHERE Factures.Date = '".$date."';";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$product = explode( "||",$row[4]);
		$quantite = explode("||",$row[5]);
		$prix = explode( "||",$row[6]);
		$client = array($row[0],$row[1],$row[2],$row[3],$product,$quantite,$prix);
		$response[] = $client;
	}
	header('Content-Type: application/json');
	return json_encode($response);
}

function tableExtract($request_info)
{
	global $conn;
	$date = $request_info['date'];
	$query = "SELECT Achat.Liste,Achat.Quantite FROM Factures 
			JOIN Achat ON Achat.`Id achat`=Factures.`Id achat`
			WHERE Factures.Date = '".$date."';";
	$response = array();
	$result = mysqli_query($conn, $query);
	while($row = mysqli_fetch_row($result))
	{
		$product = explode( "||",$row[0]);
		$quantite = explode("||",$row[1]);
		$client = array($product,$quantite);
		$response[] = $client;
	}
	header('Content-Type: application/json');
	return json_encode($response);
}

switch ($request_method) {
  	case 'PUT': 
    	break;
	case 'GET':
		if ($_GET['csv'] == True) {
			echo extractcsv($_GET);
		} elseif ($_GET['tableExtract'] == True) {
			echo tableExtract($_GET);
		}
		else{echo getListDate();}
		break;
	case 'POST':
		addfacture($_GET);
		break;
    case 'DELETE':
        break;
	default:
    	break;
}

?>			