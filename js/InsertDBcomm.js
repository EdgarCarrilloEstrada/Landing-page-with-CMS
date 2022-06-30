function insertComment(){
  let fnamef     = $('#fname');
  let fcommentf     = $('#fcomment');

  let fname     = $('#fname').val();
  let fcomment  = $('#fcomment').val();
  if(fname !== ""){
    if(fcomment !== ""){
      $.ajax({
        type: "POST",
        url: "../PHP/InsertComment.php",
        data: {
          fname: fname,
          fcomment: fcomment,
        },
        cache: false,
        success: function(data) {
          alert("hecho");
          const element = document.getElementById("valid").innerHTML="";
          fnamef.val('');
          fcommentf.val('');
          Swal.fire(
            'Hecho!',
            'Gracias por dejarnos tus comentarios!',
            'success'
          )
        },
        error: function(xhr, status, error) {
          console.error(xhr);
          const element = document.getElementById("valid").innerHTML="";
          Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Parece que algo salió mal!',
            footer: 'Inténtalo más tarde'
          })
        }
      });
    }
    else{
      var element = document.getElementById("valid").innerHTML="*Debes llenar todos los campos";
      function hide(){
        element = document.getElementById("valid").innerHTML="";
      }
      setInterval(hide ,10000);
    }
  }
  else{
    var element = document.getElementById("valid").innerHTML="*Debes llenar todos los campos";
    function hide(){
      element = document.getElementById("valid").innerHTML="";
    }
    setInterval(hide ,10000);
  }
}