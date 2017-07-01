/**
 * Created by nir on 15/12/24.
 */
$(document).ready(function(){
   /* $("#loading").hide();*/
    $("#saving").hide();
    $("#alert").hide();

    /*setTimeout(function(){
        $("#loading").fadeOut();
    },1000);*/
    $("#loading").fadeOut(3000);

    $("#content").change(function(){
        $("#saving").show();
    })
});
