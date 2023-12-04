/*
*
* Nom du pluging : cryxpad
* Auteur: Atsé Y. ange michael
* Version 1.0
* Requirement : jQuery v1.11.3,Bootstrap v4 (http://getbootstrap.com)
*/

(function($)
{
	$.fn.cryxpad=function(options)
	{
    	//On définit nos paramètres par défaut
    	var defauts =
        {
            'parentId':'cryxpad-clavier',
            'containerClass':'cryxpad-container',
            'inputFormId':'cryxpad-input-field',
            'removeButtonId':'cryxpad-remove-btn',
            'validateButtonId':'cryxpad-validate-btn',
            'containerpadding':10,
            'carreaux':10,
    		'width': 50,		//Largeur de la galerie
    		'height': 50,		//Hauteur de la galerie
            'button':{
                'class':"btn btn-primary",
                'marginLeft':3,
                'marginTop':3,
                'marginBottom':3,
            },
            'callback': null
		      //Fonction appelée à chaque nouvelle image
        };
        //var positionGenerees =[];

        //On fusionne nos deux objets ! =D
        var parametres=$.extend(defauts, options);
        var $inputcodeElement = $('input#'+parametres.inputFormId+'');

        var $removeBtnElement = $('input#'+parametres.removeButtonId+'');


        var selectednumber=null;

        var fieldArray = [];
        return this.each(function(){

           var element=$(this);
           var container = $('.'+parametres.containerClass+'');
    	
        
            element.css(
            {
                'position': 'relative',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'width': (parametres.width *parametres.carreaux)+(parametres.carreaux *parametres.button.marginLeft)+3,
                'height': (parametres.width *parametres.carreaux)+(parametres.carreaux *parametres.button.marginLeft)+3,
                'background-color': 'rgb(241, 241, 241)',
                'left': '-50%'
            });

            var numberarray=[0,1,2,3,4,5,6,7,8,9];
            for (i = 0; i < parametres.carreaux; i++) {
                var a = new Array(parametres.carreaux);
                a[i] = new Array(parametres.carreaux);
                for (j = 0; j < parametres.carreaux; j++) {
                    a[i][j] = "[" + i + "," + j + "]";
                    var tt = $("<button type='button' class='code-btn'></button>").css({
                        'position': 'absolute',
                        'width': parametres.width,
                        'height': parametres.height,
                        'text-align': "center",
                        'top': (j*parametres.height),
                        'left': i*parametres.width,
                        'margin-left':(i*parametres.button.marginLeft)+3,
                        'margin-top':(j*parametres.button.marginTop)+3
                    }).addClass(''+parametres.button.class+'');
                    tt.attr({
                        'id':j+"_"+i+"_div"
                    });
                    tt.appendTo(element);
                }
            }

            for (var i=0; i<10; i++) { 
                var rep =false
                var tt = fieldArray.length;
                if(tt ==0){
                    var x = getRandomInt(0,parametres.carreaux-1);
                    var y = getRandomInt(0,parametres.carreaux-1);
                    var data={
                       x : x,
                       y: y
                   }
                   fieldArray[i]=data;
               }
               else if(fieldArray.length>0){
                    var data={};
                    data.x = getRandomInt(0,parametres.carreaux-1);
                    data.y = getRandomInt(0,parametres.carreaux-1);

                    rep = ifExist(fieldArray,data);
                    while(!rep){
                        data.x = getRandomInt(0,parametres.carreaux-1);
                        data.y = getRandomInt(0,parametres.carreaux-1);
                        rep = ifExist(fieldArray,data);
                    }
                    fieldArray[i]=data;
                }
            }
            var i=0;
            fieldArray.forEach(function(p){
                var elId = p.y+"_"+p.x+"_div";
                var el = $('button[id="'+elId+'"]');
                el.attr("data-number",i);
                //el.html('<span style="color:with;">'+i+'</span>');
                el.html(i);
                i++;
            });

            $(document).on("click",'.'+parametres.containerClass+' .code-btn',function(e) {
                e.preventDefault();
                e.stopPropagation();
                buttonClik($(this));
            });
            /*
            * remove bnt click
            */
            $(document).on("click",'#'+parametres.removeButtonId+'',function(e) {
                e.preventDefault();
                e.stopPropagation();
                removeButtonClick($(this))
            });

            $(document).on("click",'#'+parametres.validateButtonId+'',function(e) {
                e.preventDefault();
                e.stopPropagation();
                validaterButtonClick($(this))
            });  
        });

        function buttonClik($el){
            if($el.data("number") !== undefined && $inputcodeElement.val().toString().length < 6){
                let data = $el.data("number");
                selectednumber = $inputcodeElement.val().toString()+data.toString();
                $inputcodeElement.val(selectednumber);
            }
        }

        function removeButtonClick($el){
            let inputCode = $inputcodeElement.val("");
        }

        function validaterButtonClick($el){
            alert($inputcodeElement.val());
        }

    };
    /*
    * usefull functions
    **
    */
    function getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function ifExist(dd,data){

    	for (var i = 0; i < dd.length; i++)
        {
            if(dd[i].x === data.x && dd[i].y ===data.y){
                return false;
            }
        }
        return true;
    }

})(jQuery);

