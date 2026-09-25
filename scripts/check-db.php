<?php

try {
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

    $db = new mysqli(
        getenv('DB_SERVER'),
        getenv('DB_USER'),
        getenv('DB_PASSWORD'),
        getenv('DB_DATABASE')
    );

    $row = $db->query('SELECT 1')->fetch_row();

    if ((int) $row[0] !== 1) {
        throw new RuntimeException('Unexpected database result');
    }

    $db->close();
    echo "Database communication passed\n";
} catch (Throwable $error) {
    fwrite(STDERR, "Database communication failed. Check configuration locally.\n");
    exit(1);
}
