function changeText(idvM){
  const element = document.getElementById(idvM).innerHTML;
  if(element === "Ver más"){
    document.getElementById(idvM).innerHTML="Ver menos";
  }
  else{
    document.getElementById(idvM).innerHTML="Ver más";
  }
}