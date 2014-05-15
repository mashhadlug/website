$(document).ready(function(){
  /* navbar affix */
  /*
  $('.navbar').affix({
    offset: {
      top: function(){
        return (this.top = $('.navbar').position().top);
      }
    }
  });
  * */
  
  /* Ajax Pagination*/
  $(document).on('click', '.view_more', function(){
    var parent = $(this).parent()
    var next_page = $(this).attr('data-next_page')
    if(next_page){
      $(this).button('loading')
      $.get("/reports/"+next_page+".html", function(data){
        $(parent).replaceWith(data)
      })
    }
  })
})
