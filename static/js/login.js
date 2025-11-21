
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const loginTab = document.getElementById("loginTab");
const signupTab = document.getElementById("signupTab");

function showLogin() {
  loginForm.style.display = "block";
  signupForm.style.display = "none";
  loginTab.classList.add("active");
  signupTab.classList.remove("active");
}

function showSignup() {
  signupForm.style.display = "block";
  loginForm.style.display = "none";
  signupTab.classList.add("active");
  loginTab.classList.remove("active");
}

signupForm.addEventListener('submit', (e) => {
  e.preventDefault()

  const name = document.getElementById("name").value
  const email = document.getElementById("email").value
  const password = document.getElementById("password").value
  const phoneNumber = document.getElementById("phoneNumber").value

  const data = { "name": name, "email": email, "password": password, "phoneNumber": phoneNumber }

  fetch("/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.status == "success") {
        alert(data.message)
        signupForm.reset()
        location.href = '/index'
      } else {
        throw new Error(data.message);

      }
    })
    .catch(err => {
      alert(err)
    })

})

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  const data = { "email": email,  "password": password};

  fetch("/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      if (data.status == "success") {
        alert(data.message);
        loginForm.reset(); 
        location.href='/index'
      } else {
        throw new Error(data.message);
      }
    })
    .catch(err => {
      alert(err);
    });
});
