$(document).ready(function() {
        $('#post-wordcloud-text').submit(function() { // catch the form's submit event
            $.ajax({ // create an AJAX call...
                data: {'data':$(this).serialize(),'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()}, // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(json) { // on success..
                    $('#wordcloud-output').html(response); // update the DIV
                }
            });
            return false;
        });
})