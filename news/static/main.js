
$(document).ready(function(){
	console.log("Hi there!")

	$(".button-collapse").sideNav();

	$(document).ready(function(){
    $('.parallax').parallax();
    });

///// Register /////
    $('#nav').on('click', ".register", function(event){
    	event.preventDefault();
        var template = $('#register-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#register_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "register",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

		if (data.success){
			////// if they registered then display the Login ////////
                var template = $('#login-template').html();
		        var renderM = Mustache.render(template);
		        $('#answer_div').html(renderM);
		        $('#answer_div').append("<br><br>");
		        $('#answer_div').append(data.Message);
            }
        });
    });


///// Login /////
    $('#nav').on('click', ".login", function(event){
    	event.preventDefault();
        var template = $('#login-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#login_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "login",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        $('#answer_div').html(data.Message);
        $('#answer_div').append("<br><br>");
        $('#nav').append(date.username);

        });
    });

///// Logout /////
    $('#nav').on('click', ".logout", function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "logout",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

    $('#answer_div').html(" <h2> Goodbye, See you soon!</h2>");
    $('#answer_div').append(data.Message);
	location.reload();

    });
});

///// Create Post /////
    $('#nav').on('click', ".create", function(event){
    	event.preventDefault();
        var template = $('#create-template').html();
        var renderM = Mustache.render(template);
        $('#answer_div').html(renderM);
    });

    $('#answer_div').on('submit', '#create_form',function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "create",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

    	$('#answer_div').append("<br><br>");
    	$('#answer_div').append(data.Message);

        // var template = $('#all-results').html();
        // var renderM = Mustache.render(template,data);
        // $('#answer_div').html(renderM);  
        });
    });


////// Get All Posts /////
    $('#nav').on('click', ".all", function(event){
    event.preventDefault();

    var query_string = $(this).serialize() // returns all the data in your form

    $.ajax({
        method: "POST",
        url: "all",
        data: query_string,
    }).done(function(data, status){
            console.log(data);//for testing 

        var template = $('#all-results').html();
        var renderM = Mustache.render(template,data);
        $('#answer_div').html(renderM);  
        });
    });


///// Vote Up/////
    $('#answer_div').on('click', '#up_button',function(event){
    event.preventDefault();

    if(confirm("Are you sure you would like vote this up?")){
        var query_string = $(this).serialize() // returns all the data in your form

        $.ajax({
            method: "POST",
            url: $(this).attr("href"),
            data: query_string,
        }).done(function(data, status){
                console.log(data);//for testing 
                alert("Voted Up!")

            var template = $('#all-results').html();
            var renderM = Mustache.render(template,data);
            $('#answer_div').html(renderM);  
        });
    };
});


///// Vote Down/////
    $('#answer_div').on('click', '#down_button',function(event){
    event.preventDefault();

    if(confirm("Are you sure you would like vote this down?")){
        var query_string = $(this).serialize() // returns all the data in your form

        $.ajax({
            method: "POST",
            url: $(this).attr("href"),
            data: query_string,
        }).done(function(data, status){
                console.log(data);//for testing 
                alert("Voted down!")

            var template = $('#all-results').html();
            var renderM = Mustache.render(template,data);
            $('#answer_div').html(renderM);  
        });
    };
});




});