$(function () {
    $(".js-create-store").click(function () {
      $.ajax({
        url: '/survey/store/create',
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#addStoreModal").modal("show");
        },
        success: function (data) {
          $("#addStoreModal .modal-content").html(data.html_form);
        }
      });
    });
  
  });