<?php 

$db_host = "host";
$db_name = "name";
$db_user = "user";
$db_password = "pass";
$dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8";
$db = new PDO($dsn, $db_user, $db_password);
$sql = "SELECT `location` as `id`, extract(hour from `time`) as Hourly, avg(`pm25`) as PM25
    FROM `Wang_device_data`
    WHERE `location` = :id AND `time` > DATE_SUB( NOW(), INTERVAL 1 DAY) 
    GROUP BY `id`, extract(hour from `time`)";
$responseT = $db->prepare($sql);
$id = $_POST['id'];
$responseT->execute(array('id'=>$id));

//Creating temporary array for hourly data
$device_data = array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
$device_data_length = count($device_data);
while($nt =  $responseT->fetch(PDO::FETCH_ASSOC)) {
    $device_data[$nt['Hourly']] = $nt['PM25'];
}

$table = array();
//Creating json table that is ready to be used by Google Charts
/*$table['cols'] = array (
    array('id' => "", 'label' => "Time", 'pattern' => "", 'type' => 'string'),
    array('id' => "", 'label' => "PM 2.5", 'pattern' => "", 'type' => 'number')
);
$rows = array();
for($i = 0; $i < $device_data_length; ++$i) {
    $temp = array();
    $wanted = ($i + (int)date('G')) % $device_data_length;
    $temp[] = array('v' => $wanted, 'f' => NULL);
    $temp[] = array('v' => $device_data[$wanted], 'f' => NULL);
    $rows[] = array('c' => $temp);
}
$table['rows'] = $rows;*/

//Preparing json table for d3.js
for($i = 0; $i < $device_data_length; ++$i) {
    $wanted = ($i + (int)date('G')) % $device_data_length;
    $table[] = array("Time" => $wanted, "PM25" => $device_data[$wanted]);
}
$jsonTable = json_encode($table, JSON_UNESCAPED_UNICODE);
echo $jsonTable;

?>
