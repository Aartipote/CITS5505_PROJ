

$(document).ready(function(){
    var elements = document.querySelectorAll("input");
    console.log(elements)
    for(i=1;i<5;i++){
        elements[i].setAttribute("required","true");
    }
});


var awards = document.getElementById("trophy");
console.log(awards)
var btnn1=document.getElementById("btnn");

btnn1.addEventListener("click",function(){
    
    var requestvalue = new XMLHttpRequest();
    requestvalue.open('GET','https://coronavirus-tracker-api.herokuapp.com/v2/locations')
    requestvalue.onload = function(){
        var ourdata = JSON.parse(requestvalue.responseText);
        
        justcallHTML(ourdata);
    };
    requestvalue.send();
});
function justcallHTML(data){
    var varname="";
    var country_name="";
    var latest_confirmed = "";
    locations=data.locations;

    for(i=0; i<locations.length; i++){
        country_name=locations[i].country;
        latest_confirmed = locations[i].latest;
     
        varname+= "<li> In " +"<b>" +country_name +"</b>" +" there were around "+ latest_confirmed.confirmed+" confirmed cases.</li>";

    
   }

   awards.insertAdjacentHTML('beforeend',varname);
};