
function copyRefCode() {
    const code = document.getElementById("refCode").innerText;
    navigator.clipboard.writeText(code).then(function() {
      document.getElementById("copiedMsg").style.display = "inline";
      setTimeout(() => {
        document.getElementById("copiedMsg").style.display = "none";
      }, 2000);
    });
  }

function Submit(){
  const b = document.getElementsByTagName('form')[0]
  b.submit()
}
function togglePassword(id) {
  const input = document.getElementById(id);
  input.type = input.type === "password" ? "text" : "password";
}