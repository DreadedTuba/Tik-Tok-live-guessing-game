


function fetch_word()
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "http://127.0.0.1:8080"); 
    xmlHttp.send();
    console.log(xmlHttp.responseText);
  
}


let i = 0;


fetch_word();

console.log("done!")

   
  
