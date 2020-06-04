'use strict';
var count_row = 0;
var id;
var url;
var refresh_token;
var spotify_access_token;
var redirect_uri = "https://aoighdinhjbeihojpleaohghnfecjjmo.chromiumapp.org/provider_sp";
var auth_url = "https://accounts.spotify.com/authorize?client_id=6b7918c1951a48f89dd7d360a17b4eac&response_type=code&redirect_uri="+redirect_uri+"&scope=playlist-modify-public playlist-modify-private user-read-private user-read-email";
var is_spotify_auth = false;

chrome.tabs.query({ 'active': true, 'currentWindow': true }, function (tabs) {
  url = tabs[0].url;
  let extra = url.split('v=')[1]
  id = extra.split('&')[0]
});

function setRefTokenFromStorage(value){
  chrome.storage.sync.set({"refresh_token": value}, function() {
    console.log('Refresh_Token is set to ' + value);
  });
}

function setauthTokenFromStorage(value){
  let d = (new Date()).toString()
  chrome.storage.sync.set({"auth_token": value,
                           "created_time" : d,
                        }, function() {
    console.log('Refresh_Token is set to ' + value);
  });   
}


//get OAuthCode
function getAuthCode(code,isRefreshToken){

  fetch(`http://127.0.0.1:5000/oauth?code=${code}&ru=${redirect_uri}&rf=${isRefreshToken}`)
    .then(r => r.text())
    .then(result =>{
      let jsonRes = JSON.parse(result);
      spotify_access_token = jsonRes["oauth"];
      setauthTokenFromStorage(spotify_access_token);
      refresh_token = jsonRes["refresh_token"];
      if(refresh_token != "not_defined"){
        setRefTokenFromStorage(refresh_token);
      }
      console.log(spotify_access_token,"OAUTH Token");
    })
    .catch(err => console.log(err));
}


//API CALL
function getSongs(id){
  document.getElementById("searchSongs").remove();
  document.getElementById("songs").style.visibility = "visible";
  fetch('http://127.0.0.1:5000/'+id+'?code='+spotify_access_token)
    .then(r => r.text())
    .then(result =>{
      console.log(result,"Succesfully added");
      let jsonRes = JSON.parse(result);
      if(jsonRes.response_code === 'not_music'){
        showNotAMusicVideo();
      }
      else{
        addSongsToUI(jsonRes);
      }
      
    });
}

//API Add Song Call
function addSongToPlaylist(songUri){
  fetch(`http://127.0.0.1:5000/addSong?songUri=${songUri}&code=${spotify_access_token}`)
    .then(r=>r.text())
    .then(result =>{
      console.log(result,"Song added Succesfully added or not");
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
            getAuthCode(code, "0");
            document.getElementById("authorizationBlock").remove();
            document.getElementById("searchSongs").style.visibility = "visible";
          });
    });
}

//ADD Button Listener
function addSubmitButtonListener(){
  document.getElementById('submitButton').addEventListener('click', function (evt) {
    setTimeout(() => {
      getSongs(id)
    }, 1000);
  });
}

// Add Song Button
function addSongButtonListener(){

  document.querySelectorAll('.addSongs').forEach(element => {
      element.addEventListener('click',event =>{
      let songLink = element.getAttribute("href");
      setTimeout(()=>{
        addSongToPlaylist(songLink);
      },1000);
      });
  });
}



//Add listener
window.addEventListener('load', () => {
  // refresh_token = getRefTokenFromStorage();
  addAuthButtonListener();
  chrome.storage.sync.get(["auth_token","created_time","refresh_token"],function(result){
    console.log('Auth_Token currently is ' + result.auth_token);
    console.log('Created_Time currently is ' + result.created_time);
    console.log('Refresh_Token currently is ' + result.refresh_token);
    let currentTime = new Date()
    let createdDate = new Date(result.created_time)
    let diffMins = (currentTime.getTime() - createdDate.getTime())/1000 
    console.log(diffMins,"Difference in minutes")
    if(result.auth_token != undefined && diffMins<3600){
      spotify_access_token = result.auth_token
      document.getElementById("authorizationBlock").remove();
      document.getElementById("searchSongs").style.visibility = "visible";  
    }
    else if(result.refresh_token != undefined){
      console.log("Refresh_Tag is defined")
      document.getElementById("authorizationBlock").remove();
      document.getElementById("searchSongs").style.visibility = "visible";
      getAuthCode(result.refresh_token, "1");
    }
    else{
      
      document.getElementById("searchSongs").style.visibility = "hidden";
    }
    document.getElementById("songs").style.visibility = "hidden";
    document.getElementById("notMusic").style.visibility = "hidden"
  });
  
  addSubmitButtonListener();
});

function showNotAMusicVideo(){
  document.getElementById("searchSongs").style.visibility = "hidden"
  document.getElementById("notMusic").style.visibility = "visible";
}


function addSongsToUI(response){
  let nameArr = response.names;
  let artArr = response.artists;
  let imgArr = response.images;
  let uriArr = response.uri;
  document.getElementById("loaderDiv").remove();

  let songsTable = document.getElementById("tbody");

  for(let i=0;i<response.uri.length;i++){
    let row = songsTable.insertRow(-1);
    let nameCell = row.insertCell(0);
    let artistCell = row.insertCell(1);
    let uriCell = row.insertCell(2);

    nameCell.innerHTML = `<span style="padding-right:3px; padding-top: 3px; display:inline-block;"> 
                            <img class="iconImg" src="${imgArr[i]}" width="40px"></img>
                            <p>${nameArr[i]}</p>
                          </span>`;
    artistCell.innerHTML = `<p>${artArr[i]}</p>`;
    uriCell.innerHTML = `<button class="btn addSongs" id="addSong${i}" href="${uriArr[i]}" style="background-color : transparent"><i class="fa fa-plus" style="color:white;w"></i></button>`;
  }
  addSongButtonListener();

}
