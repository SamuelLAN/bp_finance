<?php

?>
<html>
    <head>
        <meta charset="utf-8">
        <title>Login</title>
        <link href="index.css" type="text/css" rel="stylesheet">
    </head>
    <body>
<!--        <img src="" class="bg">-->
        <div id="frame">
            <input type="text" id="username" class="input" placeholder="username">
            <input type="password" id="password" class="input" placeholder="password">
            <div id="confirm">Confirm</div>
        </div>
        <div class="tip">If u want account and password, mail to me <a href="mailto:412206186@qq.com" target="_blank">412206186@qq.com</a></div>
        <div id="notice" style="display: none">
            用户名或密码错误
            <div id="cancel">Cancel</div>
        </div>
        <div id="mask" style="display: none"></div>
        <script type="text/javascript" src="jquery.min.js"></script>
        <script type="text/javascript" src="index.js"></script>
    </body>
</html>
