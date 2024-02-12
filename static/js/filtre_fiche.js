function filtrer_fiches(element){

    let blocks = document.getElementsByClassName("block-fiche");

    // for of loop
    for (let block of blocks) {
        if (element.value === "0"){
            block.setAttribute('style', 'display:block');
        } else if (block.getAttribute("data-cour") === element.value){
            block.setAttribute('style', 'display:block');
        } else {
            block.setAttribute('style', 'display:none !important');
        }

    }
}