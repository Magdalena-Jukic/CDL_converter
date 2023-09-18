<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        a{
            text-decoration: none;
            display: inline-block;
            color:black;
            margin: 10px 40px;
            font-size: 20px;
        }
        .header {
            padding: 30px;
            text-align: left;
            background: black;
            color: white;
            font-size: 20px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Configuration Reference</h1>
        <p>Here is the list of files. More information on product's configuration parameters is available in Configuration Reference document.</p>
    </div>
   
    <?php

        $path = __DIR__ ."/html";
        $files = scandir($path);

        foreach($files as $file){
            if($file != "." && $file != ".." && str_contains($file, ".html"))
            {
                $filename = pathinfo($path."/".$file);
                echo "<a href='html/{$file}'>{$filename['filename']}</a><br>";
                #bez ekstenzije
                                                #echo "<a href='{$file}'>{$file}</a><br>"; #opcija sa ekstenzijom
                
            }
        }
    ?>
</body>
</html> 

