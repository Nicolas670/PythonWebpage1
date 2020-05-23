$(document).ready(function() {

        // JQuery code to be added in here.

    $(".toggle_container").hide();

        $("p.trigger").click(function(){
            $(this).toggleClass("active").next().Toggle("normal");

        });

    $(function(){
        setTimeout(function(){
            $('.fly-in-text').removeClass('hidden');
            }, 500);
            });

    $(function(){
        setTimeout(function(){
            $('.fly-in-text-td').removeClass('hidden');
            }, 500);
            });


        /*$('#post-wordcloud-text').submit(function() { // catch the form's submit event
            $.ajax({ // create an AJAX call...
                data: {'data':$(this).serialize(),'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()}, // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(json) { // on success..
                    $('#wordcloud-output').html(json.text); // update the DIV
                }
            });
            return false;
        });

        $(document).on('submit', '#wordcloud-form', function(e){
            e.preventDefault();

            $.ajax({
                data:$(this).serialize(),
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                success: function(){
                    alert("Created new User!");
                    }
            });
        });*/
})
