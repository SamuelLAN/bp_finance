<?php

if(!isset($_COOKIE['username']) || !$_GET['symbol']) {
	echo 0;
	exit;
}

$param = ['list' => $_GET['symbol']];

$url = 'http://hq.sinajs.cn/' . http_build_query($param);

$ch = curl_init();
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$data = curl_exec($ch);
$curl_info = curl_getinfo($ch);
curl_close($ch);

$http_code = $curl_info['http_code'];

if ($http_code != 200 || !$data)
{
	echo 0;
	exit();
}

preg_match('/"([^"]+)"/', $data, $matches);

$data = $matches[1];
$data = explode(',', $data);

$name = $data[0];

$encoding = mb_detect_encoding($name, array("ASCII",'UTF-8',"GB2312","GBK",'BIG5'));
$name = mb_convert_encoding($name, 'UTF-8', $encoding);

$json = array(
	'name' => $name,
	'open' => $data[1],
	'last_end' => $data[2],
	'price' => $data[3],
	'highest' => $data[4],
	'lowest' => $data[5],
	'volume' => $data[8],
	'turnover' => $data[9],
);

echo json_encode($json);
exit();
