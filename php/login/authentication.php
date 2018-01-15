<?php
    if(!isset($_POST['username']) || !isset($_POST['password'])) {
        echo 0;
        exit;
    }

    $username = $_POST['username'];
    $password = $_POST['password'];

    if(($username == 'Samuel' || $username == '412206186@qq.com') && $password == '111111') {
        echo 1;
        setcookie('username', md5($username), time() + 3600 * 24, '/', null, null, true);
    }
