<!DOCTYPE html>
<style>
.title{
    color: forestgreen;
    font-family: monospace;
    font-size: 50px;
    margin-top: 40px;

}

.base_div{
    margin-top: 30px;
    background-color: rgb(34, 34, 34);
    border-radius: 15px;
    width: 900px;
    height: 850px;

}

.php_test{
    font-size: 40px;
}

</style>

<!-- 
    1. set up user reconition to show when a user gets it right

    2. set up a way to show what comments are sent

    3. use len() in php to set up html 

 -->


<html>
<body>
    <center>
    <div class="base_div"> 
        <h1 class="title">Welcome to Kuros tik tok guessing game!</h1>
    </div>
    </center>

    <h1 style="margin-top: -700px; margin-left: 900px;"></h1>
</body>
</html>

<?


function get_usernames() {

    $result = file_get_contents('http://localhost:8080', false); # get request
    return $result;
}












function get_random_word() {
    // send requests to get word info
    
    
    
    // post word on web interface


}









function main() {
    $x = "1";
    while ($x = "1") {
        $res = get_random_word();
        sleep(10);
        
    }
    

}

main();
?>


