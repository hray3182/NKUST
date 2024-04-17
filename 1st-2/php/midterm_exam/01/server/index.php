<?php
    // $USD = 0.030628
    // $JPY = 4.675082
    // $CNY = 0.220994
    // $SGD = 0.041442
    $data = array(
        "USD" => 0.030628,
        "JPY" => 4.675082,
        "CNY" => 0.220994,
        "SGD" => 0.041442
    );
    $selected = $_POST['currency'];
    $amount = $_POST['amount'];
    $result = $data[$selected] * (int)$amount;
    echo json_decode($result);