$(function () {

    console.log("djf--------------------")

  // $(".js-upload-photos").click(function () {
  //   $("#fileupload").click();
  // });

   $("#fileupload").fileupload({


    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {

      if (data.result.is_valid) {

          // alert("upload successful")
        $("#gallery tbody").prepend(
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
        )
          location.reload();
      }
    },

         error: function (response) {
                    // alert the error if any error occured

                   alert(response["responseJSON"]["error"]);
                    location.reload();
                    $("#modal-progress").modal("hide");
                },

  });

});
