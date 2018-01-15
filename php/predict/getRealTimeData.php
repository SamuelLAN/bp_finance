<?php

    if(!isset($_COOKIE['username']) || !isset($_GET['symbol'])) {
        echo 0;
        exit;
    }

    $symbol = $_GET['symbol'];

    $url = 'http://hq.sinajs.cn/list=' . $symbol;

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

    preg_match('/"([^"]*)"/', $data, $matches);
    if(!isset($matches[1])) {
        echo 0;
        exit;
    }
    $data = preg_split('/,/', $matches[1]);

    $encoding = mb_detect_encoding($data[0], array('UTF-8', 'GB2312', 'UTF-16', 'UCS-2', 'BIG5', 'ASCII'));
    $data[0] = iconv($encoding, 'UTF-8', $data[0]);

    $json = array(
        'name' => $data[0],
        'open' => $data[1],
        'last_end' => $data[2],
        'price' => $data[3],
        'highest' => $data[4],
        'lowest' => $data[5],
        'volume' => (int)((int)$data[8] / 100),
        'turnover' => $data[9],
    );

    echo json_encode($json);
    exit;
