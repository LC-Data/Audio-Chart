<?php

$now = DateTime::createFromFormat('U.u', microtime(true));      //get the exact datetime of upload, ensures unique file name
$nowFormatted = $now->format("m-d-Y-H:i:s:u");      //format the datetime to be a usable string
$target_dir = "/var/www/html/uploads/";             //where we are uploading to
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);         //the barebones file name "abc.txt"
$uploadOk = 1;                                  //an upload flag. default flag set to "1", ok.
$fileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));      //grabs the extension of file uploaded so we can ensure it is acceptable
$fileNameWithPath = ($target_dir . $nowFormatted . ".". $fileType);     //the path to the file on our server, !!!! NOTICE WE RENAME THE FILE TO THAT UNIQUE DATETIME !!!!
$fileNameWithoutExtension = ($target_dir . $nowFormatted);                   // ^ the above minus the file extension - we remove the extension so combine.py can handle .wav and .mp4 files that have the same name.





//Check if something was actually posted
if(isset($_POST["submit"])) {
    $uploadOK = 1;
}
// Check if file already exists
if (file_exists($fileNameWithPath)) {
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
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $fileNameWithPath)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}


echo "<br><b>Graph data did something" . "</b><br>";

echo $fileNameWithPath;


$output = shell_exec("python -u /var/www/html/hearCharts/hearCharts/audio_test.py $fileNameWithPath $fileNameWithoutExtension");
$testOut = shell_exec("python -u /var/www/html/hearCharts/hearCharts/combine.py $fileNameWithoutExtension");

?>
