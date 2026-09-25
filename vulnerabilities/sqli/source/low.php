<?php

if (isset($_REQUEST['Submit'])) {
    $raw = $_REQUEST['id'] ?? null;

    $id = is_string($raw)
        ? filter_var($raw, FILTER_VALIDATE_INT, [
            'options' => [
                'min_range' => 1,
                'max_range' => 2147483647
            ]
        ])
        : false;

    if ($id === false) {
        $html .= '<pre>Enter a valid positive integer ID.</pre>';
    } elseif ($_DVWA['SQLI_DB'] !== MYSQL) {
        $html .= '<pre>This team fix supports MySQL only.</pre>';
    } else {
        $stmt = null;

        try {
            $db = $GLOBALS['___mysqli_ston'];

            $stmt = mysqli_prepare(
                $db,
                'SELECT first_name, last_name FROM users WHERE user_id = ?'
            );

            if (!$stmt
                || !mysqli_stmt_bind_param($stmt, 'i', $id)
                || !mysqli_stmt_execute($stmt)
                || !mysqli_stmt_bind_result($stmt, $first, $last)) {
                throw new RuntimeException('Query failed');
            }

            $found = false;

            while (mysqli_stmt_fetch($stmt)) {
                $found = true;

                $firstSafe = htmlspecialchars(
                    (string) $first,
                    ENT_QUOTES | ENT_SUBSTITUTE,
                    'UTF-8'
                );

                $lastSafe = htmlspecialchars(
                    (string) $last,
                    ENT_QUOTES | ENT_SUBSTITUTE,
                    'UTF-8'
                );

                $html .= "<pre>ID: {$id}<br />First name: "
                    . $firstSafe
                    . '<br />Surname: '
                    . $lastSafe
                    . '</pre>';
            }

            if (!$found) {
                $html .= '<pre>No matching user.</pre>';
            }
        } catch (Throwable $error) {
            $html .= '<pre>Unable to complete the lookup.</pre>';
        } finally {
            if ($stmt) {
                mysqli_stmt_close($stmt);
            }
        }
    }
}
