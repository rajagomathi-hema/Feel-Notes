
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
  