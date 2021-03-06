<?php
    $username="root";
    $password="root";
    $dbname = "gamejam2021";

    $conn = new mysqli("localhost", $username, $password, $dbname);
    if ($conn->connect_error) {
        header("HTTP/1.1 500 Internal Server Error");
        die("Connection failed: " . $conn->connect_error);
    }

    if (!isset($_GET["name"]) || !isset($_GET["score"]) || !isset($_GET["hash"])) {
        header("HTTP/1.1 500 Internal Server Error");
        die("Missing parameter name, score or hash");
    }

    if ($_GET["hash"] != hash("sha256", $_GET["name"].$_GET["score"]."manySecureMuchSafeSalt")){
        header("HTTP/1.1 500 Internal Server Error");
        die("Hash mismatch! STOP CHEATING NOOB!");
    }

    $conn->query('CREATE TABLE IF NOT EXISTS scores2021 (id INT PRIMARY KEY AUTO_INCREMENT, name TEXT, score FLOAT)');
    $stmt = $conn->prepare("INSERT INTO scores2021 (name, score) VALUES (?, ?)");
    $stmt->bind_param("sd", $name, $score);
    $name = $_GET["name"];
    $score = $_GET["score"];
    $stmt->execute();
    error_log('Score saved');

    $conn->close();
    header("HTTP/1.1 200 OK");
?>

