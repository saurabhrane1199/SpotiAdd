//contentScript.js
var s = document.getElementById('stylehidecontrols');
if (s) {
s.remove();
}
else {
s = document.createElement('style');
s.id = 'stylehidecontrols';
var r = '#movie_player .ytp-gradient-top, #movie_player .ytp-gradient-bottom, #movie_player .ytp-chrome-top, #movie_player .ytp-progress-bar-container, #movie_player .ytp-chrome-controls{opacity: 0.2 !important;}';
s.appendChild(document.createTextNode(r));
document.body.appendChild(s);
}