function checkForm() {
  const leaving =
    document.querySelector("#id_origin") ||
    document.querySelector("#id_origination") ||
    document.querySelector('input[name="origin"]') ||
    document.querySelector('input[name="origination"]') ||
    document.querySelector('input[placeholder*="San Francisco"]');

  const heading =
    document.querySelector("#id_destination") ||
    document.querySelector("#id_destination_city") ||
    document.querySelector('input[name="destination"]') ||
    document.querySelector('input[name="destination_city"]') ||
    document.querySelector('input[placeholder*="Los Angeles"]');

  const leavingVal = leaving ? leaving.value.trim() : "";
  const headingVal = heading ? heading.value.trim() : "";

  // Must type at least one field
  if (leavingVal === "" && headingVal === "") {
    alert("Please enter where you're leaving from and/or where you're heading to.");
    return false;
  }

  // Block "Elon Musk" in EITHER field
  const combined = (leavingVal + " " + headingVal).toLowerCase();
  if (combined.includes("elon") && combined.includes("musk")) {
    alert("Nice try — Elon Musk isn’t carpooling today 🙂");
    return false;
  }

  return true;
}

function setCookie(name, value, days) {
  const d = new Date();
  d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
  const expires = "expires=" + d.toUTCString();
  document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function getCookie(name) {
  const cname = name + "=";
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(";");

  for (let i = 0; i < ca.length; i++) {
    let c = ca[i].trim();
    if (c.indexOf(cname) === 0) {
      return c.substring(cname.length, c.length);
    }
  }
  return "";
}



function handleFirstVisitRedirect() {
  // Choose a cookie name that won't collide with anything else
  const cookieName = "ridepals_has_visited";

  // If cookie doesn't exist, it's their first visit
  const visited = getCookie(cookieName);

  if (!visited) {
    // Mark as visited for (say) 30 days
    setCookie(cookieName, "1", 30);

    // BONUS: don't redirect if they're already on the splash page
    const path = window.location.pathname;

    // If your splash page is served at '/', redirect only when not already there
    if (path !== "/") {
      window.location.href = "/";
      return;
    }
  }
}

window.addEventListener("load", handleFirstVisitRedirect);
