<?php


$target_dir = "/var/www/html/uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$fileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $uploadOK = 1;
}
// Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}
// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}
// Allow certain file formats
if($fileType != "txt" && $fileType != "doc" && $fileType != "csv" ) {
    echo "Sorry, only simple text files are allowed.";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}




echo "<b>Graph data did something.thing." . "</b><br>";
$fileNameWithPath = ($target_dir . basename( $_FILES["fileToUpload"]["name"]));




$command = escapeshellcmd("python -u /var/www/html/hearCharts/hearCharts/audio_test.py $fileNameWithPath");
$output = shell_exec("python -u /var/www/html/hearCharts/hearCharts/audio_test.py $fileNameWithPath");

?>
