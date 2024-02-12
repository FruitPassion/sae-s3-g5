function validateForm()
{
  let fields = ["nominput", "dateinput", "lieuinput", "decriptioninput"]

  let i, l = fields.length;
  let fieldname;
  let input = document.getElementById('submit')
  for (i = 0; i < l; i++) {
    fieldname = fields[i];
    if (document.forms["ajouter"][fieldname].value === "") {
      input.disabled = true;
      break;
    } else {
      input.disabled = false;
    }
  }
}
