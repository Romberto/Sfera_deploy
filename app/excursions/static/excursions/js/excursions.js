window.addEventListener('load', function(){

    $('.block__btn').click(function(e){
        e.preventDefault()
        var name = $(this).attr('data-value') // название экскурсии
        $('.hidden').html('<input class="hidden__input" type="hidden" data-value="'+name+'">')
        $('.excursion__list, .excursion__title').fadeOut(500)
        $('.phone').fadeIn(900)
    });

    $('.limitInput').keyup(function(){
        var count = $(this).val().length
        console.log(count)
        if(count === 4){
            $(this).fadeOut()
            $.ajax({

            })
        }
    });

    /* валидция поля ввода суммы на кастомномном жетоне */

    $('.js_custom_input').keyup(function(){
        var data = $(this).val()
        if($.isNumeric(data) && parseInt(data) >= 3000){
            $('.query__excursion_link span').css('height', '0px')
        }else{
            $('.query__excursion_link span').css('height', '50px')
        }

    })



});