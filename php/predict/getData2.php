<?php

if(!isset($_COOKIE['username']) || !$_GET['symbol']) {
    echo 0;
    exit;
}

$param = array(
    'stockid' => $_GET['symbol'],
    'list' => 1,
);

$url = 'http://apis.baidu.com/apistore/stockservice/stock?' . http_build_query($param);

$headers = array(
    'apikey: 89a4bd5eca67cf899dc2490f1e2a52ae',
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
curl_setopt($ch, CURLOPT_MAXREDIRS, 10);
curl_setopt($ch, CURLOPT_IPRESOLVE, CURL_IPRESOLVE_V4 );
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
$data = curl_exec($ch);
$curl_info = curl_getinfo($ch);
curl_close($ch);


$data = json_decode($data);
if($data->errNum != 0) {
    echo 0;
    exit;
}

$data = $data->retData->stockinfo;
$data = $data[0];

$encoding = mb_detect_encoding($data->name, array('UTF-8', 'GB2312', 'UTF-16', 'UCS-2', 'BIG5', 'ASCII'));
$data->name = iconv($encoding, 'UTF-8', $data->name);

$json = array(
    'name' => $data->name,
    'open' => $data->OpenningPrice,
    'last_end' => $data->closingPrice,
    'price' => $data->currentPrice,
    'highest' => $data->hPrice,
    'lowest' => $data->lPrice,
    'volume' => $data->totalNumber,
    'turnover' => $data->turnover,
);

echo json_encode($json);
exit;
