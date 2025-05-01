<?php

// Exemplo de SQL Injection
$user = $_GET['user'];
$password = $_GET['pass'];
$query = "SELECT * FROM users WHERE username = '$user' AND password = '$password'";
$result = mysqli_query($conn, $query);

// Variável não utilizada
$debug = true;

// Função grande sem coesão
function processStuff($input) {
    for ($i = 0; $i < 100; $i++) {
        echo $i;
    }
    $json = json_decode($input);
    file_put_contents("log.txt", $json->data);
}

?>
