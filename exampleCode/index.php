<!--
    To get php running on your computer:
    IN VSCODE
    
    Go to EXTENSIONS
    type "@builtin php"
    disable PHP Language features
    keep PHP Language Basics enabled

    NOW
    Download PHP Intelephense
    ALSO
    Download PHP Server

    Get XAAMP
    https://www.apachefriends.org/download.html 
    get the version that works for your computer

    WINDOWS:
    Settings => About Computer => Advanced System Settings 
    => Environment Variables => Click Path => New 
    =>Copy the php version's path

    NOW
    Go to the file => Right Click 
    => Click "PHP Server: Serve Project" 
    => DONE!!!
-->
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>hello</title>
        <meta charset="UTF-8">
        <meta name="viewset" content="device-width,initial-scale=10">
        <title>Document</title>
    </head>
    <body>
        <form action="practice.php" method="POST">
            <!--
                GET: unsafe way to send info,
                POST: safe way to send info,
                REQUEST: if you don't know you used
                        in the other php file,
                COOKIE: 
            -->
            <input type="text" name="username">
            <button type="submit">Click Me!!!</button>
        </form>
    </body>
</html>


