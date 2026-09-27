<?php

if (isset($_POST['Upload'])) {
    $image = null;
    $destination = null;

    try {
        $upload = $_FILES['uploaded'] ?? null;

        if (!is_array($upload)
            || ($upload['error'] ?? null) !== UPLOAD_ERR_OK
            || !is_string($upload['tmp_name'] ?? null)
            || !is_string($upload['name'] ?? null)
            || !is_uploaded_file($upload['tmp_name'])) {
            throw new RuntimeException('Invalid upload');
        }

        $tmp = $upload['tmp_name'];
        $size = filesize($tmp);
        $ext = strtolower(pathinfo($upload['name'], PATHINFO_EXTENSION));
        $mime = (new finfo(FILEINFO_MIME_TYPE))->file($tmp);

        if ($size === false || $size < 1 || $size > 2 * 1024 * 1024
            || $ext !== 'png' || $mime !== 'image/png') {
            throw new RuntimeException('Invalid image type or size');
        }

        $dimensions = @getimagesize($tmp);

        if (!$dimensions || $dimensions[0] < 1 || $dimensions[1] < 1
            || $dimensions[0] > 2048 || $dimensions[1] > 2048) {
            throw new RuntimeException('Invalid dimensions');
        }

        $image = @imagecreatefrompng($tmp);

        if ($image === false) {
            throw new RuntimeException('Cannot decode image');
        }

        // Never save the original bytes or original filename.
        $name = bin2hex(random_bytes(16)) . '.png';
        $destination = '/var/lib/dvwa-uploads/' . $name;

        if (!imagepng($image, $destination)
            || !chmod($destination, 0600)) {
            throw new RuntimeException('Cannot save image');
        }

        $html .= '<pre>PNG stored outside the web root. Reference: '
            . $name . '</pre>';

    } catch (Throwable $e) {

        if ($destination && is_file($destination)) {
            unlink($destination);
        }

        $html .= '<pre>Upload rejected. Use a PNG up to 2 MiB '
            . 'and 2048 by 2048 pixels.</pre>';

    } finally {

        if ($image instanceof GdImage) {
            imagedestroy($image);
        }
    }
}