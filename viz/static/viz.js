
/** global vars */
window.GDATA = {};
window.TOKEN = null;
window.RTYPE = null;


function toColor(v) { 
  // v is -1 to 1 initially
  var h;

  if(v > 0) {
    h = 200;   // blue
    v = 1 - v; // invert so v = 0 is highest lightness (white)
  } else {
    h = 0;     // red
    v = 1 + v; // invert too
  }
  var l = (Math.floor(v * 40) + 60) + '%'; // 

  return sprintf('hsl(%d,%s,%s)', h, '60%', l);
}


function render(div, data) {
  div.html(''); // flush

  for(var i=0 ;i<data.text.length; i++) {

    var letter = data.text[i];
    var e = data.scores[i];
    e = Math.tanh(e * 2); // squash into (-1, 1) before scaling (avoid too much white)
    var col = toColor(e);
    var css = 'background-color:' + col;
    css += ';width:' + (letter.length + 'ch');

    if(letter == ' ') {
      letter = '_'; // ha, ha Justin trick
      css += ';color:' + col;
    }
    if(letter == '\n') {
      css += ';display:block;';
    }

    div.append('div').attr('class', 'd').attr('style', css).html(letter);
    if (data.word) {
      div.append('div').attr('class', 'd').attr('style', 'width:1ch').html('&nbsp;');
    }
  }
}


function resetPointer(pointer) {
  $('#pointer').text(sprintf("Showing %d cell score", pointer));
  $('#pointer-inp').val(pointer);
}


function redrawButtons() {
  $("#buttons").empty();
  if (window.RTYPE == 'mult') {
    var btnPrev = $("<button>Prev</button>");
    btnPrev.addClass("button");
    btnPrev.click(function() {route('prev', window.TOKEN);});
    btnPrev.appendTo("#buttons");
    var btnNext = $("<button>Next</button>");
    btnNext.addClass("button");
    btnNext.click(function() {route('next', window.TOKEN);});
    btnNext.appendTo("#buttons");
    var btnRandom = $("<button>Random</button>");
    btnRandom.addClass("button");
    btnRandom.click(function() {route('random', window.TOKEN);});
    btnRandom.appendTo("#buttons");
    var pointerInp = $("<input id='pointer-inp' type='number' min='0'>");
    pointerInp.addClass("button");
    pointerInp.on('keypress', function(e){
      if(e.which === 13) {
	var value = $('#pointer-inp').val();
	if (value != "") {
	  getCellActivation(window.TOKEN, value);
	}
      }
    });
    pointerInp.appendTo("#buttons");
  }
}


function onData(response) {
  if (response.status) {
    // remove message if still there
    $('#message').empty();
    // update globals
    window.GDATA.text = response.text;
    window.GDATA.scores = response.scores;
    window.GDATA.word = response.word;
    window.RTYPE = response.rtype;
    window.TOKEN = response.token;
    // redraw
    if (response.rtype == 'mult') {
      redrawButtons();
      resetPointer(response.pointer);
    }
    render(d3.select("#viz"), GDATA);
  }
}


function route(target, token) {
  var url = sprintf("http://localhost:%d/%s/", PORT, target);
  $.ajax({
    url: url,
    type: 'GET',
    success: onData,
    data: {'token': token},
    dataType: 'json'
  });
};


function getCellActivation(token, pointer) {
  $.ajax({
    url: sprintf("http://localhost:%d/getcell/", PORT),
    type: 'GET',
    success: onData,
    data: {'token': token, 'pointer': pointer},
    dataType: 'json'
  });
};


function poll(token) {
  var url = sprintf("http://localhost:%d/poll/", PORT);
  $.ajax({
    url: url,
    type: 'GET',
    success: onData,
    data: {'token': token},
    dataType: 'json'
  });
};


$(document).ready(function() {
  window.setInterval(function() {poll(window.TOKEN);}, 2000);
});
