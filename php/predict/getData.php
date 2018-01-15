<?php

if(!isset($_COOKIE['username']) || !$_GET['date']) {
    echo 0;
    exit;
}

$url = 'http://market.finance.sina.com.cn/downxls.php?' . http_build_query($_GET);

$ch = curl_init();
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
curl_setopt($ch, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4 );
curl_setopt($ch, CURLOPT_HEADER, false);
$data = curl_exec($ch);
$curl_info = curl_getinfo($ch);
curl_close($ch);

if(strpos($data, "\xb5\xb1\xcc\xec\xc3\xbb\xd3\xd0\xca\xfd\xbe\xdd") !== false)
{
    echo 0;
    exit();
}

$json = array();

$data = iconv('GB2312', 'UTF-8', $data);
$lines = preg_split("/\n/", $data);
foreach($lines as $index => $line)
{
    if($index == 0 || !$line) continue;
    $cols = preg_split('/\s+/', $line);
    $deal_time = $cols[0];
    $deal_price = (float)$cols[1];
    $price_change = $cols[2] == '--' ? 0.0 : $cols[2];
    $volume = (int)$cols[3];
    $turnover = (int)$cols[4];
    $deal_type = $cols[5];
    $json[] = array($deal_time, $deal_price, $price_change, $volume, $turnover, $deal_type);
}

echo json_encode($json);
