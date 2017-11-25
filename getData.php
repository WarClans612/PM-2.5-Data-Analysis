<?php 

$db_host = "host";
$db_name = "db";
$db_user = "user";
$db_password = "pass";
$dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8";
$db = new PDO($dsn, $db_user, $db_password);
$sql = "SELECT `id`, extract(hour from `time`) as Hourly, avg(`pm25`) as PM25 FROM `devices_data` WHERE `id` = :id AND `time` > DATE_SUB( NOW(), INTERVAL 1 DAY) GROUP BY `id`, extract(hour from `time`) ORDER BY ( Hourly + 24 - HOUR(NOW())) % 24";
$responseT = $db->prepare($sql);
$id = $_POST['id'];
$responseT->execute(array('id'=>$id));

//Creating json table that is ready to be used by Google Charts
$table = array();
$table['cols'] = array (
  array('id' => "", 'label' => "Time", 'pattern' => "", 'type' => 'string'),
  array('id' => "", 'label' => "PM 2.5", 'pattern' => "", 'type' => 'number')
);
$rows = array();
while($nt =  $responseT->fetch(PDO::FETCH_ASSOC)) {
  $temp = array();
  $temp[] = array('v' => $nt['Hourly'], 'f' => NULL);
  $temp[] = array('v' => $nt['PM25'], 'f' => NULL);
  $rows[] = array('c' => $temp);
}
$table['rows'] = $rows;
$jsonTable = json_encode($table);
echo $jsonTable;

?>
