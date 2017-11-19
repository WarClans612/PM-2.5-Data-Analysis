<?php

//Trying to connect to database
$db_host = "host";
$db_name = "db";
$db_user = "user";
$db_password = "pass";
$dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8";
$db = new PDO($dsn, $db_user, $db_password);
$sql = "SELECT `id`, `name`, `lat`, `lon` FROM `devices_info`";
$responseT = $db->prepare($sql);
$responseT->execute();
echo json_encode($responseT->fetchAll(PDO::FETCH_ASSOC), JSON_UNESCAPED_UNICODE);

?>
