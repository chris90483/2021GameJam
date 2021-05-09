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

    $conn->query('CREATE TABLE IF NOT EXISTS scores2021 (id INT PRIMARY KEY AUTO_INCREMENT, name TEXT, score FLOAT, pizzas_delivered INT, zombies_killed INT)');
    $stmt = $conn->prepare("INSERT INTO scores2021 (name, score, pizzas_delivered, zombies_killed) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("sdii", $name, $score, $pizzas_delivered, $zombies_killed);
    $name = $_GET["name"];
    $score = $_GET["score"];
    $pizzas_delivered = $_GET["pizzas_delivered"];
    $zombies_killed = $_GET["zombies_killed"];
    $stmt->execute();
    error_log('Score saved');

    $conn->close();
    header("HTTP/1.1 200 OK");
?>

