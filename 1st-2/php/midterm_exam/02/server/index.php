<?php

$data = array(
    1 => 14,
    2 => 13,
    3 => 12,
    4 => 11,  
);

$q = $_POST['q'];
$ans = $_POST['ans'];
if ($data[$q] == $ans) {
    echo json_encode(array('result' => '正確', 'color' => 'green'));
} else {
    echo json_encode(array('result' => '錯誤', 'color' => 'red'));
}
