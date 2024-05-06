<?php

$db_host = "localhost";
$db_user = "rootHAHAHA"; // 故意寫錯
$db_pwd = "";
$db_name = "student";
$db_table = "student";
$dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8";
$conn = new PDO($dsn, $db_user, $db_pwd);

$query_sql = "SELECT * FROM $db_table";

$stmt = $conn->prepare($query_sql);
$result = $stmt->execute();
if ($result) {
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    $response['status'] = 200; //OK;
    $response['message'] = "查詢成功";
    $response['result'] = $rows;
} else {
    $response['status'] = 500; //Server Error;
    $response['message'] = "查詢失敗";
}
echo json_encode($response);