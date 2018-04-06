


  function scorePassword(pass) {
      var score = 0;
      if (!pass)
          return score;
  
      // award every unique letter until 5 repetitions
      var letters = new Object();
      for (var i=0; i<pass.length; i++) {
          letters[pass[i]] = (letters[pass[i]] || 0) + 1;
          score += 5.0 / letters[pass[i]];
      }
  
      // bonus points for mixing it up
      var variations = {
          digits: /\d/.test(pass),
          lower: /[a-z]/.test(pass),
          upper: /[A-Z]/.test(pass),
          nonWords: /\W/.test(pass),
      }
  
      variationCount = 0;
      for (var check in variations) {
          variationCount += (variations[check] == true) ? 1 : 0;
      }
      score += (variationCount - 1) * 10;
  
      return parseInt(score);
  }
  
  function checkPassStrength(pass) {
      var score = scorePassword(pass);
      if (score > 80)
          return "strong";
      if (score > 60)
          return "good";
      if (score >= 30)
          return "weak";
  
      return "";
  }


$( document ).ready(function() {
  
  $('textarea').autogrow({onInitialize: true});


  //Cloner for infinite input lists
  $(".circle--clone--list").on("click", ".circle--clone--add", function(){
    var parent = $(this).parent("li");
    var copy = parent.clone();
    parent.after(copy);
    copy.find("input, textarea, select").val("");
    copy.find("*:first-child").focus();
  });

  $(".circle--clone--list").on("click", "li:not(:only-child) .circle--clone--remove", function(){
    var parent = $(this).parent("li");
    parent.remove();
  });

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });

  // jQuery datepicker
  $( "#id_date_of_birth" ).datepicker();


  // Password strength meter
  $("#id_new_password").on("keypress keyup keydown", function() {
    var pass = $(this).val();
    $("#password_strength").text(checkPassStrength(pass));
    $("#password_score").text(scorePassword(pass));
    $("#password_strength").text("hello")
  });

});