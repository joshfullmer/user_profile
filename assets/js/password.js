
$(window).load(function(){

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
    
    $(document).ready(function() {
        $("#id_new_password").on("keypress keyup keydown", function() {
            var pass = $(this).val();
            $("#password_strength").text(checkPassStrength(pass));
            $("#password_score").text(scorePassword(pass));
        });
    });
});
