<?php
// the $_POST[] array will contain the passed in filename and data
$file = $_POST['filename'].date("_d-m-y-His").'.json';
$data = $_POST['filedata'];
file_put_contents("data/".$file, $data);
?>