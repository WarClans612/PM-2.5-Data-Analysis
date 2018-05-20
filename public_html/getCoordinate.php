<?php

//Trying to connect to database
$db_host = "host";
$db_name = "name";
$db_user = "user";
$db_password = "pass";
$dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8";
$db = new PDO($dsn, $db_user, $db_password);

$sql = "
    (SELECT `first`.`id` as `id`, `name`, `lat`, `lon`, 'Edimax' as `source`, `PM25`
        FROM (SELECT `id`, `name`, `lat`, `lon` FROM `Edimax_devices_info`) as `first`
        LEFT JOIN
        (SELECT `id`, avg(`pm25`) as `PM25` FROM `Edimax_devices_data` WHERE (`time` > NOW() - INTERVAL 1 HOUR) GROUP BY `id`) as `second`
        ON `first`.`id` = `second`.`id`)
    UNION
    (SELECT `first`.`location` as `id`, `name`, `lat`, `lon`, 'Wang' as `source`, `PM25`
        FROM (SELECT `location`, `name`, `lat`, `lon` FROM `Wang_device_info`) as `first`
        LEFT JOIN
        (SELECT `location`, avg(`pm25`) as `PM25` FROM `Wang_device_data` WHERE (`time` > NOW() - INTERVAL 1 HOUR) GROUP BY `location`) as `second`
        ON `first`.`location` = `second`.`location`)
    ";
/*$sql = "(SELECT `id`, `name`, `lat`, `lon`, 'red' as `color` FROM `Edimax_devices_info`)
    UNION
    (SELECT `location` as `id`, `location` as `name`, `lat`, `lon`, 'blue' as `color` FROM `Wang_device_info`);";*/
$responseT = $db->prepare($sql);
$responseT->execute();

echo json_encode($responseT->fetchAll(PDO::FETCH_ASSOC), JSON_UNESCAPED_UNICODE);

?>
