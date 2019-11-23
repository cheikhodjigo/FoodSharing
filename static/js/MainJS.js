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
        data : {id:id},
        type : 'post',
        url : '/delete_user_offer',
        success : function(html) {
            if(html == "1"){
                location.reload();
            }
        }
    });

}