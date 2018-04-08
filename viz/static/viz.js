
/** global vars */
window.GDATA = {};
window.TOKEN = null;
window.RTYPE = null;


function toColor(v) { 
  // v is -1 to 1 initially
  var h;
  var l = (Math.floor(v * 40) + 60) + '%';

  if(v > 0) {
    h = 200;
    v = 1 - v; // invert so v = 0 is highest lightness (white)
  } else {
    h = 0;
    v = 1 + v; // invert too
  }

  return sprintf('hsl(%d,%s,%s)', h, '60%', l);
}


function render(div, data) {
  div.html(''); // flush

  for(var i=0 ;i<data.text.length; i++) {

    var letter = data.text[i];
    var e = data.scores[i];
    e = Math.tanh(e); // squash into (-1, 1)
    var col = toColor(e);
    var css = 'background-color:' + col;

    if(letter == ' ') {
      letter = '_'; // ha, ha Justin trick
      css += ';color:' + col;
    }
    if(letter == '\n') {
      css += ';display:block;';
    }

    div.append('div').attr('class', 'd').attr('style', css).html(letter);
  }
}


function onData(response) {
  console.log(response);
  
  if (response.status) {
    // remove message if still there
    $('#message').empty();
    // update globals
    window.GDATA.text = response.text;
    window.GDATA.scores = response.scores;
    window.RTYPE = response.rtype;
    window.TOKEN = response.token;
    // redraw
    redrawButtons();
    render(d3.select("#viz"), GDATA);
  }
}


function next(response) {
}

function prev(response) {
}


function redrawButtons() {
  $("#buttons").empty();
  if (window.RTYPE == 'mult') {
    var btn1 = $("<button>Next</button>");
    btn1.addClass("button");
    btn1.click(function() {next();});
    btn1.appendTo("#buttons");
    var btn2 = $("<button>Prev</button>");
    btn2.addClass("button");
    btn2.click(function() {prev();});
    btn2.appendTo("#buttons");
  }
}


function poll(token, port) {
  var url = sprintf("http://localhost:%d/poll/", port);
  $.ajax({
    url: url, type: 'GET', success: onData, data: {'token': token}, dataType: 'json'
  });
};


$(document).ready(function() {
  window.setInterval(function() {poll(window.TOKEN, PORT);}, 2000);
});
