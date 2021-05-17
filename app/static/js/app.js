console.log("Hello from app.js");

//alert("Something went wrong");


// javascript for required validation on assessment page

// function validate(){
//     var valid = false;

//     var x = document.getElementById.question1;
//     for (var i=0; i<x.length;i++){
//         if(x[i].checked){
//             valid = true;
//             break;
//         }
//     }
//     if (value == true){
//         alert("Please Select an answer.")
//         return redirect(url_for("assessment"))
//     }
// }


$(document).ready(function(){
    var elements = document.querySelectorAll("input");
    console.log(elements)
    for(i=1;i<5;i++){
        elements[i].setAttribute("required","true");
    }
})

$(document).ready(function() {
    var f = document.getElementById('Foo');
    setInterval(function() {
        // f.style.display = (f.style.display == 'none' ? '' : 'none');
        $("#Foo").fadeIn(3000);
    }, 1000);

});