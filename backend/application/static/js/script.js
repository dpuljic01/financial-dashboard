$(function() {
    var showPass = 0;
    $(".btn-show-pass").on("click", function(){
        if(showPass == 0) {
            $(this).next("input").attr("type", "text");
            $(this).find("i").text("visibility_off");
            showPass = 1;
        }
        else {
            $(this).next("input").attr("type", "password");
            $(this).find("i").text("visibility");
            showPass = 0;
        }
    });
    $('.modal').modal();

    // little hack for submitting two forms on the same site ;)
    $("#register-form").submit(function(event) {
        var csrf = $("#csrf_token").val();
        $("#register-form").prepend("<input type='hidden' name='csrf-token' value=" + csrf + ">");
    });

//    $(".dropdown-trigger").dropdown({
//        inDuration: 300,
//        outDuration: 225,
//        constrainWidth: false,
//        belowOrigin: true, // Displays dropdown below the button
//    })

//    $('input.autocomplete').autocomplete({
//      data: {
//        "Apple": null,
//        "Microsoft": null,
//        "Google": 'https://placehold.it/250x250'
//      },
//    });
console.log("BLA")
    br = 0;
    $( "input.autocomplete" ).keyup(function() {
        if(br < 2) {
            br += 1
            return
        }
        var complete = $('#autocomplete-input').val()

        $.getJSON("/tickers/autocomplete",{
            q: complete, // in flask, "q" will be the argument to look for using request.args
        }, function(data) {
            $('input.autocomplete').autocomplete({
                minLength: 2,
                data: data
            }); // matching_results from jsonify
        });
    })

//    $('#autocomplete').autocomplete({
//        source: function(request, response) {
//            $.getJSON("{{url_for('autocomplete')}}",{
//                q: $('#autocomplete').val(), // in flask, "q" will be the argument to look for using request.args
//            }, function(data) {
//                response(data); // matching_results from jsonify
//            });
//        },
//        minLength: 2,
//        select: function(event, ui) {
//            console.log(ui.item.value); // might help later
//        }
//    });

    $('.collapsible').collapsible();
 });
