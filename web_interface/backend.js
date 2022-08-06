


function fetch_word()
{
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8080", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: 'value'
    }));
    xhr.onload = function() {
      console.log("done (;")
      console.log(this.responseText);
      var data = JSON.parse(this.responseText);
      console.log(data);
    }

}


fetch_word();

console.log("Sleep done!")

   
  
