const more_filters=document.querySelector("#mrefil");
more_filters.style.display='none';
const submit = document.querySelector('#go');
const search = document.querySelector('#q');


submit.disabled = true;


search.onkeyup = () => {
    if (search.value.length > 2) {
        submit.disabled = false;
    }
    else {
        submit.disabled = true;
    }
}

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1;
var yyyy = today.getFullYear();
if(dd<10){
    dd='0'+dd
}
if(mm<10){
    mm='0'+mm
}

today = yyyy+'-'+mm+'-'+dd;
document.getElementById("frmdt").setAttribute("max", today);
document.getElementById("todt").setAttribute("max", today);
submit.onclick=function(e){
  const from=document.querySelector("#frmdt");
  const to=document.querySelector("#todt");
  const source=document.querySelector("#src");
  const domain=document.querySelector("#dom");
  if (from.value!=="" && to.value!==""){
    if(from.value>to.value){
    alert("Error in date entry, please try again!");
    e.preventDefault();
    return;}
  }
  else if(from.value==="" && to.value!==""){
    alert("From date not provided, please try again!");
    e.preventDefault();
    return;
  }

};

document.querySelector("#more_fil").onclick=function(){
  if(more_filters.style.display=='block'){
  more_filters.style.display='none';
  document.querySelector("#spl").innerHTML=`&darr;`;}
  else {
    more_filters.style.display='block';
      document.querySelector("#spl").innerHTML=`&uarr;`;
  }
};
const tp_submit = document.querySelector('#q-go');
const tp_search = document.querySelector('#q-top');


tp_submit.disabled = true;


tp_search.onkeyup = () => {
    if (tp_search.value.length > 2) {
        tp_submit.disabled = false;
    }
    else {
        tp_submit.disabled = true;
    }
}

tp_submit.onclick=function(e){
  if(document.querySelector("#countries").value=="" || document.querySelector("#categories").value=="")
    {
      alert("One or more fields missing, please try again!");
      e.preventDefault();
      return;
    }

};
//get cookie for category update
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;}

//category stuff
document.querySelectorAll(".cat").forEach((button, i) => {
  button.onclick=function(){


    fetch("/updateCategory",{
      method: 'PUT',
      body:JSON.stringify({
        category:button.dataset.cat
      }),
      credentials: 'same-origin',
      headers: {
      "X-CSRFToken": getCookie("csrftoken")
  }
    })
    .then(response=>response.json())
    .then(result=>{
      if(result.status){
        button.className="btn btn-outline-danger rounded-circle btn-sm";
        button.innerHTML=`&minus;`
      }
      else{
        button.className="btn btn-outline-success rounded-circle btn-sm";
        button.innerHTML=`&plus;`
      }
    });

  };

});
