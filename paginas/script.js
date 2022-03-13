//Función a la que se llama al cargar la página principal
function inicio() {

  //True significa que volveremos a cargar la página inicial
  var flag_redir = true;

  //True significa que no está creada la cookie de visita
  var flag_visita = true;

  //Miramos las cookies de la página
  var cookies = document.cookie.split(';');
  for(var i =0;i<cookies.length; i++){
    //La cookie de index nos dice si debemos pedir el apodo al usuario o no
    if(cookies[i].includes("index")){
      flag_redir=false;
      //Significa que tiene la cookie pero aún no se ha pedido el apodo
      if(cookies[i].split('=')[1] === "primera"){
        document.cookie="index=completo; path = /";

        //Esto se hace para poder poner caracteres especiales en el prompt
        var div = document.createElement('div');
        div.innerHTML = "&iquestApodo?";
        var decoded = div.firstChild.nodeValue;

        var nombre = prompt(decoded);
        document.cookie="apodo=" + nombre + "; path = /";

        //Volvemos a cargar la página
        window.location.replace("/");
      }
      //Ya se ha pedido el apodo, se indica el nombre en la cabecera
      else{
        //Buscamos la cookie de apodo
        for(var j =0;j<cookies.length; j++){
          if(cookies[j].includes("apodo")){
            //Añadimos el apodo a la web
            document.getElementById('apodo').innerHTML = "Ha iniciado sesi&oacuten como: " + cookies[j].split('=')[1];
          }
        }
      }

      //La cookie de visita nos indicará los grupos que ha visitado el usuario
    }else if(cookies[i].includes("visita")){
      flag_visita = false;
      anterior = cookies[i].split("=")[1];

      //Si no ha visitado ninguno aún
      if(anterior === ""){
        gruVisi = "Ninguno";

      }else{
        //Si el usuario ha visitado más de 10 grupos
        if (anterior.split("*TFG*").length >= 10){
          //Modificamos el texto dado el caso
          document.getElementById("visi").innerHTML = "&Uacuteltimos 10 grupos visitados: <span id='gruVisi'></span>";
        }

        //Grupos visitados
        gruVisi = anterior;

      }

      //Añadimos la cookie
      document.cookie="visita=" + gruVisi.replace("Ninguno","") + "; path = /";

      //Obtenemos los grupos de la cookie
      gruVisiSplit = gruVisi.split("*TFG*");

      textoFinal = "";

      //Obtenemos el texto a añadir
      if(gruVisi==="Ninguno"){
        textoFinal = gruVisi + "..";
      }
      else{
        for(k=0; k<gruVisiSplit.length; k++){
          textoFinal = textoFinal + "<a href='/grupos/" + replaceName(gruVisiSplit[k]) + "' class='link' >" + gruVisiSplit[k] + "</a>, "
        }
      }

      //Añadimos lo conveniente en cada caso al apartado Visitados: de la web
      document.getElementById("gruVisi").innerHTML = textoFinal.substring(0,textoFinal.length -2);

    }
  }

  //Redirigimos a la página principal si hiciera falta
  if(flag_redir){
    document.cookie="index=primera; path = /";
    window.location.replace("/");
  }

  //Creamos la cookie de visita si hiciera falta
  if(flag_visita){
    document.cookie="visita=; path = /";
  }

}

//Función a la que se llama al cargar las páginas de los grupos
function inicioGrupos() {
  //True significa que volveremos a cargar la página inicial
  var flag_redir = true;

  //True significa que no está creada la cookie de visita
  var flag_visita = true;

  //Miramos qué grupo estamos visitando
  var grupo = document.getElementById("nombreGrupo").innerHTML.split("&amp;").join("&");

  //Miramos las cookies de la página
  var cookies = document.cookie.split(';');
  for(var i =0;i<cookies.length; i++){
    //La cookie de index nos dice si debemos pedir el apodo al usuario o no
    if(cookies[i].includes("index")){
      flag_redir=false;
      for(var j =0;j<cookies.length; j++){
        //Buscamos la cookie de apodo
        if(cookies[j].includes("apodo")){
          //Añadimos el apodo a la web
          document.getElementById('apodo').innerHTML = "Ha iniciado sesi&oacuten como: " + cookies[j].split('=')[1];
        }
      }

      //La cookie de visita nos indicará los grupos que ha visitado el usuario
    }else if(cookies[i].includes("visita")){
      flag_visita = false;
      anterior = cookies[i].split("=")[1];

      //Si no ha visitado ninguno aún
      if(anterior === ""){
        gruVisi = grupo;

        //Si se está visitando un grupo inexistente o uno que ya se ha visitado antes
      }else if(grupo.includes("Este grupo no existe") || anterior.includes(grupo)){
        gruVisi = anterior;
      }else{
        //Si el usuario ha visitado más de 10 grupos (contando el actual)
        if (anterior.split("*TFG*").length >= 10){
          //Cogemos solo los 9 últimos grupos
          indice = anterior.indexOf("*TFG*");
          anterior = anterior.substring(indice +5);

          //Modificamos el texto a mostrar
          document.getElementById("visi").innerHTML = "&Uacuteltimos 10 grupos visitados: <span id='gruVisi'></span>";
        }
        //Añadimos el grupo actual
        gruVisi = anterior + "*TFG*" + grupo;

      }

      //Añadimos el grupo a la cookie
      document.cookie="visita=" + gruVisi + "; path = /";

      //Obtenemos los grupos
      gruVisiSplit = gruVisi.split("*TFG*");

      //Obtenemos el texto a mostrar
      textoFinal = "";
      for(k=0; k<gruVisiSplit.length; k++){
        textoFinal = textoFinal + "<a href='/grupos/" + replaceName(gruVisiSplit[k]) + "' class='link' >" + gruVisiSplit[k] + "</a>, "
      }

      //Añadimos el texto
      document.getElementById("gruVisi").innerHTML = textoFinal.substring(0,textoFinal.length -2);

    }
  }

  //Redirigimos a la página principal si hiciera falta
  if(flag_redir){
    document.cookie="index=primera; path = /";
    window.location.replace("/");
  }

  //Creamos la cookie de visita si hiciera falta
  if(flag_visita && !grupo.includes("Este grupo no existe")){
    document.cookie="visita=" + grupo + "; path = /";
  }

}

//Función para modificar el nombre de los grupos para poder procesarlos correctamente
function replaceName(name){
  return name.split("'").join("%TFGComa").split("/").join("%TFGBarra").split("?")
  .join("%TFGPregunta").split(".").join("%TFGPunto");
}

//Función para reiniciar todo (grupos visitados, apodo, etc.)
function reset(){
  document.cookie="index=primera; path = /";
  window.location.replace("/");
  document.cookie = "visita=; path =/"
}


//Función a la que se llama cada vez que se presiona una tecla en el recuadro de buscar
//Se encarga de enviar una petición al servidor para buscar grupos y de presentar el resultado
function buscar(){
  //Obtenemos el texto de la caja de búsqueda
  var texto = document.getElementById("buscar").value.split("?")
  .join("%TFGPregunta").split(".").join("%TFGPunto");

  //Obtenemos el elemento donde se va a presentar el resultado
  var lista = document.getElementById("lista");
  lista.innerHTML=""

  if(texto==""){
    lista.style.visibility = "hidden";
  }else{

    //Hace la petición al servidor
    httpGet("/buscar/" + texto).then(function (e){
      var respuesta = e.target.response;

      //No se han encontrado grupos
      if(respuesta.includes("MAINPAGE")){
        respuesta="<li>No se ha encontrado ning&uacuten grupo</li>";
      }

      //Sin grupos
      if(respuesta==""){
        lista.style.visibility = "hidden";
      }else{
        //La respuesta contiene grupos
        lista.innerHTML= respuesta;
        lista.style.visibility = "visible";
      }
    });

  }

}

//Función para obtener nuevos grupos aleatorios
function aleatorio(){

  var ale = document.getElementById("aleatorio")
  var load = document.getElementById("loading")
  var aleButton = document.getElementById("aleatorioButton")

  ale.style.display="none";
  aleButton.style.display="none";
  load.style.display="inline-block";

  //Hace la petición al servidor
  httpGet("/aleatorio").then(function (e){
    var respuesta = e.target.response;
    //Reemplaza el contenido del elemento por la respuesta
    if(respuesta !== ""){
      ale.innerHTML= respuesta;
    }else{
      ale.innerHTML= "Error, prueba otra vez";
    }

    ale.style.display="inherit";
    aleButton.style.display="inherit";
    load.style.display="none";

  })

}

//Función para realizar cualquier petición al backend
function httpGet(nombre)
{
  return new Promise(function (resolve, reject) {
    //Calcula la url de la página
    var loc = window.location.href;
    var index = 0;
    for (var i = 0; i<3; i++){
      index = loc.indexOf("/", index+1);
    }

    //Realiza la petición
    var url = loc.substring(0,index) + nombre;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url );
    xmlHttp.onload = resolve;
    xmlHttp.onerror = reject;
    xmlHttp.send();

  });
}


//Función para ir a la página de top 100 grupos
function topGrupos(){
  //Calcula la url de la página y le añade /top
  var loc = window.location.href;
  var index = 0;
  for (var i = 0; i<3; i++){
    index = loc.indexOf("/", index+1);
  }

  window.location.href = loc.substring(0,index) + "/top";
}

//Función para ir a la página principal
function inicioBoton(){
  window.location.replace("/");
}
