function mostrarPreguntas(id){
    clear();
    var element2 = document.getElementById("main");
    element2.style.display = "none";
    const element = document.getElementById(id);
    switch(id){
        case 'empresa':{
            $("#empresa").load("../FAQ/empresa.html");
            element.style.display = "block";
            break;
        }
        case 'servicios':{
            $("#servicios").load("../FAQ/servicios.html");
            element.style.display = "block";
            break;
        }
        case 'pago':{
            $("#pago").load("../FAQ/pago.html");
            element.style.display = "block";
            break;
        }
    }
}

function clear(){
    const element2 = document.getElementsByClassName("faq");
    for(var i = 0; i < element2.length; i++){
        element2[i].style.display = "none";
    }
}