
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>VIZ</title>
    <script type="text/javascript" src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.13.0/d3.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sprintf/1.1.1/sprintf.min.js"></script>
    <link href="http://fonts.googleapis.com/css?family=Cousine" rel="stylesheet" type="text/css">
    <link href="static/style.css" rel="stylesheet">
    <script type="text/javascript" src="static/viz.js"></script>
    <script>var PORT={{port}}</script>
  </head>
  <body>
    <div id="message" style="display:flex;justify-content:center; margin-top:100px">
      {{msg}}
    </div>
      <div id="buttons" style="display:inline-block"></div>
      <div id="pointer" style="display:inline-block"></div>
    <div id="wrap">
      <div id="viz"></div>
    </div>
  </body>
</html>
