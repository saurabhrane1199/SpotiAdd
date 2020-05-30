'use strict';
var clientId = "6b7918c1951a48f89dd7d360a17b4eac";
var clientSecret = "a435d9849f194fe08319203c936a5c5b";
var count_row = 0;
var id;
var url;
var spotify_access_token;
var redirect_uri = "https://aoighdinhjbeihojpleaohghnfecjjmo.chromiumapp.org/provider_sp";
var auth_url = "https://accounts.spotify.com/authorize?client_id=6b7918c1951a48f89dd7d360a17b4eac&response_type=code&redirect_uri="+redirect_uri+"&scope=playlist-modify-public playlist-modify-private";
var is_spotify_auth = false;
var submitButton = 

chrome.tabs.query({ 'active': true, 'currentWindow': true }, function (tabs) {
  url = tabs[0].url;
  id = url.split('v=')[1]
});


//get OAuthCode
function getAuthCode(code){
  let encodedData = btoa(clientId + ':' + clientSecret);
  console.log(encodedData,"Encoded Data");

  var myHeaders = new Headers();
myHeaders.append("Authorization", "Basic " + encodedData);
myHeaders.append("Content-Type", "application/x-www-form-urlencoded");

var urlencoded = new URLSearchParams();
urlencoded.append("grant_type", "authorization_code");
urlencoded.append("code", code);
urlencoded.append("redirect_uri", redirect_uri);

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: urlencoded,
};

fetch("https://accounts.spotify.com/api/token", requestOptions)
  .then(response => response.text())
  .then(result => {
    let jsonRes = JSON.parse(result);
    console.log(jsonRes["access_token"],"RESULT DUMP")
    spotify_access_token =  jsonRes["access_token"];
    console.log(spotify_access_token,"SPOTIFY ACCESS TOKEN")
    return;
  })
  .catch(error => console.log('error', error));

}


//API CALL
function getSongs(id){
  fetch('http://127.0.0.1:5000/'+id+'?code='+spotify_access_token)
    .then(r => r.text())
    .then(result =>{
      console.log(result,"Succesfully added");
      let jsonRes = JSON.parse(result);
      addSongsToUI(jsonRes);
    });
}

//ADD Button Listener
function addAuthButtonListener(){
  document.getElementById("authSpotify").addEventListener('click',function(){
    chrome.identity.launchWebAuthFlow(
      {'url': auth_url, 'interactive': true},
      function(redirect_url) {
          let code = redirect_url.split('code=')[1].split('&')[0]
          console.log(code);
          getAuthCode(code);
          document.getElementById("authorizationBlock").style.visibility = "hidden";
          document.getElementById("searchSongs").style.visibility = "visible";
        })
  });
}

//ADD Button Listener
function addSubmitButtonListener(){
  document.getElementById('submitButton').addEventListener('click', function (evt) {
    var span_notFound = document.getElementById('not-found');
    span_notFound.innerHTML = "Loading Results...";
    setTimeout(() => {
      getSongs(id)
    }, 1000)
  });
}

//Add listener
window.addEventListener('load', () => {
  document.getElementById("searchSongs").style.visibility = "hidden";
  document.getElementById("songs").style.visibility = "hidden";
  addAuthButtonListener();
  addSubmitButtonListener()
});


function addSongsToUI(response){

  document.getElementById("songs").style.visibility = "visible";
  let nameArr = response.names;
  let artArr = response.artists;
  let imgArr = response.images;

  let songsTable = document.getElementById("tbody");

  for(let i=0;i<response.uri.length;i++){
    let row = songsTable.insertRow(-1);
    let nameCell = row.insertCell(0);
    let artistCell = row.insertCell(1);
    let urlCell = row.insertCell(2);

    nameCell.innerHTML = `<p>${nameArr[i]}</p>`;
    artistCell.innerHTML = `<p>${artArr[i]}</p>`;
    urlCell.innerHTML = `<a href=${imgArr[i]} target="_blank">Click Me</a>`;
  
  }
  


}
