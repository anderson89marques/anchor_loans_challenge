$(document).ready(function() {
    $('#exampleModalCenter').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget) // Button that triggered the modal
        var recipient = button.data('whatever') // Extract info from data-* attributes
        var modal = $(this)
        console.log(recipient);
        modal.find('.modal-body img').attr('src', recipient)
      });
      
      $('.like').click(function (event) {
            var i = $(this).find('i');
            var class_ = i.attr('class');
            var _id =  $( this ).attr('id');
            var t_obj = {like: false, _id: _id}
            if (class_ == "far fa-heart") {
                i.attr('class', "fas fa-heart");
                t_obj.like = 1
            } else {
                i.attr('class', "far fa-heart");
                t_obj.like = 0
            }
            var strong = $("#like" + _id);
            console.log(strong);
            var url = "/likes"
            var posting = $.post( url, t_obj, 'json');
            posting.done(function( data ) {
                strong.text(data.total_likes + " like(s)");   
            });
      });
});