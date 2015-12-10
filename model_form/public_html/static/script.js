/* script.js */

/* When the madlib form is submitted, run this function */
$("#madlibForm").submit(function() 
{
    
    $("#errorMessage").html("");
    $("#madlibStory").html("");

    var showMadlib = true;

    /* Our beginning madlib story (is empty) */
    var madlibStory = "Hi"

    /* Start Validations */
    var nameValue = $("#madlibForm input[name= 'name']").val();
    if (!nameValue) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please enter your name.</p></div>");
        showMadlib = false;
    }

    var isTitleChecked = $("#madlibForm input[name= 'title']").is(":checked");
    var titleValue = $("#madlibForm input[name= 'title']:checked").val();
    if (!isTitleChecked) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please select a title.</p></div>");
        showMadlib = false;
    }

    var placeValue = $("#madlibForm input[name= 'place']").val();
    if (!placeValue) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please enter a place.</p></div>");
        showMadlib = false;
    }

    var numberValue = $("#madlibForm input[name = 'number']").val();
    if(!numberValue)
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please enter a number.</p></div>"); 
        showMadlib = false;
    }
    else if(isNaN(numberValue)) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please enter only numeric values in the number field.</p></div>");  
        showMadlib = false;
    }

    var isRideChecked = $("#madlibForm input[name= 'ride']").is(":checked");
    var rideValue = $("#madlibForm input[name= 'ride']:checked").val();
    if (!isRideChecked) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please select your ride.</p></div>");
        showMadlib = false;
    }
    
    var weaponValue = $("#madlibForm select[name = 'weapon']").val();
    if (!weaponValue) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please select your weapon.</p></div>");
        showMadlib = false;
    }

    var monsterValue = $("#madlibForm input[name= 'monster']").val();
    if (!monsterValue) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please enter a monster name.</p></div>");
        showMadlib = false;
    }

    var islikes1Checked = $("#madlibForm input[name= 'likes1']").is(":checked");
    var likes1Value = $("#madlibForm input[name= 'likes1']").val();
    var islikes2Checked = $("#madlibForm input[name= 'likes2']").is(":checked");
    var likes2Value = $("#madlibForm input[name= 'likes2']").val();
    var islikes3Checked = $("#madlibForm input[name= 'likes3']").is(":checked");
    var likes3Value = $("#madlibForm input[name= 'likes3']").val();
    var islikes4Checked = $("#madlibForm input[name= 'likes4']").is(":checked");
    var likes4Value = $("#madlibForm input[name= 'likes4']").val();
    if (!islikes1Checked && !islikes2Checked && !islikes3Checked && !islikes4Checked) 
    {
        $("#errorMessage").append("<div class = \"div-error\"><p>Please select at least one thing that you like.</p></div>");
        showMadlib = false;
    }
    /* END VALIDATIONS */

    /* If all validations pass, add the story to the page */
    if (showMadlib) 
    {   
        madlibStory = "<p id=\"para-story\">"+titleValue + " " + nameValue + " rode into the kingdom of " + placeValue + " riding on his magnificent " + rideValue + ", with his glorious armies of "+numberValue+ " Sparkly Puffs. Suddenly out of the wild, a big " + monsterValue + " appeared and blocked their path. 'Raaaaaaawwwwwrrrrrr!!!! Who dares enter my kingdom of " + placeValue + "? Defeat me you must, if you wish to pass!', it said. 'I " + titleValue + " " + nameValue;
        if (islikes1Checked) 
        {
            madlibStory = madlibStory + ", the protector of " + likes1Value 
        }
        if (islikes2Checked) 
        {
            madlibStory = madlibStory + ", the champion of " + likes2Value 
        }
        if (islikes3Checked) 
        {
            madlibStory = madlibStory + ", the defender of " + likes3Value 
        }
        if (islikes4Checked) 
        {
            madlibStory = madlibStory + ", the liberator of " + likes4Value 
        }

        madlibStory = madlibStory + ", challenge you to a duel.', said " + titleValue + " " + nameValue + " pulling out his " + weaponValue + ". The " + monsterValue +" saw the glorious weapon of war and shiverred in fear. 'You may pass " + titleValue + " " + nameValue +"', it said.</p>"
        $("#madlibStory").html(madlibStory);

        /*Scroll To Bottom*/
        window.scrollTo(0,document.body.scrollHeight);
    }
    
    /* Don't load a new page after clicking submit */
    return false;
});

/* When the luhn form is submitted, run this function */
$("#luhnAlgorithmForm").submit(function()
{
    $("#errorMessage2").html("");
    var numberValue = $("#luhnAlgorithmForm input[name = 'number']").val();
    if(!numberValue)
    {
        $("#errorMessage2").append("<div class = \"div-error\"><p>Please enter a number.</p></div>"); 
    }
    else if(isNaN(numberValue)) 
    {
        $("#errorMessage2").append("<div class = \"div-error\"><p>Please enter only numeric values in the credit card number field.</p></div>");  
    }
    else if(numberValue.length != 16)
    {
        $("#errorMessage2").append("<div class = \"div-error\"><p>Please enter a 16 digit number.</p></div>");
    }
    else
    {
        var checksum = 0;
        var count = 0;
        while(numberValue > 1)
        {
            count += 1;
            var modulus = numberValue%10;
            if (count%2 == 0) 
            {
                modulus = modulus*2;
                if (modulus>9) 
                {
                    var innerModulus = modulus%10;
                    modulus = Math.floor(modulus/10);
                    modulus = modulus + innerModulus;
                };
            }
            checksum = checksum + modulus;
                
            numberValue = Math.floor(numberValue/10);
        }
        


        if (checksum%10 == 0) 
        {
            $("#errorMessage2").append("<div class = \"div-success div-error\"><p>The credit card number is valid.</p></div>");
        }
        else
        {
            $("#errorMessage2").append("<div class = \"div-error\"><p>The credit card number is not valid.</p></div>"); 
        }
    }

    /* Don't load a new page after clicking submit */
    return false;
}
);




