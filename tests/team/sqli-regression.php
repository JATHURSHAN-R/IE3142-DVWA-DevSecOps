<?php

mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

define('MYSQL', 'mysql');
$_DVWA = ['SQLI_DB' => MYSQL];

$db = new mysqli(
    getenv('DB_SERVER'),
    getenv('DB_USER'),
    getenv('DB_PASSWORD'),
    getenv('DB_DATABASE')
);

$GLOBALS['___mysqli_ston'] = $db;

function lookupForTest($input): string {
    global $_DVWA;

    $_REQUEST = [
        'Submit' => 'Submit',
        'id' => $input
    ];

    $html = '';

    require __DIR__ . '/../../vulnerabilities/sqli/source/low.php';

    return $html;
}

try {
    $db->query(
        'CREATE TEMPORARY TABLE users (
            user_id INT PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100)
        )'
    );

    $db->query(
        "INSERT INTO users VALUES (1, 'A & B', 'Example')"
    );

    $invalid = 'Enter a valid positive integer ID.';

    $cases = [
        ['existing ID and encoded name', '1', 'First name: A &amp; B'],
        ['missing ID', '2', 'No matching user.'],
        ['empty input', '', $invalid],
        ['alphabetic input', 'abc', $invalid],
        ['mixed input', '1abc', $invalid],
        ['zero', '0', $invalid],
        ['negative input', '-1', $invalid],
        ['array input', ['1'], $invalid]
    ];

    foreach ($cases as [$label, $input, $expected]) {
        $actual = lookupForTest($input);

        if (!str_contains($actual, $expected)) {
            throw new RuntimeException("FAIL: {$label}");
        }

        echo "PASS: {$label}\n";
    }

    echo "All SQL regression checks passed\n";
} finally {
    // Closing this connection also removes its temporary table.
    $db->close();
}
