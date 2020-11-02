$("form[name=login_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var $success = $form.find(".success");

    var student_id = $("#student_id").val().trim();
    var password = $("#password").val().trim();

    toastr.options.progressBar = true;
    toastr.options.closeButton = true;
    toastr.options.debug = false;
    toastr.options.newestOnTop = false;
    toastr.options.progressBar = true;
    toastr.options.onclick = null;
    toastr.options.positionClass = "toast-top-full-width";
    toastr.options.preventDuplicates = true;
    toastr.options.showDuration = "100";
    toastr.options.extendedTimeout = "0";
    toastr.options.fadeIn = "100";
    toastr.options.fadeOUt = "50";

    var data = {"student_id": student_id, "password": password};

    if (student_id === "" || password === "") {
        toastr.error("Missing One or More Parameters. Inputs can not be empty");
    } else {
        $.ajax({
            url: "/",
            type: "POST",
            dataType: "json",
            contentType:'application/json',
            data: JSON.stringify(data),
            success: function (resp) {
                toastr.success(resp.data);
                setTimeout(() => { document.location.href="/profile"; }, 3000);
            },
            error: function(resp) {
                console.log(resp);
                if (resp.status === 400) {
                    toastr.error(resp.responseJSON.error);
                    setTimeout(() => { document.location.href="/register"; }, 3000);
                } else {
                    toastr.error(resp.responseJSON.error);
                }
            }
        });
    }

    e.preventDefault();
})

$("form[name=registration_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var $success = $form.find(".success");

    var student_id = $("#student_id").val().trim();
    var password = $("#password").val().trim();
    var confirm_password = $("#confirm_password").val().trim();

    toastr.options.progressBar = true;
    toastr.options.closeButton = true;
    toastr.options.debug = false;
    toastr.options.newestOnTop = false;
    toastr.options.progressBar = true;
    toastr.options.onclick = null;
    toastr.options.positionClass = "toast-top-full-width";
    toastr.options.preventDuplicates = true;
    toastr.options.showDuration = "100";
    toastr.options.extendedTimeout = "0";
    toastr.options.fadeIn = "100";
    toastr.options.fadeOUt = "50";

    if (student_id === "" || password === "" || confirm_password === "") {
        toastr.error("One of the parameters can not be empty.");
    } else {
        if (password !== confirm_password || confirm_password !== password){
            toastr.error("Passwords do not match.");
        } else {
            let data = {"student_id": student_id, "password": password};

            $.ajax({
                url: "/register",
                type: "POST",
                dataType: "json",
                contentType:'application/json',
                data: JSON.stringify(data),
                success: function (resp) {
                    toastr.success(resp.data);
                    setTimeout(() => { document.location.href="/"; }, 3000);
                },
                error: function(resp) {
                    console.log(resp);
                    if (resp.status === 406) {
                        toastr.error(resp.responseJSON.error);
                        setTimeout(() => { document.location.href="/"; }, 3000);
                    } else {
                        toastr.error(resp.responseJSON.error);
                    }
                }
            });
        }
    }

    e.preventDefault();
})

$("form[name=password_reset_form").submit(function(e) {
    var $form = $(this);
    var data = $form.serialize();
    var email = $("#email").val().trim();

    toastr.options.progressBar = true;
    toastr.options.closeButton = true;
    toastr.options.debug = false;
    toastr.options.newestOnTop = false;
    toastr.options.progressBar = true;
    toastr.options.onclick = null;
    toastr.options.positionClass = "toast-top-full-width";
    toastr.options.preventDuplicates = true;
    toastr.options.showDuration = "100";
    toastr.options.extendedTimeout = "0";
    toastr.options.fadeIn = "100";
    toastr.options.fadeOUt = "50";

    function validateEmail(email_address) {
        let emailCheck =/^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/i;
        return emailCheck.test(String(email).toLowerCase());
    }

    if (email === "") {
        toastr.error("Email is Required.");
    } else {
        if (!validateEmail(email)){
            toastr.error("Email is invalid");
        } else {
            $.ajax({
                url: "/reset_password",
                type: "POST",
                data: data,
                dataType: "json",
                success: function (resp) {
                    toastr.success(resp.data);
                    setTimeout(() => { document.location.href="/"; }, 3000);
                },
                error: function(resp) {
                    toastr.error(resp.responseJSON.error);
                }
            });
        }
    }

    e.preventDefault();
})

$("form[name=reset_with_token_form").submit(function(e) {
    console.log("asdf");
    var $form = $(this);
    var data = $form.serialize();
    var password = $("#password").val().trim();
    var confirm_password = $("#confirm_password").val().trim();
    var token = url.lastIndexOf('/') + 1;
    console.log(token);

    toastr.options.progressBar = true;
    toastr.options.closeButton = true;
    toastr.options.debug = false;
    toastr.options.newestOnTop = false;
    toastr.options.progressBar = true;
    toastr.options.onclick = null;
    toastr.options.positionClass = "toast-top-full-width";
    toastr.options.preventDuplicates = true;
    toastr.options.showDuration = "100";
    toastr.options.extendedTimeout = "0";
    toastr.options.fadeIn = "100";
    toastr.options.fadeOUt = "50";

    if (password === "" || confirm_password === "") {
        toastr.error("Missing one or more parameters");
    } else {
        $.ajax({
            url: "/reset_with_token/" + token,
            type: "POST",
            data: data,
            dataType: "json",
            success: function (resp) {
                console.log(resp);
//                console.log(resp.data);
                toastr.success(resp.data);
                setTimeout(() => { document.location.href="/"; }, 3000);
            },
            error: function(resp) {
                console.log(resp);
                if (resp.status === 400) {
                    toastr.error(resp.responseJSON.error);
                    setTimeout(() => { document.location.href="/reset"; }, 3000);
                } else {
                    toastr.error(resp.responseJSON.error);
                }
            }
        });
    }

    e.preventDefault();
})