function searchTable(tabname, searchPersonnel)
{
    var noresultname = tabname + 'Res';
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById(searchPersonnel);
    filter = input.value.toUpperCase();
    table = document.getElementById(tabname);
    tr = table.getElementsByClassName("row-to-search");
    var nbr = 0;
    for (i = 0; i < tr.length; i++) {
        var display = "none";
        for (var j = 0; j < tr[i].getElementsByTagName("td").length; j++) {
            td = tr[i].getElementsByTagName("td")[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    display = "";
                    nbr++;
                } 
            }
        }
        tr[i].style.display = display;
    }

    if (nbr == 0) {
        document.getElementById(noresultname).style.display = "";
        table.style.display = "none";
    } else {
        document.getElementById(noresultname).style.display = "none";
        table.style.display = "";
    }
}