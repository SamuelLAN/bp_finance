<?php

    if(isset($_COOKIE['username'])) {
        setcookie('username', $_COOKIE['username'], time() - 3600, '/', null, null, true);
    }
