<?php
    $username="root";
    $password="root";
    $dbname = "gamejam2021";

    $conn = new mysqli("localhost", $username, $password, $dbname);
    if ($conn->connect_error) {
        header("HTTP/1.1 500 Internal Server Error");
        die("Connection failed: " . $conn->connect_error);
    }

    $conn->query('CREATE TABLE IF NOT EXISTS scores2021 (id INT PRIMARY KEY AUTO_INCREMENT, name TEXT, score FLOAT)');
    $sql = "SELECT name, score FROM scores2021 ORDER BY score DESC";
    $result = $conn->query($sql);
    $scores = [];
    while ($result && $row = $result->fetch_assoc()) {
        $scores[] = $row;
    }
    $conn->close();
?><!doctype html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>GameJam 2021 Highscores</title>

    <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css" integrity="sha384-B0vP5xmATw1+K9KRQjQERJvTumQW0nPEzvF6L/Z6nronJ3oUOFUFpCjEUQouq2+l" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/js/bootstrap.min.js" integrity="sha384-+YQ4JLhjyBLPDQt//I+STsc9iw4uQqACwlvpslubQzn4u2UU2UFM80nGisd026JF" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container pt-5">
        <div class="text-center pt-5">
            <h1>GameJam 2021 Highscores</h1>
            <table class="table table-striped table-bordered mt-5">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($scores as $score): ?>
                        <tr>
                            <td><?= strip_tags($score['name']) ?></td>
                            <td><?= strip_tags($score['score']) ?></td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>