<?php
if (isset($_GET['file_name'])) {
    header('Content-type: image/png');
    $im = imagecreatefrompng($_GET['file_name']);
    $im0 = imagecreatefrompng($_GET['file_name']);
    $w = imagesx($im);
    $h = imagesy($im);
    for ($y = 0; $y < $h; $y++) {
        for ($x = 0; $x < $w; $x++) {
            if ((imagecolorat($im, $x, $y) & 0xFF) > (256 / 2)) {
                imagesetpixel($im, $x, $y, 0xFFFFFF);
                imagesetpixel($im0, $x, $y, 0xFFFFFF);
            } else {
                imagesetpixel($im, $x, $y, 0x000000);
                imagesetpixel($im0, $x, $y, 0x000000);
            }
        }
    }
    $open = false;
    for ($y = 0; $y < $h; $y++) {
        for ($x = 0; $x < $w; $x++) {
            if ($open != true) {
                if (imagecolorat($im, $x, $y) == 0xFFFFFF) {
                    $open = true;
                    $start = $x;
                }
            } else {
                if (imagecolorat($im, $x, $y) == 0x000000) {
                    $open = false;
                    $x0 = $x - 1;
                    $c = round(($start + $x0) / 2);
                    imageline($im, $start, $y, ($c - 1), $y, 0x000000);
                    imageline($im, ($c + 1), $y, $x0, $y, 0x000000);
                }
            }
        }
    }
    $open = false;
    for ($x = 0; $x < $w; $x++) {
        for ($y = 0; $y < $h; $y++) {
            if ($open != true) {
                if (imagecolorat($im0, $x, $y) == 0xFFFFFF) {
                    $open = true;
                    $start = $y;
                }
            } else {
                if (imagecolorat($im0, $x, $y) == 0x000000) {
                    $open = false;
                    $y0 = $y - 1;
                    $c = round(($start + $y0) / 2);
                    imagesetpixel($im, $x, $c, 0xFFFFFF);
                }
            }
        }
    }
    imagepng($im);
    imagedestroy($im);
} else
    echo "Ви не задали шаблон для виведення";
?>