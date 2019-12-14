function add_user(){
    let form = document.getElementById("form-subscribe");
    if ($(form)[0].checkValidity()) {
        $.ajax({
            data : $(form).serialize(),
            type : 'post',
            url : '/inscription',
            success : function(html) {
                if(html=="0"){
                    $('.invalid-password').css("display", "block");
                }else if(html == "1"){
                    window.location = "/successInscription";
                }
            }
        });
    }
}

function add_offer(){
    let form = document.getElementById("form-add-offer");
    if ($(form)[0].checkValidity()) {
        $.ajax({
            data : $(form).serialize(),
            type : 'post',
            url : '/add_offer',
            success : function(html) {
                if(html=="0"){
                    $('.invalid-password').css("display", "block");
                }else if(html == "1"){
                    window.location = "/offer_created";
                }
            }
        });
    }
}

function delete_annonce(id){
    $.ajax({
        data: id,
        type: 'post',
        url: '/delete_user_offer',
        success: function (html) {
            if (html == "1") {
                location.reload();
            }
        }
    });
}

function update_user_information(form){
    if ($(form)[0].checkValidity()) {
        $.ajax({
            data: $(form).serialize(),
            type: 'post',
            url: '/update_user_infos',
            success: function (html) {
                if (html == "1") {
                    location.reload();
                }else{
                    $('.s').html(html);
                }
            }
        });
    }
}

function connect(){
    let form = document.getElementById("log-form");
    if ($(form)[0].checkValidity()) {
        $.ajax({
            data : $(form).serialize(),
            type : 'post',
            url : '/login',
            success : function(html) {
                if(html=="0"){
                    $(".champ_log").css("display","block");
                }else if(html == "2"){
                    window.location = "/accueil";
                }else if(html == "1") {
                    window.location = "/admin";
                }else if(html == "4"){
                    $(".champ_inactive_user").css("display","block");
                }else{
                    $(".champ_log").css("display","block");
                }
            }
        });
    }
}

function search_value(form){
    if ($(form)[0].checkValidity()) {
        $.ajax({
            data: $(form).serialize(),
            type: 'post',
            url: '/update_user_infos',
            success: function (html) {
                if (html == "1") {
                    location.reload();
                }else{
                    $('.s').html(html);
                }
            }
        });
    }
}