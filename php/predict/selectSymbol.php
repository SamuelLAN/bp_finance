<?php

if(!isset($_COOKIE['username']) || !isset($_GET['symbol'])) {
    echo 0;
    exit;
}

$symbol = preg_replace('/\%/', '', $_GET['symbol']);
if(!$symbol) {
    echo 0;
    exit;
}

$symbol = '%' . $symbol . '%';

$host = 'localhost';
$port = 3306;
$db_name = 'finance';
$sql_user = "root";
$sql_pass = "";

try
{
    $dsn = "mysql:host=$host;port=$port;dbname=$db_name";
    $db = new PDO($dsn, $sql_user, $sql_pass);

    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);           // 设置异常可捕获
    $db->exec('SET NAMES "UTF8"');

    $select = 'select id from code where id like ?';
    $query = $db->prepare($select);
    $query->execute(array($symbol));

    $rtn = array();
    while($data = $query->fetch(PDO::FETCH_ASSOC))
    {
        $rtn[] = $data['id'];
        if(count($rtn) >= 8) {
            break;
        }
    }

    echo json_encode(array('symbol' => $rtn));
}
catch (PDOException $err)
{
//    echo $err->getMessage();
}